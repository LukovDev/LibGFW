#
# light.py - Создаёт поддержку освещения.
#


# Импортируем:
if True:
    from .gl import *
    from .draw import Draw2D
    from .camera import Camera2D
    from .shader import ShaderProgram
    from .sprite import Sprite2D
    from .texture import Texture
    from .renderer import Renderer2D
    from .batch import SpriteBatch2D
    from ..math import *


# Класс 2D освещения:
class Light2D:
    # Класс слоя освещения:
    class LightLayer:
        def __init__(self, camera: Camera2D, ambient: list = None) -> None:
            if ambient is None: ambient = [0, 0, 0, 0.5]

            self.camera   = camera                 # Ваша 2D камера.
            self.ambient  = ambient                # Цвет окружающего света.
            self.lights   = []                     # Список источников света.
            self.batch    = SpriteBatch2D(camera)  # Пакетная отрисовка спрайтов.
            self.renderer = Renderer2D(camera)     # Конвейер рендеринга.

        # Отрисовываем световое окружение:
        def render(self, s, t) -> None:
            # Закрашиваем текстуру кадрового буфера в фоновый цвет освещения:
            self.renderer.fill(self.ambient)

            # Начинаем рисовать источники света в окружении (слое света):
            self.renderer.begin()

            # Устанавливаем специальный режим смешивания:
            gl_set_blend_mode(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

            # Рисуем источники света:
            self.batch.begin()
            for light in self.lights:
                if type(light) is Light2D.PointLight:
                    light.__render__()

                # Если это спрайтовый источник света:
                elif type(light) is Light2D.SpriteLight:
                    if light.color == [1, 1, 1]:
                        self.batch.draw(
                            light.sprite,
                            light.position.x - light.size.x / 2,
                            light.position.y - light.size.y / 2,
                            light.size.x, light.size.y,
                            light.angle)
                    else:
                        light.sprite.render(
                            light.position.x - light.size.x / 2,
                            light.position.y - light.size.y / 2,
                            light.size.x, light.size.y,
                            light.angle, light.color
                        )
            self.batch.end()
            self.batch.render()

            # Возвращаем обычный режим смешивания:
            gl_set_blend_mode()

            # Рисуем слой света:
            self.renderer.end()
            self.renderer.render()

        # Вызывается при изменении размера окна:
        def resize(self, width: int, height: int) -> None:
            self.renderer.resize(width, height)

        # Удаляем световое окружение:
        def destroy(self) -> None:
            self.shader.destroy()

    # Класс точечного источника света:
    class PointLight:
        def __init__(self,
                     layer:        "Light2D.LightLayer",
                     position:     vec2,
                     intensity:    float = 0.5,
                     color_inner:  list = None,
                     color_outer:  list = None,
                     inner_radius: float = 32,
                     outer_radius: float = 128
                     ) -> None:
            if color_inner is None: color_inner = [1, 1, 1]
            if color_outer is None: color_outer = [1, 1, 1]

            # Вершинный шейдер:
            vertex_shader = """
            #version 330 core

            // Матрицы камеры:
            uniform mat4 u_modelview;
            uniform mat4 u_projection;

            // Позиция вершины:
            layout (location = 0) in vec3 a_position;

            // Основная функция:
            void main(void) {
                gl_Position = u_projection * u_modelview * vec4(a_position, 1.0);
            }
            """

            # Фрагментный шейдер:
            fragment_shader = """
            #version 330 core

            // Входные переменные:
            uniform vec2  u_resolution;     // Размер окна.
            uniform vec2  u_cam_position;   // Позиция камеры.
            uniform float u_cam_zoom;       // Масштаб камеры.

            // Параметры источника света:
            uniform vec2  u_position;       // Позиция источника света.
            uniform float u_intensity;      // Сила альфа канала внутри круга.
            uniform vec4  u_ambient_color;  // Фоновый цвет света.
            uniform vec3  u_color_inner;    // Цвет источника света внутри.
            uniform vec3  u_color_outer;    // Цвет источника света снаружи.
            uniform float u_inner_radius;   // Внутренний радиус.
            uniform float u_outer_radius;   // Внешний радиус.

            // Константы:
            const float offset_pixel = 4.0;  // Смещение между внутренним и наружным радиусом в пикселях.

            // Выходной цвет:
            out vec4 FragColor;

            // Основная функция:
            void main(void) {
                // Настраиваем систему координат шейдера:
                vec2 position = (u_position - u_cam_position) * (1.0 / u_cam_zoom);
                vec2 uv = (((gl_FragCoord.xy - position) / u_resolution.xy) - 0.5) * u_resolution.xy * 2;

                vec3  color;  // Финальный цвет пикселя.
                float alpha;  // Альфа финального пикселя.

                float inner_rad = u_inner_radius * (1.0 / u_cam_zoom);  // Настраиваем внутренний радиус.
                float outer_rad = u_outer_radius * (1.0 / u_cam_zoom);  // Настраиваем наружный радиус.

                // Если вдруг внутренний радиус будет больше чем наружный:
                if (inner_rad > outer_rad - offset_pixel) {
                    inner_rad = outer_rad - offset_pixel;
                }

                // Вычисляем альфа канал:
                alpha = smoothstep(inner_rad, outer_rad, length(uv));

                // Вычисляем цвет пикселя:
                color = mix(u_color_inner, u_color_outer*(alpha+1), alpha);

                // Задаём окончательный цвет:
                FragColor = mix(vec4(color, mix(0.0, u_intensity, 1.0-alpha)), u_ambient_color, alpha);
            }
            """

            self.layer        = layer         # Слой освещения.
            self.position     = position      # Позиция источника света.
            self.intensity    = intensity     # Интенсивность света.
            self.color_inner  = color_inner   # Цвет внутри.
            self.color_outer  = color_outer   # Цвет снаружи.
            self.inner_radius = inner_radius  # Внутренний радиус освещения.
            self.outer_radius = outer_radius  # Внешний радиус освещения.

            # Шейдер источника света:
            self.shader = ShaderProgram(frag=fragment_shader, vert=vertex_shader).compile()

            # Добавляем этот источник света в список источников света:
            self.layer.lights.append(self)

        # Обновить источник света:
        def __render__(self) -> None:
            """ Эта функция не нуждается в ручном вызове. Она вызывается в слое света автоматически. """

            camera = self.layer.camera

            # Устанавливаем переменные шейдера:
            if True:
                # Входные переменные:
                self.shader.begin()
                self.shader.set_uniform("u_modelview",     camera.modelview)
                self.shader.set_uniform("u_projection",    camera.projection)
                self.shader.set_uniform("u_resolution",    [camera.width, camera.height])
                self.shader.set_uniform("u_cam_position",  camera.position.xy)
                self.shader.set_uniform("u_cam_zoom",      camera.zoom)

                # Параметры источника света:
                self.shader.set_uniform("u_position",      self.position.xy)
                self.shader.set_uniform("u_intensity",     self.intensity)
                self.shader.set_uniform("u_ambient_color", self.layer.ambient)
                self.shader.set_uniform("u_color_inner",   self.color_inner)
                self.shader.set_uniform("u_color_outer",   self.color_outer)
                self.shader.set_uniform("u_inner_radius",  float(self.inner_radius))
                self.shader.set_uniform("u_outer_radius",  float(self.outer_radius))
                self.shader.end()

            # Рисуем шейдер:
            self.shader.begin()
            w = h = self.outer_radius / 2
            x, y = self.position.xy
            Draw2D.quads([1, 1, 1], [(-w + x, -h + y), (+w + x, -h + y), (+w + x, +h + y), (-w + x, +h + y)])
            self.shader.end()

    # Класс спрайтного источника света:
    class SpriteLight:
        def __init__(self,
                     layer:    "SpriteLight.LightLayer",
                     sprite:   Sprite2D | Texture,
                     position: vec2,
                     angle:    float,
                     size:     vec2,
                     color:    list = None,
                     ) -> None:
            """
                Заметки насчёт спрайта освещения:
                1. Сама по себе текстура может быть цветной, но так же её цвет можно указать в параметре color.
                2. Если вы хотите указывать цвет спрайта света, сделайте цвет картинки спрайта белой.
            """
            
            if color is None: color = [1, 1, 1]

            self.layer    = layer     # Слой освещения.
            self.position = position  # Позиция источника света.
            self.angle    = angle     # Угол наклона источника света.
            self.size     = size      # Размер источника света.
            self.color    = color     # Цвет света.
            self.sprite   = sprite    # Спрайт света.

            # Добавляем этот источник света в список источников света:
            self.layer.lights.append(self)

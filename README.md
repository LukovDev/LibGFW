# PyGDF - Python Game Development Framework
### Незамышлённый фреймворк для разработки OpenGL игр на Python, основанный на [Python Program Framework](https://github.com/LukovDev/Python-Program-Framework)
### Описание:
#### Представляет из себя Python Program Framework структуру, в которой есть встроенный python-модуль (ядро) в котором собраны разные скрипты, которые работают воедино, и создают единую среду для разработки игр.
Этот фреймворк разрабатывался вдохновлёнными фреймворками, такими как ```LibGDX``` и ```LwJGL```

### TODO лист есть в [конце](https://github.com/LukovDev/PyGDF?tab=readme-ov-file#todo) этого ReadMe файла.

#

### Краткая инструкция по использованию:
Данный фреймворк для разработки программ и игр, был разработан на ```Python``` версии ```3.11.x```!</br>
Пожалуйста, не используйте данный фреймворк на версиях не ниже ```Python 3.11```, потому что он может работать нестабильно или вовсе не работать!</br>

Скачать Python 3.11:</br>
[Python 3.11.8 for Windows](https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe)</br>
[Python 3.11.8 for MacOS](https://www.python.org/ftp/python/3.11.8/python-3.11.8-macos11.pkg)</br>

#### Хорошо, а как скачать этот ваш фреймворк?

Скачать репозиторий можно [zip-файлом](https://github.com/LukovDev/PyGDF/archive/refs/heads/master.zip), или склонировать репозиторий с помощью Git ```git clone https://github.com/LukovDev/PyGDF.git```

#### Окей, вот я скачал, и что дальше?

А дальше, разархивируйте архив и переместите из полученной папки содержимое (все файлы и папки) в другую папку, или переименуйте её так как вам удобнее. Обычно, это название вашего проекта.

Типа так:</br>
![](https://github.com/LukovDev/PyGDF/assets/103067811/fd5ce8c1-76ee-4ba2-a10b-98601bd755ca)</br>

#### А потом что?

Теперь, откройте эту папку как папку проекта в редакторе кода. Все исходные скрипты и коды должны находиться в папке ```src```!</br>
![](https://github.com/LukovDev/PyGDF/assets/103067811/acf5e6fb-91c5-4381-a229-bf525f81983d)</br>

#

### Важно! После того как вы установили ```Python 3.11.x``` и убедились что он работает в консоле, запустите файл ```pypi.bat``` в папке проекта (фреймворка), чтобы установить все необходимые библиотеки для работы фреймворка.

#

### Теперь поясню за структуру фреймворка и её работы (Это Важно!)

- PyGDF содержит такую структуру:</br>
  - ```build```</br>
  - ```data```</br>
  - ```src```</br>
  - ```build.bat```</br>
  - ```pypi.bat```</br>
  - ```run.bat```</br>

Давайте по порядку.</br>

#

#### Папка ```build```:
Структура этой папки такая:</br>
- ```build```</br>
  - ```tools```</br>
  - ```config.json```</br>
  - ```pypi.txt```</br>

- Папку ```tools``` не трогайте, там всего лишь находится python скрипт сборки вашей программы, и в ней же будут храниться</br>
временные файлы и папки при сборке проекта. Просто игнорируйте эту папку. Пожалуйста.</br>

- Файл ```config.json``` содержит настройки сборки вашей программы в виде JSON файла.</br>
Позже вернёмся к содержимому этого файла.

- Файл ```pypi.txt``` по своему названию говорит всё за себя. Этот файл используется сценарием ```pypi.bat``` для установки всех нужных ```pypi``` библиотек.
Пожалуйста, записывайте название всех отдельно-устанавливаемых библиотек в этот файл.</br>
Это надо, чтобы другой человек смог установить все зависимости для запуска проекта у себя на компьютере.</br>

#### Вернёмся к ранее упомянутому файлу ```config.json``` и разберём его содержимое, и узнаем что за что отвечает.

По умолчанию, его содержимое должно быть примерно таким:</br>
```json
{
    "program-name": "PyGDF Game",

    "main-file":    "/src/main.py",

    "data-folder":  "/data/",

    "program-icon": "/data/icons/build-icon.ico",

    "console-disabled": true,

    "pyinstaller-flags": [
        "--onefile", "--log-level WARN"
    ]
}
```

Страшно? Сейчас разберёмся как это настраивать под себя.</br>

- ```"program-name":``` - Это параметр, который хранит текст в двойных кавычках, в которых записано название, которое примет итоговый бинарный файл.
  Ничего сверхъестественного тут нет. Потому что вы сами потом сможете просто напросто переименовать итоговый бинарный файл. Это сделано для удобства!</br>

- ```"main-file":``` - Это очень важный параметр. Он хранит путь в двойных кавычках до основного запускаемого файла вашей программы.
  Он нужен чтобы система сборки поняла, какой файл является основным, и какой файл будет запускаться первым при запуске бинарника.</br>

- ```"data-folder":``` - Просто указывает путь в двойных кавычках до папки в которой вы храните данные программы. Система сборки просто скопирует эту папку
  в папку ```out``` которая появится в основной папке ```build``` после окончания сборки.</br>

- ```"program-icon":``` - Параметр, который хранит путь до иконки бинарного файла с расширением ```.ico```. Путь указывается в двойных кавычках, и обычно,
  иконка программы хранится в папке ```/data/```, вместе с другими файлами программы.</br>

- ```"console-disabled":``` - Параметр, который указывает системе сборки, выключить ли окно консоли программы при запуске бинарного файла, или нет.
  Важно! Если ваша программа использует консольные команты по типу ```os.system("какая то команда")```, то окно консоли может появляться на несколько миллисекунд!</br>
  ```true``` = Отключить консольное окно.</br>
  ```false``` = Оставить консольное окно.</br>

- ```"pyinstaller-flags":``` - Это список дополнительных флагов при компиляции программы. Эти флаги встраиваются в основную команду компиляции программы,
  и вы можете вписать сюда что то своё. Например, ```"--onefile"``` и ```"--log-level WARN"``` это команды которые будут отдельно добавлены в ход компиляции.</br>
  ```--onefile``` - Сделает так, чтобы все файлы программы были в одном исполняемом файле (не касается файлов которые будут загружаться отдельно в программе).</br>
  ```--log-level``` - Устанавливает уровень логирования сборки.</br>
  Всего есть вот столько уровней: ```TRACE, DEBUG, INFO, WARN, ERROR, FATAL```</br>
  Каждые из них, указывают, какие сообщения выводить во время компиляции.</br>
  ```TRACE``` - Выводит абсолютно все сообщения и действия компилятора.</br>
  ```DEBUG``` - Выводит отладочные сообщения.</br>
  ```INFO``` - Выводит информационные сообщения компилятора.</br>
  ```WARN``` - Выводит предупреждения при компиляции.</br>
  ```ERROR``` - Выводит ошибки при компиляции.</br>
  ```FATAL``` - Выводит фатальные ошибки, при которых продолжать компиляцию невозможно.</br>

Вот и всё! Вы сами можете изменить любой из этих параметров под себя!</br>
Тут ничего сложного.</br>

Едем дальше.</br>

#

#### Папка ```data```:

Ну, тут всё просто. Я сделал эту папку как основную папку для хранения всех ресурсов программы.</br>
В этой папке может храниться абсолютно всё, что как-то подгружается программой.</br>
Например, спрайты, иконки, шейдеры, текстуры, модельки и так далее...</br>
Эта папка по умолчанию копируется системой сборки, и размещается в папке ```/build/out/```</br>
Вы можете изменить папку данных программы в конфигурационном файле системы сборки, которое мы обсудили выше.</br>

#

#### Папка ```src```:

Это папка в которой хранятся все файлы с исходным кодом программы.</br>

Структура этой папки такая:</br>
- ```src```</br>
  - ```gdf```</br>
  - ```main.py```</br>

- Модуль ```gdf``` - Это папка, в которой хранятся скрипты, которые представляют из себя весь функционал этого фреймворка.
  Это по факту "библиотека" которую можно назвать "ядром" или "движком" этого фреймворка.</br>В эту папку мы не лезем, потому что иначе, вы можете сломать ядро фреймворка.</br>
  Помните, что мы игнорируем только 2 папки в этом фреймворке. Это ```build/tools``` и ```src/gdf```. Никак не взаимодействуйте с ними. Не перемещайте, и не переименовывайте.</br>
  Хотя, это желательно не делать и с другими папками во фреймворке, без должного понимания его работы.</br>

- Файл ```main.py``` - Является основным запускаемым файлом по умолчанию, который вы также можете изменить в конфигурационном файле системы сборки.</br>

#

#### Файл ```build.bat```:

Запускает систему сборки проекта.</br>
В папке ```/build/tools/``` создаются всеменные файлы сборки, но после её окончания или ошибки, они удаляются автоматически.</br>
Также, на последнем этапе сборки проекта, после удаления временных файлов, идёт копирование папки ```data``` в папку ```build/out```.</br>
Вообщем, если хотите собрать свою игру в бинарный вид, запустите этот файл.</br>

##### Важно! Во время компиляции проекта, у вас может вывестись предупреждения по типу таких:</br>
![](https://github.com/LukovDev/PyGDF/assets/103067811/3fd15368-edf8-4e53-bc40-71e39d2c6f6b)</br>
Если вы получили такие предупреждения, то просто игнорьте их. Ничего страшного не будет. Это просто предупреждения в библиотеках NumPy и Numba.

##### Весь результат сборки, находится в папке ```build/out```

#

#### Файл ```pypi.bat```:

Устанавливает все используемые внешние библиотеки, которые необходимо установить для запуска проекта из исходного кода.</br>
Этот файл устанавливает все библиотеки из файла ```build/pypi.txt``` и заодно и все используемые библиотеки в ядре фреймворка.</br>

##### Важно! Библиотеки будут установлены только если все из них были установлены без ошибок.

#

#### Файл ```run.bat```:

Самый простой файл. Просто запускает файл ```src/main.py``` и ничего другого не делает.</br>

После того, как вы установили все нужные библиотеки для работы фреймворка, и попытаетесь запустить программу, вы должны увидеть что-то типа такого:</br>
![](https://github.com/LukovDev/PyGDF/assets/103067811/74afcdbb-276d-4e42-8f53-329566386971)</br>

#

### Вот и всё. Вы только что прошли краткое обучение о структуре и использовании этого фреймворка.</br>Если вы хотите ознакомиться с API ядра фреймворка, то я написал об этом [тут.](https://github.com/LukovDev/PyGDF/blob/master/README_API.md)

#

### TODO:

Всё что вы увидите ниже, будет рано или поздно, реализовано.

#### Планы на **PyGDF 1.0**:

Много чего из этого списка было уже реализовано и убрано.</br>
Например, ускорение пакетной отрисовки, реализации простой системы частиц, поддержки аудио, и так далее.</br>
Осталось только то, что вы видите сейчас.

- [x] **Реализовать конвейер рендеринга.**

- [x] **Сделать 2D аниматора для покадровой анимации.**

- [x] **Сделать чтобы у параметров спрайта не обязательно было указывать текстуру.**

- [x] **Переделать ```utils.py```. В частности, название и назначение функций.**

- [x] **Сделать простую поддержку ```Discord Rich Presence```. Реализовано в ```utils.py```**

- [x] **Сделать простую поддержку [PyImGUI[pygame]](https://github.com/pyimgui/pyimgui).**

- [x] **Исправить баги в эффекте системы частиц 2D.**

- [x] **Сделать 2D освещение:**
  - [x] Сделать точечный источник света:
    - [x] Спрайтовый источник света.
    - [x] Шейдерный источник света.

- [x] **Улучшить работу Font.**
  - [x] Переделать в другой класс - ```FontGenerator``` и обновить старый код.

- [ ] **Сделать поддержку Net:**
  - [ ] Сделать минимальный API для работы с Socket (Сделать реализацию TCP/IP протокола).
  - [ ] Сделать простую реализацию Host / Client для того, чтобы вы могли сделать сетевую игру.

- [ ] **Переписать 2D физику:**
  - [ ] Сделать чтобы создавалась сетка коллизии из маски текстурки объекта.
  - [ ] Сделать отображение сетки коллизии.
  - [ ] Вообще переделать весь API 2D физического движка.

- [ ] **Написать API документацию по ядру фреймворка перед релизом версии.**

#### Планы на **PyGDF 2.0** (всё ещё не полный список плановых изменений):

- [ ] **Обновить систему сборки [фреймворка](https://github.com/LukovDev/Python-Program-Framework), чтобы тот делал сборку под мобильные устройства (хотя бы на android).**

- [ ] **Сделать базовую поддержку 3D:**
  - [ ] Добавить ```mesh.py``` в graphics для работы с сеткой 3D моделей.
  - [ ] Добавить 3D освещение в ```gdf.graphics.light``` -> ```Light3D```
  - [ ] Добавить 3D эффект частиц в ```gdf.graphics.particles``` -> ```SimpleParticleEffect3D```
  - [ ] Добавить поддержку 3D физики в ```gdf.physics```
  - [ ] Добавить поддержку 3D текстуры.</br>
  _Список всё ещё не закончен._

- [ ] **Улучшить эффект частиц:**
  - [ ] Сделать 3D эффект частиц.
  - [ ] Сделать больше контроля и параметров системы частиц как для SimpleParticleEffect2D так и для SimpleParticleEffect3D.
  - [ ] Сделать коллизию частиц как для 2D так и для 3D физических движков.</br>
  _Список всё ещё не закончен._

- [ ] **Улучшить 2D освещение:**
  - [ ] Сделать направленный источник света.
  - [ ] Сделать поддержку теней (путём raycast/ray-tracing).

- [ ] **Улучшить Font:**
  - [ ] Сделать чтобы его можно было размещать в 3D пространстве.

- [ ] **Сделать Glow эффект спрайта. Другими словами, свечение текстуры, с учётом цветов на её краях.**

- [ ] **Переделать алгоритм упаковщика текстур. На данный момент, он упаковывает текстуры крайне просто и с большими пустотами, куда могут поместиться другие текстуры.**

- [ ] **Сделать поддержку реверберации и прочих аудио-эффектов в поддержке звука (только sound звуков! на music это не будет распространяться).**

- [ ] **Сделать AI модуль, и сделать простой класс для поиска пути по 2D сетке тайлов.**

_Список может изменяться._

#

### Связь со мной:
#### [Telegram](https://t.me/mr_lukov)

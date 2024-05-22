# Библиотека для кэширования взаимосвязанных объектов
- [Wiki](https://github.com/Nikita-Barabanov/UniversalCache/wiki)

## Использование

- Перейдите в директорию с исходниками и соберите пакет:

```shell
python3 -m build
```

- Затем установите пакет в виртуальное окружение вашего проекта:

```shell
pip install univcache-{*version*}-py3-none-any.whl
```

- Создайте python-скрипт для описания правил, импортируйте в нем пользовательские функции univcache.univcache:
```python
from univcache.univcache import build, clean, fields
...
```

- Далее описывайте правила сборки, используя декоратор `fields`:

```python
@fields(name="src.name")
def compile(src: CFile) -> OFile:
    ...
```

- Запускайте процесс сборки при помощи build:

```python
build(OFile, name="example")
```


- Теперь  можно пользоваться функциональностью библиотеки (подробнее [HowTo](https://github.com/Nikita-Barabanov/UniversalCache/wiki/HowTo))

- Подробнее о синтаксисе описания правил [Syntax](https://github.com/Nikita-Barabanov/UniversalCache/wiki/Syntax)

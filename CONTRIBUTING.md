для участников comptechschool
* создаем в github projects задачу
* под нее создаем ветку, где в начале идет nickname человека, а последующий текст это название карточки через `-` (на англ)
* добавляете/удаляете/изменяете/.. нужный код
* запускаете [pre-commit](https://github.com/pre-commit/pre-commit)
  * `$ pip install -U reorder-python-imports flake8 black pre-commit`
  * `$ pre-commit run -a`
* создаете pull request в ветку `stage`

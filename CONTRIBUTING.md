для участников comptechschool
* создаем в github projects задачу
* под нее создаем ветку, наследовавшись от `stage` в виде `nicname-<name-branch-based-on-name-task>` (без `<>`)
* добавляете/удаляете/изменяете/.. нужный код
* проверить все ли pass/tokens/.. убраны
* запускаете [pre-commit](https://github.com/pre-commit/pre-commit)
  * `$ pip install -U reorder-python-imports flake8 black pre-commit`
  * `$ pre-commit run -a`
* создаете pull request в ветку `stage`

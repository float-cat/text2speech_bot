для участников comptechschool
* создаем в github projects задачу
* создаем ветку, наследовавшись от `stage` в виде `nicname-<name-branch-based-on-name-task>` (без `<>`)
* добавляете/удаляете/изменяете/.. нужный код
* проверить все ли pass/tokens/.. убраны (к примеру, заменив их на `your_code`)
* опишите как запускать ваш код в `readme.md`
* добавьте нужные зависимости в корне проекта `requirements.txt` (советую использовать [pipreqs](https://github.com/bndr/pipreqs)
* запускаете [pre-commit](https://github.com/pre-commit/pre-commit)
  * `$ pip install -U reorder-python-imports flake8 black pre-commit`
  * `$ pre-commit run -a`
* создаете pull request в ветку `stage`

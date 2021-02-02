для участников comptechschool
* создаем ветку, наследовавшись от `stage` в виде `nicname-<name-feature>` (без `<>`)
* добавляете/удаляете/изменяете/.. нужный код
* проверить все ли pass/tokens/.. убраны (к примеру, заменив их на `your_code`)
* опишите как запускать ваш код в `readme.md`
* добавьте нужные зависимости в корне проекта `requirements.txt` (советую использовать [pipreqs](https://github.com/bndr/pipreqs)
* выполните [pre-commit](https://github.com/pre-commit/pre-commit)
  * `$ pip install -U reorder-python-imports flake8 black pre-commit`
  * `$ pre-commit run -a`
* создаете pull request (pr) в ветку `stage`
* в pr справа в "projects" выбираете "team bord", чтобы создать задачу в github projects

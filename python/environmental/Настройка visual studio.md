1. Необходимо установить расширения:
	-  Flake8
	- Mypy Type Checker
	- Black Formatter
	- isort
2.  Создать в корне проекта папку `.vscode` и в ней файл `settings.json`
3. Вставить в файл `settings.json` конфиг (при этом в корне проекта должны существовать файлы `.flake8 и .mypy.ini`)
```json
{
"[python]": {
"editor.defaultFormatter": "ms-python.black-formatter",
"editor.formatOnSave": true,
"editor.codeActionsOnSave": {
		"source.organizeImports": "explicit"
	},
},
"black-formatter.args": ["--config",".black"],
"isort.args": ["--profile","black"],
"flake8.args": ["--config",".flake8"],
"mypy-type-checker.args": ["--config-file=.mypy.ini"]
}
```
	
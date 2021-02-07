# @tts_tg_bot

## цель
разработка бота для мессенджера telegram: преобразования текста в голосовую речь

## задачи
* автоматизация преобразования текста в речевой формат
* разработка telegram-бота
* демонстрация прототипа бота, обеспечивающего
  * извлечение текста от пользователя
  * преобразование текста в голосовую речь с помощью внешних служб (text2speech.org, яндекс speechkit и др.)
  * дополнительную функциональность (скорость воспроизведения и голос)

## структура проекта
```markdown
├── .github
│   ├── workflows
│   │   ├── ci.yml
│   │   └── codeql-analysis.yml
│
├── experiments
│   ├── text2speech_org
│   │   ├── minimalbot.py
│   │   ├── sk_adapter.py
│   │   └── README.md
│   │
│   └── README.md
│
├── t2s
│   ├── modules
│   │   ├── asyncmgr.py
│   │   ├── audiosender.py
│   │   ├── botcfg.py
│   │   ├── buffermgr.py
│   │   ├── keyboard.py
│   │   ├── preprocessing.py
│   │   ├── speakers.py
│   │   ├── speechkitadapter.py
│   │   ├── usercfg.py
│   │   └── README.md
│   │
│   ├── t2sbot.py
│   └── README.md
│
├── LICENSE
├── README.md
│
├── requirements.txt
├── CONTRIBUTING.md
│
├── .gitignore
└── .pre-commit-config.yaml
```

## другое
* учет задач ведется с помощью [github projects](https://github.com/vtrokhymenko/text2speech_bot/projects/1)
* основное обсуждение – [github discussions](https://github.com/vtrokhymenko/text2speech_bot/discussions)
* содействие в проект – [CONTRIBUTING.md](./CONTRIBUTING.md)
* [техническая документация](https://docs.google.com/document/d/1Tby2kgqtaEe28O-ZC9ePsSMEASLG5M1t07tjQYhByXE/edit?usp=sharing)

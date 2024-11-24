# Домашняя работа №2. Сервис


Сервис реализован на FastAPI и предназначен для выдачи результатов последовательной работы
 модели [выделения автомобильного номера](https://gitlab.deepschool.ru/cvr-dec23/d.iunovidov/hw-02-model-det/-/tree/DEV?ref_type=heads) и
 модель [распознования текста номера](https://gitlab.deepschool.ru/cvr-dec23/d.iunovidov/hw-02-model-ocr/-/tree/DEV?ref_type=heads)


[Адрес для тестов](http://91.206.15.25:5039)

[Документация и тестирование GET и POST запросов](http://91.206.15.25:5039/docs)

В `src/container_task.py` лежит код двух классов:

* `Storage` - умеет сохранять рассчитанные значения в `*.json` (позволяет "кешировать" результаты работы модели).
* `ProcessPlates` - умеет загружать ONNX модели и определять текст автомобильного номера, после чего зовет `Storage`, чтобы тот сохранил контент.

В `app.py` лежит приложение FastAPI, у которого две ручки:
1. `get_content` - возвращает контент по `content_id`.
2. `process_content` - генерирует контент с помощью нейронной сети для переданного изображения.

Пример работы можно посмотреть в `src/container_task.py`


## Настройка окружения

Сначала создать и активировать venv:

```bash
python3 -m venv venv
. venv/bin/activate
```

Дальше поставить зависимости:

```bash
make install
```

### Команды

#### Подготовка
* `make install` - установка библиотек

#### Запуск сервиса
* `make run_app` - запустить сервис. Можно с аргументом `APP_PORT`

#### Сборка образа
* `make build` - собрать образ. Можно с аргументами `DOCKER_TAG`, `DOCKER_IMAGE`

#### Статический анализ
* `make lint` - запуск линтеров

#### Тестирование
* `make run_unit_tests` - запуск юнит-тестов
* `make run_integration_tests` - запуск интеграционных тестов
* `make run_all_tests` - запуск всех тестов

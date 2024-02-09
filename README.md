# Тестовое задание для ООО "Квазар"


---
## Установка и запуск

1. Создайте виртуальное окружение и активируйте его:

    ```bash
    $ python3.11 -m venv venv
    $ source venv/bin/activate  # Для Unix
    $ .\venv\Scripts\activate  # Для Windows
    ```

2. Склонируйте репозиторий:

    ```bash
    $ git clone https://github.com/saltitc/fastapi-test-task.git
    $ cd fastapi-test-task/
    ```

3. Установите зависимости:

    ```bash
    $ pip install -r requirements.txt
    ```

4. Запустите сервер:

    ```bash
    $ uvicorn app.main:app --reload
    ```

5. Откройте браузер и перейдите по адресу `http://127.0.0.1:8000/docs/'.

---
## Дополнительно
> В репозитории есть готовая база данных для тестирования работы API

> Запуск тестов:
>
>    ```bash
>    $ TESTING=True pytest
>    ```

> В случае возникновения ошибки "ModuleNotFoundError: No module named 'app'" введите в консоль следующую команду:
>
>    ```bash
>    $ export PYTHONPATH=$(pwd)
>    ```


> Деактивировать виртуальное окружение:
>
>    ```bash
>    $ deactivate
>    ```
---

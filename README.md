## :smile_cat: "Благотворительный фонд поддержки котиков" :smile_cat:

<p align="center">
  <img src="https://github.com/AndyFebruary74/cat_charity_fund/blob/master/cat.jpg"
    alt="cat fund"/>
</p>

---

Фонд собирает пожертвования на различные целевые проекты: на медицинское 
обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале,
на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой
кошачьей популяции.

---

### :mechanical_arm: Проекты

В Фонде может быть открыто несколько целевых проектов. У каждого проекта
есть название, описание и сумма, которую планируется собрать. После того как
нужная сумма собрана — проект закрывается.
Пожертвования в проекты поступают по принципу First In, First Out:
все пожертвования идут в проект, открытый раньше других; когда этот проект
набирает необходимую сумму и закрывается — пожертвования начинают поступать в
следующий проект.


### :heavy_dollar_sign: Пожертвования

Каждый пользователь может сделать пожертвование и сопроводить его комментарием.
Пожертвования не целевые: они вносятся в фонд, а не в конкретный проект. Каждое
полученное пожертвование автоматически добавляется в первый открытый проект,
который ещё не набрал нужную сумму. Если пожертвование больше нужной суммы или
же в Фонде нет открытых проектов — оставшиеся деньги ждут открытия следующего 
проекта. При создании нового проекта все неинвестированные пожертвования
автоматически вкладываются в новый проект.

### :family_man_woman_girl_boy: Пользователи

Целевые проекты создаются администраторами сайта. Так же администраторы могут
выгружать закрытые проекты в гугл таблицу.  
Любой пользователь может видеть список всех проектов, включая требуемые и уже
внесенные суммы. Это касается всех проектов — и открытых, и закрытых.
Зарегистрированные пользователи могут отправлять пожертвования и просматривать 
список своих пожертвований.

---

### :hammer_and_wrench: Как пользоваться: 

<details> 
<summary> <b>Инструкция</b> </summary>
<br>

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/AndyFebruary74/cat_charity_fund
```

```
cd cat_charity_fund
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Применение миграций:

```
alembic upgrade head

```

Запуск:

```
uvicorn main:app
```

</details>

---
### :scroll: Документация 

После запуска документация API доступна по адресу `http://127.0.0.1:8000` 

[Swagger](http://127.0.0.1:8000/docs)

[Redoc](http://127.0.0.1:8000/redoc)

---

### :lock: .env

`cat_charity_fund\.env` - расположение

#### Example:

```
#project settings
APP_TITLE=DEFAULT TITLE
APP_DESCRIPTION=DEFAULT DESCRIPTION
DATABASE_URL=sqlite+aiosqlite:///./cat_charity_fund.db
SECRET=DEFAULT SECRET KEY

# google cloud settings
TYPE = "service_account"
PROJECT_ID = "symbolic-base-00000"
PRIVATE_KEY_ID = "00000000000000000000000000000000"
PRIVATE_KEY = "-----BEGIN PRIVATE KEY-----"
CLIENT_EMAIL = "my-first-service-account@symbolic-base-000000.iam.gserviceaccount.com"
CLIENT_ID = "12345678901234567890"
AUTH_URI = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URI = "https://oauth2.googleapis.com/token"
AUTH_PROVIDER_X509_CERT_URL = "https://www.googleapis.com/oauth2/v1/certs"
CLIENT_X509_CERT_URL = "https://www.googleapis.com/robot/v1/metadata/x509/my-first-service-account%40symbolic-base-000000.iam.gserviceaccount.com"

# google account
EMAIL = "cat_charity_fund@gmail.com"
```

---

### :high_brightness: Используемые технологии([requirements](https://github.com/AndyFebruary74/cat_charity_fund/blob/master/requirements.txt)):
- [x] Python 3.10
- [x] FastAPI 0.7.8
- [x] SQLAlchemy 1.4.36
- [x] Alembic 1.7.7
- [x] Uvicorn 0.17.6
- [x] Aiogoogle 4.2.0
- [x] Google Cloud Platform
  - [x] Google Sheets API
  - [x] Google Docs API

---

**_Author: [Andrey Kilanov](https://github.com/AndyFebruary74/) [telegram](https://t.me/AndyFebruary)_**
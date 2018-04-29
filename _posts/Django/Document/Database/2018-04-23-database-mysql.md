---
layout: post
title: '[DB] Django 앱에 MySQL 연동하기'
excerpt: 'Django 어플리케이션에 MySQL 데이터베이스를 연동시키는 방법을 알아보자.'
category: Django
author: Che1
tags:
  - Database
  - MySQL
  - RDS
---

## MySQL 설치

터미널 창을 열고 아래와 같이 입력하여 `MySQL` 을 설치한다.

```
sudo apt-get install mysql-server mysql-client
```

설치 시 루트 사용자의 비밀번호를 입력하라는 창이 뜨면 비밀번호를 설정해준다.

- - -

## MySQL Monitor 접속하기

MySQL은 터미널에서 MySQL을 컨트롤 할 수 있도록 `MySQL Monitor` 라는 CLI 인터페이스를 기본적으로 제공한다.  

```
mysql -u유저명 -p비밀번호
```
```
mysql -h호스트주소 -p포트번호 -u아이디 -p비밀번호
```
비밀번호를 한꺼번에 입력하면 보안상의 문제가 있을 수 있으므로 -p 이후 엔터를 쳐서 비밀번호를 숨긴 채로 입력하도록 한다.

- - -

## MySQL 기본적인 명령어

- 데이터베이스 생성

```sql
CREATE DATABASE 데이터베이스명;
```

- 데이터베이스 목록 확인

```sql
SHOW DATABASES;
```

- 데이터베이스 선택

```sql
USE 데이터베이스명;
```

- - -

## Django와 연동하기

Django에 MySQL을 연동시키기 연습을 위해서 AWS 의 RDS 서비스를 이용할 것이다.  

아래 포스트를 참고하여 Django와 연동할 MySQL이 설치된 RDS 서버를 하나 생성한다.  

[Django 프로젝트 배포하기 - 5. RDS](/django-deploy-5-rds/)

- - -

### 데이터베이스 생성하기

RDS가 세팅되었으면 터미널에서 다음 명령을 입력하여 MySQL 데이터베이스에 접속한다.

```
mysql -h호스트주소 -p포트번호 -u아이디 -p비밀번호
```

다음으로 데이터베이스를 생성해준다.  

```sql
mysql> CREATE DB명;
```

데이터베이스를 생성했으면 다음의 명령어로 생성한 데이터베이스를 선택한다.  

```sql
mysql> USE DB명;
```

- - -

### MySQL DB API Driver 설치

PostgreSQL을 Django와 연동시키기 위해서는 `psycopg2` 가 필요하듯이, MySQL을 Django와 연동시키기 위해서는 `mysqlclient` 가 필요하다.

```
sudo apt-get install libmysqlclient-dev
pip install mysqlclient
```

`pymysql` 이라는 인터페이스도 있다.  

```
pip install pymysql
```

pymysql을 사용할 경우, `settings.py` 에 아래와 같이 추가해주어야 한다.

```py
# settings.py

import pymysql

pymysql.install_as_MySQLdb()
```

이외에도 몇 가지 인터페이스가 더 있는데 공식 문서에서는 mysqlclient를 사용하는 것을 권장한다.

[Django 공식 문서](https://docs.djangoproject.com/en/2.0/ref/databases/#mysql-db-api-drivers)

- - -

### settings.py 설정

`settings.py` 의 `DATABASE` 변수에 연동시킬 데이터베이스의 정보를 입력해주어야 한다.  

입력해야하는 항목들은 다음과 같다.  

```py
# settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '', # DB명
        'USER': '', # 데이터베이스 계정
        'PASSWORD': '', # 계정 비밀번호
        'HOST': '', # 데이테베이스 주소(IP)
        'PORT': '', # 데이터베이스 포트(보통은 3306)
    }
}
```

- `NAME`: 생성한 데이터베이스 이름  
- `USER`: RDS 생성시 입력했던 유저명  
- `PASSWORD`: RDS 생성시 입력했던 페스워드  
- `HOST`: RDS 엔드포인트 주소  
- `PORT`: 데이터베이스 포트 번호 - MySQL의 경우 3306  

코드들을 `Git` 으로 관리하는 경우, 위와 같이 settings.py에 직접 설정들을 입력하면 보안상의 문제가 생길 수 있으므로 별도의 파일에서 설정들을 불러와 입력하도록 하자.  

다음은 새로 알게된 별도의 파일에서 설정 정보를 불러오는 방법이다.  

`cnf` 라는 확장자를 가진 파일을 만들고 그 안에 다음과 같이 입력한다. 이름은 `mysql.cnf` 라고 지어주었다.  

```conf
# mysql.cnf

[client]
database = DB명
host = 데이테베이스 주소(IP)
user = 데이터베이스 계정
password = 계정 비밀번호
```

그 다음, 위의 파일을 아래와 같이 불러와 적용시켜준다. `OPTIONS` 라는 항목을 사용한다.  

```py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': "path/to/mysql.cnf"),
        }
    }
}
```

- - -


### STRICT Mode

위 단계까지 진행한 다음 `migrate` 를 해보면 아래와 같은 경고 메세지가 나타난다.  

```
?: (mysql.W002) MySQL Strict Mode is not set for database connection 'default'
        HINT: MySQL's Strict Mode fixes many data integrity problems in MySQL, such as data truncation upon insertion, by escalating warnings into errors. It is strongly recommended you activate it. See: 
```

MySQL 의 `Strict Mode` 가 설정이 안되어있다는 경고이다.  

보통 데이터베이스에 데이터를 입력하는 경우 설정된 필드의 특성에 따라 데이터를 검증하고 검증을 통과하지 못한 경우 데이터의 입력이 되지 않는데, MySQL의 경우 임의적으로 데이터를 변경해서 집어넣는 경우가 있나보다.  
예를 들어, MySQL의 `CHAR` 나 `VARCHAR` 필드가 가진 글자 수 제한을 넘어서는 데이터가 입력되는 경우 제한된 글자 수 만큼만 데이터가 잘려서 입력된다거나, 어떤 경우에는 -1 을 입력했는데 0이 들어가는 대참사가 일어나기도 한다고 한다.  

이를 해결할 수 있는 방법이 바로 `Strict Mode` 이다.  
Strict 모드를 설정하면 올바르지 않은 데이터가 입력되었을 때 오류를 일으키면서 데이터 입력이 되지 않는다.  
Strict 모드는 기본적으로 설정되어있지 않으며, `MySQL 5.7 버전` 부터는 기본적으로 설정되어있다고 한다.  

Django 에서 Strict 모드를 설정해주려면 다음과 같이 추가한다.  

```py
# settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(SECRET_DIR, "mysql.cnf"),
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'" # strict mode 설정 추가
        }
    }
}
```

[Django 공식 문서](https://docs.djangoproject.com/en/2.0/ref/databases/#mysql-sql-mode)


- - -

#### Reference

[Django 공식문서](https://docs.djangoproject.com/en/2.0/ref/databases/#mysql-notes)  
[lesstif.com](https://www.lesstif.com/pages/viewpage.action?pageId=24445406)  
[생활코딩](https://opentutorials.org/course/195/1399)  
[권남's Blog](http://kwonnam.pe.kr/wiki/database/mysql/basic)  
[dojun's Blog](https://dojunblog.wordpress.com/2017/02/20/django%EC%97%90%EC%84%9C-pymysql%EC%9D%84-%EC%9D%B4%EC%9A%A9%ED%95%B4-mysql-%EC%97%B0%EB%8F%99%ED%95%98%EA%B8%B0/)  
[Stackoverflow](https://stackoverflow.com/questions/19189813/setting-django-up-to-use-mysql)  
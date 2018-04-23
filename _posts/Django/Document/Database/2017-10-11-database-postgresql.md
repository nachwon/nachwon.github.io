---
layout: post
title: '[DB] PostgreSQL'
category: Django
author: Che1
tags:
  - Database
  - Postgresql
  - RDS
---

#### 설치

```
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```

#### postgres 계정으로 접속하기

Postgres 계정으로 접속하기

```
sudo -i -u postgres
```
```
psql
```

나가려면
```
\q
```


#### 롤 생성

postgres 계정으로 접속한뒤

```
createuser --interactive
```
또는

```
sudo -u postgres createuser --interactive
```

#### 데이터베이스 생성

```
createdb 롤이름
```

#### 롤로 접속해서 프롬프트 열기

```
sudo adduser sammy
```
```
sudo -i -u sammy
psql
```

- - -

#### 비밀번호 바꾸기

롤로 접속한 프롬프트에서

```
\password
```

#### db 바꾸고 데이터 가져오기

./manage.py dumpdata 앱이름 > 파일이름.json

./manage.py loaddate 파일이름.json
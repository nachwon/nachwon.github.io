---
layout: post
title: '[Django Tutorial] Blog 만들기 - 3. 데이터베이스'
category: Django
author: Che1
---
<div class="navigation-menu">
    <h5>[Django Tutorial] Blog 만들기</h5>
    <ol>
        <li><a href="/django/2017/09/28/django-1-setting.html">환경설정</a></li>
        <li><a href="/django/2017/09/30/django-2-start.html">프로젝트 시작</a></li>
        <li><a href="/django/2017/09/30/django-3-database.html">데이터베이스</a></li>
        <li></li>
    </ol>
</div>

- - -

웹사이트의 데이터들은 `데이터베이스` 에 저장된다.  
데이터베이스에 저장된 데이터를 가져와서 사용자에게 보여주기도 하고, 사용자가 입력한 데이터를 데이터베이스에 저장하기도 한다.  
우리가 만들 `Blog` 에 사용할 데이터베이스를 설정해보자.

- - -

다시 `runserver` 를 실행하였을 때 나타나던 메세지를 보자.

```re
Performing system checks...

System check identified no issues (0 silenced).

You have 13 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.

September 30, 2017 - 09:45:46
Django version 1.11.5, using settings 'config.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
이 중 이전 포스트에서 무시하고 넘어갔던 빨간색으로 쓰인 세 번째 문단의 내용을 해석해보자.

>You have 13 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.  
>
>13개의 적용 안된 `migration` 이 있으며, `admin`, `auth`, `contenttypes`, `sessions` 앱에 `migration` 을 적용하지 않으면 프로젝트가 제대로 작동하지 않을 수 있습니다.

`admin`, `auth`, `contenttypes`, `sessions` 앱이 잘 작동하지 않을 수 있다는 경고메세지였다. 
뭔지는 모르겠지만 잘 작동하지 않을 수 있다니 참 큰일이다. 이것을 해결하기 위해 일단 `앱(Application)` 에 대해 알아보자.  

- - -

#### 앱(Application)

`앱(Application)`은 `Django` 프로젝트 내에서 **어떤 기능을 수행**하는 한 단위이다. 형식은 Python 패키지이다.  
위와 같이 기본적으로 제공되는 앱들이 있고, 또 사용자가 직접 만들어서 추가할 수도 있다. 우리가 만들려고 하는 `blog` 도 하나의 앱이 된다.

모든 `Django` 프로젝트에 대한 설정은 `settings.py` 에 저장되어있으며, 이 곳에서 현재 `Django` 프로젝트 내부에서 엑티브 상태인 앱의 목록을 확인할 수 있다. 나중에 앱을 만들면 바로 이 곳에 추가하여 엑티브 상태로 만들어준다.

```python
# settings.py line 33

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```
위의 목록을 보면 이미 몇 가지의 앱들이 기본적으로 포함되어 있는 것을 볼 수 있다.  
아까 경고 메세지에 나타났던 `admin`, `auth`, `contenttypes`, `sessions` 등의 앱들이 이 목록에 포함되어 있다.

이제 앱이 무엇인지 알았다. 그렇다면 `migration` 은 무엇일까? 

- - -

#### Migrations

`Migrations` 는 `Django`의 `모델` 에서 설정한 데이터베이스의 테이블 구조를 데이터베이스에 적용시기 위한 기록으로 볼 수 있다. `모델`에 대해서는 나중에 자세히 다루도록 한다.

> #### Migrations
> Migrations are Django’s way of propagating changes you make to your models (adding a field, deleting a model, etc.) into your database schema. They’re designed to be mostly automatic, but you’ll need to know when to make migrations, when to run them, and the common problems you might run into.  
> 출처: [Django 공식 문서](https://docs.djangoproject.com/en/1.10/topics/migrations/)

`admin`, `auth`, `contenttypes`, `sessions` 등과 같은 앱들은 데이터를 저장할 공간이 필요한 작업을 수행하는 앱들이며, 따라서 데이터베이스에 **데이터들이 저장될 테이블**이 미리 만들어져있어야 제대로 작동한다.  
위의 경고 메세지는 앱들이 필요로하는 데이터베이스 구조가 데이터베이스에 구성되어 있지 않기 때문에 나타난 것이다.  
앱들이 필요로하는 **데이터베이스 구조를 기록**한 것이 `Migrations` 파일이고, 이를 **데이터베이스에 적용**시키는 것을 `migrate` 한다고 한다.  
위의 메세지에 의하면 앱들에 의해 이미 13개의 `Migrations` 파일이 생성되어 있지만 실제 데이터베이스에 `migrate` 되지 않았다고 한다.  
그럼 지금부터 앱들이 저장공간으로 사용할 수 있도록 데이터베이스를 셋팅해보자.

- - -

#### SQLite

데이터베이스에는 다양한 종류가 있다. `Django` 는 데이터베이스의 하나인 `SQLite` 를 포함하고 있다.  

> ##### SQLite
> SQLite는 MySQL나 PostgreSQL와 같은 데이터베이스 관리 시스템이지만, 서버가 아니라 응용 프로그램에 넣어 사용하는 비교적 가벼운 데이터베이스이다. 영어권에서는 '에스큐엘라이트(ˌɛskjuːɛlˈlaɪt)'또는 '시퀄라이트(ˈsiːkwəl.laɪt)'라고 읽는다.  
>출처: [위키백과](https://ko.wikipedia.org/wiki/SQLite)

`SQLite` 는 하나의 파일에 데이터를 저장하여 쉽고 간편하게 사용할 수 있다는 점이 특징이다.

`settings.py` 에서 프로젝트에 사용할 데이터베이스를 지정해줄 수 있으며, 기본적으로 `SQLite3` 을 사용하도록 설정되어 있다.

```python
# settings.py line 76

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

`SQLite` 는 데이터베이스를 `db.sqlite3` 라는 파일에 모두 저장한다.

- - -

#### Migrate 하기

이제 데이터베이스에 대해서도 알아봤으니, 앱들을 위한 데이터베이스 테이블을 만들어주도록 하자.

콘솔에서 `manage.py` 가 있는 폴더까지 이동한 후, 아래의 명령어를 입력한다.

```
python manage.py migrate
```

`migrate` 명령어는 `settings.py` 의 `INSTALLED_APPS` 리스트를 확인하여 리스트에 포함된 앱이 필요로하는 테이블을 데이터베이스에 생성한다.

```re
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying sessions.0001_initial... OK
```

위와 같이 무언가가 잔뜩 생성되는 것을 볼 수 있다. 대충 살펴보면 아까 언급되었던 앱들에 대한 테이블들인 것을 알 수 있다.

이렇게 테이블들을 생성해준 뒤 다시 `runserver`를 실행시켜보면 빨간색 경고메세지가 뜨지 않는다.

- - -
#### SQLite Browser

`SQLite`  데이터베이스를 좀 더 직관적으로 관리할 수 있도록 해주는 GUI 프로그램이 있다.  
`SQLite Browser` 이라는 프로그램이며, 아래 링크에서 다운받아 설치할 수 있다.  
[SQLiteBrowser](http://sqlitebrowser.org/)

이 프로그램을 통해서 우리가 생성한 테이블을 직접 확인해볼 수 있다.  
`SQLite Browser` 를 실행한 뒤 `데이터베이스 열기(O)` 를 클릭하면 아래의 창이 나타난다.

<img width="500px" src="/img/django_tutorial/dbsqlite3.png">

`myproject` 폴더의 `db.sqlite3` 파일을 연다.

<img width="950px" src="/img/django_tutorial/dbbrowser.png">

테이블들이 생성되어 있는 것을 확인할 수 있다.  

- - -

###### Reference
이한영 강사님 강의자료  
School of Web: [http://schoolofweb.net/blog/posts/%EB%82%98%EC%9D%98-%EC%B2%AB-django-%EC%95%B1-%EB%A7%8C%EB%93%A4%EA%B8%B0-part-2-1/](http://schoolofweb.net/blog/posts/%EB%82%98%EC%9D%98-%EC%B2%AB-django-%EC%95%B1-%EB%A7%8C%EB%93%A4%EA%B8%B0-part-2-1/)  
Djangogirls: [https://tutorial.djangogirls.org/ko/](https://tutorial.djangogirls.org/ko/)  


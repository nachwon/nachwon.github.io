---
layout: post
title: '[Django Tutorial] Blog 만들기 - 2. 프로젝트 시작'
category: Django
tags:
  - Django
  - Tutorial
---



이제 본격적으로 `Django` 를 시작해보자.

지금까지의 상황은 아래와 같다.
```re
djangogirls_assignment
├──.git
├──.gitignore
├──.idea
├──.python-version
├──README.md
└──requirements.txt
```
이번 과정부터 `Pycharm Community Edition 2017.2.3` 을 활용하므로 설치하기 바란다.  
[Pycharm Community Edition 다운로드](https://www.jetbrains.com/pycharm/download/download-thanks.html?platform=linux&code=PCC)

- - -
## Django 프로젝트 시작
콘솔에서 프로젝트폴더로 이동한 뒤 `django-admin startproject 프로젝트명` 을 입력하여 새 `Django` 프로젝트를 시작한다.
```
django-admin startproject myproject
```
```re
djangogirls_assignment
├── myproject  # myproject라는 이름의 폴더가 생성되었다.
│   ├── manage.py
│   └── myproject
│       ├── __init__.py
│       ├── settings.py
│       ├── urls.py
│       └── wsgi.py
├── README.md
└── requirements.txt
```

`myproject` 라는 폴더가 생성되었고, 그 안에는 뭔가가 많이 들어있다. 살펴보기 전에 **몇 가지 전처리**를 하고 넘어가도록 하자. 

- - -

### 폴더 이름 Refactor
폴더 구조를 보면 `myproject` 폴더 안에 또 `myproject` 라는 폴더가 있는 것을 볼 수 있다. 헷갈리니까 일단 하위 `myproject` 폴더를 `config` 로 바꾸어주자. 이 때, `Pycharm` 의 `refactor` 기능을 활용하여 내부 파일들이 바뀐 폴더이름을 제대로 참조할 수 있도록 하는 것이 중요하다. `djangogirls_assignment` 폴더를 `Pycharm` 으로 열고 아래와 같이 설정하자.

<img width="950px" src="/img/django_tutorial/refactor.png">

이름변경하려는 폴더를 우클릭한 뒤, `Refactor` > `Rename` 의 순서로 클릭한다.

<img width="500px" src="/img/django_tutorial/rename.png">

`Rename` 창에서 **두 개의 체크박스를 모두 체크**한 뒤 `config` 를 입력하고 `Refactor` 버튼을 클릭한다.  
`Search for references`: 이 폴더명이 참조된 곳을 찾아 모두 바꿔준다.  
`Search for comments and strings`: 이 폴더명이 포함된 코멘트나 문자열까지 찾아 바꿔준다.

<img width="950px" src="/img/django_tutorial/do_refactor.png">

`Refactor` 버튼을 누르면 아래 쪽에 `Preview` 창이 하나 뜨고, 어떤 항목이 영향을 받는지 모두 보여준다.  
사항들을 확인하고 `Do Refactor` 버튼을 누르면 변경사항이 최종적으로 적용된다.

- - -

### Sources Root 설정

현재 `myproject` 폴더 내의 모듈들이 참조하고 있는 이 프로젝트의 `Root directory` 는 가장 최상위 폴더인 `djangogirls_assignment` 이다.  
이 경우 나중에 내부 모듈들이 패키지를 참조할 때 문제가 될 수 있다. 이를 예방하기 위해 `Root directory` 를 `Django Applicaion` 폴더 즉, `myproject` 폴더와 일치시켜주어야 한다.

<img width="950px" src="/img/django_tutorial/sources.png">

`myproject` 폴더를 우클릭한 뒤, `Mark Directory as` > `Sources Root` 를 클릭한다.

<img width="500px" src="/img/django_tutorial/sources_result.png">

`myproject` 폴더가 파란색으로 변한 것을 확인할 수 있다.  
이제 내부 모듈들이 다른 패키지를 참조할 때 이 폴더를 기준으로 경로를 출발하게 된다.  
항상 `Django Applicaion` 폴더를 `Root directory` 로 만들어 주는 것이 좋다.

- - -

### Python 인터프리터 설정

이 부분은  `Pycharm` 에 대한 설정이다. `Pycharm` 이 우리가 설정한 환경을 제대로 인식할 수 있도록 동일한 가상환경의 Python을 인터프리터로 설정해주도록 하자.
우선 `File` > `Setting` 을 클릭하여 설정창을 연다.

<img width="950px" src="/img/django_tutorial/pycharm_setting.png">

설정창에서 `Project: djangogirls_assignment` 항목 아래의 `Project Interpreter` 메뉴를 클릭하여 나타난 우측 창에서 `Project Interpreter` 를 우리가 설정했던 가상환경인 `django_assignment` 로 선택해준다.  
프로젝트마다 이렇게 알맞는 인터프리터 설정을 해주어야 한다.

- - -

이제 `myproject` 폴더의 내부는 아래와 같다. 하나씩 간단히 살펴보도록 하자.

```re
myproject
├── manage.py
└── config
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```
**`myproject`**: `myproject` 폴더는 `Django Application` 이 된다. `Django` 로 만들어진 웹 어플리케이션이다 뭐 그런 정도로 이해하면 될 것 같다. 이 후에 나올 `Django 앱` 과는 다른 것이다.  
**`manage.py`**: 웹사이트의 관리를 도와주는 역할을 하는 스크립트 파일이다. 이 파일의 기능으로 여러가지 개발작업을 수행할 수 있다.  
**`config`**: 웹사이트의 핵심 설정 정보들을 가지고 있는 하위폴더이다. 여러가지 설정과 페이지, 기능 간의 연결을 수행하는 파일들이 들어있다. `__init__.py` 가 있는 걸 보면 알 수 있듯이 Python 패키지이다.  
**`__init__.py`**: 이 파일 때문에 Python은 `myproject` 폴더를 패키지로 인식한다.  
**`settings.py`**: 웹사이트의 여러가지 설정이 들어있는 파일이다.  
**`urls.py`**: 웹사이트의 페이지들을 연결해주는 패턴 목록이 포함된 파일이다.  
**`wsgi.py`**: 뭔지 모르겠다 나중에 알게되면 추가함. 일단 이 튜토리얼에서는 사용하지 않는다.

- - -

## 개발용 서버 시작하기

이제 `Django` 프로젝트를 시작시켰으니 잘 동작하는지 확인해보자.  
먼저 `manage.py` 가 있는 폴더인 `myproject` 폴더로 이동한다.

```
cd myproject
```

그 다음, 아래와 같이 입력하면 `manage.py` 를 활용하여 `Django` 에 포함되어 있는 `runserver` 라는 개발용 웹 서버를 실행시킨다.

```
python manage.py runserver
```

아래와 같은 메세지가 뜨면 성공이다. (빨간색의 경고메세지는 일단 무시한다.)

```
Performing system checks...

System check identified no issues (0 silenced).

You have 13 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.

September 30, 2017 - 08:00:17
Django version 1.11.5, using settings 'config.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

`http://127.0.0.1:8000/` 의 주소에 개발용 서버가 시작되었다고 한다.  
`Chrome` 으로 위의 주소에 접속해보자.

<img width="950px" src="/img/django_tutorial/runserver.png">

우왕 개발용 서버가 진짜로 열려있다! 위와 같이 `It worked!` 라는 메세지가 뜨는 것을 확인하면 된다!  
이제부터 추가되는 다른 기능들은 이 개발용 서버를 들락날락하면서 확인하면 된다.  
개발용 서버는 변경사항이 있을 때마다 **자동으로 리로드하여 적용**시켜 보여준다. 따라서 서버를 껏다 켤 필요가 없다.  
단, **새로운 파일이 추가되었을 경우에는 서버를 다시 실행해주어야 적용된다.**

- - -

### 다른 포트에 runserver 열기

나의 경우 `Jekyll` 블로그의 개발용 서버와 `Django`의 개발용 서버를 동시에 열어놓을 때가 있는데, 가끔 포트가 이미 사용중이라면서 충돌이 날 때가 있다. 이럴 때는 `Django` 개발용 서버를 다른 포트에 열어서 해결하면 된다. 필요하다면 IP도 바꿔줄 수 있다.
```
python manage.py runserver IP번호 포트번호
```

- - -

{% include tutorial-toc-base.html %}

- - -

#### Reference

이한영 강사님 강의자료  
Djangogirls: [https://tutorial.djangogirls.org/ko/](https://tutorial.djangogirls.org/ko/)  
School of Web: [http://schoolofweb.net/blog/posts/%EB%82%98%EC%9D%98-%EC%B2%AB-django-%EC%95%B1-%EB%A7%8C%EB%93%A4%EA%B8%B0-part-1-1/](http://schoolofweb.net/blog/posts/%EB%82%98%EC%9D%98-%EC%B2%AB-django-%EC%95%B1-%EB%A7%8C%EB%93%A4%EA%B8%B0-part-1-1/)
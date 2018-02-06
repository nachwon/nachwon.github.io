---
layout: post
title: '[Django Tutorial] Blog 만들기 - 8. 템플릿'
category: Django
tags:
  - Django
  - Tutorial
  - Template
---



이제 우리는 원하는 내용을 원하는 주소에 표시하는 방법을 알았다.  
그럼 이제 원하는 내용을 그럴싸하게 꾸며서 보여주기만 하면 된다.  
이제 우리의 블로그가 사용자에게 어떻게 보여질지를 한 번 구성해보자. 페이지가 좀 더 블로그 답게 변할 것이다.

- - -

지난 포스트에서 `helloworld` 뷰를 통해 `hello world!` 라는 문자를 출력하도록 해보았다.  
이 `hello world!` 는 `html` 형식으로 표시된 것 같이 보이지만 사실은 `HttpResponse` 로 전달된 데이터에 불과하다. 아무런 가공이 되지 않은 `Raw data` 를 보고 있는 것이다.

<img width="600px" src="/img/django_tutorial/viewsource.png">

크롬에서 `view-source` 를 통해 페이지를 보면 정말 아무것도 없이 `hello world!` 라는 문자열만 덩그러니 있는 것을 볼 수 있다.  
저 문자열 대신에 `html` 파일인 `템플릿 (Template)`을 만들어 출력하도록 한 번 바꿔보자.

- - -
## 템플릿 생성하기

우선 `myproject` 폴더 아래에 `templates` 라는 폴더를 만들어주자. 그리고 `templates` 폴더 아래에 `blog` 라는 이름으로 폴더를 만들어주자.  
```
myproject
├── blog
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── config
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── db.sqlite3
├── manage.py
└── templates  # 템플릿 폴더
    └── blog  # 블로그 앱이 사용할 템플릿을 모아두는 폴더
```

이렇게 하는 이유는 템플릿을 좀 더 체계적으로 관리하기 위함이다. 템플릿들이 어느 위치에 있어도 불러올 수는 있지만 규모가 커질수록 관리하기가 힘들어지기 때문에 모든 템플릿은 `templates` 폴더에 모아놓고, 또 그 안에서 각 템플릿을 사용하는 앱의 이름으로 된 폴더 아래에 템플릿 파일들을 분류해서 관리한다.  
우리는 `blog` 앱 하나만 사용하므로 `templates` 폴더 아래에는 `blog` 폴더 아래에 템플릿 파일을 모아두고 관리하도록 한다.  

`templates/blog` 폴더에 `helloworld.html` 파일을 하나 만들자.

```
templates
└── blog
    └── helloworld.html
```

그리고 아래와 같이 간단한 `html` 을 작성해주자.

```html
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Hello World Template</title>
</head>
<body>
    <h1>Hello World!</h1>
</body>
</html>
```

자 이제 템플릿 파일이 생성되었다. 이 파일을 뷰를 통해 출력해보자.

- - -

## 템플릿 경로 설정하기

뷰에서 템플릿을 출력하기에 앞서 먼저 `Django` 에게 템플릿 폴더의 위치를 알려주어야한다.
`settings.py` 를 열어 아래의 코드를 확인하자.

``` python
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
```
`BASE_DIR` 은 이 프로젝트의 루트 디렉토리를 의미한다.  
`os.path.abspath(__file__)` 는 현재파일 즉, `settings.py` 의 절대경로를 뜻하며,  
`os.path.dirname` 는 인자로 받은 객체가 포함된 경로를 나타내준다.  
따라서 `BASE_DIR` 은 `settings.py` 의 절대경로가 포함된 경로인 `config` 폴더의 경로를 포함하는 `myproject` 폴더를 가리키고 있는 것이 된다.

이렇게 `myproject` 폴더까지의 경로를 `BASE_DIR` 이라는 변수에 저장하여 프로젝트 이곳 저곳에 사용하는 것이다.  
이와 마찬가지로 템플릿 폴더의 위치를 변수로 저장해두고 필요할 때마다 호출해서 쓸 수 있도록 해주자.  

```python
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
```

`os.path.join` 은 두 개의 문자열을 인자로 받아서 첫 번째 인자와 두 번째 인자를 이어 붙인 경로를 만들어준다.  
`BASE_DIR` 은 `myproject` 폴더이므로, 이 경로에 `templates` 를 붙인 `myproject/templates` 를 `TEMPLATE_DIR` 변수에 저장하게 된다.  
이 변수를 `settings.py` 의 `TEMPLATES` 내의 `DIRS` 키의 값으로 넣어주자.

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            TEMPLATE_DIR,  # 템플릿 경로 추가
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
``` 
이렇게 해주면 `Django` 에 템플릿들이 모여있는 폴더의 위치를 알려주는 작업이 끝난다.

- - -

## 템플릿 출력하기

이제 뷰에서 `templates` 폴더 안에 있는 템플릿 파일을 불러와 출력시켜보자.  

`blog` 폴더의 `views.py` 를 열어 `helloworld` 함수를 아래와 같이 바꿔주자.

```python
from django.shortcuts import render


def helloworld(request):
    return render(request, 'blog/helloworld.html')
```

`render` 함수는 두 개의 인자를 필수적으로 받는다. 첫 번째 인자로 `request` 를 받으며, 두 번째 인자로 출력할 템플릿 파일을 받는다. 옵션으로 세 번째 인자에 데이터들이 들어있는 딕셔너리 자료형을 받는데 이것에 대해서는 나중에 자세히 다루도록 하겠다. 

이제 `runserver` 를 실행하고 `localhost:8000` 으로 접속하여 결과를 확인해보자.

<img width="600px" src="/img/django_tutorial/template_helloworld.png">

우리의 템플릿이 잘 출력되는 것을 볼 수 있다.

페이지소스 보기를 해보면 단순히 데이터가 출력된 것이 아니라 `html` 형식으로 출력된 것을 확인할 수 있다.

<img width="600px" src="/img/django_tutorial/template_source.png">

- - -

이제 뷰를 통해 템플릿을 출력하는 것까지 해보았다. 하지만 아직까지 우리가 데이터베이스에 저장해둔 데이터들을 직접 사용한 결과물을 출력하는 것은 구현하지 않았다.  
다음 포스트에서는 템플릿에 데이터를 불러와서 동적으로 `html` 파일을 생성하기 위해 필요한 것들에 대해 알아볼 것이다.

- - -

{% include tutorial-toc-base.html %}

- - -

#### Reference

이한영 강사님 강의자료  
Djangogirls: [https://tutorial.djangogirls.org/ko/](https://tutorial.djangogirls.org/ko/)   
[예제로 배우는 Python 프로그래밍](http://pythonstudy.xyz/python/article/307-Django-%ED%85%9C%ED%94%8C%EB%A6%BF-Template)  
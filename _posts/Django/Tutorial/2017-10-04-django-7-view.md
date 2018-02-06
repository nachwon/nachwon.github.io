---
layout: post
title: '[Django Tutorial] Blog 만들기 - 7. 뷰'
category: Django
tags:
  - Django
  - Tutorial
---



지금까지 `Post` 모델을 만들고 관리자 페이지를 통해서 `Post` 데이터들을 생성해보았다.  
하지만 아직 글의 작성이 관리자 페이지를 통해서만 이루어지도록 되어있다.  
매번 글을 작성하러 관리자 페이지를 들락날락할 수는 없으니, 사용자의 요청에 따라 적절한 결과값을 돌려줄 수 있도록 구성해보자.

- - -

## View 만들기

어떤 사용자가 블로그에 접속했을 때, 무엇을 보게될까?  
지금 우리의 블로그에 접속하면 아래와 같은 화면이 뜬다.

<img width="600px" src="/img/django_tutorial/noview.png">

`runserver` 가 잘 작동하고 있다는 안내메세지가 뜰 뿐 사실상 아무것도 없는 상태이다.  
우린 분명 지난 시간에 관리자 페이지를 통해서 다섯 개의 `Post` 를 작성하였다. 어딘가에는 분명 우리가 작성한 블로그 글들이 존재하고 있지만, 관리자 페이지를 접속하여 직접 데이터베이스를 보는 방법 외에는 글들을 볼 방법이 없다.  
따라서 우리가 가지고 있는 데이터를 가져와서 사용자가 볼 수 있도록 가공하는 과정이 필요할 것이며, 그 작업을 해주는 것이 바로 `MTV` 패턴의 `뷰 (View)` 이다.  

`Django` 는 뷰를 `views.py` 파일을 통해 관리한다. `models.py` 에 모델을 추가해준 것 처럼, `views.py` 에 뷰를 추가해서 뷰를 활성화한다.  
`views.py` 를 열어 아래와 같이 간단한 뷰를 하나 작성해보자.

```python
from django.http import HttpResponse
from django.shortcuts import render

def helloworld(request):
    return HttpResponse('hello world!')
```

뷰는 함수의 형태로 작성하며, `request` 를 인자로 받아서 어떤 `response` 를 돌려준다.  
위의 `helloworld` 뷰는 `request` 를 받아서 `HttpResponse` 를 돌려주며, 그 내용은 `hello world!` 라는 문자열이다.  
이제 이 뷰에 사용자들이 `request` 를 보낼 수 있도록 `URL` 주소를 할당해주어야 한다.

- - -

## URL 설정

웹 어플리케이션의 다양한 기능은 각각의 고유 `URL` 주소를 가지고 있으며, 해당 기능의 주소에 접속하므로써 그 기능을 활성화한다.  
사용자가 어떤 `URL` 주소에 접속하면 그 주소에 `request` 를 보내게 되고, 뷰는 이 `request` 를 받아 `response` 를 돌려주는 것이다. 따라서 우리가 만든 뷰가 작동하려면 다시 말해, `request` 를 받으려면, 어떤 `URL` 주소에 할당되어 있어야한다. 그래야 사용자가 그 주소로 접속하여 `request` 를 보낼 수 있기 때문이다. 우리가 만든 `helloworld` 뷰에 `URL` 주소를 할당해보자.  

`Django` 는 각 기능의 `URL` 주소를 `urls.py` 파일로 관리한다.  
`urls.py` 파일을 열어 내용을 확인해보자.

```python
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]
```

`urlpatterns` 라는 리스트가 보이고, 그 안에 `url` 객체가 하나 들어있는 것을 볼 수 있다.  
이미 들어있는 이 `url` 은 바로 우리가 이전에 보았던 관리자 페이지의 주소이다.  
`url` 객체는 두 개의 인자를 받는다.  

```python
url(정규표현식, 뷰)
```

첫 번째 인자는 정규표현식이며, 해당 정규표현식과 매치가 되면, 두 번째 인자로 받은 뷰를 실행시킨다.  
여기서 잠깐, `Django` 가 `request` 를 받았을 때 처리하는 과정을 간단히 살펴보고 넘어가자.

> #### How Django processes a request
> 
> 한 사용자가 `Django` 웹 페이지를 호출하면, `Django` 는 아래의 알고리즘을 거쳐 어떤 Python 코드를 실행할지 결정한다.
> 1. 먼저 어떤 `URLconf` 모듈을 사용할지 결정한다. 보통의 경우, `settings.py` 의 `ROOT_URLCONF` 변수에 정의되어 있는 모듈을 사용한다. 우리의 경우 `config.urls` 모듈이다.
> 2. 해당 `URLconf`, 즉, 우리의 경우 `config` 폴더안의 `urls.py` 모듈에서 `urlpatterns` 라는 리스트 객체를 찾는다. 이 리스트 객체는 `django.conf.urls.url()` 의 인스턴스인 `url` 객체들의 리스트이다.
> 3. 이 `urlpatterns` 리스트안의 `url` 객체들을 순서대로 하나씩 순회하면서 각 객체가 가진 정규표현식을 호출된 웹 페이지의 `URL` 주소와 매칭시킨다.
> 4. 정규표현식들 중 하나와 매치가 되는 순간 순회를 멈추고 매치된 정규표현식을 가진 `url` 객체의 `view` 를 실행시킨다.
> 5. 만약 매칭되는 정규표현식이 없거나, 어떤 다른 예외가 이 과정 중에 발생할 경우 상황에 적합한 에러 메세지를 리턴한다.


우리가 `localhost:8000/admin/` 이라는 주소로 접속했을 때 관리자 페이지를 볼 수 있었던 것은 `URL` 주소가 정규표현식 `^admin/` 와 매치되어 `admin.site.urls` 라는 뷰를 실행하게 되고 뷰에서 `response` 로 관리자 페이지를 리턴해주었기 때문이다.  

그럼 이제 우리가 만든 `helloworld` 뷰에 `URL` 주소를 할당해보자.  
`urls.py` 를 열어 아래와 같이 작성한다.

```python
from django.conf.urls import url
from django.contrib import admin

from blog.views import helloworld  # views.py에서 우리가 만든 helloworld 함수를 가져온다.

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', helloworld)  # url 객체를 만들어준다.
]
```

정규표현식 `^$` 는 빈 문자열을 뜻한다. `^` 는 뒤따르는 문자열로 시작되는 문자열과 매칭되고, `$` 는 앞선 문자열로 끝이 나는 문자열과 매칭된다. `^admin/` 은 `admin/` 이라는 문자열로 시작하면 매칭된다.  
따라서 `^$` 는 시작하자마자 끝나는 문자열, 다시 말해, 빈문자열과 매칭됨을 뜻한다. 즉, 아무 추가 주소 없는 기본 주소인 `localhost:8000` 과 매칭됨을 뜻한다. 정규표현식에 대한 자세한 사항은 [정규표현식](/python/2017/09/17/regular-expressions.html) 포스트를 참조하기 바란다.  
`URL` 주소를 할당했으니 이제 해당 주소로 접속을 해보자.  
`runserver` 를 실행시키고 웹 브라우저에서 `localhost:8000` 으로 접속해보자.  

<img width="600px" src="/img/django_tutorial/helloworldview.png">

기본 메세지가 아닌 `hello world!` 라는 문자열이 뜨는 것을 확인할 수 있다.  
이제 우리가 원하는 내용을 원하는 주소에 띄울 수 있게 되었다. 지금은 간단하게 `hello world!` 라는 문자열을 `response` 로 돌려주는 것을 해보았지만, 이것 대신에 `html` 문서를 돌려주면 하나의 웹 페이지가 되는 것이다. 온전히 사용자가 보게되는 부분만을 담은 이 `html` 문서를 바로 `템플릿 (Template)` 이라고 한다. 

- - -

{% include tutorial-toc-base.html %}

- - -

#### Reference
이한영 강사님 강의자료  
Djangogirls: [https://tutorial.djangogirls.org/ko/](https://tutorial.djangogirls.org/ko/)  
예제로 배우는 Python 프로그래밍: [http://pythonstudy.xyz/python/article/306-Django-%EB%B7%B0-View](http://pythonstudy.xyz/python/article/306-Django-%EB%B7%B0-View)  
예제로 배우는 Python 프로그래밍: [http://pythonstudy.xyz/python/article/311-URL-%EB%A7%A4%ED%95%91](http://pythonstudy.xyz/python/article/311-URL-%EB%A7%A4%ED%95%91)  
Django 공식문서: [https://docs.djangoproject.com/en/1.9/topics/http/urls/](https://docs.djangoproject.com/en/1.9/topics/http/urls/)
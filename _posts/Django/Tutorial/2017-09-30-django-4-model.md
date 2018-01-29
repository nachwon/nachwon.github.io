---
layout: post
title: '[Django Tutorial] Blog 만들기 - 4. 모델 생성'
category: Django
tags:
  - Django
  - Tutorial
  - Model
---



앱을 시작하였으니 이제 앱이 원하는 기능을 하도록 그 내부를 만들어 주어야한다. `Django` 의 앱은 크게 `모델 (Model)`, `템플릿 (Template)`, `뷰 (View)` 로 구성이 되어 있으며, 앱이 이렇게 구성되도록 하는 개발 패턴을 `MTV` 패턴이라고 한다. 이에 대해 좀 더 알아보자.

- - -

### MVC 패턴

어떤 어플리케이션이 `모델(Model)`, `뷰(View)`, `컨트롤러(Controller)` 로 구성되도록 개발하는 방법을 `MVC` 패턴이라고 한다.

> #### Model-View-Controller (MVC)
>
> 모델-뷰-컨트롤러(Model–View–Controller, MVC)는 소프트웨어 공학에서 사용되는 소프트웨어 디자인 패턴이다. 이 패턴을 성공적으로 사용하면, 사용자 인터페이스로부터 비즈니스 로직을 분리하여 애플리케이션의 시각적 요소나 그 이면에서 실행되는 비즈니스 로직을 서로 영향 없이 쉽게 고칠 수 있는 애플리케이션을 만들 수 있다. MVC에서 모델은 애플리케이션의 정보(데이터)를 나타내며, 뷰는 텍스트, 체크박스 항목 등과 같은 사용자 인터페이스 요소를 나타내고, 컨트롤러는 데이터와 비즈니스 로직 사이의 상호동작을 관리한다.  
> 출처: [위키피디아](https://ko.wikipedia.org/wiki/%EB%AA%A8%EB%8D%B8-%EB%B7%B0-%EC%BB%A8%ED%8A%B8%EB%A1%A4%EB%9F%AC)

`MVC` 패턴은 웹 어플리케이션 개발에서 주로 사용되는 `디자인 패턴` 이다. 

> #### 디자인 패턴
>
> 프로그램 개발에서 자주 나타나는 과제를 해결하기 위한 방법 중 하나로, 과거의 소프트웨어 개발 과정에서 발견된 설계의 노하우를 축적하여 이름을 붙여, 이후에 재이용하기 좋은 형태로 특정의 규약을 묶어서 정리한 것이다.  
> 출처: [위키피디아](https://ko.wikipedia.org/wiki/%EB%94%94%EC%9E%90%EC%9D%B8_%ED%8C%A8%ED%84%B4)

`MVC` 패턴은 웹 어플리케이션을 크게 `모델`, `뷰`,`컨트롤러` 의 세 부분으로 구분한다.

- **모델**: 데이터베이스나 파일 등의 데이터 소스를 제어한다.
- **뷰**: 모델로부터 제공된 데이터를 반영하여 사용자에게 보여주게 되는 부분이다.
- **컨트롤러**: 사용자의 요청을 파악하여 그에 맞는 데이터를 모델에 의뢰하고, 그것을 뷰에 반영하여 사용자에게 제공한다.


<img width="400px" src="/img/django_tutorial/MVC.png">

사용자가 `컨트롤러` 를 조작하면, `컨트롤러` 는 `모델` 을 통해 데이터를 가져오고 그 정보를 `뷰` 에 반영하여 다시 사용자에게 돌려주게 된다.  
웹 어플리케이션이 이와 같은 동작 과정을 가지도록 개발하는 방법론을 `MVC` 패턴이라고 한다. 이러한 방식으로 개발을 하면 유지보수가 용이하며, 개발 참여자들 간 효율적인 커뮤니케이션이 가능해진다는 이점이 있다.

- - -
## MTV 패턴
`Django` 에서는 일반적인 웹 프레임워크들의 `MVC` 패턴과는 조금 다른 `MTV` 패턴을 따른다.  
`MTV` 패턴은 `모델(Model)`, `템플릿(Template)`, `뷰(View)` 로 구성되어 있으며, **템플릿이 `MVC` 의 뷰 역할**을 하고, **뷰가 `MVC` 의 컨트롤러 역할**을 담당한다.

- 모델은 데이터를 표현하는데 사용되며, Python 클래스 형식으로 정의된다. 하나의 모델 클래스는 데이터베이스에서 하나의 테이블로 표현된다.
- 템플릿은 사용자에게 보여지는 부분만을 담당한다.
- 뷰는 HTTP Request를 받아 HTTP Response를 리턴하는 컴포넌트로, 모델로부터 데이터를 읽거나 저장할 수 있다.

- - -

### 모델 만들기

먼저 블로그 앱의 모델을 만들어보자.

> #### Models
>A model is the single, definitive source of information about your data. It contains the essential fields and behaviors of the data you’re storing. Generally, each model maps to a single database table.  
>출처: [Django 공식 문서](https://docs.djangoproject.com/en/1.11/topics/db/models/)

모델은 데이터에 대한 정보를 담고 있으며, 데이터베이스와 직접적으로 연결된다.

- 모델은 Python 클래스이며, `django.db.models.Model` 클래스를 상속받는 서브클래스이다.
- 모델 클래스의 속성들은 데이터베이스의 필드가 된다.
- `Django` 는 모델 클래스를 통해 데이터베이스에 접근할 수 있는 `API` 를 자동적으로 생성해준다.

모델은 `blog` 폴더 내의 `models.py` 파일에 클래스 객체를 생성하여 만들 수 있다.  

우리가 만들려는 블로그에는 어떤 모델이 필요할까? 블로그가 다루는 **데이터**에 대해 잠깐 생각해보자.  
자신이 쓴 글을 등록하여 열람할 수 있게 하는 것이 블로그의 기본 기능일 것이다. 그렇다면 이 때 데이터는 자신이 쓴 **글들**이 될 것이다. 

그럼 하나의 글은 어떤 구조를 가져야할 까?  

- 가장 기본적으로 글의 제목과 내용이 있어야할 것이다.  
- 또, 글쓴이가 누구인지를 표시해주면 좋을 것 같다.  
- 언제 작성된 글인지 표시해주면 유용할 것이다.

이를 정리하면 다음과 같다.  
```
[글] 
 ├─ 글쓴이  
 ├─ 글 제목  
 ├─ 글 내용  
 └─ 글 생성 시간
```
블로그 앱의 `글` 이라는 데이터는 위와 같은 구조를 가진다.  
이 내용을 가지고 모델을 작성해보자.

`blog` 폴더의 `models.py` 파일을 열어 아래와 같이 작성한다.

```python
from django.conf import settings
from django.db import models


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True, null=True)
```

작성글을 뜻하는 `Post` 라는 이름의 클래스를 하나 생성하였다.  
이 클래스는 `django.db.models.Model` 을 상속받아 모델 클래스가 되었다.
그리고 그 클래스 안에 `author (작성자)`, `title (제목)`, `content (글 내용)`, `created_date (글 작성날짜)`, `published_date (글 게시날짜)` 라는 속성을 정의하였다. 모델 클래스의 속성은 데이터베이스에서 하나의 필드가 된다.  


`Post` 클래스에 정의된 필드들을 하나씩 살펴보자.

- - -

- author: 작성자
```python
author = models.ForeignKey(settings.AUTH_USER_MODEL)
```

`models.ForeignKey` 는 필드를 **외래키**로 만들며, 이는 **다른 테이블과 연결**됨을 뜻한다.  
`models.ForeignKey` 는 기본적으로 `일 대 다 (many-to-one)` 관계이며, 연결 대상이 되는 테이블을 인자로 받는다.  
그 외에 다른 여러 옵션을 인자로 전달하여 관계에 대한 자세한 정의를 내릴 수 있다.  
`settings.AUTH_USER_MODEL` 은 `Django` 에 기본적으로 내장된 유저 모델이다. 글들이 작성자 목록 테이블에 연결되도록 `settings.AUTH_USER_MODEL` 를 외래키의 인자로 전달하였다.

- - -

- title: 글 제목
```python
title = models.CharField(max_length=100)
```

`models.CharField` 는 글자 수가 제한된 텍스트 필드를 뜻한다. 글 제목과 같이 짧은 문자열 정보를 저장할 때 사용한다.
필수적으로 제한할 최대 글자 수인 `max_length` 를 인자로 받는다. `max_length=100`은 100자까지 허용하도록 설정한 것이다.

- - -
- content: 글 내용
```python
content = models.TextField(blank=True)
```
`models.TextField` 는 많은 양의 문자열을 저장하는 필드를 뜻한다.  
`blank` 옵션은 필드가 비어 있는 경우를 허용하는가에 대한 옵션이다.

- - -
- created_date: 글 작성 날짜
- published_date: 글 게시 날짜

```python
created_date = models.DateTimeField(auto_now_add=True)
published_date = models.DateTimeField(blank=True, null=True)
```
`models.DateTimeField`는 날짜와 시간 필드를 뜻한다. Python의 `datetime.date` 의 인스턴스로 생성되며 몇 가지 옵션을 인자로 전달할 수 있다.  
`auto_now_add` 옵션은 객체가 처음 생성될 때의 시간을 자동으로 저장하는 옵션이다. 이 옵션은 `settings.py` 에 설정되어 있는 타임존의 시간을 따른다.  
`null` 은 비어있는 값을 데이터베이스에 `NULL` 으로 저장할지에 대한 옵션이다.

- - -

이리하여 블로그에 필요한 핵심 데이터인 `작성글` 에 대한 모델을 만들었다. 다음 과정에서는 이 데이터 구조를 사용할 수 있도록 모델을 데이터베이스에 테이블로 적용시켜 보도록 하자.

- - -

{% include tutorial-toc-base.html %}

- - -

#### Reference
이한영 강사님 강의자료  
Djangogirls: [https://tutorial.djangogirls.org/ko/](https://tutorial.djangogirls.org/ko/)  
Django 공식문서: [https://docs.djangoproject.com/en/1.11/topics/db/models/](https://docs.djangoproject.com/en/1.11/topics/db/models/)  
예제로 배우는 Python 프로그래밍: [http://pythonstudy.xyz/python/article/308-Django-%EB%AA%A8%EB%8D%B8-Model](http://pythonstudy.xyz/python/article/308-Django-%EB%AA%A8%EB%8D%B8-Model)  


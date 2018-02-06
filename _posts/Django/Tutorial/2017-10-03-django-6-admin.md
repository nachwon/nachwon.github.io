---
layout: post
title: '[Django Tutorial] Blog 만들기 - 6. 관리자 페이지'
category: Django
tags:
  - Django
  - Tutorial
---



지난 포스트에서 블로그를 위한 데이터베이스를 설정해주었다. 설정된 데이터베이스에 접근하여 데이터를 생성하거나 삭제하기 위해서는 `관리자` 기능이 필요하다. `Django` 는 데이터베이스 관리를 위한 `관리자 페이지` 를 기본적으로 제공하고 있으므로, 따로 만들어주거나 직접 데이터베이스의 데이터를 수정할 필요가 없다.  

- - -

## 모델 등록

관리자 페이지는 `admin.py` 파일에서 관리한다. 우리가 `blog` 앱을 만들었을 때 `settings.py` 에 등록하여 프로젝트에 사용할 수 있도록 했던 것 처럼, 우리가 만든 `Post` 모델을 관리자 페이지를 통해 사용하려면 `admin.py` 에 등록해주어야 한다.  

`admin.py` 파일을 열어 아래와 같이 추가해준다.

```python
from django.contrib import admin
from blog.models import Post  # models.py로부터 Post 모델을 가져온다.

admin.site.register(Post)  # Post를 관리자 페이지에 등록한다.
```

- - -

## 관리자 페이지 접속

관리자 페이지에 접속하려면 `runserver` 를 실행한 뒤, 웹 브라우저에서 `http://127.0.0.1:8000/admin` 으로 접속한다.  

<img width="500px" src="/img/django_tutorial/admin_main.png">

관리자 로그인 페이지가 뜬다.  
관리자 페이지에 로그인하기 위해서는 먼저 사용자 등록을 해야한다.  
콘솔에서 `manage.py` 파일이 있는 위치로 간 뒤 아래와 같이 입력한다.
```
./manage.py createsuperuser
```

그러면 아래와 같이 `Username` 을 입력하라고 한다. 아이디로 쓸 사용자명을 입력해준다.
```re
Username (leave blank to use 'che1'): nachwon # 비워두면 기본값으로 컴퓨터 유저명이 입력됨.
```

사용자명을 입력하면 `Email` 을 입력하라고 한다. 건너뛰려면 아무것도 입력하지 않으면 된다.
```re
Email address: 
```

그 다음 `Password` 를 입력하라고 한다. 한 번 입력한 후 동일한 비밀번호를 재입력해준다.
```re
Password:
Password (again):
```

아래와 같은 메세지가 출력되면 사용자 등록이 완료된 것이다.
```re
Superuser created successfully.
```

생성한 아이디와 비밀번호로 로그인을 해보자.

<img width="950px" src="/img/django_tutorial/admin_login.png">

관리자 페이지에 접속한 모습이다.

`AUTHENTICATION AND AUTHORIZATION` 항목의 `Users` 를 클릭해보면 등록된 사용자들을 확인할 수 있다.

<img width="950px" src="/img/django_tutorial/admin_users.png">

- - -

## 관리자 페이지에서 데이터 추가하기

이제 관리자 페이지를 이용하여 블로그에 글을 올려보자.  
관리자 페이지 메인화면에서 우리가 만든 `blog` 앱과 그 하위에 있는 `Post` 모델을 확인할 수 있다.  
`add` 버튼을 눌러 새로운 `Post` 를 작성해보자.

<img width="950px" src="/img/django_tutorial/add_post.png">

연습삼아 다른 포스트의 글을 복사해서 채워넣어 보았다.  
`Today` 와 `Now` 를 클릭해 현재 날짜와 시간을 `published_date` 에 넣어주었다.  
내용을 채워넣은 뒤 `Save` 버튼을 누르면 `Post object` 가 성공적으로 추가되었다는 메세지와 함께 `Post object` 가 목록에 추가된 것을 볼 수 있다.


<img width="400px" src="/img/django_tutorial/post_added.png">

같은 방식으로 다섯 개의 글을 추가로 작성해보자. 단, 다섯 개 중 두 개의 글에는 `published_date` 를 빈 칸으로 남겨둔 뒤 저장하자.

<img width="400px" src="/img/django_tutorial/5posts_added.png">

- - -

## 관리자 페이지 환경설정

이어서 진행하기 전에 몇 가지 설정을 해주고 넘어가자.

- - -

### 표준시간 설정

글을 작성할 때 `published_date` 필드의 시간을 입력하는 칸에 `Now` 를 눌러 현재시간을 입력해주었었다. 그런데 입력된 시간이 현재시간이 아닌 것을 볼 수 있다. (23시 34분에 글 작성함.)

<img width="400px" src="/img/django_tutorial/time_message.png">

그리고 그 아래에 작은 글씨로
```re
Note: You are 9 hours ahead of server time.
```

라고 쓰여 있는 것을 볼 수 있다.  
그렇다. 서버의 시간이 실제 현재시간보다 9시간 느린 것이다.  
`Django` 의 서버 시간은 `settings.py` 의 `TIME_ZONE` 변수에 입력된 표준시간 값을 사용한다. 기본값으로는 협정 세계시를 뜻하는 `UTC` 가 입력되어있다.  
아래와 같이 입력하여 대한민국 시간으로 바꿔주자.

```python
TIME_ZONE = 'Asia/Seoul'
```

- - -

### 언어 설정

`TIME_ZONE` 변수 바로 위에 있는 `LANGUAGE_CODE` 변수는 `Django` 에서 사용할 언어를 결정한다. 기본값은 영어인 `en-us` 이다.  
아래와 같이 입력하면 한글로 바뀐 관리자 페이지를 볼 수 있을 것이다.

```python
LANGUAGE_CODE = 'ko-kr'
```

<img width="950px" src="/img/django_tutorial/admin_kor.png">

- - -

### Post 제목 보이게 하기

이 부분은 관리자 페이지 설정은 아니지만 여기서 짚고 넘어가도록 한다.  
앞서 다섯 개의 글을 작성했는데 모든 글들이 `Post object` 라는 이름으로 등록되어 있는 것을 볼 수 있다.  

<img width="400px" src="/img/django_tutorial/5posts_added.png">

`Post object` 대신에 글 제목이 목록에 나타나면 좀 더 글을 구별하기 쉬울 것이다.  
`models.py` 의 `Post` 클래스에 아래와 같이 `__str__` 속성을 추가해주자.

```python
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title
```

이제 다시 관리자 페이지를 확인해보면 글 제목이 목록에 보이는 것을 확인할 수 있다.

<img width="500px" src="/img/django_tutorial/admin_title.png">

- - -

지금까지 관리자 페이지 사용법을 알아보았고, 직접 블로그에 글들도 추가해보았다.  
그런데 지금 상태로는 매번 새로운 글을 쓸 때마다 관리자 페이지에 접속해야한다.  
이러한 상태가 지속되지 않도록 이제부터는 뷰와 템플릿을 통해서 블로그를 좀 더 블로그 답게 만들어보도록 하자.

- - -

{% include tutorial-toc-base.html %}

- - -

#### Reference

이한영 강사님 강의자료  
Djangogirls: [https://tutorial.djangogirls.org/ko/](https://tutorial.djangogirls.org/ko/)  
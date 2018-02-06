---
layout: post
title: '[Django Tutorial] Blog 만들기 - 12. 자세히 보기 페이지'
category: Django
tags:
  - Django
  - Tutorial
---



지금까지 블로그의 메인화면에 글 목록을 나타내도록 했다. 이제 글 하나를 클릭하여 글의 전체 내용을 확인할 수 있는 `자세히 보기` 페이지를 만들어보자.

- - -

## 자세히 보기 페이지 생성

글 하나를 클릭했을 경우 나타날 페이지의 뷰와 템플릿을 작성해보자.  
먼저 `views.py` 를 열어 아래와 같이 추가해준다.

```py
def post_detail(request):
    post = Post.objects.first()
    context = {
        'post': post
    } 
    return render(request, 'blog/post_detail.html', context)
```

이번에는 글 하나에 대한 데이터가 필요하므로, `.first()` 를 써서 첫 번째 `Post` 객체 하나를 `post` 변수에 할당하도록 한 다음, `post` 변수를 딕셔너리로 `post_detail.html` 템플릿에 전달하였다.  
이제 `post_detail.html` 템플릿을 만들어주자.  
`template/blog` 폴더 아래에 `post_detail.html` 파일을 만든 다음 아래와 같이 채워준다.

```html
{{ "{% load static " }}%}
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <link rel="stylesheet" href="{{ "{% static 'bootstrap/css/bootstrap.css' " }}%}">
    <link rel="stylesheet" href="{{ "{% static 'css/blog.css' " }}%}">
    <title>Post_list</title>
</head>
<body>
    <div class="header">
            <h1>Che1's Blog!</h1>
    </div>
    <div class="container">
        <ul class="list">
            <li class="item">
                <h3><a href="">{{ "{{ post.title " }}}}</a></h3>
                <div class="content">{{ "{{ post.content " }}}}</div>
            </li>
        </ul>
    </div>
</body>
</html>
```

딕셔너리로 전달된 `post` 는 쿼리셋이 아닌 `Post` 객체 하나이므로, `for` 문으로 순회할 필요없이 바로 접근할 수 있다. 그래서 `for` 문을 삭제하고 `post.title` 과 `post.content` 를 사용해서 글의 제목과 글 전체 내용이 모두 표시되도록 해주었다. 이제 `URL` 주소를 할당해줄 차례이다.
`urls.py` 를 열어 아래와 같이 `urlpatterns` 리스트에 새로 추가해주자.

```py
from blog.views import post_list, post_detail  # post_detail 뷰를 불러오기

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', post_list),
    url(r'^post/', post_detail),  # post로 시작하는 url 주소와 매치
]
```

`기본주소/post/` 를 자세히 보기 페이지의 `URL` 주소로 할당해주었다. `runserver` 를 열어서 접속해보자.

<img width="950px" src="/img/django_tutorial/post_detail_first.png">

글 제목과 글 내용 전체가 잘 표시되는 것을 확인할 수 있다. 그런데, 글에 줄바꿈이 하나도 없이 쭉 붙어있다... 이 부분은 템플릿에서 필터를 적용해주어 고쳐줄 수 있다.  
`post_detail.html` 의 `post_content` 부분을 아래와 같이 바꿔준다.

```html
<div class="content">{{ "{{ post.content|linebreaksbr " }}}}</div>
```

`html` 은 기본적으로 공백문자를 인식하지 못하는데 `linebreaksbr` 필터를 사용하면 줄바꿈이 일어나는 곳에 `<br>` 테그를 추가해준다.

<img width="950px" src="/img/django_tutorial/post_detail_linebreaks.png">

자 이제 자세히 보기 페이지가 완성되었다. 그런데 아직 해결되지 않은 몇 가지 문제점이 있다. 일단 가장 시급한 문제는 `Post.objects.first()` 로 인해 첫 번째 `Post` 객체만 조회할 수 있다는 것이다. 코드를 수정해서 각각의 `Post` 객체들이 자기 자신만의 `post_detail` 페이지를 가질 수 있도록 해보자.

- - -

## URL 주소 동적 생성

지금까지는 `URL` 주소를 정적으로 생성해왔다. `post_detail.html` 템플릿은 `기본주소/post/` 라는 고정된 하나의 주소로만 접근이 가능하다. 만약에 각각의 `Post` 객체에 `post_detail` 템플릿을 부여하고, `URL` 주소를 할당하려면 각각의 `Post` 에 대해 따로 뷰와 템플릿을 만들어주고 고유의 `URL` 주소를 매번 할당해주어야 할 것이다.

```py
# views.py
def post_detail_1(request):
    post = Post.objects.filter(id=1)
    context = {
        'post': post
    }
    return render(request, 'blog/post_detail_1.html', context)


def post_detail_2(request):
    post = Post.objects.filter(id=2)
    context = {
        'post': post
    }
    return render(request, 'blog/post_detail_2.html', context)
.
.
.
```
```py
# urls.py
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', post_list),
    url(r'^post/1', post_detail_1),
    url(r'^post/2', post_detail_2),
    .
    .
    . 
]
```
```py
# template/blog
post_detail_1.html
post_detail_2.html
.
.
.
```

생각만해도 끔찍하기 때문에 한 줄의 코드로 여러 개의 자세히 보기 페이지를 동적으로 생성해보자.  
먼저 `urls.py` 를 열어 아래와 같이 수정한다.

```py
from blog.views import post_list, post_detail  

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', post_list),
    url(r'^post/(?P<pk>\d+)/', post_detail),
]
```

정규표현식 `post/(?P<pk>\d+)/` 은 `post/` 에 이어서 `\d+` 즉, 어떤 숫자(`\d`)가 1 개 이상(`+`) 올 수 있으며, 그 숫자는 `pk` 라는 이름의 그룹에 포함된다는 뜻이다. 여기서 `pk` 는 `primary key` 의 약자로, 데이터베이스의 `기본키`를 뜻한다.  

여기까지 해두고 잠깐 `runserver` 를 실행시켜 확인해보자. `기본주소/post/` 끝에 아무 숫자나 넣어서 접속해보자.  

<img width="950px" src="/img/django_tutorial/post_detail_error.png">

위와 같이 에러가 뜬다.
```
post_detail() got an unexpected keyword argument 'pk'
```

에러 내용을 살펴보면 `post_detail` 뷰가 `pk` 라고 하는 예상치 못한 키워드 인자를 받았다고 한다. 즉, `views.py` 의 `post_detail` 함수는 키워드 인자를 받지 않는데 `pk` 라는 키워드 인자가 전달되었다는 말이다.  
사용자가 예를들어 `post/1` 의 주소에 접속하면 `r'^post/(?P<pk>\d+)/'` 와 매칭되고 `post_detail` 함수에 `request` 가 전달되어 실행된다. 그런데 여기서 숫자 `1` 이 `pk` 라는 이름의 그룹에 저장되어 있는데 이럴 경우에는 `post_detail` 함수에 `request` 와 함께 `pk=1` 이라는 키워드 인자가 전달된다. `post_detail` 함수는 `request` 만 받도록 되어 있으므로 에러가 나는 것이다.  
이를 해결하기 위해서 아래와 같이 `post_detail` 함수가 `pk` 라는 키워드 인자를 받도록 해주자.

```py
def post_detail(request, pk):  # pk 매개변수 추가
    post = Post.objects.first()
    context = {
        'post': post
    }
    return render(request, 'blog/post_detail.html', context)
```

그럼 이제 다시 자세히 보기 페이지가 나타나는 것을 볼 수 있다.  
이제 `URL` 주소는 `post/` 뒤에 어떤 숫자가 붙던간에 자세히 보기 페이지를 보여준다. 동적으로 `URL` 주소가 할당되는 것이다. 하지만 아직까지 어떤 숫자가 오던 `Post.objects.first()` 로 불러온 데이터를 담고 있는 `post_detail.html` 만을 불러온다. 그럼 `post/` 뒤에 붙는 값에 따라 서로 다른 `Post` 객체를 데이터베이스에서 불러와 `post_detail.html` 템플릿에 전달하게 해주면 되지 않을까? 

- - -

## 동적 뷰를 통한 템플릿 구성

그렇게 하기 위해서는 데이터베이스에서 각 `Post` 객체들이 고유하게 가지는 어떤 값을 참조해 데이터를 불러와야한다. 글 제목 같은 것을 참조해오면 되지 않을까 싶지만 만에 하나 똑같은 글 제목을 가진 `Post` 가 생성된다면 문제가 생길 것이다. 항상 각 객체가 고유하게 가지는 값이 하나 있는데 이 값을 `기본키` 라고 한다.

> ##### 기본키 (Primary Key)
>
> 기본 키(primary key)는 주 키 또는 프라이머리 키라고 하며, 관계형 데이터베이스에서 조(레코드)의 식별자로 이용하기에 가장 적합한 것을 관계 (테이블)마다 단 한 설계자에 의해 선택, 정의된 후보 키를 말한다. 유일 키는 0~1개 이상의 속성의 집합으로 볼 수 있다.[1] 즉, 관계에 저장된 레코드를 고유하게 식별하는 후보 키 (=속성 또는 속성의 집합) 가운데, 설계자가 일반적으로 이용되어야한다고 정해 놓은 것을 가리킨다.  
> 출처: [위키피디아](https://ko.wikipedia.org/wiki/%EA%B8%B0%EB%B3%B8_%ED%82%A4)

`Post` 모델을 생성할 때 잠깐 보고 넘어갔었는데, `Post` 모델에는 우리가 지정해주지 않은 필드인 `id` 라는 필드가 자동으로 생성되어 있으며 이 필드는 `기본키` 로 설정되어있다. `id` 필드는 글이 생성될 때마다 1 부터 시작해서 하나씩 커지는 값을 저장한다.  
`SQLite Browser` 를 열어서 직접 확인해보자.

<img width="600px" src="/img/django_tutorial/primary_key.png">

각 데이터마다 숫자로된 `id` 값을 가지고 있는 것을 볼 수 있다. 이 값을 참조해오도록 하자.  
사실 정규표현식에서 `post/` 뒤에 **숫자**를 받도록 하고 그 숫자를 `pk` 라는 그룹에 할당해준 것이 모두 `id` 값을 참조해서 데이터를 불러오도록 하려는 큰그림을 그린 것이었던 것이다.  
아까 `views.py` 의 `post_detail` 함수가 `pk` 값을 받도록 설정했다. 이 `pk` 값은 사용자가 접속한 `기본주소/post/` 에 따라 붙는 숫자이며 이 값을 가지고 데이터베이스의 `id` 값과 매칭시켜 같은 `id` 값을 가지는 `Post` 객체를 불러와 템플릿에 전달할 것이다.  
아래와 같이 `post_detail` 함수를 수정하자.

```py
def post_detail(request, pk):  
    post = Post.objects.get(pk=pk)
    context = {
        'post': post
    }
    return render(request, 'blog/post_detail.html', context)
```

`.get()` 은 전달받은 인자와 일치하는 하나의 객체를 가져온다. `pk` 는 `primary key` 를 의미하며 지금의 경우 `blog_post` 테이블의 `id` 필드의 레코드 값이다. `=pk` 의 `pk` 는 우리가 만들었던 정규표현식의  `pk` 그룹의 값이 키워드 인자로 전달된 것이다.  
이제 `기본주소/post/1` 의 주소로 접속하면 `post_detail` 함수에 `pk=1` 이 전달되어 `Post.objects.get(pk=1)` 이 실행되고, 이 명령은 `ORM` 을 통해 기본키, 즉 `id` 값이 1 인 `Post` 객체를 불러와 `post` 변수에 할당하고 이것을 `post_detail.html` 템플릿에 전달하여 데이터를 표시하게 된다. `post_detail.html` 템플릿은 하나이지만 그 내부에서 표시할 데이터만 `id` 값에서 참조해온 데이터로 바꿔치기 해줌으로써 서로 다른 내용을 표시할 수 있게 되었다. 

```
localhost:8000/post/1/
```

<img width="950px" src="/img/django_tutorial/post_1_detail.png">

```
localhost:8000/post/2/
```

<img width="950px" src="/img/django_tutorial/post_2_detail.png">


- - -

## 링크 동적으로 연결하기

이제 각 `Post` 객체를 연결할 수 있는 `post_detail.html` 템플릿을 그려주는 뷰가 완성되었고, 각각의 템플릿으로 접속할 수 있는 `URL` 또한 동적으로 할당할 수 있게 되었다. 이제 마지막으로 각 `URL` 을 간편하게 접속할 수 있도록 `post_list` 템플릿의 `a` 태그에 연결해주는 일만 남았다.  
`post_list.html` 을 열어 내용을 확인해보자.

```html
<body>
    <div class="header">
            <h1>Che1's Blog!</h1>
    </div>
    <div class="recent">Recent Posts</div>
    <div class="container">
        <ul class="list">
            {{ "{% for post in posts " }}%}
            <li class="item">
                <h3><a href="">{{ "{{ post.title " }}}}</a></h3>
                <div class="content">{{ "{{ post.content|truncatewords:50 " }}}}</div>
                <div class="info">
                    <div class="published-date"><span>Date | </span>{{ "{{ post.published_date " }}}}</div>
                    <div class="author"><span>Author | </span>{{ "{{ post.author " }}}}</div>
                </div>
                
            </li>
            {{ "{% endfor " }}%}
        </ul>
    </div>
</body>
```

각 `Post` 의 제목을 클릭하면 해당 `Post` 의 자세히 보기 페이지로 넘어갈 수 있도록 링크를 걸어주자.

```html
<h3><a href="post/{{ "{{ post.pk "}}}}">{{ "{{ post.title " }}}}</a></h3>
```

이렇게 해주면 `{{ "{{ post.pk "}}}}` 자리에 각 `Post` 의 `id` 값이 불러져와서 `post/id값` 의 주소로 `request` 를 보내게 된다. `runserver` 를 열어서 `post_list` 템플릿의 소스보기를 해보자.

```html
<h3><a href="/post/3">[Django Tutorial] Blog 만들기 - 3. 앱</a></h3>
<h3><a href="/post/2">[Django Tutorial] Blog 만들기 - 2. 프로젝트 시작</a></h3>
<h3><a href="/post/1">[Django Tutorial] Blog 만들기 - 1. 환경설정</a></h3>
```

생성된 `a` 태그들의 `href` 속성을 보면 각각의 `id` 값이 들어간 `URL` 이 생성되어 있는 것을 볼 수 있다.

- - -

다음 포스트에서는 템플릿 들의 중복된 부분을 하나로 묶어주는 **템플릿 확장**에 대해 알아볼 것이다.

- - -

{% include tutorial-toc-base.html %}

- - -

#### Reference
이한영 강사님 강의자료  
Djangogirls: [https://tutorial.djangogirls.org/ko/](https://tutorial.djangogirls.org/ko/)
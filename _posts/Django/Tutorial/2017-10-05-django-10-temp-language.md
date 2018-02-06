---
layout: post
title: '[Django Tutorial] Blog 만들기 - 10. 템플릿 언어'
category: Django
tags:
  - Django
  - Tutorial
  - Template
---



이제 `ORM` 을 통해 데이터베이스의 데이터를 다루는 방법까지 알았으니 이렇게 불러온 데이터를 템플릿에 적용시켜주면 동적으로 템플릿을 생성할 수 있다. 그럼 데이터를 템플릿에 적용하는 방법에 대해 알아보자.

- - -

우리가 만들려고 하는 블로그의 메인 페이지는 어떻게 구성되어야 하는지에 대해 잠시 생각해보자. 보통 블로그 메인 페이지에는 작성된 글들이 최근 업데이트된 순서대로 나열되어 있다. 이것을 구현하는 `html` 구조를 간단히 생각해보자.

```html
<body>
    <ul>
        <li>Post</li>
        <li>Post</li>
        <li>Post</li>
        .
        .
        .
    </ul>
</body>
```

이런 식으로 구성을 하면 메인화면에 `Post` 들이 쭉 나열된 화면을 볼 수 있을 것이다. 그런데 새로운 글이 추가되었을 경우를 생각해보자. 새로운 글이 추가될 때 마다 `html` 구조를 수정해야한다.
```html
<body>
    <ul>
        <li>New_Post</li>
        <li>Post</li>
        <li>Post</li>
        <li>Post</li>
        .
        .
        .
    </ul>
</body>
```

이렇게 하면 매우 번거로울 것이다. 그래서 중복되는 작업을 자동화해두면 좋을 것 같다.
```html
<body>
    <ul>
        <li>Post_data</li>  # 이 부분을 자동화
    </ul>
</body>
```
`Post` 데이터가 표시될 부분은 항상 일정하므로 데이터베이스에서 데이터만 가져와서 `Post` 데이터가 표시될 부분에 데이터만 바꿔서 여러 개의 태그를 자동적으로 생성해주면 일일히 새 태그를 추가해줄 필요가 없을 것 같다. 이것을 가능하게 해주는 것이 `템플릿 언어` 이다.

- - -

## 템플릿에 데이터 전달하기

템플릿에 데이터를 적용시켜 표시하려면 먼저 데이터를 전달하는 방법을 알아야한다. 이 작업은 뷰에서 이루어진다.   
일단 블로그 메인 화면에 나타날 `Post` 들의 목록을 만들어 줄 것이므로 `views.py` 를 열어 `helloworld` 함수를 `post_list` 라는 함수로 바꿔주자.

```py
def post_list(request):
    return render(request, 'blog/post_list.html')
```

이에 맞춰서 `urls.py` 와 `helloworld.html` 파일의 이름도 수정해준다.

```py
# urls.py
from blog.views import post_list

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', post_list)
```
```
helloworld.html -> post_list.html
```

이제 `views.py` 로 다시 돌아와서 아래와 같이 추가로 입력해주자.

```py
def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'blog/post_list.html', context)
```

무슨 짓을 한건지 하나씩 살펴보자.

```py
posts = Post.objects.all()
```
위 명령은 지난 포스트에서 알아보았던 `ORM` 을 통해 쿼리셋을 가져오는 명령이다. 블로그 메인화면에 모든 `Post` 들을 나타나게 해야하므로 `all()` 을 사용해 모든 `Post` 객체의 쿼리셋을 가져와 `posts` 라는 변수에 할당한 것이다.

```py
context = {
    'posts': posts,
}
```

가져온 `posts` 쿼리셋을 `posts` 라는 키의 값으로 할당하여 딕셔너리를 만든 다음 이것을 `context` 라는 변수에 할당하였다. 이렇게 하는 이유는 바로 다음에 이어지는 `render` 함수의 세 번째 인자에 전달하기 위함이다.

```py
return render(request, 'blog/post_list.html', context)
```
`render` 는 세 번째 인자로 딕셔너리 타입의 데이터를 받는다. 그리고 템플릿 내부에서 템플릿 언어를 통해 이 딕셔너리 타입 데이터의 키를 호출하여 데이터를 가져올 수 있다. 즉, 템플릿 언어가 `posts` 라는 키를 호출하면 `posts` 변수에 할당되어있는 쿼리셋에 접근할 수 있게 되는 것이다.

- - -

## 템플릿 언어

이제 템플릿에 데이터를 전달까지 했으니 그 데이터를 호출해서 `html` 파일에 적용시키기만 하면 된다. 그런데 데이터를 가져오려면 딕셔너리 데이터의 키를 호출해야하는데 `html` 에서 무슨 수로 키를 호출할 수 있을까?  
Python 문법을 알아들을 수 없는 `html` 을 위해 템플릿 언어라는 것을 사용한다. `Django` 에는 내장된 템플릿 언어가 기본적으로 적용되어 있으며, 템플릿 언어의 지정은 `settings.py` 의 `TEMPLATES` 딕셔너리에서 `BACKEND` 키의 값을 수정하여 해줄 수 있다.

```python
TEMPLATES = [
    {
        # 기본적으로 Django 템플릿 언어인 DjangoTemplates 가 설정되어있다.
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  
        'DIRS': [
            TEMPLATE_DIR,
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

- - -

### 변수 호출

템플릿 언어에서 변수 호출은 아래와 같이 한다.

```html
{{ "{{ 변수명 " }}}}
```

`post_list.html` 을 열어 아래와 같이 입력해보자.

```html
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Post_list</title>
</head>
<body>
    <h1>{{ "{{ posts " }}}}</h1>
</body>
</html>
```

그리고 `runserver` 를 열어 확인해보면 아래와 같이 뜨는 것을 확인할 수 있다.

<img width="950px" src="/img/django_tutorial/Post_list.png">

`shell_plus` 에서 `Post.objects.all()` 을 입력한 것과 똑같은 결과가 출력되었다. `view.py` 에서 전달된 딕셔너리에 `posts` 키의 값이 쿼리셋이기 때문에 그것이 그대로 출력된 것이다.

- - -

### 객체 순회하기

쿼리셋은 `순회가능(Iterable)` 객체이다. `shell_plus` 에서 아래와 같이 실행해보자.

```python
posts = Post.objects.all()
for post in posts:
    print(post)
```
```re
[Django Tutorial] Blog 만들기 - 1. 환경설정
[Django Tutorial] Blog 만들기 - 2. 프로젝트 시작
[Django Tutorial] Blog 만들기 - 3. 앱
[Django Tutorial] Blog 만들기 - 4. 모델
[Django Tutorial] Blog 만들기 - 5. 데이터베이스
```

`Post` 를 하나씩 출력시키기 위해서는 이 쿼리셋을 순회하면서 `Post` 데이터 하나씩을 가져와 출력시켜야한다.  

템플릿 언어에서 순회가능 객체를 순회하기 위해서는 아래와 같이 `for` 문을 사용한다.

```html
{{ "{% for 변수 in 순회가능객체 " }}%}
    {{ "{{ 변수 " }}}}
{{ "{% endfor " }}%}
```

`post_list.html` 에 아래와 같이 적용해보자. (가독성을 위해 `body` 부분만 표시함.)

```html
<body>
    <h1>Welcome to Che1's Blog!</h1>
    <ul>
        {{ "{% for post in posts " }}%}
        <li>
            <div class="title"><a href="">{{ "{{ post.title " }}}}</a></div>
        </li>
        {{ "{% endfor " }}%}
    </ul>
</body>
```

`runserver` 로 확인해보면 아래와 같이 목록이 나타나는 것을 확인할 수 있다!!

<img width="600px" src="/img/django_tutorial/post_lists.png">

`for` 문으로 쿼리셋의 객체를 하나씩 순회하면서 `Post` 객체의 `title` 필드의 내용에 `li`, `div`, `a` 태그를 붙여주었다.  
좀 더 응용해서 글 내용까지 보여주도록 만들어보자.

```html
<body>
    <h1>Welcome to Che1's Blog!</h1>
    <ul>
        {{ "{% for post in posts " }}%}
        <li>
            <div class="title"><a href="">{{ "{{ post.title " }}}}</a></div>
            <div class="content">{{ "{{ post.content " }}}}</div>
        </li>
        {{ "{% endfor " }}%}
    </ul>
</body>
```

<img width="950px" src="/img/django_tutorial/post_content.png">

- - -

### 필터 적용하기

글 내용까지 보이게 만들긴 했는데 글 전체가 다 보이니 너무 정신이 없다. 몇 개의 단어까지만 보여주도록 설정해보자.
```html
{% raw %}
<body>
    <h1>Welcome to Che1's Blog!</h1>
    <ul>
        {% for post in posts %}
        <li>
            <div class="title"><a href="">{{ "{{ post.title " }}}}</a></div>
            <div class="content">{{ "{{ post.content|truncatewords:30 " }}}}</div>
        </li>
        {% endfor %}
    </ul>
</body>
{% endraw %}
```

변수 옆에 `|` 를 붙여서 필터를 적용할 수 있다. 여기서는 글 내용에 `truncatewords` 라는 단어 수 필터를 적용하여 30 단어까지만 보여주도록 만들어 주었다. 필터의 종류는 [Django 공식문서](https://docs.djangoproject.com/en/1.11/ref/templates/builtins/#ref-templates-builtins-filters1) 에서 확인할 수 있다.

<img width="950px" src="/img/django_tutorial/truncate.png">

- - -

### if 조건문 

이제 어느 정도 깔끔해진 것 같다. 이제 글 게시 날짜도 표시해보자.

```html
<body>
    <h1>Welcome to Che1's Blog!</h1>
    <ul>
        {{ "{% for post in posts " }}%}
        <li>
            <div class="title"><a href="">{{ "{{ post.title " }}}}</a></div>
            <div class="content">{{ "{{ post.content|truncatewords:30 " }}}}</div>
            <div class="published-date">{{ "{{ post.published_date " }}}}</div>
        </li>
        {{ "{% endfor " }}%}
    </ul>
</body>
```

<img width="950px" src="/img/django_tutorial/published_date.png">

글 게시날짜도 잘 표시가 되는 것을 볼 수 있다. 그런데 몇몇 글에는 게시날짜가 없는 것을 볼 수 있다. 이는 우리가 `Post` 객체를 만들 때 몇 개의 글에는 `published_date` 필드를 비워두었기 때문인데, 게시날짜가 없는 글은 표시가 되지 않도록 한번 바꿔보자.

```html
<body>
    <h1>Welcome to Che1's Blog!</h1>
    <ul>
        {{ "{% for post in posts " }}%}
        {{ "{% if post.published_date != None " }}%}
        <li>
            <div class="title"><a href="">{{ "{{ post.title " }}}}</a></div>
            <div class="content">{{ "{{ post.content|truncatewords:30 " }}}}</div>
            <div class="published-date">{{ "{{ post.published_date " }}}}</div>
        </li>
        {{ "{% else " }}%}
        {{ "{% endif " }}%}
        {{ "{% endfor " }}%}
    </ul>
</body>
```

게시날짜가 없는 글은 표시되지 않도록 하는 방법은 크게 두 가지가 있다.  
하나는 위의 예 처럼 템플릿 언어에서 `if` 문을 사용하는 것이다. `if` 문은 아래와 같이 사용한다.

```html
{{ "{% if 조건 1 " }}%}
조건 1이 참인 경우 실행할 명령
{{ "{% elif 조건 2 " }}%}
조건 2가 참인 경우 실행할 명령
.
.
.
{{ "{% else " }}%}
모든 조건이 거짓인 경우 실행할 명령
{{ "{% endif " }}%}
```

위의 예에서는 `published_date` 가 `None` 이 아니면 `li` 태그를 만들고, `None` 이면 아무것도 하지 않도록 `if` 문을 넣어준 것이다.  
또다른 방법은 뷰에서 컨트롤해주는 방법이다. `views.py` 를 열어 아래와 같이 수정해주자.

```py
def post_list(request):
    posts = Post.objects.filter(published_date__isnull=False).order_by('-created_date')  # 수정된 부분
    context = {
        'posts': posts,
    }
    return render(request, 'blog/post_list.html', context)
```

기존에는 `Post.objects.all()` 을 통해 모든 `Post` 객체들의 쿼리셋을 `posts` 로 템플릿에 전달했지만, 이번에는 `.filter(published_date__isnull=False)` 로 필터를 걸어서 `published_date` 가 빈 값이 아닌 `Post` 객체들의 쿼리셋을 가져오도록 바꿔준 것이다.  
아 그리고 바꿔주는 김에 `order_by('-created_date')` 를 추가해서 최신 글이 가장 위로 오도록 정렬해주었다.  
이 두 방법의 결과는 아래와 같이 동일하다.

<img width="950px" src="/img/django_tutorial/published_date_none.png">

위 두 가지 방법 중 더 좋은 방법은 아무래도 뷰를 통해 쿼리셋 자체를 바꿔주는 방법일 것이다. 더 적은 쿼리셋을 가져오게 되므로 처리속도가 더 빠르지 않을까? 흠... 이 부분에 대해서는 데이터베이스 쿼리에 대한 좀 더 자세한 이해가 필요할 것 같다. 처리속도를 고려하지 않고서도 데이터의 가공은 뷰의 역할이므로 가능한 모든 데이터의 가공은 뷰에서 처리해주는 것이 구조상으로도 더 나아보인다.  

- - -

아무튼 이제 블로그의 메인화면이 구성되었다. 이제 좀 더 알록달록하고 예쁘게 꾸며보도록 하자.
- - -

{% include tutorial-toc-base.html %}

- - -

#### Reference

이한영 강사님 강의자료  
Djangogirls: [https://tutorial.djangogirls.org/ko/](https://tutorial.djangogirls.org/ko/)  
Django 공식문서: [https://docs.djangoproject.com/en/1.11/ref/templates/language/](https://docs.djangoproject.com/en/1.11/ref/templates/language/)
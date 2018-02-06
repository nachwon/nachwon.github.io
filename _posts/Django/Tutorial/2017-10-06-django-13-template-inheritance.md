---
layout: post
title: '[Django Tutorial] Blog 만들기 - 13. 템플릿 상속'
category: Django
tags:
  - Django
  - Tutorial
  - Template
---



지난 포스트에서 `post_detail` 이라는 템플릿을 새로 만들어 주었다. 그런데 이 템플릿은 `post_list` 템플릿과 많은 부분에서 겹친다. 지금이야 템플릿이 `post_list` 와 `post_detail` 두 개 밖에 없지만, 만약 많은 수의 템플릿이 있고 모두 공통적으로 가지고 있는 부분이 있다고 할 때, 공통적인 그 부분을 수정할 일이 생기면 모든 템플릿을 하나 하나 수정해주어야하는 대참사가 생길 수 있다. 진정한 프로그래머는 같은 코드를 반복하지 않는다고 하던데 우리도 반복되는 부분을 한 번 줄여보자.
- - -

`post_list` 템플릿과 `post_detail` 템플릿을 열어서 내용을 비교해보자.

```html
# post_list.html

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
    <div class="recent">Recent Posts</div>
    <div class="container">
        <ul class="list">
            {{ "{% for post in posts " }}%}
            <li class="item">
                <h3><a href="/post/{{ post.id }}">{{ "{{ post.title " }}}}</a></h3>
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
</html>
```

```html
# post_detail.html

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
                <div class="content">{{ "{{ post.content|linebreaksbr " }}}}</div>
            </li>
        </ul>
    </div>
</body>
</html>
```

자세히 살펴보면 `<div class="recent">Recent Posts</div>` 와 `<div class="container">` 안에 있는 내용을 제외하면 완전히 동일한 구조임을 알 수 있다. 이러한 상태에서 `<title>` 태그 안의 내용을 `Che1's blog` 로 바꾸려면 `post_list` 템플릿에서 한 번, `post_detail` 템플릿에서 한 번, 총 두 번의 수정을 해야한다.  
`템플릿 상속` 을 사용하면 이러한 수고를 덜어줄 수 있다.  
`template` 폴더 바로 아래에 `base.html` 이라는 파일을 하나 만들고 두 템플릿에서 겹치는 부분을 복사해서 붙여넣기 하자. 이 `base.html` 은 **부모 템플릿**이 된다.

```html
# base.html

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

</body>
</html>
```

그리고 `post_list.html` 과 `post_detail.html` 에서 `base.html` 과 겹치는 부분을 모두 지워준다. `post_list.html` 는 `Recent Post` 부분과 `<div class="container">` 부분만, `post_detail.html` 는 `<div class="container">` 부분만 남겨주면 된다. 이 두 템플릿은 **자식 템플릿**이 된다.

```html
# post_list.html

    <div class="recent">Recent Posts</div>
    <div class="container">
        <ul class="list">
            {{ "{% for post in posts " }}%}
            <li class="item">
                <h3><a href="/post/{{ post.id }}">{{ "{{ post.title " }}}}</a></h3>
                <div class="content">{{ "{{ post.content|truncatewords:50 " }}}}</div>
                <div class="info">
                    <div class="published-date"><span>Date | </span>{{ "{{ post.published_date " }}}}</div>
                    <div class="author"><span>Author | </span>{{ "{{ post.author " }}}}</div>
                </div>
            </li>
            {{ "{% endfor " }}%}
        </ul>
    </div>
```

```html
# post_detail.html

    <div class="container">
        <ul class="list">
            <li class="item">
                <h3><a href="">{{ "{{ post.title " }}}}</a></h3>
                <div class="content">{{ "{{ post.content|linebreaksbr " }}}}</div>
            </li>
        </ul>
    </div>
```

이제 다시 `base.html` 로 돌아와서 아래와 같이 입력해준다.

```html
# base.html

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
    {{ "{% block content " }}%}
    {{ "{% endblock " }}%}
</body>
</html>
```
`block` 템플릿 태그는 부모 템플릿에서는 자식 템플릿이 들어갈 부분을 표시해주는 역할을 하고, 자식 템플릿에서는 상속받은 부모 템플릿에 들어갈 부분을 표시하는 역할을 한다. 

```html
{{ "{% block 블럭이름 " }}%}
{{ "{% endblock" }}%}
```

자식 템플릿은 부모 템플릿을 상속받아서 같은 이름의 블럭 태그 자리에 들어가게 된다.  
위와 같이 부모 템플릿인 `base.html` 에 다른 내용이 덧붙여질 부분에 블럭 태그를 넣어주고, 그 다음 자식 템플릿들을 열어 아래와 같이 추가해주자.

```html
# post_list.html

{{ "{% extends 'base.html' " }}%}

{{ "{% block content " }}%}
    <div class="recent">Recent Posts</div>
    <div class="container">
        <ul class="list">
            {{ "{% for post in posts " }}%}
            <li class="item">
                <h3><a href="/post/{{ post.id }}">{{ "{{ post.title " }}}}</a></h3>
                <div class="content">{{ "{{ post.content|truncatewords:50 " }}}}</div>
                <div class="info">
                    <div class="published-date"><span>Date | </span>{{ "{{ post.published_date " }}}}</div>
                    <div class="author"><span>Author | </span>{{ "{{ post.author " }}}}</div>
                </div>
            </li>
            {{ "{% endfor " }}%}
        </ul>
    </div>
{{ "{% endblock " }}%}
```

```html
# post_detail.html

{{ "{% extends 'base.html' " }}%}

{{ "{% block content " }}%}
    <div class="container">
        <ul class="list">
            <li class="item">
                <h3><a href="">{{ "{{ post.title " }}}}</a></h3>
                <div class="content">{{ "{{ post.content|linebreaksbr " }}}}</div>
            </li>
        </ul>
    </div>
{{ "{% endblock " }}%}
```

`extends` 태그는 자식 템플릿이 상속받을 부모 템플릿을 알려주는 역할을 한다.
```html
{{ "{% extends '부모템플릿.html' " }}%}
```

이렇게 작성해주면 자식 템플릿의 `{{ "{% block content " }}%}` 부터 `{{ "{% endblock " }}%}` 사이에 있는 내용이 부모 템플릿의 `{{ "{% block content " }}%}` 와 `{{ "{% endblock " }}%}` 사이에 들어가서 이어지게 된다.  
`runserver` 를 실행시켜 확인해보면 원래 표시되던 화면 그대로 나타나는 것을 확인할 수 있다.  
이제 `title` 태그의 내용을 바꿔보자.

```html
# base.html

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
    <title>Che1's blog</title>
</head>
<body>
    <div class="header">
            <h1>Che1's Blog!</h1>
    </div>
    <div class="recent">Recent Posts</div>
    {{ "{% block content " }}%}
    {{ "{% endblock " }}%}
</body>
</html>
```

`runserver` 를 확인해보면 블로그 메인 화면과 자세히 보기 페이지 모두의 탭 이름이 `Che1's blog` 로 바뀐 것을 볼 수 있다.

<img width="400px" src="/img/django_tutorial/post_list_tab.png"> <img width="400px" src="/img/django_tutorial/post_detail_tab.png">

이렇게 공통된 부분을 따로 템플릿으로 만들어 두면 템플릿 관리하는 것이 훨씬 간결해질 것이다.

- - -

{% include tutorial-toc-base.html %}

- - -

#### Reference
이한영 강사님 강의자료  
Djangogirls: [https://tutorial.djangogirls.org/ko/](https://tutorial.djangogirls.org/ko/)  
Django 공식문서: [https://docs.djangoproject.com/en/1.11/ref/templates/language/#id1](https://docs.djangoproject.com/en/1.11/ref/templates/language/#id1)
---
layout: post
title: '[SoundHub] AJAX 요청에 CSRF 토큰 담아서 보내기'
excerpt: Django 템플릿에서 AJAX로 POST 요청을 보낼 때 어떻게 CSRF 토큰을 담아서 보내는지 알아보자.
category: Front-end
project: true
tags:
  - Django
  - AJAX
  - CSRF
  - SoundHub
  - Project
---

Django에서는 `사이트간 요청 위조(CSRF)` 를 방지하기 위해 POST 요청에 `CSRF Token` 을 담아서 보내도록 하고있다. Form을 통한 POST 요청에서는 간단히 `{{ "{% csrf_token " }}%}` 를 폼안에 포함시키면 되었다.  
그렇다면 AJAX를 통해 POST 요청을 보내는 경우에는 어떻게 해야하는지 알아보자.

- - -

## CSRF Token 생성

먼저 HTML에 `{{ "{% csrf_token " }}%}` 를 포함시켜 CSRF 토큰을 담은 input 태그를 생성시켜준다.

```html
<body>
...
{{ "{% csrf_token " }}%}
...
</body>
```

그러면 페이지가 렌더링 될 때 아래와 같은 `hidden` 타입의 input 태그가 생성된다.

```html
<body>
...
<input type="hidden" name="csrfmiddlewaretoken" value="YrBQxfk6cyAlKqAigDhXJkHaMiwaqvnDktDq2lqP4b1vUcKjdo8tXoKrjBlnt5NG">
...
</body>
```

이 input 태그는 `value` 속성에 CSRF 토큰 값을 포함하고 있다.  
POST 요청을 보낼 때 리퀘스트 헤더에 이 값을 포함시켜 보내면 요청이 정상적으로 처리된다.

- - -

## AJAX로 요청 보내기

AJAX로 POST 요청을 보낼 때는 `XMLHttpRequest()` 객체의 header에 input 태그의 value 값을 `X-CSRFToken` 라는 키에 집어넣어주면 된다.

```javascript
// XMLHttpRequest 객체 생성
var xhttp = new XMLHttpRequest(); 

// name 값이 csrfmiddlewaretoken인 객체의 value 값을 가져와 csrf_token 이라는 변수에 할당
var csrf_token = $('[name=csrfmiddlewaretoken]').val();

// POST 요청 생성
xhttp.open("POST", "요청 주소", true);

// header에 X-CSRFToken 키의 값으로 csrf_token 변수를 입력
xhttp.setRequestHeader('X-CSRFToken', csrf_token);

// 요청 보냄
xhttp.send()
```

- - -

###### Reference

Django 공식문서 : [https://docs.djangoproject.com/en/2.0/ref/csrf/](https://docs.djangoproject.com/en/2.0/ref/csrf/)
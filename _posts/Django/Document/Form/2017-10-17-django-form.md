---
layout: post
title: '[Form] 폼'
subtitle: Forms in Django
category: Django
tags:
  - Django
  - Form
---

폼은 웹 상에서 사용자들이 서버로 데이터를 전송할 수 있도록 짜여진 양식이다. 사용자가 양식에 맞게 데이터를 작성하면 그것을 폼을 통해 서버에 전송하고 서버에서 데이터를 처리하여 필요한 결과물을 돌려주게 된다.  
폼은 HTML 태그인 `<form>` 에 다양한 폼 요소를 포함시켜 구성하게 된다. HTML 폼에 대한 설명은 [여기](/html&css/2017/10/17/forms.html)를 참조하기 바란다.  

- - -

## Django에서 폼 다루기

`Django` 는 폼을 좀 더 간편하고 자동화된 방법으로 다룰 수 있도록 다양한 기능을 제공한다.  

- 즉시 렌더링할 수 있도록 데이터를 준비 및 재구성
- 데이터를 받을 수 있는 HTML 폼 생성
- 사용자로부터 제공받은 폼 데이터를 처리

- - -

### Django에서 폼 생성하기

`Django` 에서 폼을 다룰 때의 핵심은 `Form Class` 이다. 데이터의 구조, 행동, 표시방식 등을 정의하는데 `Model Class` 를 사용했던 것과 같이, 폼의 구조, 행동, 표시형식 등을 정의하는데 폼 클래스를 사용한다.  

- - -

#### 폼 클래스 생성

모델 클래스들이 `models.Model` 을 상속받는 것처럼, 모든 폼 클래스는 `forms.Form` 을 상속받는다.  
또 모델 클래스의 속성들을 통해 테이블의 필드를 정의하는 것 처럼, 폼 클래스의 속성들을 통해 각각의 폼 필드들을 정의하게 된다.

폼 클래스의 기본 구조는 다음과 같다. 폼은 `forms.py` 에 모아서 정의해준다.

```py
# forms.py

from django import forms

class 폼이름(forms.Form):
    name속성값 = forms.폼필드타입(옵션)
    폼필드2
    폼필드3
    .
    .
    .
```

아래는 유저 로그인 정보를 받는 폼 클래스의 예이다.

```py
# forms.py

class LoginForm(forms.Form):
    username = forms.Charfield(label='Username')
    password = forms.Charfield(label='Password', widget=forms.PasswordInput())
```

위의 폼 클래스는 아래와 같은 HTML 폼 태그를 생성하게 된다.

```html
<label for="id_username">Username</label>
<input type="text" name="username" required id="id_username">
<label for="id_password">Password</label>
<input type="password" name="password" required id="id_password">
```

폼 클래스에서 하나의 폼 필드는 HTML에서 하나의 폼 요소 태그가 된다. 폼 필드 역시 하나의 클래스이며, 폼 요소에 들어갈 데이터를 정의하고 폼이 제출될 때 데이터에 대한 검증을 수행하는 역할을 한다.  
폼 클래스를 통해 폼을 생성하면, <form> 태그와 `submit` 버튼은 생성되지 않으므로 직접 추가해주어야 한다.

- - -

#### 폼 처리를 위한 뷰 생성

폼으로 제출된 데이터는 뷰에서 받아 처리한다. 대부분의 경우 폼을 생성하는데 사용했던 뷰를 그대로 사용하며, 이 때의 뷰는 다음과 같이 구성할 수 있다.

```py
from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import LoginForm

def login(request):
    # http 요청이 POST 방식이면,
    if request.method == 'POST':
        # POST 방식으로 전달된 데이터를 담은 폼 인스턴스를 생성한다.
        form = LoginForm(request.POST)
        # 폼이 유효한지 검사하여 유효하면,
        if form.is_valid():
            # form.cleaned_data 에 저장된 데이터들을 활용해 필요한 처리를 한다.
            data = form.cleaned_data
            .
            .
            .
            return HttpResponseRedirect('You are logged in!')
    # http 요청이 GET 방식 또는 이외의 방식이면,
    else:
        # 비어있는 폼을 생성한다.
        form = LoginForm()
    # 위 작업들로부터 폼을 받아와 딕셔너리 형태의 자료에 저장한다.
    # POST 요청을 받았고 유효성 검증을 통과하지 못한 경우, form = LoginForm(request.POST)
    # GET 요청을 받았다면, form = LoginForm()이 되어 비어있는 폼이 생성된다.
    context = {
        'form': form
    }
    # 폼을 담은 딕셔너리 자료를 login.html에 전달하면서 페이지를 렌더링한다.
    return render(request, 'login.html', context)
```

사용자가 `login.html` 에 처음 접속하게 되면, `GET` 요청을 보내게 되고, `form = LoginForm()` 이 실행되어 비어있는 폼이 페이지에 생성되게 된다.  
이 후 사용자가 폼에 데이터를 입력한 다음 제출하게 되면, `login.html` 으로 `POST` 요청을 보내게 된다. 이 때, 사용자가 폼에 입력한 데이터는 `request.POST` 라는 딕셔너리 자료로 페이지에 넘겨지게 된다.  

`form = LoginForm(request.POST)` 이 실행되면, `request.POST` 를 `LoginForm` 클래스에 전달하여 사용자가 입력한 데이터를 담은 폼 인스턴스를 생성하고, `form.is_valid()` 를 통해 데이터가 유효한지를 검사한다.  

`is_valid()` 는 폼 클래스의 메서드이며, 각 폼 필드에 전달된 데이터가 폼 필드에 정해진 데이터 양식에 맞는지를 검사한 다음, 그 결과를 `boolean` 값으로 리턴한다.  
예를 들어, `required` 속성이 있는 필드의 값이 비어 있는 경우, 또는, `email` 타입의 필드에 이메일 형식이 아닌 데이터가 입력된 경우 등등의 경우 `False` 값을 리턴한다. 

모든 데이터가 유효하다면 `True` 값을 리턴하고 데이터들을 `cleaned_data` 라는 속성에 딕셔너리 형태로 저장한다. 이 `cleaned_data` 에서 필요한 정보를 추출하여 필요한 가공을 해주는 것이다.  

만약 `form.is_valied()` 가 `False` 인 경우, `form = LoginForm(request.POST)` 인 채로 `login.html` 에 `GET` 요청을 보내게 된다. 이 때는 비어있는 폼이 보여지는 대신, 사용자가 이전에 입력했던 데이터들이 입력되어 있는 채로 폼을 보여주게 된다. 따라서, 사용자는 데이터를 처음부터 다시 작성할 필요 없이, 유효성 검사를 통과하지 못한 데이터에 대해 수정을 하여 다시 제출할 수 있게 된다.

- - -

#### 폼을 보여줄 템플릿 생성

뷰에서 `login.html` 에 `GET` 요청을 보낼 때, `context` 변수에 폼을 담아 템플릿으로 전달하도록 하였다. 이를 호출하여 템플릿에 적용하기 위해서는 다음과 같이 할 수 있다.  

```html
<!-- login.html -->

<form action="" method="post">
    {{ "{% csrf_token " }}%}
    {{ "{{ form " }}}}
    <input type="submit" value="submit">
</form>
```

`context` 변수의 `form` 키에 폼 인스턴스가 저장되어 있으므로, 키를 호출하여 폼 인스턴스를 템플릿에 적용시킨다.  
이 때, 폼 인스턴스의 폼 필드들이 아래와 같이 하나씩 자동으로 HTML 태그로 생성되게 된다.

```html
<!-- login.html -->

<form action="" method="post">
    {{ "{% csrf_token " }}%}
    <label for="id_username">Username</label>
    <input type="text" name="username" required id="id_username">
    <label for="id_password">Password</label>
    <input type="password" name="password" required id="id_password">
    <input type="submit" value="submit">
</form>
```

- - -

<form action="" method="post">
    <label for="id_username">Username</label>  
    <input type="text" name="username" required id="id_username">  
    <label for="id_password">Password</label>  
    <input type="password" name="password" required id="id_password">  
    <input type="submit" value="submit">
</form>

- - -

이 후 사용자가 폼에 데이터를 입력하여 제출하게 되면, 데이터와 함께 `POST` 요청을 페이지에 보내게 되고, 유효성 검사를 통과하면 데이터를 가공하여 다른 작업을 실행하게 된다.

- - -

### Bound 폼, Unbound 폼

폼 인스턴스는 항상 어떤 데이터에 대해 `Bound` 또는 `Unbound` 된 상태를 가진다.  

- 데이터에 Bound 된 폼은 해당 데이터를 검증할 수 있으며, HTML 폼을 렌더링할 때, 데이터를 포함한 HTML을 생성할 수 있다.

- Unbound 된 폼은 검증할 데이터가 없기 때문에 데이터를 검증할 수 없으며, HTML 폼을 렌더링할 때는 비어있는 폼을 생성하게 된다.

- - -

#### is_bound

폼 인스턴스의 `is_bound` 속성에 접근하면 폼의 바운드 상태를 확인할 수 있다.

```py
form = LoginForm()
form.is_bound
```
```re
False
```

- - -

###### Reference

Django 공식문서: [https://docs.djangoproject.com/en/1.11/topics/forms/](https://docs.djangoproject.com/en/1.11/topics/forms/)
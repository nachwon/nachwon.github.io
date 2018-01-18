---
layout: post
title: 'Facebook 로그인 구현하기'
subtitle: How To Set Up Facebook Login
category: Django
comments: true
tags:
  - Django
  - OAuth
  - Facebook
---

페이스북을 통한 로그인 기능을 붙여주는 방법에 대해 알아본다.  
페이스북 로그인과 같은 다른 서비스를 통한 사용자 인증은 페이스북과 같은 믿을 수 있는 사이트에 등록된 사용자임을 증명할 수 있으면 그 정보를 그대로 사용하여 우리의 웹 서비스에 등록해서 이용할 수 있도록 해주는 사용자 인증 간소화 기능이다.  

아래는 페이스북 로그인이 이루어지는 전체 흐름을 나타낸 그림이다.  

<img width="600px" src="/img/facebook_login/flow.png" style="box-shadow:none;">

- - -

## 페이스북 앱 생성

페이스북은 [개발자 전용 페이지](https://developers.facebook.com/) 에서 각종 페이스북 관련 API를 제공한다.  

개발자 전용 페이지로 들어가서 `앱 만들기` 버튼을 클릭하여 앱을 하나 생성해준다.


<img width="950px" src="/img/facebook_login/facebook_dev.png">

- - -

생성된 앱의 메인 화면에서 `Facebook 로그인` 의 `설정` 을 눌러 기능을 시작한다.

<img width="950px" src="/img/facebook_login/app_main.png">

- - -

일단 그대로 두고 `대시 보드` 로 이동하여 `앱 ID` 를 확인한다.

<img width="950px" src="/img/facebook_login/dashboard.png">

- - -

## 페이스북으로 로그인 요청 보내기

<img width="600px" src="/img/facebook_login/fb0.png" style="box-shadow:none;">

사용자가 웹에서 `페이스북 로그인` 버튼을 누르면 페이스북으로 이동하여 사용자에게 페이스북 로그인을 요청한다.  
사용자가 페이스북에 로그인하고 나면 우리가 만든 앱에 등록하도록 한다.  

사용자를 페이스북 로그인 화면으로 이동시키기 위해서는 페이스북 로그인 버튼을 눌렀을 때 아래와 같은 주소로 요청을 보내야한다.

```
https://www.facebook.com/v2.11/dialog/oauth?client_id={ app_id }&redirect_uri={ redirect_url }
```

`{ app_id }` 부분에는 앱 대시보드에서 확인할 수 있었던 `앱 ID` 를 넣어주고, `{ redirect_url }` 에는 사용자 인증이 끝나고 난 뒤 이동할 주소를 넣어준다.  


- - -

#### 장고 프로젝트 세팅

우선 이 과정을 수행할 수 있도록 간단한 장고 프로젝트를 하나 만들어준다.  
`fb_login` 이라는 프로젝트를 하나 만들고, `login` 이라는 앱을 추가해주었다.  

```
django_fblogin
├── README.md
├── fb_login
│   ├── config
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── db.sqlite3
│   ├── login
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   └── views.py
│   ├── manage.py
└── requirements.txt
```

이제 `template` 폴더를 하나 만들고 그 아래에 `login.html` 파일을 생성한 후, 간단한 `a` 태그를 하나 추가해 준다.

```html
<a href="https://www.facebook.com/v2.11/dialog/oauth?
client_id={{ "{{ app_id " }}}}&
redirect_uri=http://localhost:8000{{ "{% url 'login' " }}%}">페이스북 로그인!</a>
```

`redirect_uri` 는 절대경로를 입력해주어야 한다.  
지금은 로컬에서 간단히 테스트만 하는 것이니 `http://localhost:8000` 을 입력해준다.

- - -

#### 뷰 생성

이 템플릿을 렌더링 해줄 뷰와 인증이 끝나고 난 뒤 리다이렉트 될 뷰도 만들어 준다.

```py
# views.py

def index(request):
    app_id = 1552973814793221
    context = {
        "app_id": app_id,
    }
    return render(request, 'login.html', context)

def login(request):
    return HttpResponse('hello')
```

`index` 뷰는 `app_id` 변수에 `앱 ID` 를 할당한 다음 `login.html` 템플릿으로 전달하여 렌더링 해준다.  
`login` 뷰는 인증을 마친 후 돌아온 응답을 처리할 뷰이다.


- - -

#### url 생성

다음으로 `urls.py` 에 뷰를 호출할 주소를 입력해준다.  

```py
# urls.py

from django.conf.urls import url
from django.contrib import admin

from login.views import index, login

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name='index'),
    # 인증 후 리다이렉트 될 주소. {{ "{% url 'login' " }}%} 에서 호출한다.
    url(r'^fb-login/$', login, name='login')
]
```

- - -

#### 유효한 OAuth 리디렉션 URI 추가하기

이제 `runserver` 를 실행하고 `페이스북 로그인` 버튼을 눌러보자.  

<img width="850px" src="/img/facebook_login/url_error.png">

- - -

`https://www.facebook.com/v2.11/dialog/oauth?client_id=1552973814793221&redirect_uri=http://localhost:8000/fb-login/` 으로 요청을 보냈으나 URL을 읽어들일 수 없다는 에러가 발생한다.  

이 에러는 인증 후 리다이렉트 되는 주소인 `http://localhost:8000/fb-login/` 이 앱에 등록되어 있지 않기 때문에 발생하는 에러이다.  
인증 요청을 보낸 결과로 돌려받는 응답이 탈취되어 우리가 관리하는 특정 주소가 아닌 다른 곳으로 전달되는 경우 보안상의 문제가 발생할 수 있다.  
따라서 페이스북 로그인 앱은 우리가 등록한 특정 주소로만 응답이 리다이렉트될 수 있도록 제한한다.  

페이스북 개발자 페이지에서 아까 추가한 `Facebook 로그인` 기능으로 이동한 다음, `유효한 OAuth 리디렉션 URI` 에 `http://localhost:8000/fb-login/` 를 추가해주고 `변경사항 저장` 버튼을 누른다.

<img width="950px" src="/img/facebook_login/redirect_uri.png">

- - -

이제 다시 `localhost:8000` 페이지에서 `페이스북 로그인` 버튼을 눌러보면 아래와 같이 페이스북에 로그인하도록 유도한다.  

<img width="500px" src="/img/facebook_login/facebook_login.png">

- - -

페이스북에 로그인하고 나면 아래와 같이 아까 만들었던 앱인 `Test App` 에 등록하는 화면이 나타난다.  

<img width="500px" src="/img/facebook_login/app_continue.png">

- - -

`Continue` 버튼을 눌러 앱에 등록하고나면 리다이렉트 주소로 이동하면서 뷰에서 리턴해주도록 한 메세지가 뜨는 것을 확인 할 수 있다. 

<img width="900px" src="/img/facebook_login/redirected.png">

- - -

전체 흐름 중 아래의 부분까지 진행 되었다.

<img width="600px" src="/img/facebook_login/fb1.png" style="box-shadow:none;">



- - -

## 응답을 엑세스 토큰과 교환하기

<img width="600px" src="/img/facebook_login/fb2.png" style="box-shadow:none;">

- - -

지금까지 사용자를 페이스북 인증시키고 앱에 등록시키는 과정을 진행하였다.  
이제 사용자는 페이스북에 등록된 사용자임을 인증 받았고 그 증거를 응답으로 되돌려받았다... 고 생각할 수 있지만 아직 아니다.

리다이렉트된 페이지의 주소를 살펴보자. 무엇인가 잔뜩 달려있는 것을 볼 수 있다.

```
http://localhost:8000/fb-login/?code=AQB9Epx4iPDF2OaThwHTqJ-QpXK8ET9wxTCEq7_6r5mkRLiaGv9PABkC-SGoMVbPmWieqXmF-8Iagoub-rsKeVcOiRfdUSObBoCJnInRT5IFz8Ri-Ih2fGrKi_sLtVWN5zfUc_w-06SzF01TG6Rec0qhJYaLiNqW17RaXpW6_rTN2MIM5YxnlWkD6syoOH2t3Fk_GfcVeYpVHQnT4KGo-frXc1bq9ulbfFaeAiLAdBDuq9Z0LF1Wfkmt5uVJDxF2WfmBcs7kNutWQqAcgIWOfN7i4Xirh6geGMp9fQM1KFxHdOlqisXwwzA0KqffTHmGzDA#_=_
```

주소에 `code` 라는 변수가 포함되어 되돌아왔다.  
이제 이 code를 가지고 사용자가 신뢰할 수 있는 사용자임을 증명하는 `엑세스 토큰` 을 발급 받아야 한다.  
처음 사용자가 버튼을 눌렀을 때는 `app_id` 라는 공개된 정보를 통해 앱에 접근하였다.  
그 다음 사용자가 페이스북에 로그인하고 앱에 등록한 다음 리다이렉트된 페이지에서는 위와 같이 `code` 라는 변수가 주소에 공개된 채로 나타난다.  
code는 서버를 거치지 않고 바로 클라이언트에게로 보내지기 때문에 공개되어있다.  
따라서 만약 `code` 만으로 사용자를 온전히 신뢰하게 한다면 이 정보를 탈취당했을 경우, 공격자가 사용자의 권한을 마음대로 사용할 수 있게 된다.  
즉, 아직까지 보안이 된 믿을만 한 수단으로 사용자 인증이 이루어지지 않았다.  
이 때 사용하게 되는 것이 `앱 시크릿 코드` 이다.  

앱 시크릿 코드는 페이스북 개발자 페이지의 대시보드에서 `보기` 버튼을 눌러 확인할 수 있다.

<img width="900px" src="/img/facebook_login/app_secret_code.png">

- - -

비밀번호를 입력하고 나면 아래와 같이 앱 시크릿 코드를 확인할 수 있다.

<img width="900px" src="/img/facebook_login/secret_revealed.png">

- - -

사용자를 온전히 인증시켜주는 엑세스 토큰을 발급받으려면 아래와 같은 주소로 요청을 보내야한다.  

```
https://graph.facebook.com/v2.11/oauth/access_token?
client_id={app-id}
&redirect_uri={redirect-uri}
&client_secret={app-secret}
&code={code-parameter}
``` 

`client_id`: 앱 ID를 입력한다.
`redirect_uri`: 처음 입력했던 리다이렉트 주소와 동일한 주소를 입력한다. 앱에 등록되어 있는 동일한 주소로 응답이 전달되는지를 검사한다.  
`client_secret`: 앱 시크릿 코드를 입력한다.
`code`: 처음 인증으로 전달받은 code 변수를 입력한다.

이 요청은 뷰에서 처리하도록 하여 서버 쪽에서 전송하도록 해준다.

```py
# views.py

import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse

# app_id와 특히 app_secret은 외부에 공개되지 않도록 따로 관리해주는 것이 좋다.
# 지금은 연습이니까 그냥 진행한다.
app_id = 1552973814793221
app_secret = 'bb9f21234cde9c81be4df7c13f6f82b9'


def index(request):
    context = {
        "app_id": app_id,
    }
    return render(request, 'login.html', context)


def login(request):
    # 인증 후 GET 요청으로 리다이렉트 되어서 온 주소에 포함된 'code' 를 가져온다.
    code = request.GET['code']
    # 처음 입력한 리다이렉트 주소와 동일한 주소를 입력한다.
    # 아래는 동적으로 동일한 주소를 다시 구성하도록 한 것이다.
    # request.scheme: 현재 페이지에 전달된 요청의 유형 정보이다. 지금의 경우 'http'
    # request.META['HTTP_HOST']: 호스트 URI 주소 정보이다. 지금의 경우 'localhost:8000'
    # revers('login'): login 이라는 URL 명에 연결되어 있는 실제 URL을 가져온다. 지금의 경우 '/fb-login/'
    redirect_uri = f"{request.scheme}://{request.META['HTTP_HOST']}{reverse('login')}"

    # access_token을 받기위해 요청을 보내야하는 URL
    url_access_token = "https://graph.facebook.com/v2.11/oauth/access_token"

    # access_token을 받기위해 보내야하는 매개변수들
    params_access_token = {
        "client_id": app_id,
        "redirect_uri": redirect_uri,
        "client_secret": app_secret,
        "code": code,
    }

    # requests 패키지를 사용해서 URL에 매개변수들을 추가하여 GET 요청을 보낸다.
    # pip install requests 로 설치
    response = requests.get(url_access_token, params=params_access_token)

    # 돌려받은 응답을 JSON 형식으로 변환한다.
    result = response.json()

    # JSON 형식을 화면에 띄워준다.
    return HttpResponse(result.items())
```

하는 김에 템플릿에서 페이스북 로그인 버튼으로 보내는 첫 요청의 리다이렉션 주소도 동적으로 생성할 수 있도록 해주자.

```html
# login.html
...
redirect_uri={{ "{{ request.scheme " }}}}://{{ "{{ request.META.HTTP_HOST " }}}}{{ "{% url 'login' " }}%}
...
```

위의 요청은 뷰에서 처리해주기 때문에 외부로 노출되지 않기 때문에 사용자를 온전히 인증해줄 수 있는 정보를 포함하여 요청을 보낼 수 있다. 그 결과로 사용자를 인증해주는 `access_token` 을 되돌려 받는다.  

<img width="950px" src="/img/facebook_login/access_token.png">

돌려받은 응답은 `access_token`, `token_type`, `expires_in` 으로 구성되어 있다.

지금까지의 과정을 요약하면 아래와 같다.

```
페이스북 로그인 버튼 클릭 > 사용자 인증 > 앱 등록 > 'code' 를 돌려받음 > 'code' 및 다른 정보들로 access_token 요청 > 응답으로 access_token 을 받음
```


<img width="600px" src="/img/facebook_login/fb3.png" style="box-shadow:none;">


- - -

## 엑세스 토큰 검사하기

access_token 은 유효기간이 있어서 유효기간이 지난 토큰은 사용할 수 없게 된다.  
따라서 토큰이 유효한지 검사하는 과정이 필요하다.  
토큰을 오랜기간 유지하고 싶다면 60일 동안 지속되는 `장기 토큰` 을 발급 받아서 사용하면 된다.    

토큰의 검사는 아래와 같은 형식의 URI로 요청을 보내면 된다.  

```
graph.facebook.com/debug_token?
     input_token={token-to-inspect}
     &access_token={app-token-or-admin-token}
```

`token-to-inspect` 에는 검사할 access_token을 넣어준다.  
`app-token-or-admin-token` 에는 `앱 엑세스 토큰` 이라는 것을 넣어준다.

`앱 엑세스 토큰` 은 `{app_id}|{app_secret}` 이다.  

위 주소로 GET 요청을 보내도록 views.py를 수정한다.

```py
# views.py

...
def login(request):
    code = request.GET['code']
    redirect_uri = f"{request.scheme}://{request.META['HTTP_HOST']}{reverse('login')}"
    url_access_token = "https://graph.facebook.com/v2.11/oauth/access_token"

    params_access_token = {
        "client_id": app_id,
        "redirect_uri": redirect_uri,
        "client_secret": app_secret,
        "code": code,
    }

    response = requests.get(url_access_token, params=params_access_token)
    url_debug_token = 'https://graph.facebook.com/debug_token'
    params_debug_token = {
        "input_token": response.json()['access_token'],
        "access_token": f'{app_id}|{app_secret}'
    }

    user_info = requests.get(url_debug_token, params=params_debug_token)

    return HttpResponse(user_info.json().items())
```
위 요청의 결과로 아래와 같은 데이터가 되돌아온다.  
엑세스 토큰이 유효하면 `is_valid` 항목이 `True` 인 것을 볼 수 있다.

```
(
    'data', 
    {
        'app_id': '1552973814793221', 
        'type': 'USER', 
        'application': 'Test App', 
        'expires_at': 1515897901, 
        'is_valid': True, 
        'issued_at': 1510713901, 
        'scopes': ['public_profile'], 
        'user_id': '10214169173528135'
    }
)
```

- - -

## 유저정보 가져오기

유효한 엑세스 토큰이 있다면 페이스북에 등록된 유저 정보를 가져와 우리 서비스 회원가입에 이용할 수 있다.  

유저 정보는 아래의 주소로 요청을 보내서 가져올 수 있다.  

```
https://graph.facebook.com/me?
    fields={user-info-fields}&
    access_token={access-token}
```

`user_info_fields` 에는 `id`, `first_name` 등 가져올 유저 정보를 나열해준다.  
`access_token` 에는 엑세스 토큰을 넣어준다.  

어떤 유저정보를 가져올 수 있는지 테스트 해보려면 페이스북의 `그래프 API` 를 사용한다.  

페이스북 개발자 페이지에서 `도구 및 지원` 메뉴로 이동한 다음 `그래프 API 탐색기` 를 클릭한다.

<img width="900px" src="/img/facebook_login/graph_api.png">

- - -

나타나는 화면의 왼쪽 아래에서 필요한 유저 정보 `fields` 를 추가하고 `제출` 버튼을 누르면 그 결과가 출력된다.

<img width="900px" src="/img/facebook_login/graph_api_main.png">

- - -

추가하고 싶은 유저 정보 필드들을 테스트 해본 다음 필요한 필드들의 이름을 그대로 가져와서 `{user-info-fields}` 자리에 넣어주면 된다.  

`views.py` 에 작성해주자.

```py
# views.py

...
    url_user_info = 'https://graph.facebook.com/me'
    user_info_fields = [
        'id',  # 아이디
        'first_name',  # 이름
        'last_name',  # 성
        'picture',  # 프로필 사진
        'email',  # 이메일
    ]
    params_user_info = {
        "fields": ','.join(user_info_fields),
        "access_token": access_token
    }
    user_info = requests.get(url_user_info, params=params_user_info)

    return HttpResponse(user_info.json().items())
```

이제 다시 `페이스북 로그인` 버튼을 클릭해보면 아래와 같은 데이터를 돌려받는다.

```
('id', '10214169173528135')
('first_name', 'Chaewon')
('last_name', 'Na')
('picture', {
    'data': {
        'height': 50, 
        'is_silhouette': False, 
        'url': 'https://scontent.xx.fbcdn.net/v/t1.0-1/...', 
        'width': 50
        }
    }
)
```

그런데 분명 이메일 정보도 요청을 했는데 돌아오지 않았다.  
이메일은 추가적인 권한 요청이 필요한 정보이기 때문이다.  

어떤 정보를 가져올 수 있는 지에 대한 권한을 확인하려면 페이스북 개발자 페이지의 `앱 검수` 항목을 확인한다.

<img width="900px" src="/img/facebook_login/app_permissions.png">

- - -

추가적인 정보 취득 권한을 얻으려면 앱 검수를 받아서 페이스북 측의 승인을 받아야 한다.  
불순한 용도로 정보를 악용할 우려가 있는지 등을 확인해서 권한을 부여한다.  
하지만 기본적으로 이메일, 친구 목록, 공개 프로필 정보는 검수를 받을 필요 없이 가져올 수 있다.  

URI에 fields 값으로 가져올 수 있는 정보는 기본적으로 `public_profile` 항목에 포함된 정보이다.  

public_profile에는 다음과 같은 정보들이 포함된다.  
```
id
cover
name
first_name
last_name
age_range
link
gender
locale
picture
timezone
updated_time
verified
```

public_profile 이외의 다른 승인된 항목들에 해당하는 유저 정보를 가져오려면 클라이언트 측에서 최초로 페이스북 로그인 요청을 보낼 때 URI에 `scope` 이라는 값에 승인된 항목을 포함 시켜주어야 한다.  
`scope` 를 지정해주지 않으면 기본적으로 `scope=public_profile` 이라고 지정해준 것과 동일하게 되며, 이러한 이유로 `id`, `name`, `picture` 등과 같은 정보를 기본적으로 가져올 수 있었던 것이다.

승인된 나머지 항목들인 `이메일` 과 `친구 목록` 을 가져오기 위해 페이스북 로그인 버튼이 있는 템플릿을 열고 다음과 같이 `scope` 을 추가해준다.  

```html
<a href="https://www.facebook.com/v2.11/dialog/oauth?
client_id={{ "{{ app_id " }}}}&
scope=user_friends,email,public_profile&
redirect_uri={{ "{{ request.scheme " }}}}://{{ "{{ request.META.HTTP_HOST " }}}}{{ "{% url 'login' " }}%}">페이스북 로그인!</a>
```

그 다음 다시 runserver를 실행해서 페이스북 로그인 버튼을 클릭해보자.  

<img width="600px" src="/img/facebook_login/additional_permissions.png">
- - -

앱이 이메일과 친구 목록에 접근하도록 허용할 것인지를 물어보는 창이 새롭게 나타난다.  
public_profile은 이미 승인했으므로 나머지 항목에 대해서 권한을 요청하는 것이다.  
버튼을 눌러 승인하면 아래와 같이 이메일이 포함되어 되돌아오는 것을 볼 수 있다.

```
('id', '10214169173528135')
('first_name', 'Chaewon')
('last_name', 'Na')
('picture', {
    'data': {
        'height': 50, 
        'is_silhouette': False, 
        'url': 'https://scontent.xx.fbcdn.net/v/t1.0-1/c0.0.50.50...', 
        'width': 50
        }
    }
)
('email', 'nachwon@******.com')
```

참고로 친구 목록은 scope에 포함되어 유저에게 권한 요청을 하였지만 가져올 fields에는 포함시키지 않았기 때문에 되돌아온 유저 정보에 포함되지 않았다.  

이제 이 정보들을 가지고 회원가입을 시키는 로직을 구현해주기만 하면 페이스북을 통한 로그인 프로세스가 완성된다.



- - -

###### Reference
이한영 강사님 강의자료  
페이스북 로그인 공식 문서: [https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow](https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow)

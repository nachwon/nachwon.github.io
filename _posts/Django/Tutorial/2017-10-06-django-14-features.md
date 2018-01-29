---
layout: post
title: '[Django Tutorial] Blog 만들기 - 14. 기능 추가하기'
category: Django
tags:
  - Django
  - Tutorial
---



이번에는 블로그에 여러 가지 기능을 추가해보자. 아래에 있는 기능들을 추가해 볼 것이다.  
<div id='menu'></div>
- <a href="#post-publish">`Post` 게시하기</a>
- <a href="#post-hide">`Post` 숨기기</a>
- <a href="#post-add">`Post` 추가하기</a>
- <a href="#post-delete">`Post` 삭제하기</a>

- - -

## <span id="post-publish">`Post` 게시하기</span>

앞선 포스트에서 `published_date` 가 없는 `Post` 는 블로그 메인 화면에 나타나지 않도록 해주었었다. 이제 보이지 않는 `Post` 에 `published_date` 를 부여해서 메인 화면에 나타나도록 해보자.  
`models.py` 의 `Post` 모델에 아래와 같이 `publish` 메서드를 추가해보자.

```py
from django.utils import timezone  # timezone 모듈을 불러온다.

def publish(self):
    self.published_date = timezone.now()  # published_date 에 현재시간을 할당
    self.save()  # 변경된 데이터베이스를 저장
```

`Post` 객체에 `publish` 메소드를 호출하면 현재시간이 `published_date` 필드에 입력되도록 해주었다.  
`save()` 는 변경된 데이터베이스를 저장하는 명령이다.  

`shell_plus` 에서 `published_date` 가 없는 `Post` 들을 모두 불러와서 메인화면에서 보이도록 해보자. 먼저 `published_date` 가 `null` 인 `Post` 들을 쿼리셋으로 가져오자.

```py
posts = Post.objects.filter(published_date__isnull=True)
posts
```
```re
<QuerySet [<Post: [Django Tutorial] Blog 만들기 - 4. 모델>, <Post: [Django Tutorial] Blog 만들기- 5. 데이터베이스>]>
```

그 다음 쿼리셋의 `Post` 들을 하나씩 순회하면서 `publish` 메서드를 호출해주자.

```py
for post in posts:
    post.publish()
```

<img width="950px" src="/img/django_tutorial/publish.png">

메인 화면에서 보이지 않던 4번, 5번 글들까지 모두 나타난 것을 볼 수 있다.

<a href="#menu">위로</a>
- - -

## <span id="post-hide">`Post` 숨기기</span>

이번에는 `Post` 객체의 `published_date` 필드 값을 `null` 로 바꿔서 메인 화면에서 `Post` 를 숨겨주는 기능을 만들어보자.  
이번에도 역시 `models.py` 에 `hide` 라는 메서드로 추가해준다.

```py
def hide(self):
    self.published_date = None
    self.save()
```

작동방식은 `publish` 메서드와 비슷하다. `published_date` 를 `None` 으로 만들어준 뒤, `save()` 로 데이터베이스를 저장해준다.  
`hide` 메서드로 5번 글을 숨겨보자.  
```py
post = Post.objects.get(id=5)
post.hide()
```

<img width="950px" src="/img/django_tutorial/hide.png">

`runserver` 에서 메인 화면을 확인해보면 5번 글이 숨겨진 것을 확인할 수 있다.

<a href="#menu">위로</a>
- - -

## <span id="post-add">Post 추가하기</span>

좀 더 복잡한 기능을 추가해보자. 현재 블로그에 새 글을 추가하기 위해서는 관리자 페이지를 사용하거나 `ORM` 을 활용하는 방법이 있다. 하지만 이 방법들은 사용자가 활용하기에 적절한 방법이 아니다. 새로운 글을 추가하는 페이지를 따로 만들어 글을 등록하는 `User-friendly` 한 기능을 추가해보자.  

- - -

### 템플릿 생성

먼저 새로운 템플릿 만들어보자. `template` 폴더에 `post_add.html` 파일을 만들고 아래와 같이 입력한다.

```html
{{ "{% extends 'base.html' " }}%}

{{ "{% block content " }}%}
<form action="" method="post">
    <h2 class="post-add">새 글 작성</h2>
    <div class="container">
        <div class="form-group">
            <label for="input-title">제목: </label>
            <input name="title" id="input-title" type="text" class="form-control" placeholder="글 제목">
        </div>
        <div class="form-group">
            <label for="input-content">내용: </label>
            <textarea name="content" id="input-content" class="form-control" rows="5" placeholder="글 내용"></textarea>
        </div>
        <button type="submit" class="btn btn-primary btn-lg">글 등록</button>
    </div>
</form>
{{ "{% endblock " }}%}
```

`form` 태그를 사용해서 글 제목과 글 내용을 입력받아 데이터베이스에 전달하도록 구성하였다. `CSS` 를 조금 첨가해서 아래와 같이 만들어주었다.

<img width="950px" src="/img/django_tutorial/post_add.png">

- - -

### 뷰와 URL 생성

다음으로 `views.py` 에 `post_add` 함수를 추가해주고, `url.py` 에서 `post/add/` 라는 `URL` 주소를 할당해주었다.  

```py
# views.py

def post_add(request):
    return render(request, 'blog/post_add.html')
```

```py
# urls.py

from blog.views import post_list, post_detail, post_add

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', post_list),
    url(r'^post/(?P<pk>\d+)/', post_detail),
    url(r'^post/add/', post_add),
]
```

`runserver` 를 실행해서 `post/add/` 로 접속해보자. 

<img width="500px" src="/img/django_tutorial/post_add_url.png">

이제 `post_add` 템플릿을 통해 데이터를 전달해보자. 제목과 내용에 아무 내용이나 입력한 뒤 `글 등록` 버튼을 눌러보자. 

<img width="950px" src="/img/django_tutorial/csrf_forbidden.png">

이게 무슨 에러인지 알아보도록하자.  

- - -

### CSRF 토큰

> #### 사이트 간 요청 위조 (Cross-Site Request Forgery, CSRF)
>
> 사이트 간 요청 위조는 웹사이트 취약점 공격의 하나로, 사용자가 자신의 의지와는 무관하게 공격자가 의도한 행위(수정, 삭제, 등록 등)를 특정 웹사이트에 요청하게 하는 공격을 말한다.  
> 출처 : [위키피디아](https://ko.wikipedia.org/wiki/%EC%82%AC%EC%9D%B4%ED%8A%B8_%EA%B0%84_%EC%9A%94%EC%B2%AD_%EC%9C%84%EC%A1%B0)

`CSRF` 공격에 대한 자세한 내용은 [여기](http://www.egocube.pe.kr/Translation/Content/asp-net-web-api/201402030001)를 참고하면 될 것 같다.  
간단히 요약하면 아래와 같다.

- 사용자가 웹사이트에 인증 폼을 보내어 로그인을 한다.
- 웹사이트는 인증 쿠키를 포함한 응답을 돌려주어 사용자를 인증한다. 
- 사용자가 인증이 된 채로 어쩌다가 공격자가 심어 놓은 사이트를 방문한다.
- 그 사이트에 아래와 같은 폼이 있다고 가정해보자. 폼에는 `hidden` 타입의 `input` 들이 숨겨져 있다.

```html
<h1>You Are a Winner!</h1>
<form action="http://example.com/api/account" method="post">
    <input type="hidden" name="Transaction" value="withdraw" />
    <input type="hidden" name="Amount" value="1000000" />
    <input type="submit" value="Click Me"/>
</form>
```

- 사용자가 `submit` 버튼을 눌러 폼을 전송하면 브라우저가 인증 쿠키를 포함하여 전송한다.
- 요청에는 사용자 인증 쿠키까지 포함되어있으므로 인증된 사용자가 수행할 수 있는 모든 작업을 수행할 수 있다. 만약 `hidden` 타입 `input` 에 그런 작업이 있다면 그대로 실행되는 것이다.

`CSRF` 공격을 방지하기 위해서 위조 방지 토큰을 사용한다. 위조 방지 토큰이 작동하는 방식은 다음과 같다.  

- 사용자가 폼이 있는 웹사이트에 접속한다.
- 웹사이트는 두 개의 토큰을 응답으로 보낸다. 하나는 쿠키를 통한 인증 토큰이고, 다른 하나는 폼 안에 숨겨진 채로 전송된다. 숨겨진 토큰은 무작위로 생성된 값을 가진다.
- 사용자가 폼을 제출할 때 위의 두 가지 토큰 모두가 다시 서버로 돌아와야 한다. 쿠키 토큰은 쿠키를 통해 전송되고, 폼 토큰은 폼 데이터로 전송된다.
- 하나의 토큰이라도 되돌아오지 않으면 웹사이트가 요청을 거부한다.

`Django` 는 폼으로 데이터를 받을 때 위조 방지 토큰을 함께 받도록 되어있으며, `글 등록` 버튼을 눌렀을 때 위조 방지 토큰이 서버로 재전송되지 않았기 때문에 위의 에러메세지가 뜬 것이다.  
이를 해결하기 위해서 폼안에 위조방지 토큰을 포함시켜주어야 한다. 위조방지 토큰은 아래와 같이 태그로 입력한다.

```html
{{ "{% csrf_token " }}%}
```

이 태그를 폼 안에 넣어주면 된다.

```html
{{ "{% extends 'base.html' " }}%}

{{ "{% block content " }}%}
<form action="" method="post">
    {{ "{% csrf_token " }}%}  # 위조방지토큰
    <h2 class="post-add">새 글 작성</h2>
    <div class="container">
        <div class="form-group">
            <label for="input-title">제목: </label>
            <input name="title" id="input-title" type="text" class="form-control" placeholder="글 제목">
        </div>
        <div class="form-group">
            <label for="input-content">내용: </label>
            <textarea name="content" id="input-content" class="form-control" rows="5" placeholder="글 내용"></textarea>
        </div>
        <button type="submit" class="btn btn-primary btn-lg">글 등록</button>
    </div>
</form>
{{ "{% endblock " }}%}
```

이제 다시 `runserver` 로 가서 제목과 내용에 아무거나 입력한 뒤 `글 등록` 버튼을 눌러보면, `CSRF` 에러가 뜨지않는 것을 확인할 수 있다. `ctrl + U` 를 눌러서 페이지 소스를 열어보면, 폼 부분에 위조방지토큰이 `hidden` 타입 `input` 으로 포함되어 있는 것을 볼 수 있다.

```html
<form action="" method="post">
    # 위조방지 토큰
    <input type='hidden' name='csrfmiddlewaretoken' value='4JqOsmu4o09wq4OGyqFJmYLHWpNLBnO6deJmMgGsEDAyygXKP61SieFw45sukNCJ' />
    <h2 class="post-add">새 글 작성</h2>
    <div class="container">
        <div class="form-group">
            <label for="input-title">제목: </label>
            <input name="title" id="input-title" type="text" class="form-control" placeholder="글 제목">
        </div>
        <div class="form-group">
            <label for="input-content">내용: </label>
            <textarea name="content" id="input-content" class="form-control" rows="5" placeholder="글 내용"></textarea>
        </div>
        <button type="submit" class="btn btn-primary btn-lg">글 등록</button>
    </div>
</form>
```

`글 등록` 버튼을 누를 때 위의 토큰 값도 같이 보내지며, 이 값은 폼이 요청될 때마다 랜덤으로 생성되는 값이므로 공격자가 알아낼 수 없다.  

- - -

### 폼 데이터 전송하기

이제 글 등록 페이지의 겉모습은 얼추 구현이 다 되었다. 하지만 아직까지 `글 등록` 버튼을 누르면 아무 일도 일어나지 않는다. 글 등록 버튼을 눌러 새 글이 등록되게 해주려면 글 등록 페이지에서 `제목` 과 `내용` 에 입력한 데이터를 서버에 전송해서 데이터베이스에 저장하도록 구현해주어야 한다. 이 때 활용할 부분이 `form` 태그의 `method` 속성이다.  
- - -
#### form 태그 method 속성

`form` 태그의 `method` 속성은 `GET` 과 `POST` 를 값으로 가질 수 있다. `form` 태그의 `method` 안에 값을 입력하면 각각 폼으로 받은 데이터를 `GET` 방식과 `POST` 방식으로 서버에 전달하게 된다. 기본값은 `GET` 방식이다.

폼 태그의 `method` 속성 값에 따른 차이점은 아래와 같다.

- - -

#### GET

`GET` 은 폼에서 받은 데이터를 `URL` 주소에 질의문자 형태로 이어붙여서 데이터를 전달한다.
예를 들어 폼의 `method` 가 `GET` 인 경우, 글 등록 페이지에서 제목에 'Helloworld', 내용에 'Byeworld' 라고 입력한 다음 `글 등록` 버튼을 눌러보면 아래와 같은 `URL` 로 접속이 된다. 

```re
http://localhost:8000/post/add/?csrfmiddlewaretoken=YsdYAglbqtgrRwAg0wsSm8hB2ALlpgz87XwwUaxzG6HtZIJkhcO1iobqagq48GnL&title=Helloworld&content=Byeworld
```

주소를 뜯어보면

```re
http://localhost:8000/post/add/
```

이 부분은 글 등록 페이지의 `URL` 주소이다.  
그 다음 따라오는 `?` 는 이 뒷부분이 `질의문자 (Query string)` 라는 것을 뜻한다. 질의문자에 대한 설명은 [여기](https://en.wikipedia.org/wiki/Query_string#Structure)를 참조하도록 하고 넘어가겠다. `Django` 의 `url` 객체가 가지는 정규표현식은 질의문자 부분과 매칭되지 않는다.

```re
csrfmiddlewaretoken=YsdYAglbqtgrRwAg0wsSm8hB2ALlpgz87XwwUaxzG6HtZIJkhcO1iobqagq48GnL
```

이 부분은 좀 전에 폼에 포함시켰던 위조방지 토큰이다. 이 값도 폼을 통해 전송되므로 `URL` 에 포함되어진 것이다.  
그 다음 따라오는 `&` 는 질의문자에서 필드를 구분해주는 역할을 한다.

```re
title=Helloworld&content=Byeworld
```

이 부분이 우리가 폼에 입력했던 제목과 내용이다. `input` 태그의 `name` 속성이  `key` 로, `input` 속성에 입력한 데이터가 `value` 로 `URL` 에 표시되어 있다. 이렇게 `GET` 방식은 데이터를 `URL` 주소에 질의 문자 형태로 포함하여 전달한다. 그렇기 때문에 공개하면 안되는 데이터를 전송할 때는 `GET` 을 사용하지 않는다.

- - -
#### POST

`POST` 방식은 폼에서 받은 데이터를 내부적으로 서버에 전달한다. 폼 태그의 `method` 속성을 `POST` 로 바꾸고 똑같은 제목과 내용으로 `글 등록` 버튼을 눌러보자.  

`URL` 주소도 그대로이고 겉으로는 아무 일도 일어나지 않은 것 같지만 내부적으로는 데이터가 서버로 전달되었다. 이를 브라우저에서 확인해볼 수 있다.  
먼저 크롬에서 `post/add/` 로 접속한다.  
그 다음, `F12` 를 눌러 개발자 도구를 열어 `Network` 탭을 누른다.  
그리고 제목과 내용을 채워준 뒤 `글 등록` 버튼을 눌러 폼 데이터를 전송하자.  
그러면 개발자 도구에서 `add/` 라는 것이 기록이 되는 것을 볼 수 있을 것이다.  
이것이 `request` 이며 이걸 클릭해보면 내부 정보를 볼 수 있다. 내부 정보 중 `Headers` 탭의 가장 아래쪽에 `form data` 라는 항목이 있고 그 안에 우리가 전송한 위조방지 토큰 값, `title`, `content` 가 들어있는 것을 볼 수 있다.

<img width="950px" src="/img/django_tutorial/form_data.png">

- - -

새 글을 등록하기 위해서는 `POST` 방식으로 전달한 이 데이터를 받아와서 데이터베이스에 기록해주어야 한다.  
우선 뷰에서 글 등록 버튼을 눌렀을 때 보내지는 `POST` 요청을 받아올 수 있도록 해보자.  

```py
def post_add(request):
    return render(request, 'blog/post_add.html')
```

지금의 `post_add` 뷰에는 `request` 를 받으면 `post_add.html` 템플릿을 띄워주는 기능만 구현되어 있다. 이것을 아래와 같이 수정하여 `request`를 `GET` 방식과 `POST` 방식으로 구분하여 받아오도록 한다.  
```py
def post_add(request):
    if request.method == 'POST':
        return HttpResponse('POST method')
    elif request.method == 'GET':
        return render(request, 'blog/post_add.html')
```

뷰가 받는 `request` 는 객체처럼 다룰 수 있다. `request.method` 는 어떤 방식의 `request` 인지에 대한 정보를 담고있다.  
사실 `GET` 과 `POST` 는 `HTTP` 메소드이다. `HTTP` 메소드에 대한 자세한 설명은 별도의 포스트에서 다루도록 하겠다. 간단히 설명하자면,  
- `GET` 은 요청 받은 `URL` 에서 리소스를 가져온다. 우리가 `post/add/` 주소로 접속하면 그 주소에 연결되어있는 데이터인 글 등록 페이지를 가져와서 보여주게 되는 것이다.  
- `POST` 는 클라이언트에서 서버로 데이터를 전송한다. `글 등록` 버튼을 누르면 폼 안에 입력된 제목과 내용 등의 데이터를 서버로 전송한다.  

`form` 태그의 `method` 속성은 어떤 `HTTP` 메소드를 활용해서 데이터를 처리하는 지를 결정하는 것이다. 실제로 어떤 방식의 요청이 전달되는 지는 `runserver` 의 로그를 보면 알 수 있다.  
`runserver` 를 실행하고 `post/add/` 에 접속한 다음 콘솔에 뜨는 로그를 확인해보자.  
```re
[07/Oct/2017 18:28:35] "GET /post/add/ HTTP/1.1" 200 1454
```

이 로그는 `/post/add/` 라는 주소에 `GET` 요청이 전달되었다는 뜻이다. `post_add` 뷰가 이 주소에 연결되어 있고 뷰에서 이 요청을 받아 `post_add.html` 을 응답으로 돌려주게 되어 있으므로 우리가 글 등록 페이지를 보게 되는 것이다.
이번에는 아무 내용이나 입력한 다음 `글 등록` 버튼을 눌러보자.  

```re
[07/Oct/2017 18:45:12] "POST /post/add/ HTTP/1.1" 200 11
```

`/post/add/` 로 `POST` 요청이 전달되었다는 로그를 볼 수 있다. 그리고 `POST` 요청을 받으면 뜨도록 해둔 `POST method` 라는 문자열이 출력되는 것도 확인할 수 있다. 

<img width="400px" src="/img/django_tutorial/post_method.png">

이번에는 `post_add.html` 의 폼 `method` 를 `GET` 으로 바꾸고 다시 `글 등록` 버튼을 눌러보자.  

```html
<form action="" method="GET">
```
```re
"GET /post/add/?csrfmiddlewaretoken=J9Ziw4prn5h55yfRTQhynKT5LafJKwBgSEiQQYBPDII7dKoVawDHj0NUTQUstWpT&title=test&content=test HTTP/1.1" 200 1453
```
`/post/add/?csrfmiddlewaretoken=....`이라는 주소로 `GET` 요청이 보내진 것을 로그를 통해 확인할 수 있다. `GET` 요청을 받으면 `post_add.html` 을 띄우게 되어 있으므로 화면에는 변화가 없다.  
정리하자면 `request.method` 를 통해서 `post/add/` 주소로 들어오는 요청이 어떤 방식인지를 알 수 있으며 `if` 문을 통해서 요청 방식에 따라 서로 다른 반응을 돌려주도록 해주었다. 이렇게 구분해주는 것은 `post/add/` 주소에 접속해서 `post_add.html` 템플릿을 보려면 `GET` 방식으로 요청을 보내야하는데, 템플릿에서 폼 데이터를 보내면 `POST` 요청이 같은 `URL` 인 `post/add/` 주소로 전달되기 때문이다.  
이제 `post/add/` 주소로 `POST` 요청을 받았을 때 반응을 따로 구분해주었으니, 이 부분에서 데이터를 가져와서 데이터베이스에 저장하면 될 것 같다.

- - -

### 폼 데이터를 데이터베이스에 저장

`POST` 로 전송되는 데이터는 `POST` 라는 객체로 전달된다. 이 객체는 `QueryDict` 라는 딕셔너리 타입의 데이터이다.  
이 데이터에 접근하려면 아래와 같이 입력한다.

```py
request.POST
```

그럼 이제 뷰에서 `POST` 요청을 받았을 때 전달된 데이터를 데이터베이스에 저장하도록 코드를 작성해보자.  
```py
# views.py

def post_add(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        post = Post.objects.create(
            title=title,
            content=content,
        )
        return HttpResponse('POST method')
    elif request.method == 'GET':
        return render(request, 'blog/post_add.html')
```

하나씩 살펴보자.

```py
title = request.POST['title']
content = request.POST['content']
```

위의 두 코드는 `POST` 요청으로 받아온 `POST` 딕셔너리 데이터의 키를 호출하여 변수에 할당하는 코드이다.  
각각 `title` 키의 값과 `content` 키의 값을 가져와 변수에 할당하였다.

```py
post = Post.objects.create(
            title=title,
            content=content,
        )
```

위의 코드는 `ORM` 을 통해서 `Post` 객체를 생성하고, 생성한 `Post` 객체의 `title`, `content` 필드에 `POST` 데이터로부터 가져온 데이터를 할당한 변수들을 넣어준 것이다. 그리고 생성된 `Post` 객체를 `post` 라는 변수에 할당하여 `Post` 모델의 인스턴스를 만들어 주었다.  
하지만 `Post` 객체는 반드시 작성자를 뜻하는 `author` 필드를 채워주어야 한다. 그리고 이 `author` 필드는 `User` 테이블과 연결된 외래키 필드이므로 `User` 객체로만 채워질 수 있다.  
`author` 필드에 넣을 `User` 객체를 불러올 때는 아래와 같이 입력해준다.  

```py
from django.contrib.auth import get_user_model

User = get_user_model()
```

`User` 는 `User` 객체이므로 `ORM` 을 통해 `User` 테이블의 데이터를 제어할 수 있다.  
아래와 같이 추가해서 `username` 이 `nachwon` 인 사용자 데이터를 불러와서 `Post` 객체의 `author` 에 할당해주자.

```py
def post_add(request):
    if request.method == 'POST':
        # User 객체를 생성
        User = get_user_model()  
        # User 객체를 통해 이름이 'nachwon' 인 User 객체를 불러와 'author' 변수에 할당
        author = User.objects.get(username='nachwon')  
        title = request.POST['title']
        content = request.POST['content']
        post = Post.objects.create(
            # Post 객체의 author 필드에 'author' 변수 할당 
            author=author,
            title=title,
            content=content,
        )
        return HttpResponse('POST method')
    elif request.method == 'GET':
        return render(request, 'blog/post_add.html')
```

마지막으로 `published_date` 필드가 비어있으면 메인 화면에서 글이 보이지 않으므로 이것도 넣어주자.  
`post` 는 `Post` 객체이므로 미리 만들어두었던 `publish` 메서드를 활용하자.

```py
def post_add(request):
    if request.method == 'POST':
        User = get_user_model()  
        author = User.objects.get(username='nachwon')  
        title = request.POST['title']
        content = request.POST['content']
        post = Post.objects.create(
            author=author,
            title=title,
            content=content,
        )
        # publish 메서드 호출
        post.publish()
        return HttpResponse('POST method')
    elif request.method == 'GET':
        return render(request, 'blog/post_add.html')
```
  
자 이제 모든 준비가 끝났다. `runserver` 를 실행하고 `post/add/` 로 접속해서 제목과 내용을 채워준 뒤 `글 등록` 버튼을 눌러보자.

<img width="400px" src="/img/django_tutorial/new_post_result.png">

이제 메인 화면에 접속해보면 아래와 같이 새 글이 추가되어 있는 것을 볼 수 있다.

<img width="950px" src="/img/django_tutorial/new_post_added.png">

- - -

### redirect()

보통 블로그에서 새 글을 등록하면 바로 등록한 글의 자세히 보기 페이지로 넘어간다. 지금 우리의 블로그는 `Post method` 라는 문자열을 돌려주도록 짜여있는데 이것을 고쳐보자.  
`views.py` 를 아래와 같이 수정해준다.

```py
# views.py

def post_add(request):
    if request.method == 'POST':
        User = get_user_model()
        author = User.objects.get(username='nachwon')
        title = request.POST['title']
        content = request.POST['content']
        post = Post.objects.create(
            author=author,
            title=title,
            content=content,
        )
        post.publish()
        # 등록한 글의 기본키를 가져와서 post_pk 변수에 할당.
        post_pk = post.pk
        # 기본키를 전달한 post_detail 뷰를 redirect 함수에 전달.
        return redirect(post_detail, pk=post_pk)
    elif request.method == 'GET':
        return render(request, 'blog/post_add.html')
```

`redirect()` 함수는 인자로 다음의 세 가지를 받을 수 있다.

- 모델: 모델의 `get_absolute_url()` 함수가 실행되어 그 결과가 인자로 전달됨.
- 뷰: 뷰가 인자를 받는다면 `redirect('뷰이름', 매개변수명=인자)` 의 형태로 뷰에 인자를 전달해줄 수 있다.
```py
redirect('뷰이름', 매개변수명=인자)
```
**주의!!: 뷰 오브젝트 자체를 넘겨주어도 작동하지만 그렇게할 경우 `역참조 url` 문제가 발생할 수가 있어서 권장되지 않는다.** 

- 절대 또는 상대 URL 주소: 해당 주소로 요청을 보낸다.  

우리의 경우 등록한 글의 `pk (기본키)` 를 `post_pk` 변수에 할당하고, 이 것을 `post_detail` 뷰에 전달한 것을 `redirect` 함수의 인자로 전달하였다. 다시 새로운 글을 등록해서 잘 작동하는지 확인해보자.

<img width="950px" src="/img/django_tutorial/redirect_test.png">

글을 등록하자마자 아래와 같이 자세히 보기 페이지가 뜨는 것을 확인할 수 있다.

- - -
### Post 추가 버튼 만들기

이제 새 `Post` 를 추가하는 모든 기능이 구현되어 있으니, 그 기능으로 쉽게 접근할 수 있도록 메인 화면에 링크만 하나 만들어주면 될 것 같다. 하는 김에 블로그 타이틀을 누르면 메인 화면으로 가는 기능도 추가하자.
`base.html` 을 열고 아래와 같이 수정한다.

```html
<div class="header">
    # h1 태그를 a 태그로 감싸고 href 속성에 `/` 넣어주어 클릭하면 메인 화면으로 가도록 해준다. 
    <a class="home" href="/"><h1>Che1's Blog!</h1></a>
    # Add Post 버튼 추가
    <a class="add-post" href="">
        <button type="button" class="btn btn-info">Add Post</button>
    </a>
</div>
```

`blog.css` 를 적절히 수정해준다.

```css
.add-post {
    position: absolute;
    right: 50px;
    top: 30px;
}
```

버튼을 추가해준 모습.

<img width="950px" src="/img/django_tutorial/add_post_button.png">

이제 `<a class="add-post" href="">` 의 `href` 값을 `/post/add/` 로 입력해주기만 하면된다.  
그냥 `/post/add/` 라고 입력해주어도 작동하겠지만, `{{ "{% url " }}%}` 템플릿 태그를 사용해서 동적으로 링크 주소를 생성하도록 해보자.  

```html
{{ "{% url '주소 또는 주소이름' " }}%}
```

`{{ "{% url " }}%}` 는 나타낼 주소를 문자열로 직접 입력하거나, `url` 객체를 전달할 수 도 있다.  
`urls.py` 를 열고 아래와 같이 수정하여 `post_add` 라는 이름을 `post_add` 뷰를 가리키는 `url` 객체에 부여해보자.
```py
# urls.py

url(r'^post/add/$', post_add, name='post_add'),
```

`url` 객체에 `name` 키워드 인자에 값을 전달해서 `post_add` 라는 이름을 붙여주었다. 이제 이것을 `url` 탬플릿 태그에 전달해서 `href` 에 넣어주자.  

```html
# base.html

<div class="header">
    # h1 태그를 a 태그로 감싸고 href 속성에 `/` 넣어주어 클릭하면 메인 화면으로 가도록 해준다. 
    <a class="home" href="/"><h1>Che1's Blog!</h1></a>
    # Add Post 버튼 추가
    <a class="add-post" href="{{ "{% url 'post_add' " }}%}">
        <button type="button" class="btn btn-info">Add Post</button>
    </a>
</div>

```

이제 `runserver` 를 열고 메인 화면에 있는 `Add Post` 버튼을 눌러서 잘 작동하는지 확인해보자.

<a href="#menu">위로</a>
- - -

## <span id="post-delete">Post 삭제하기</span>

새 글을 추가하는 기능을 넣었으니 이제 삭제하는 기능도 넣어보자.

- - -

### 글 삭제 버튼 추가

`post_detail.html` 을 열고 아래와 같이 추가해주자.

```html
# post_detail.html

<div class="container">
    <ul class="list">
        <li class="item">
            <h3><a href="">{{ "{{ post.title " }}}}</a></h3>
            <div class="content">{{ "{{ post.content|linebreaksbr " }}}}</div>
        </li>
    </ul>
    # 메인 화면으로 가는 버튼 추가
    <a href="/">
        <button type="button" class="btn btn-primary to-main">To Main</button>
    </a>
    # 글 삭제 버튼 추가
    <form action="" method="POST">
        {{ "{% csrf_token " }}%}
        <button type="submit" class="btn btn-danger">Delete Post</button>
    </form>
</div>
```

`href` 에 `/`를 넣어준 메인 화면으로 가는 버튼과 글 삭제 버튼을 추가시켰다.

<img width="950px" src="/img/django_tutorial/delete_button.png">

- - -

### delete 템플릿 생성

글을 삭제했을 때, 글이 삭제되었다는 메세지를 띄워주는 템플릿을 하나 만들자.

`template/blog` 폴더에 `post_delete.html` 파일을 추가하고 아래와 같이 넣어주자.

```html
{{ "{% extends 'base.html' " }}%}

{{ "{% block content " }}%}
<div class="container">
    <h1>글이 삭제되었습니다.</h1>
    <a href="/">
        <button type="button" class="btn btn-primary to-main">To Main</button>
    </a>
</div>
{{ "{% endblock " }}%}
```


이 안의 내용은 자유롭게 작성해주면 된다.

- - -

### delete URL 주소 설정

`post_delete.html` 이 표시될 `URL` 주소를 설정해주자.  
`urls.py` 를 열어서 `urlpatterns` 에 아래와 같이 추가해주자.

```py
url(r'^post/(?P<pk>\d+)/delete/$', post_delete, name='post_delete'),
```

`post_detail` 과 비슷하게 `pk` 값을 뷰에 넘겨준다.

- - -

### delete 뷰 생성

이제 글 삭제 기능을 구현하면서 `post_delete.html` 템플릿을 띄워줄 뷰를 생성한다.  
`views.py` 를 열고 아래와 같이 추가해준다.

```py
def post_delete(request, pk):
    if request.method == 'POST':
        post = Post.objects.get(pk=pk)
        post.delete()
        return render(request, 'blog/post_delete.html')

    elif request.method == 'GET':
        return HttpResponse('잘못된 접근 입니다.')
```

`POST` 요청을 통해서만 삭제가 가능하도록 `if` 문으로 나누어주고 받아온 `pk` 값으로 데이터베이스에서 기본키를 검색하여 해당 `Post` 를 삭제한다. 그리고나서 `post_delete.html` 파일을 렌더해준다.

- - -

### form action 설정

글 삭제 버튼은 어떤 글의 자세히 보기 페이지에 있으며, 그 버튼을 누르면 현재 보고있는 페이지를 삭제해야한다. 그렇게 해주려면 설정해준 `URL` 인 `r'^post/(?P<pk>\d+)/delete/$'` 의 `pk` 그룹 값으로 현재 보고있는 페이지의 `pk` 값을 전달해야한다.  
일단 코드를 먼저 보자.

```html
# post_detail.html

<form action="{{ "{% url 'post_delete' pk=post.pk " }}%}" method="POST">
    {{ "{% csrf_token " }}%}
    <button type="submit" class="btn btn-danger">Delete Post</button>
</form>
```

`form` 의 `action` 속성은 `URL` 주소를 받으며, 폼을 통해 데이터를 전달할 때 해당 주소로 요청을 보내게 된다. 이 버튼은 글 삭제 버튼이므로 `post_delete` 뷰를 실행시키기 위해서는 `post/글번호/delete/` 의 주소로 요청을 보내야한다. 따라서 아래와 같이 `url` 템플릿 태그를 사용해준다.

```html
{{ "{% url 'post_delete' pk=post.pk " }}%}
```

위 템플릿 태그는 `post_delete` 라는 이름의 `url` 객체를 가져오고 그 객체의 `pk` 값에 현재 글의 `pk` 값을 뜻하는 `post.pk` 를 할당한다. 결국, `post/현재 글번호/delete` 라는 `URL` 주소가 `action` 속성에 전달되는 것이다.

이제 `runserver` 를 실행하고 아무 글이나 들어가서 `Post Delete` 버튼을 눌러보자.

<img width="950px" src="/img/django_tutorial/post_delete.png">

글이 잘 삭제되는 것을 볼 수 있다.


<a href="#menu">위로</a>

- - -

{% include tutorial-toc-base.html %}

- - -

#### Reference
이한영 강사님 강의자료  
Django 공식문서: [https://docs.djangoproject.com/en/1.11/ref/templates/builtins/#ref-templates-builtins-tags](https://docs.djangoproject.com/en/1.11/ref/templates/builtins/#ref-templates-builtins-tags)  
Django 공식문서: [https://docs.djangoproject.com/en/1.11/topics/http/shortcuts/](https://docs.djangoproject.com/en/1.11/topics/http/shortcuts/)  
정보통신기술용어해설: [http://www.ktword.co.kr/abbr_view.php?m_temp1=3791](http://www.ktword.co.kr/abbr_view.php?m_temp1=3791)  
paulaner80 블로그: [http://paulaner80.tistory.com/entry/%ED%81%AC%EB%A1%AC%EC%97%90%EC%84%9C-request-response-header-%ED%99%95%EC%9D%B8%ED%95%98%EA%B8%B0](http://paulaner80.tistory.com/entry/%ED%81%AC%EB%A1%AC%EC%97%90%EC%84%9C-request-response-header-%ED%99%95%EC%9D%B8%ED%95%98%EA%B8%B0)  
egocube : [http://www.egocube.pe.kr/Translation/Content/asp-net-web-api/201402030001](http://www.egocube.pe.kr/Translation/Content/asp-net-web-api/201402030001)


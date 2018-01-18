---
layout: post
title: '[Deploy] Django 프로젝트 배포하기 - 7. Amazon S3'
subtitle: Storing Static Files in S3 Storages
comments: true
category: Django
tags:
  - Django
  - AWS
  - S3
  - Deploy
---

`Amazon S3` 는 아마존 웹 서비스(AWS)에서 제공하는 클라우드 스토리지 서비스이다.  

이번 포스트에서는 장고 프로젝트에 필요한 스태틱 파일 및 미디어 파일들을 Amazon S3라는 별도의 저장소에 저장하여 관리하는 방법에 대해 알아본다.  
이번 포스트에 사용할 간단한 장고 프로젝트 `s3_practice` 를 새로 시작하고 `practice` 라는 앱을 하나 추가해 주었다.

```re
django_s3
├── README.md
├── .git
├── .gitignore
├── .idea
├── .python-version
├── requirements.txt
└── s3_practice
    ├── config
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── manage.py
    └── practice
        ├── __init__.py
        ├── admin.py
        ├── apps.py
        ├── migrations
        ├── models.py
        ├── storages.py
        ├── tests.py
        └── views.py
```

- - -

## Django의 Storage 클래스

장고는 파일을 다루기 위해 `Storage` 라는 클래스를 제공한다. Storage 클래스는 파일을 다루는데 필요한 기본적인 메소드들을 가지고 있으며, 다른 파일 저장 시스템 클래스들은 이 클래스를 상속받아 만들어진다.  
Storage 클래스가 가지는 기본적인 메소드들에는 `open`, `save`, `delete`, `path`, `exists` 등등이 있고 이들 중 대부분의 메소드는 Storage를 상속받는 서브 클래스에서 반드시 정의해주어야하도록 되어있다.  

장고에서 기본적으로 사용하는 파일 저장 시스템은 **`FileSystemStorage`** 클래스이다. `Storage` 클래스를 상속받는 이 클래스는 로컬 저장소에 파일을 저장하는 기본적인 파일 저장 시스템 기능을 가지고 있다.  

우리가 지금까지 파일을 저장할 경로로 지정해주었던 `MEDIA_ROOT` 변수와 저장한 파일을 요청할 때 사용했던 `MEDIA_URL` 변수는 모두 `FileSystemStorage` 클래스에서 사용하는 변수이다.  

`FileSystemStorage` 는 로컬 저장소에 파일을 저장하는 저장 시스템이다. 실제 운영되는 서비스의 경우 프로젝트와 같은 공간에 미디어 파일들을 저장한다면 저장 용량, 보안, 백업 등 여러가지 문제가 생길 수 있다.  
따라서 미디어 파일들을 관리하는데 특화된 별도의 저장소를 구축하여 운영하는 것이 좋으며, 그러한 별도의 저장소 서비스 중 하나가 `Amazon S3` 이다.

- - -

## Django_storages 패키지

위에서 언급했듯이 `FileSystemStorage` 클래스는 로컬에 파일을 저장하는 저장 시스템 클래스이다. 우리가 필요한 것은 로컬이 아닌 Amazon S3 저장소에 파일을 저장하는 저장 시스템 클래스이다.  
그런 기능을 하는 클래스를 구현하려면 `Storage` 클래스를 상속받아 서브클래스를 만들고 Amazon S3의 API에 맞는 요청을 보내주는 메소드들을 직접 구현해주면 된다.  
예를 들어, S3 저장소에 있는 `my-second-image.jpg` 파일을 삭제하고 싶으면 아래와 같은 HTTP 요청을 보내면 된다.

```
DELETE /my-second-image.jpg HTTP/1.1
Host: bucket.s3.amazonaws.com
Date: Wed, 12 Oct 2009 17:50:00 GMT
Authorization: authorization string
Content-Type: text/plain
```

이러한 요청을 보내는 Python 코드를 직접 만든 저장 시스템 클래스에 `delete` 메소드로 정의해주면 되는 것이다.  
정확하지는 않지만 대략적인 예시를 들자면 아래와 같다.

```py
from django.core.files.storage import Storage
import requests

class S3Storage(Storage):
    .
    .
    .
    def delete(self, file_name):
        url = f'http://s3.amazonaws.com/{file_name}'
        response = requests.delete(url, credentials=...)
        return response == 204
    .
    .
    .
```

`requests` 패키지를 이용해서 `http://s3.amazonaws.com/my-second-image.jpg` 라는 주소로 `DELETE` 요청을 보내면 S3에서 이 요청을 처리하여 저장소에 있는 `my-second-image.jpg` 파일을 삭제하게 된다.  
이런 식으로 일일이 모든 기능을 구현해주려면 매우 번거로울 것이다. 그래서 사람들은 S3 저장소와 통신할 수 있는 저장 시스템 클래스를 미리 구현하여 패키지로 만들어 두었다. 그게 바로 `django_storages` 패키지이다.

- - -

#### django_storages 설치하기

터미널에서 아래 명령을 입력하여 `django_storages` 패키지를 설치한다.

```
pip install django_storages
```

그 다음 `settings.py` 의 `INSTALLED_APPS` 에 `storages` 를 추가해준다.

```py

INSTALLED_APPS = [
    'django.contrib.admin',
    ...
    'storages',

    'practice',
]
```

- - -

## boto3

django_storages 패키지는 `boto3` 라는 패키지를 사용하여 S3와 통신하도록 구성되어있다.  
`boto3` 는 S3를 조작할 수 있는 API에 맞는 요청을 Python으로 작성해놓은 패키지이다.  
`boto3` 를 사용하면 `requests` 패키지를 사용해서 직접 요청을 보내도록 코딩을 할 필요 없이 미리 정의된 메서드를 사용해서 간편히 API를 다룰 수 있다.  
예를 들어, 위의 `my-second-image.jpg` 파일을 S3 저장소에서 삭제하는 코드를 boto3를 사용해서 작성하면 아래와 같다.

```py
import boto3
...
    def delete(file_name):
        boto3.delete(bucket, file_name)
...
```

`boto3` 는 단순한 파일 저장, 삭제 등과 같은 기능 이외에도 버킷 생성, 권한 설정 등과 같은 S3 편의 기능도 제어할 수 있도록 작성되어 있다. django_storages 는 이 boto3를 사용하여 S3에 파일을 저장하는 저장 시스템 클래스인 것이다.  

- - -

#### boto3 설치하기

아래 명령을 터미널에서 입력하여 boto3 를 설치한다.

```
pip install boto3
```

- - -

## S3 시작하기

#### S3 권한 추가

S3는 EC2와는 별개의 서비스이므로 `IAM` 으로 생성했던 유저에 새로 S3 사용 권한을 추가해주어야 사용할 수 있다.  

[AWS 콘솔](https://ap-northeast-2.console.aws.amazon.com/console/home?region=ap-northeast-2) 로 접속한 다음 `서비스 > 보안, 자격 증명 및 규정 준수 > IAM` 으로 이동한다.

`User` 탭을 눌러 사용자 관리 화면으로 간 다음, 생성되어 있는 사용자 이름을 클릭하여 사용자 수정화면으로 들어간다.

<img width="600px" src="/img/AWS_deploy/edit_user.png">

- - -

`Add_permissions` 버튼을 눌러 권한 추가 화면으로 넘어간다.

<img width="600px" src="/img/AWS_deploy/add_permissions.png">

- - -

권한 추가 화면에서 세 번째 박스인 `Attach existing policies directly` 항목을 클릭하면 나타나는 검색창에서 `s3full` 이라고 검색하면 나오는 `AmazonS3FullAccess` 권한을 체크하고 다음으로 넘어간다.

<img width="600px" src="/img/AWS_deploy/s3_full.png">

- - -

`Add permission` 을 눌러 최종적으로 권한을 추가한다.  
`Summary` 페이지에서 `AmazonS3FullAccess` 가 추가 된 것을 확인하면 된다.

<img width="600px" src="/img/AWS_deploy/s3_summary.png">

- - -

#### 버킷 생성하기

S3 서비스는 `버킷 (bucket)` 이라는 단위로 저장소를 나눈다. 마치 `EC2` 서비스에서 가상 컴퓨터의 인스턴스를 생성하여 사용했듯이, 버킷이라는 각각의 저장소를 만들어 사용하는 것이다.  

버킷은 직접 S3 콘솔 사이트로 접속해서 생성할 수 있다. 

S3 콘솔: [https://s3.console.aws.amazon.com/](https://s3.console.aws.amazon.com/)

콘솔에 접속해서 `버킷 만들기` 버튼을 눌러 새로운 버킷을 생성한다.  
이름을 입력하고 `다음` 을 누른다.  
버킷의 이름은 `DNS` 형식이어야하므로 모든 버킷 이름은 고유한 이름이어야 하며, `_` 와 같이 주소에 포함될 수 없는 문자는 사용할 수 없다.

<img width="600px" src="/img/AWS_deploy/create_bucket.png">

- - -

나머지 설정들은 기본 설정 그대로 두고 `다음` 을 클릭하여 넘어간다.  
마지막으로 설정들을 확인한 뒤 `버킷 만들기` 를 눌러 버킷을 생성한다.

<img width="600px" src="/img/AWS_deploy/bucket_create.png">

- - -

버킷은 boto3 를 사용해서 Python으로 생성할 수도 있다.  
boto3 가 설치된 가상환경이 적용된 프로젝트 폴더로 이동한 다음 `python` 을 입력하여 `Python REPL` 을 실행한다.

```
python
```
```re
Python 3.6.3 (default, Oct 29 2017, 20:29:12) 
[GCC 5.4.0 20160609] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```

아래의 명령을 차례대로 입력한다.  
`client.create_bucket` 의 `Bucket` 은 생성하는 버켓의 이름이며, 콘솔에서 생성할 때와 똑같은 규칙으로 생성해야한다.

```py
>>> import boto3
>>> session = boto3.Session()
>>> client = session.client('s3')
>>> client.create_bucket(Bucket='버켓이름', CreateBucketConfiguration={'LocationConstraint': 'ap-northeast-2'})
```

```re
{'ResponseMetadata': {'RequestId': '9F7DF05FA5A12882', 'HostId': 'VgPI7JSg/szpSnN62egag4pyuu0jwLKyeDE3rQ1ODTZaTAhfO1Bukmv7sdTsW9+wdpB19Y7Gy9Y=', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amz-id-2': 'VgPI7JSg/szpSnN62egag4pyuu0jwLKyeDE3rQ1ODTZaTAhfO1Bukmv7sdTsW9+wdpB19Y7Gy9Y=', 'x-amz-request-id': '9F7DF05FA5A12882', 'date': 'Tue, 31 Oct 2017 15:20:49 GMT', 'location': 'http://버켓이름.s3.amazonaws.com/', 'content-length': '0', 'server': 'AmazonS3'}, 'RetryAttempts': 0}, 'Location': 'http://버켓이름.s3.amazonaws.com/'}
```

- - -

만들어진 버켓은 S3 콘솔에서 확인할 수 있다.



- - -

## Django 설정

이제 S3가 준비되었으니 장고에서 S3 저장소를 사용하도록 설정해주어야 한다.

장고에서 S3에 관한 설정은 `settings.py` 에 django_storages 패키지에서 미리 정의한 특정 변수명으로 설정한다.  
많은 옵션이 있지만 그 중 필수적인 설정은 아래와 같다.  

- - -

#### S3 관련 필수 설정

- `DEFAULT_FILE_STORAGE`: 장고의 기본 저장 시스템 클래스를 지정해주는 설정이다. 기본적으로 `FileSystemStorage` 를 사용한다.
```py
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

- `STATICFILES_STORAGE`: `collectstatic` 명령을 실행했을 때 생성되는 스태틱 폴더를 S3 버킷 저장소에 생성하도록 하는 설정이다.
```py
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

- `AWS_ACCESS_KEY_ID`: AWS 계정의 엑세스 키 아이디를 문자열로 입력한다. IAM에서 유저를 생성했을 때 다운 받은 `credentials.csv` 파일 안에서 확인할 수 있다.  
```py
AWS_ACCESS_KEY_ID = 'AKIAJOP4E4KWP3XYGMEA'
```

- `AWS_SECRET_ACCESS_KEY`: AWS 계정의 비밀 엑세스 키를 문자열로 입력한다. 역시 `credentials.csv` 에서 확인할 수 있다.
```py
AWS_SECRET_ACCESS_KEY = '**************'
```

- `AWS_STORAGE_BUCKET_NAME`: S3에 생성했던 버킷 이름을 문자열로 입력한다.
```py
AWS_STORAGE_BUCKET_NAME = 'che1-s3-practice'
```

위의 설정들을 모두 `settings.py` 에 넣어주면 된다.

```py
# settings.py

...
# S3 Storage
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# AWS Access
AWS_ACCESS_KEY_ID = 'AKIAJOP4E4KWP3XYGMEA'
AWS_SECRET_ACCESS_KEY = '************'
AWS_STORAGE_BUCKET_NAME = 'che1-s3-practice'
...
```

- - -

#### S3에 Static 파일 모으기

이제 S3의 설정은 모두 끝났으니 잘 저장이 되는지 확인을 해보자.  
`static` 폴더를 하나 생성해주고 `STATICFILES_DIRS` 에 경로를 추가한다.

```py
# settings.py

STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    STATIC_DIR,
]
```

그 다음 간단한 뷰와 템플릿을 생성한다.

```html
# index.html

{{ "{% load static " }}%}
...
<body>
    <h1>TEST!</h1>
    <a href="{{ "{% static 'test.txt' " }}%}">
</body>
...
```

```py
# views.py

def test(request):
    return render(request, 'index.html')
```

```py
# urls.py

from practice.views import test

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('^$', test, name='test'),
]
```

이제 `static` 폴더안에 테스트로 출력해볼 `test.txt` 파일도 하나 만들어 둔다.

최종적으로 아래와 같이 만들어준다.

```re
django_s3
├── config
├── db.sqlite3
├── manage.py
├── practice
├── static
│   └── test.txt
└── templates
    └── index.html
```

모든 세팅이 끝났으면 `collectstatic` 명령으로 모든 정적 파일들을 모아준다.

```
./manage.py collectstatic
```

```re
You have requested to collect static files at the destination
location as specified in your settings.

This will overwrite existing files!
Are you sure you want to do this?

Type 'yes' to continue, or 'no' to cancel: 
```

`yes` 를 입력하고나면 `STATIC_ROOT`, `MEDIA_ROOT` 를 지정해주지 않았음에도 `collectstatic` 이 실행되는 것을 볼 수 있다.  
`STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'` 라고 설정해주었기 때문에 `STATIC_ROOT` 경로가 아닌 S3 저장소에 저장한다.

실행이 완료되면 S3 콘솔로 가서 생성했던 버킷으로 들어가보자.  

<img width="700px" src="/img/AWS_deploy/collectstatic_result.png">

프로젝트에서 사용하는 스태틱 파일들이 모여있는 것을 볼 수 있다.  
우리가 추가한 `test.txt` 도 추가되어있다.  

이제 `runserver` 를 실행해서 템플릿에서 스태틱 파일을 잘 불러오는지도 확인해보자.  

<img width="900px" src="/img/AWS_deploy/static_test_result.png">

링크를 타고 들어가보면 `test.txt` 의 내용이 표시되는 것을 볼 수 있다.  
링크 주소를 확인해보면 아래와 같이 S3 저장소 주소인 것을 확인할 수 있다.
```
https://s3.ap-northeast-2.amazonaws.com/che1-s3-practice/test.txt?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=...
```

- - -

#### S3에 미디어 파일 저장하기

스태틱 파일들은 해결되었고, 이제 미디어 파일이 S3 저장소에 저장되는지 확인해보자.  
미디어 파일을 `POST` 요청으로 올렸을 때 S3 저장소에 업로드되는지 확인하면 된다.  

아래와 같이 간단한 `model` 을 추가하고 `view`, `template` 을 수정해서 파일을 `POST` 요청으로 보낼 수 있도록 만들어 보자.  

```py
# models.py

class Image(models.Model):
    img = models.ImageField(upload_to='usr')
```

```py
# views.py

def show_img(request):
    if request.method == 'POST':
        img = request.FILES.get('img-file')
        Image.objects.create(img=img)
        return redirect(show_img)
    else:
        img = Image.objects.first()
    context = {
        'object': img
    }
    return render(request, 'index.html', context)
```

```html
# index.html

...
<body>
    <h1>TEST!</h1>
    <form action="" method="post" enctype="multipart/form-data">
        {{ "{% csrf_token " }}%}
        <input type="file" name="img-file">
        <input type="submit">
    </form>
{{ "{% if object.img " }}%}
    <img src="{{ "{{ object.img.url " }}}}" alt="">
{{ "{% else " }}%}
{{ "{% endif " }}%}
</body>
...
```

`runserver` 를 실행해서 이미지 파일을 하나 올려보면 잘 나타나는 것을 볼 수 있다.  

<img width="900px" src="/img/AWS_deploy/media_test_result.png">

물론 S3에도 파일이 올라간 것을 볼 수 있다.  
미디어 파일이 `usr` 라는 폴더 안에 들어가 있는 것을 볼 수 있는데 이는 모델에서 `img` 필드를 생성할 때 지정한 `upload_to` 옵션 때문이다.

<img width="600px" src="/img/AWS_deploy/s3_test_result.png">

이미지 파일의 경로는 역시 `s3.ap-northeast-2.amazonaws.com` 으로 시작하는 S3 주소이다.  
템플릿에서 이 주소를 참조하게 하려면 `{{ "{{ object.img.url " }}}}` 과 같이 `url` 을 붙여주어야 한다.

- - -

#### 별도의 경로에 저장하기

지금까지 미디어 파일들과 스태틱 파일들을 S3 버킷 저장소에 저장하는 것을 해보았는데 문제는 미디어 파일과 스태틱 파일이 구분이 없이 모두 한 곳에 저장된다는 점이다. 파일이 많아지면 관리가 어려워질 수 있으니 미디어 파일은 미디어 폴더에, 스태틱 파일들은 스태틱 폴더에 구분해서 저장하도록 해보자.  

먼저 `settings.py` 에 아래와 같이 추가해준다.  
어디에 추가해도 상관없지만 가독성을 위해 다른 S3 설정들과 같은 자리에 추가해주면 좋을 것 같다.

```py
# settings.py

...
# S3 Storage
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIAFILES_LOCATION = 'media'
STATICFILES_LOCATION = 'static'
...
```

다음으로 `config` 폴더 아래에 `storages.py` 를 생성한 다음 아래와 같이 입력해준다.  

```py
# storages.py

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION


class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION
```

`MediaStorage` 와 `StaticStorage` 는 모두 `S3Boto3Storage` 클래스를 상속받으며, 각각 `settings.py` 에서 지정해놓은 `..._LOCATION` 변수의 값으로 저장 경로를 지정하는 `location` 메소드를 오버라이드 한다.  

다시 `settings.py` 로 돌아가서 커스터마이징 한 저장 시스템 클래스를 사용하도록 바꿔주자.

```py
# settings.py

...
# S3 Storage
DEFAULT_FILE_STORAGE = 'config.storages.MediaStorage'
STATICFILES_STORAGE = 'config.storages.StaticStorage'
MEDIAFILES_LOCATION = 'media'
STATICFILES_LOCATION = 'static'
...
```

제대로된 확인을 위해 S3 저장소에 있는 모든 자료를 다 삭제하고 다시 `collectstatic` 을 해보자.

<img width="600px" src="/img/AWS_deploy/s3_static_folder.png">

이제 `runserver` 를 실행시키고 이미지 파일도 한 번 업로드 해보자.  
관리자 페이지에서 기존에 있던 모든 `Image` 객체들을 삭제해주고 파일을 업로드 한다.

<img width="600px" src="/img/AWS_deploy/s3_media_folder.png">

`media` 폴더가 생성되었고, 그 안에 `usr` 폴더 안에 업로드한 이미지 파일이 저장된 것을 볼 수 있다.

- - -

#### 중요 정보 분리

`settings.py` 의 `AWS_SECRET_ACCESS_KEY` 와 같은 정보는 절대로 외부에 공개되어서는 안되는 정보이다.  
만약에 이대로 커밋을 하여 깃 저장소에 올려버리면 모든 사람들이 비밀 엑세스 키를 볼 수 있게 된다.  
따라서 이런 중요 정보들은 따로 파일을 만들어 관리하는 것이 좋다.

먼저 `s3_practice` 폴더와 같은 위치에 `.config_secret` 이라는 숨김 폴더를 하나 생성한 다음 그 안에 `settings_common.json` 파일을 하나 만들어 준다.

```re
django_s3
├── .config_secret
│   └── settings_common.json
├── .git
├── .gitignore
├── .idea
├── .python-version
├── README.md
├── requirements.txt
└── s3_practice
```

이제 `settings.py` 에 있는 중요 정보들은 이 `settings_common.json` 파일에 옮겨놓고 불러오는 식으로 사용할 것이다.  

`settings.py` 에 입력한 AWS 관련 정보들을 옮겨주고 옮긴 내용들은 삭제해준다.

```json
# settings_common.json

{
  "aws": {
    "access_key_id": "AKIAJOP4E4KWP3XYGMEA",
    "secret_access_key": "***********",
    "s3_bucket_name": "che1-s3-practice"
  }
}
```

그리고나서 `settings.py` 에서 이 json 파일의 내용을 불러와주면 된다.

```py
# settings.py

import json
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)
CONFIG_SECRET_DIR = os.path.join(ROOT_DIR, '.config_secret')
CONFIG_SETTINGS_COMMON_FILE = os.path.join(CONFIG_SECRET_DIR, 'settings_common.json')

# S3 Storage
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# AWS Access
config_secret = json.loads(open(CONFIG_SETTINGS_COMMON_FILE).read())
AWS_ACCESS_KEY_ID = config_secret['aws']['access_key_id']
AWS_SECRET_ACCESS_KEY = config_secret['aws']['secret_access_key']
AWS_STORAGE_BUCKET_NAME = config_secret['aws']['s3_bucket_name']
```

**생성한 `.config_secret` 폴더는 Github에 업로드되면 안되므로 `.gitignore` 파일에 반드시 포함해주어야한다. 안그러면 돈나간다 나처럼 ㅠㅠ**

- - -

{% include /deploy/deploy-toc-base.html %}

- - -

###### Reference

이한영 강사님 블로그: [https://lhy.kr/ec2-ubuntu-deploy](https://lhy.kr/ec2-ubuntu-deploy)  
Django 공식 문서: [https://docs.djangoproject.com/en/1.11/ref/files/storage/#django.core.files.storage.DefaultStorage](https://docs.djangoproject.com/en/1.11/ref/files/storage/#django.core.files.storage.DefaultStorage)  
django_storages 공식 문서: [https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html](https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html)  
boto3 공식 문서: [https://boto3.readthedocs.io/en/latest/](https://boto3.readthedocs.io/en/latest/)  
S3 공식 문서: [https://aws.amazon.com/ko/documentation/s3/](https://aws.amazon.com/ko/documentation/s3/)

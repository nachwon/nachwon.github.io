---
layout: post
title: '[Deploy] Django 프로젝트 배포하기 - 7. Amazon S3'
subtitle: Storing Static Files in S3 Storages
category: Django
author: Che1
---

{% include /deploy/deploy-toc-base.html %}

- - -

`Amazon S3` 는 아마존 웹 서비스(AWS)에서 제공하는 클라우드 스토리지 서비스이다.  

이번 포스트에서는 장고 프로젝트에 필요한 스태틱 파일 및 미디어 파일들을 Amazon S3라는 별도의 저장소에 저장하여 관리하는 방법에 대해 알아본다.

- - -

## Django의 Storage 클래스

장고는 파일을 다루기 위한 `Storage` 라는 클래스를 제공한다. Storage 클래스는 파일을 다루는데 필요한 기본적인 메소드들을 가지고 있으며, 다른 파일 저장 시스템 클래스들은 이 클래스를 상속받아 만들어진다.  
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

그 다음 `settings.py` 의 `INSTALLED_APPS` 에 추가해준다.

```py

INSTALLED_APPS = [
    'django.contrib.admin',
    ...
    'storages',
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

`boto3` 는 단순한 파일 저장, 삭제 등과 같은 기능 이외에도 버킷 생성, 권한 설정 등과 같은 S3 편의 기능도 제어할 수 있도록 작성되어 있다. django_storages 는 이 boto3를 사용하여 S3에 파일을 저장하는 시스템 클래스인 것이다.  

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

<img width="700px" src="/img/AWS_deploy/bucket_list.png">

- - -

## Django 설정
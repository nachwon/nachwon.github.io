---
layout: post
title: '[Deploy] Django 프로젝트 배포하기 - 2. WSGI'
excerpt: uWSGI 설치하기
comments: true
category: Django
tags:
  - Django
  - uWSGI
  - Deploy
---



지난 포스트에서는 AWS의 가상 컴퓨터 인스턴스를 생성하여 공개 서버를 열고, 그 서버에 장고 프로젝트를 업로드한 다음 `runserver` 를 실행해보았다.  
`runserver` 는 개발용이므로 실제 서비스를 운영하는데 부적합하기 때문에 실제로 어플리케이션을 서비스할 때는 웹서버를 사용하게 된다.  
웹서버를 사용하기 위해서는 먼저 `WSGI` 를 설치해야 한다.

- - -

## WSGI

> #### Web Server Gateway Interface
>
> 웹 서버 게이트웨이 인터페이스(WSGI, Web Server Gateway Interface)는 웹서버와 웹 애플리케이션의 인터페이스를 위한 파이선 프레임워크다.  
> 기존의 파이선 웹 애플리케이션 프레임워크는 웹서버를 선택하는데 있어서 제약이 있었다. 보통 CGI, FastCGI, mod_python 과 같은 커스텀API 중에 하나만 사용할 수 있도록 디자인 되었는데, WSGI는 그에 반하여 low-level로 만들어져서 웹서버와 웹 애플리케이션,프레임워크간의 벽을 허물었다.  
> 출처: [위키피디아](https://ko.wikipedia.org/wiki/%EC%9B%B9_%EC%84%9C%EB%B2%84_%EA%B2%8C%EC%9D%B4%ED%8A%B8%EC%9B%A8%EC%9D%B4_%EC%9D%B8%ED%84%B0%ED%8E%98%EC%9D%B4%EC%8A%A4)

WSGI는 장고와 웹서버를 연결해주는 역할을 하는 Python 프레임워크이다. 프로토콜 개념으로도 이해할 수 있다.  
웹서버가 직접적으로 Python으로 된 장고와 통신할 수 없기 때문에 그 사이에서 `WSGI Server(middleware)` 가 실행되어 웹서버와 장고를 연결해준다.
웹서버가 전달받은 사용자의 요청을 WSGI Server에서 처리하여 Django로 넘겨주고, 다시 Django가 넘겨준 응답을 WSGI Server가 받아서 웹서버에 전달한다.

```
사용자 <-> 웹서버 <-> WSGI Server <-> Django
```

WSGI Server에는 여러 가지 종류가 있는데, 그 중 기능이 강력하고 확장성이 뛰어난 `uWSGI` 를 사용할 것이다.

- - -

#### uWSGI 설치

먼저 `ssh` 를 통해 AWS 서버에 접속한 다음, 배포에 사용할 새로운 유저를 `deploy` 라는 이름으로 생성해준다.  
보안을 위해 각 기능 별 유저를 설정해주는 것이 좋다.  

```
sudo adduser deploy
```

그런 다음, uWSGI를 설치할 별도의 Python 가상환경을 생성해준다.

```
pyenv virtualenv 3.6.2 uwsgi-env
```

이 가상환경을 지금 현재의 가상 컴퓨터 셸에만 일시적으로 적용하도록 설정해준다.  
서버 전체에서 하나의 uwsgi를 사용하게 하기 위함이다.

```
pyenv shell uwsgi-env
```

이제 가상환경에 `uwsgi` 를 설치한다.

```
pip install uwsgi
```

- - -

#### uWSGI로 서버 열어보기

uWSGI를 실행하려면 `pyenv shell uwsgi-env` 를 입력해 uwsgi-env를 적용한 다음, 아래와 같이 입력한다.

```
uwsgi \
--http :[포트번호] \
--home [virtualenv 경로] \
--chdir [장고프로젝트폴더 경로] \
-w [wsgi 모듈명].wsgi
```

현재 진행중인 프로젝트의 경우를 대입해보면 다음과 같다.

- **포트번호**: 8080  
- **virtualenv 경로**: /home/ubuntu/.pyenv/versions/ec2_deploy  
- **장고프로젝트폴더 경로**: /srv/EC2_Deploy_Project/mysite (manage.py가 있는 경로를 지정해주면 된다.)  
- **wsgi 모듈명**: config.wsgi  

```
uwsgi \ 
--http :8080 \
--home /home/ubuntu/.pyenv/versions/ec2_deploy \
--chdir /srv/EC2_Deploy_Project/mysite \
-w config.wsgi
```

위 명령을 실행하면 아래와 같이 뜨고, uWSGI가 요청을 받을 수 있는 상태가 된다.

<img width="600px" src="/img/AWS_deploy/uwsgi_test.png">

이제 브라우저에서 퍼블릭 DNS의 8080번 포트에 접속해보자.  
```
ec2-13-124-186-240.ap-northeast-2.compute.amazonaws.com:8080
```

<img width="950px" src="/img/AWS_deploy/runserver.png">

runserver를 실행하지 않았는데도 접속이 가능한 것을 볼 수 있다. WSGI를 통해 사용자의 요청을 받을 수 있게 되었기 때문이다.  
터미널창을 확인해보면 GET 요청이 들어와있는것을 확인할 수 있다.

<img width="600px" src="/img/AWS_deploy/uwsgi_get_request.png">

- - -

#### ini 파일로 uWSGI 실행하기

매번 uWSGI를 실행할 때마다 위의 복잡한 명령을 입력하기 번거로우므로, 미리 옵션을 파일로 만들어 저장해놓고 실행할 수 있다.

로컬에서 장고 프로젝트 폴더에 `.config` 라는 폴더를 하나 새로 생성하고 그 안에 다시 `uwsgi` 폴더를 생성한다.  
`uwsgi` 폴더 안에 `mysite.ini` 파일을 만들어 준다.

```re
EC2_Deploy_Project
├── .config
│   └── uwsgi
│       └── mysite.ini
├── .git
├── .gitignore
├── mysite
└── requirements.txt
```

mysite.ini를 열고 다음과 같이 입력한다.

```
[uwsgi]
chdir = /srv/EC2_Deploy_Project/mysite
module = config.wsgi:application
home = /home/ubuntu/.pyenv/versions/ec2_deploy

uid = deploy
gid = deploy

http = :8080

enable-threads = true
master = true
vacuum = true
pidfile = /tmp/mysite.pid
logto = /var/log/uwsgi/mysite/@(exec://date +%%Y-%%m-%%d).log
log-reopen = true
```

- **`chdir`**: 장고 프로젝트 폴더의 경로(manage.py가 있는 폴더)
- **`module`**: 장고 프로젝트 내의 `wsgi.py` 파일의 경로
- **`home`**: 장고 프로젝트가 실행되는 Python 가상환경 경로

- **`uid, gid`**: uWSGI를 실행할 사용자 및 사용자그룹 지정

- **`http`**: http를 통해서 요청을 받을 수 있도록 하며, 요청을 받을 포트 번호를 설정한다.

- **`enable-threads`**: 스레드 사용 여부
- **`master`**: 마스터 프로세스 사용 여부
- **`vaccum`**: 실행시 자동 생성되는 파일 또는 소켓들을 종료될 때 삭제하는 옵션
- **`pidfile`**: `pidfile` 이 생성될 폴더의 경로를 설정한다. pidfile은 Linux에서 실행되는 프로세스의 `id` 값을 담고있는 파일이다.
- **`logto`**: 로그 파일을 작성할 위치 설정. 보통 로그는 `/var/log/` 폴더 아래에 생성한다.
- **`log-reopen`**: uWSGI를 재시작할때 로그를 다시 열어주는 옵션

이제 프로젝트 폴더를 scp를 통해 서버에 전송한 다음 ssh를 통해 서버에 접속한다.

```
scp -i ~/.ssh/EC2-Che1.pem -r EC2_Deploy_Project ubuntu@ec2-13-124-186-240.ap-northeast-2.compute.amazonaws.com:/srv/ 
```
```
ssh -i ~/.ssh/EC2-CH1.pem ubuntu@ec2-13-124-186-240.ap-northeast-2.compute.amazonaws.com
```

uWSGI를 실행하기 전에 `mysite.ini` 파일에 설정해주었던 `logto` 옵션의 디렉토리를 직접 생성해주어야 한다.

```
sudo mkdir -p /var/log/uwsgi/mysite
```

그 다음 아래의 명령을 실행해 `ini` 파일로 uWSGI를 실행한다. `sudo` 권한으로 실행해야 하기 때문에, uwsgi-env 가상환경 폴더 안에 있는 uwsgi를 직접 실행해주어야 한다.

```
sudo /home/ubuntu/.pyenv/versions/uwsgi-env/bin/uwsgi -i /srv/EC2_Deploy_Project/.config/uwsgi/mysite.ini 
```

이제 브라우저에서 퍼블릭 도메인의 8080번 포트로 접속해보면 접속이 되는 것을 볼 수 있다.  
uWSGI 실행 로그를 확인하려면 아까 생성해주었던 로그 폴더 안의 `.log` 파일을 열어보면 된다.  

```
sudo cat /var/log/uwsgi/mysite/로그파일이름.log
```

<img width="600px" src="/img/AWS_deploy/uwsgi_log.png">

이전과 같이 GET 요청을 받았다는 로그를 확인할 수 있다.

- - -


{% include /deploy/deploy-toc-base.html %}

- - -

###### Reference

이한영 강사님 블로그: [https://lhy.kr/ec2-ubuntu-deploy](https://lhy.kr/ec2-ubuntu-deploy)  
파포푸 블로그: [http://paphopu.tistory.com/37](http://paphopu.tistory.com/37)  
불곰 블로그: [http://brownbears.tistory.com/16](http://brownbears.tistory.com/16)  
uWSGI 공식 문서: [http://uwsgi-docs.readthedocs.io/en/latest/Options.html](http://uwsgi-docs.readthedocs.io/en/latest/Options.html)
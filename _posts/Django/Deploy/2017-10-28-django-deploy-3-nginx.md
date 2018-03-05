---
layout: post
title: '[Deploy] Django 프로젝트 배포하기 - 3. Nginx'
subtitle: Attaching Nginx Web Server
comments: true
category: Django
category: Django
tags:
  - Django
  - Nginx
  - Deploy
---



지금까지 구축한 구조는 아래와 같다.

```
사용자 <-> uWSGI <-> Django
```

사용자가 보낸 http 요청을 uWSGI가 받아 장고에 넘겨주고 장고는 요청을 처리하여 적절한 응답을 uWSGI로 보내면 uWSGI가 다시 사용자에게 응답을 돌려주는 구조이다.  
하지만 보통은 사용자의 브라우저가 직접 uWSGI에 요청을 보내지 않는다. 이 요청을 받는 역할을 하는 것이 웹서버이다. 지금부터 웹서버 `Nginx` 를 연동시켜 다음과 같은 스택 구조를 최종적으로 구성할 것이다.

```
사용자 <-> Nginx 웹서버 <-> uWSGI <-> Django
```

- - -

## Nginx 설치 및 설정

> #### 웹 서버
> 
> 웹 서버(Web Server)는 HTTP를 통해 웹 브라우저에서 요청하는 HTML 문서나 오브젝트(이미지 파일 등)을 전송해주는 서비스 프로그램을 말한다.  
> 웹 서버의 주된 기능은 웹 페이지를 클라이언트로 전달하는 것이다. 주로 그림, CSS, 자바스크립트를 포함한 HTML 문서가 클라이언트로 전달된다.  
> 주된 기능은 콘텐츠를 제공하는 것이지만 클라이언트로부터 콘텐츠를 전달 받는 것도 웹 서버의 기능에 속한다. 이러한 기능은 파일 업로드를 포함하여 클라이언트에서 제출한 웹 폼을 수신하기 위해 사용된다.  
> 출처: [위키피디아](https://ko.wikipedia.org/wiki/%EC%9B%B9_%EC%84%9C%EB%B2%84)

`Nginx` 는 성능에 중점을 둔 차세대 웹 서버 소프트웨어이다.  

- - -

#### Nginx 설치

AWS 서버에 접속해서 Nginx를 설치한다.

```
# PPA 추가를 위한 필요 패키지
sudo apt-get install software-properties-common python-software-properties

# nginx 안정화 최신버전 PPA 추가
sudo add-apt-repository ppa:nginx/stable

# PPA 저장소 업데이트
sudo apt-get update

# nginx 설치
sudo apt-get install nginx
```

우분투 소프트웨어 센터는 항상 최신 버전의 패키지를 제공하는 것은 아니다. 그렇기 때문에 안정성보다는 최신 버전을 사용하는 것이 중요한 경우에는 `PPA(Personal Package Archive)` 를 통해 패키지를 다운로드 받을 수 있다.  

설치를 완료하고 나면 버전확인을 해서 잘 설치되었는지 확인한다.

```
nginx -v
```
```
nginx version: nginx/1.12.1
```

- - -

#### Nginx 환경 설정

- - -

##### 유저 설정

배포에 관한 작업은 `deploy` 유저가 담당하므로 `Nginx` 의 유저를 `deploy` 로 바꿔준다.  
`Nginx` 관련 설정은 `/etc/nginx/nginx.conf` 에서 관리한다.

```
sudo vi /etc/nginx/nginx.conf
```

파일의 첫 줄 `user www-data;` 를 `user deploy;` 로 수정해준다.

```
# nginx.conf

user deploy;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;

events {
        worker_connections 768;
        # multi_accept on;
}

http {
    .
    .
    .
```

- - -

##### Nginx 설정 파일 생성 및 연결

이제 로컬 서버로 빠져나가서 장고 프로젝트 폴더로 이동한다.  
uWSGI 설정을 저장했던 `.config` 폴더에 `nginx` 폴더를 새로 만들고 그 아래에 `mysite.conf` 파일을 생성한다.  

```
.config
├── nginx
│   └── mysite.conf
└── uwsgi
    └── mysite.ini
```

`mysite.conf` 파일을 열어 아래와 같이 작성한다.

```nginx
server {
    listen 80;
    server_name *.compute.amazonaws.com;
    charset utf-8;
    client_max_body_size 128M;

    location / {
        uwsgi_pass  unix:///tmp/mysite.sock;
        include     uwsgi_params;
    }
}
```

중요한 부분만 간단히 설명하면...

- `listen 80`: 80번 포트로 오는 요청을 받겠다는 뜻이다.
- `server_name`: `.compute.amazonaws.com` 로 끝나는 주소로 들어오는 요청을 받겠다는 뜻이다.
- `location /`: `.compute.amazonaws.com/` 의 주소로 오는 요청을 `tmp/mysite.sock` 이라는 파일에 담아 `uWSGI` 에 넘긴다는 뜻이다.


작성이 끝나면 `scp` 로 장고 프로젝트 폴더를 서버에 업로드한다.  

```
scp -i ~/.ssh/EC2-Che1.pem -r EC2_Deploy_Project ubuntu@ec2-13-124-186-240.ap-northeast-2.compute.amazonaws.com:/srv/
```

`ssh` 로 서버에 접속한 다음 아래의 명령을 입력해서 장고 프로젝트 폴더 내의 `mysite.conf` 파일을  
`/etc/nginx/sites-available/` 경로에 복사해준다.  

```
sudo cp -f /srv/EC2_Deploy_Project/.config/nginx/mysite.conf /etc/nginx/sites-available/mysite.conf
```

```
sites-available
├── default
└── mysite.conf
```

이제 다음 명령을 입력하여 `sites-available` 에 있는 설정파일을 `sites-enabled` 폴더에 링크해준다.  
```
sudo ln -sf /etc/nginx/sites-available/mysite.conf /etc/nginx/sites-enabled/mysite.conf
```

```
sites-enabled
├── default -> /etc/nginx/sites-available/default
└── mysite.conf -> /etc/nginx/sites-available/mysite.conf
```

`sites-enabled` 폴더의 `default` 링크는 삭제해준다.

```
sudo rm /etc/nginx/sites-enabled/default
```
```
sites-enabled
└── mysite.conf -> /etc/nginx/sites-available/mysite.conf
```

- - -

## uWSGI 설정

Nginx를 설치했으니 uWSGI를 Nginx와 통신하도록 설정해준다.

- - -

#### uWSGI 백그라운드 실행

Nginx는 기본적으로 백그라운드에서 실행되도록 되어있다. 그렇지만 uWSGI는 서버에 접속할 때 마다 직접 실행을 해주어야한다.  
리눅스에서 관리하는 `service` 파일을 만들어 서버가 실행될 때 자동으로 uWSGI를 백그라운드에 실행시켜주도록 하자.  

로컬에서 `/장고 프로젝트 폴더/.config/uwsgi/` 에 `uwsgi.service` 파일을 생성한다.  

```
.config
├── nginx
│   └── mysite.conf
└── uwsgi
    ├── uwsgi.service
    └── mysite.ini
```

`uwsgi.service` 파일안에 아래와 같이 작성한다.

```
[Unit]
Description=uWSGI service
After=syslog.target

[Service]
ExecStart=/home/ubuntu/.pyenv/versions/uwsgi-env/bin/uwsgi -i /srv/ec2_deploy_project/.config/uwsgi/mysite.ini

Restart=always
KillSignal=SIGQUIT
Type=notify
StandardError=syslog
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```

`scp` 를 통해 AWS 서버에 전송해준다.

AWS 서버에 접속해서 `uwsgi.service` 파일을 `/etc/systemd/system/` 에 하드링크를 걸어준다.

```
sudo ln -f /srv/EC2_Deploy_Project/.config/uwsgi/uwsgi.service /etc/systemd/system/uwsgi.service
```

`systemd` 는 리눅스에서 프로세스들을 관리하는 init 시스템이며 systemd 의 `d` 는 `데몬(daemon)` 을 의미한다.

> ##### 데몬
>
> **데몬 (Daemon)**은 컴퓨터 시스템의 운영에 관련된 작업을 후선(background) 상태로 동작하면서 실행하는 프로그램이다. 처리해야 할 작업 조건이 발생하면 자동으로 작동하여 필요한 작업을 실행한다. 예를 들면, 인터넷 웹 서비스를 제공하는 주 컴퓨터 시스템에서 웹 서버는 후선 상태로 동작하고 있다가 통신망상의 웹 브라우저로부터 자료 요청이 있으면 작업을 실행한다.  
> 출처: [네이버 지식백과](http://terms.naver.com/entry.nhn?docId=1611073&cid=50372&categoryId=50372)

`uwsgi.service` 파일을 `/etc/systemd/system/` 에 넣어 데몬으로 등록하면 서버가 시작할 때 자동으로 백그라운드에서 실행되도록 할 수 있다.  

파일을 연결해준 뒤 아래 명령을 실행해서 데몬을 리로드 해준다.

```
sudo systemctl daemon-reload
```

그 다음 아래 명령어로 uwsgi 데몬을 활성화 해준다.

```
sudo systemctl enable uwsgi
```

이제 서버에 접속하기만 해도 uwsgi와 Nginx가 백그라운드에서 실행된다.  
아래 명령을 통해 백그라운드에서 실행중인 프로그램을 확인할 수 있다.

```
sudo systemctl | grep nginx
```
```
nginx.service loaded active running A high performance web server and a reverse proxy server
```
```
sudo systemctl | grep uwsgi
```
```
uwsgi.service loaded active running uWSGI service
```

- - -

#### 소켓 통신 설정

로컬에서 `mysite.ini` 파일을 열어 `http = :8080` 을 삭제하고 그 부분에 아래와 같이 추가한다.  
```ini
# mysite.ini

socket = /tmp/mysite.sock
chmod-socket = 666
chown-socket = deploy:deploy
```

uWSGI가 http 요청을 받는 대신, `/tmp/mysite.sock` 파일을 통해 요청을 받도록 소켓 통신을 설정해주는 것이다.  

아까전에 작성했던 Nginx 설정 파일 `mysite.conf` 를 열어보면 아래와 같은 항목을 볼 수 있다.

```conf
# mysite.conf

...
    location / {
        uwsgi_pass  unix:///tmp/mysite.sock;
        include     uwsgi_params;
    }
```

여기서 `location /` 는 루트 URL로 들어오는 요청을 뜻하며, 이 요청들을 `tmp/mysite.sock` 파일을 통해 uWSGI로 넘겨준다. 이 소켓 파일을 uWSGI에서 받아 처리하는 것이다.  

수정한 파일은 `scp` 를 통해 AWS 서버에 올려준다.  

올리고 나면 서버에서 데몬 리로드로 다시 불러와주고, Nginx와 uWSGI를 재부팅해준다.

```
sudo systemctl daemon-reload
sudo systemctl restart nginx uwsgi
```

- - -

## AWS 서버 설정

`mysite.conf` 파일을 보면 아래의 항목을 볼 수 있다.

```conf
# mysite.conf

server {
    listen 80;
    server_name *.compute.amazonaws.com;
.
.
.
```

`listen 80` 은 요청을 80번 포트를 통해 받도록 설정하는 것이고, `server_name` 의 `*.compute.amazonaws.com` 는 서버의 URL 주소를 말한다.  
80번 포트는 웹 브라우저에서 기본적으로 요청을 보내는 포트이다. 아직 AWS 서버의 보안 그룹에 등록되어 있지 않기 때문에 80번 포트를 등록시켜주자.  

<img width="800px" src="/img/AWS_deploy/inbound_80.png">

- - -

설정이 끝났으므로 브라우저에서 접속해보자.

```
ec2-13-124-186-240.ap-northeast-2.compute.amazonaws.com
```

`It worked` 라고 쓰인 페이지가 나타난다면 정상적으로 작동하는 것이다.

이제 아래와 같은 스택 구조로 사용자 요청을 처리한다.

```
사용자 <-포트:80-> Nginx <-tmp/mysite.sock-> uWSGI <-> Django
```

만약 에러가 난다면 아래의 명령으로 에러 로그를 확인해서 문제점을 찾을 수 있다.

```
# Nginx 에러 로그
cat /var/log/nginx/error.log

# uWSGI 로그
cat /var/log/uwsgi/mysite/로그작성날짜.log
```

- - -

{% include /deploy/deploy-toc-base.html %}

- - -

###### Reference

이한영 강사님 블로그: [https://lhy.kr/ec2-ubuntu-deploy](https://lhy.kr/ec2-ubuntu-deploy)  
Webdir 블로그: [http://webdir.tistory.com/197](http://webdir.tistory.com/197)  
uWSGI 공식 문서: [http://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html](http://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html)  
위키피디아 systemd: [https://ko.wikipedia.org/wiki/Systemd](https://ko.wikipedia.org/wiki/Systemd)  
양민스쿨 블로그: [http://threestory.tistory.com/30](http://threestory.tistory.com/30)

---
layout: post
title: '음악 공동 프로듀싱 플랫폼 서비스 - SoundHub'
category: Django
excerpt:  SoundHub 에 대한 설명
project: true
tags:
  - SoundHub
  - Project
---

# SoundHub

음악 공동 프로듀싱 플랫폼 서비스 SoundHub 입니다.

`주소`: https://soundhub.che1.co.kr

SoundHub 는 여러 사람들이 자신이 직접 녹음한 음원을 업로드하여 서로 공유할 수 있는 음악 커뮤니티 사이트입니다.

- - -

## 어플리케이션

`SoundHub` 는 Django 웹 프레임워크를 사용해 만들어진 어플리케이션으로, `Python 3.6.3`, `Django 1.11` 을 사용하였습니다.

- - -

## 배포

```
soundhub.che1.co.kr <-> Route 53 <-> ELB Port:443 <-> Auto Scaling Group[EC2 Port:80 [NginX Port:80 <-> Docker[NginX <-> uWSGI <-> Django]]] <-> RDS(PostgreSQL) & S3
```

SoundHub는 어플리케이션의 모든 구성이 하나로 엮여있는 `Monolithic architecture` 구조로 만들어졌습니다.   

처음 만드는 프로젝트인데다가 아직 어플리케이션의 규모가 크지 않기 때문에 Monolithic architecture 구조로 만들었지만, 추후 어플리케이션의 규모가 커져 유지 보수에 어려움이 생기기 시작하면 `MSA` 구조로 변경하는 것이 가능한지 한 번 검토해볼 예정입니다.  

AWS에서 제공하는 PaaS 인 `Elastic Beanstalk` 을 사용하여 배포하였습니다.

- - -

### Route 53

Amazon 에서 제공하는 `DNS` 서비스인 `Route 53` 을 통해서 `soundhub.che1.co.kr` 의 주소로 오는 요청을 웹 어플리케이션이 배포된 서버에 보내줍니다.  
`Amazon Certificate Manager` 를 통해 `SSL/TLS 인증서` 를 발급받아 적용하여 보안이 강화된 `HTTPS` 요청을 사용하여 통신하도록 하였습니다.

- - -

### Elastic Beanstalk

SoundHub 의 배포는 `AWS Elastic Beanstalk` 을 사용하여 이루어집니다.  

AWS EB 는 배포와 관련된 다양한 편의 기능을 자동으로 구성해주어 사용자가 어플리케이션 관리에만 집중할 수 있도록 하는 `PaaS` 에 가까운 서비스입니다.  

AWS EB 는 EC2 클라우드 서버와 어플리케이션에 가해지는 부하의 크기에 따라 EC2의 수를 조절해주는 `Auto Scaling` 서비스와 여러 개의 EC2 인스턴스들에 적절히 요청을 분산시켜주는 `Elastic Load Balancer` 서비스를 자동으로 설정해줍니다.  

EB에 의해 생성되는 AWS EC2 인스턴스의 내부는 어떤 컨테이너 유형을 사용하는지에 따라 다르게 구성됩니다.  
예를 들어 파이썬 3.6 버전을 사용하는 구성의 컨테이너를 선택한다면 다음과 같은 구성의 EC2가 생성됩니다.  
- 운영 체제: Amazon Linux AMI 2017.09
- 언어: Python 3.6.2
- 패키지 관리자: pip 9.0.1
- 패키저: setuptools 28.8.0
- 프록시 서버: Apache 2.4.27 with mod_wsgi 3.5

만약 도커를 사용한다면 도커 컨테이너를 사용하여 EC2 를 구성할 수 있습니다.  

SoundHub 는 도커 컨테이너를 사용하는 방식으로 배포 되었으며, 그 중에서도 하나의 컨테이너를 사용하는 단일 컨테이너 도커 환경을 사용하였습니다.  

도커 컨테이너를 사용하는 방식으로 EC2 를 생성하는 경우 다음과 같은 구성의 EC2가 생성됩니다.  
- 운영 체제: Amazon Linux AMI 2017.09
- 도커 버전: 17.12.0-ce
- 프록시 서버: NginX 1.12.1

따라서 Load Balancer 가 요청을 받아서 알맞는 EC2 에 적절히 요청을 분배하여 넘겨주면 EC2 의 NginX 프록시 서버가 요청을 받아 EC2에서 실행되고 있는 도커 컨테이너 내부로 보냅니다.  
이 요청을 컨테이너 내부의 NginX 가 받아서 uWSGI 에 넘겨주고 uWSGI 는 이를 다시 Django 어플리케이션으로 전달하여 적절한 응답을 리턴하게 됩니다.  

SSL/TLS 인증서를 설치하였으므로 Load Balancer 가 HTTPS 요청 표준 포트인 443 포트로 요청을 받을 수 있도록 443번 포트를 Load Balancer 의 보안그룹에 추가해 주었습니다.
- - -

### Docker

Soundhub 는 Docker 이미지로 생성된 컨테이너에서 실행됩니다.  
하나의 도커 내에 웹서버와 WSGI, 장고 어플리케이션 등 모든 구성이 다 포함되어 있는 구조입니다.  
웹 서버로는 Nginx 를, WSGI 로는 uWSGI 를 각각 사용합니다.  
기본적으로 도커는 하나의 서비스만을 실행하므로 여러 개의 서비스를 동시에 실행하기 위해서 `Supervisord` 를 사용하였습니다.  
어플리케이션이 들어있는 컨테이너를 EC2 내에서 실행하고 80번 포트를 열어(EXPOSE) EC2 의 NginX 프록시 서버와 통신합니다.  



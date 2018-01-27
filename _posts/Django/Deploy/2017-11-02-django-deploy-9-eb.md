---
layout: post
title: '[Deploy] Django 프로젝트 배포하기 - 9. Elastic Beanstalk'
subtitle: Deploying With Elastic Beanstalk
comments: true
category: Django
tags:
  - Django
  - AWS
  - Elasticbeanstalk
  - Deploy
---

지금까지 배운 것들을 보면 다음과 같다.

- AWS EC2 가상 컴퓨터에 프로젝트를 올려서 모든 사람들이 볼 수 있도록 하기
- RDS 서버에 데이터베이스를 두고 별도로 관리하기
- S3 서버에 파일들을 올려두고 별도로 관리하기
- Docker로 미리 설정해둔 환경으로 배포하기

우리는 사실 웹 어플리케이션을 만드는데 집중해야 하는데 어째 서버 구축하고 환경 설정하는데 더 많은 노력이 드는 것 같다.  
슬슬 웹 어플리케이션 개발자인지 서버 기술자인지 헷갈리기 시작하면서 정체성에 혼란이 온다.  
그래서 웹 어플리케이션 개발자 답게 서버 구축에 쏟아 붓는 시간을 줄이고 웹 어플리케이션 개발에 집중할 수 있도록 도와주는 `Elastic Beanstalk` 이라는 것이 나왔다.

이번 포스트에서는 `Elastic Beanstalk` 을 이용해서 프로젝트를 간편하게 배포하는 방법을 알아본다.  
- - -

## Elastic Beanstalk

`Beanstalk` 은 콩나무 줄기를 뜻한다. 특히 잭과 콩나무에 나오는 그 콩나무를 말하는 것 같다.  

<img width="200px" src="/img/AWS_deploy/beanstalk.png" style="box-shadow:none;"> 

잭과 콩나무에서는 콩나무 씨앗을 심으면 저절로 자라서 거대한 콩나무가 된다.  

Elastic Beanstalk도 콩나무처럼 실행하면 저절로 자라서 배포에 필요한 모든 환경을 구축해준다.  
게다가 그냥 콩나무도 아니고 무려 `탄력적 (Elastic)` 콩나무란다.  
왜 탄력적이냐면 이 콩나무는 필요에 따라 크기가 변하기도 하고 모양이 변하기도 한다.  

서버를 세팅할 때 우리가 해주었던 `Nginx`, `uWSGI`, `Django` 및 여러가지 Python 패키지 들의 설치를 간편하게 Docker로 묶어주었다면 Elastic Beanstalk은 이 Docker를 실행할 `EC2`, 데이터베이스를 운영할 `RDS`, 파일을 저장할 `S3` 등을 모두 알아서 연결해준다. 
여기에 `Elastic Load Balancing`, `Auto Scaling` 등의 서비스까지 설정해주어서 트래픽의 크기에 따라 서버의 크기도 적절하게 늘렸다 줄였다 해주기까지 한다.  
그래서 탄력적 콩나무라고 이름 지은 것 같다. 알고보니 잘 지은 이름이었다.  

<iframe width="560" height="315" src="https://www.youtube.com/embed/SrwxAScdyT0" frameborder="0" allowfullscreen></iframe>

간단한 소개영상을 감상한 다음 직접 탄력적 콩나무를 심어보자.  

- - -

## Elastic Beanstalk 시작하기

- - -

#### Elastic Beanstalk 유저 생성

가장 먼저 할일은 Elastic Beanstalk 전용 유저를 새로 만드는 것이다.  

만드는 방법은 AWS 콘솔에서 `IAM` 으로 `EC2` 유저를 만들었을 때와 동일하다.  

단, 권한 설정에서 `AWSElasticBeanstalkFullAccess` 를 선택해준다.  

<img width="600px" src="/img/AWS_deploy/EB/ebfull.png">  

이번에도 유저를 만들고나면 생성되는 `Access_Key_ID` 와 `Access_Secret_Key` 를 잘 저장해놓자.  

`~/.aws/` 경로의 `credentials` 파일에 추가해주는 것이 좋다.  

```
vim ~/.aws/credentials
```

credentials 파일에 아래와 같이 추가해준다.

```
[eb-user]
aws_access_key_id = AKIAJZ2BWJXHGPIYC26Q
aws_secret_access_key = *********************************
```

`[]` 안의 내용은 해당 유저의 별명이 된다.  

- - -

#### awsebcli 설치

이제 배포하려는 장고 프로젝트 폴더로 이동해서 pyenv 가상환경에 `awsebcli` 를 설치해준다.

```
pip install awsebcli
```

awsebcli는 Python용 Elastic Beanstalk Command Line Interface 이다.  
터미널에서 Elastic Beanstalk 관련 설정을 조작할 수 있게 해주는 패키지이다.  

다음 명령을 입력하면 새로운 Elastic Beanstalk 환경이 시작된다.

```
eb init --profile 유저명
```

유저명에는 아까 credentials에 입력했던 유저 별명을 입력하면 된다.  

```
eb init --profile eb-user
```

위 명령을 입력하면 먼저 아래의 질문이 나타난다.

```
Note: Elastic Beanstalk now supports AWS CodeCommit; a fully-managed source control service. To learn more, see Docs: https://aws.amazon.com/codecommit/
Do you wish to continue with CodeCommit? (y/N) (default is n): 
```

Elastic Beanstalk이 이제 `AWS CodeCommit` 이라는 서비스를 지원하는데 이 서비스를 사용할 것이냐는 질문이다.  
나중에 AWS CodeCommit에 대해 배우게 되면 써보는 것으로 하고 지금은 `N` 를 입력해서 넘어가자.  

## To Be Continued...

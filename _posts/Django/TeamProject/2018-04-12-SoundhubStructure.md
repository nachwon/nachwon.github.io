---
layout: post
title: '[SoundHub] SoundHub의 구조'
category: Django
excerpt:  SoundHub가 어떤 구조로 배포되어 있는지 설명한 글
project: true
tags:
  - SoundHub
  - Project
---

## 어플리케이션

SoundHub 는 Django 웹 프레임워크를 사용해 만들어진 어플리케이션으로,`Python 3.6.3`, `Django 1.11` 을 사용하였습니다.

- - -

## 배포

AWS의 클라우드 서버인 EC2 에 Django 어플리케이션을 구동시키는 Docker 이미지를 실행하는 방식으로 프로젝트를 배포하였습니다.  

사용중인 AWS EC2 인스턴스는 Amazon Linux AMI 2017.09 버전 입니다.

SoundHub는 어플리케이션의 모든 구성이 하나로 엮여있는 Monolithic architecture 구조로 만들어졌습니다.  
이에 따라 어플리케이션의 모든 구성이 하나의 도커 이미지에서 실행되는 단일 컨테이너 구성으로 배포하였습니다.  

아직 어플리케이션의 규모가 크지 않기 때문에 MSA 구조로 Monolithic architecture 구조로 만들었지만, 추후 어플리케이션의 규모가 커져 유지 보수에 어려움이 생기기 시작하면 MSA 구조로 변경할 계획입니다.  

- - -

## Docker

Soundhub 는 Docker 컨테이너를 통해 실행됩니다.  
하나의 도커 내에 웹서버와 WSGI, 장고 어플리케이션, Celery, RabbitMQ 서버 등 모든 구성이 다 포함되어 있는 구조입니다.  
웹 서버로는 Nginx 를, WSGI 로는 uWSGI 를 각각 사용합니다.




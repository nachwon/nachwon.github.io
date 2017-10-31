---
layout: post
title: '[Deploy] AWS 서버에 Django 프로젝트 띄우기 - 7. S3 Storages'
subtitle: Storing Static Files in S3 Storages
category: Django
author: Che1
---

{% include /deploy/deploy-toc-base.html %}

- - -

이번 포스트에서는 장고 프로젝트에 필요한 스태틱 파일 및 미디어 파일들을 Amazon S3라는 별도의 저장소에 저장하여 관리하는 방법에 대해 알아본다.

- - -

`Amazon S3` 는 아마존 웹 서비스(AWS)에서 제공하는 클라우드 스토리지 서비스이다.


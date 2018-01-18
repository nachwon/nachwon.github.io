---
layout: post
title: '[TDD Tutorial] 사전 준비'
category: Django
subtitle: Prerequisites and Assumptions
tags:
  - TDD
  - Tutorial
---



TDD Tutorial 포스트에서는 테스트 주도 개발 방법론을 간단한 장고 어플리케이션을 하나 만들어보면서 배워 볼 것이다. 주로 `Test-Driven Development with Python` 의 내용을 요약 번역하면서 내가 이해한 대로 부가설명을 조금씩 덧붙이는 식으로 작성할 것이다. 내용 중 장고에 대한 설명은 대부분 생략하였다. 장고에 대한 튜토리얼은 따로 포스트를 작성해두었으니 장고에 대해 잘 모른다면 장고 튜토리얼을 먼저 읽어보고 이번 튜토리얼을 진행하는 것을 권장한다.

- - -

### Test Driven Development with Django 준비 사항

- Python 버전 3.4 이상

- 기본적인 `HTML` 지식

- 약간의 `Javascript` 지식

- 기본적인 `Vi` 텍스트 에디터 사용법


- 필요한 소프트웨어
    - 웹 브라우저: 구글 크롬 또는 파이어폭스 (이 튜토리얼에서는 크롬을 쓴다.)
    - Git
    - pip Python 패키지 매니저


- 필요한 Python 패키지
    - Django
    ```
    pip install django
    ```

    - Selenium
    ```
    pip install --upgrade selenium
    ```

- - -

{% include /tdd/tdd-tutorial-toc-base.html %}

- - -

###### Reference

Test-Driven Development with Python, Harry Percival: [http://chimera.labs.oreilly.com/books/1234000000754/pr02.html](http://chimera.labs.oreilly.com/books/1234000000754/pr02.html)
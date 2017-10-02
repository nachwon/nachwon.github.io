---
layout: post
title: '[Django Tutorial] Blog 만들기 - 1. 환경설정'
category: Django
author: Che1
---
<div class="navigation-menu">
    <h5>[Django Tutorial] Blog 만들기</h5>
    <ol>
        <li><a href="/django/2017/09/28/django-1-setting.html">환경설정</a></li>
        <li><a href="/django/2017/09/30/django-2-start.html">프로젝트 시작</a></li>
        <li><a href="/django/2017/09/30/django-3-database.html">데이터베이스</a></li>
        <li></li>
    </ol>
</div>

- - -

Python으로 만들어진 웹 프레임워크인 `Django` 를 가지고 간단한 블로그를 하나 만들어보자.  
이 튜토리얼은 아래의 환경에서 작성되었다.
```
Ubuntu 16.04 LTS
Pycharm Community Edition 2017.2.3
```
- - -

#### Python 가상환경 설정
프로젝트를 시작할 폴더를 하나 만들고 그 폴더에 `pyenv` 를 활용하여 Python 가상환경을 설정해준다.  

##### virtualenv 생성
먼저 콘솔에서 `pyenv virtualenv 파이썬버전 가상환경이름` 의 순서로 입력하여 가상환경 하나를 생성한다.
```
pyenv virtualenv 3.6.2 django_assignment
```

##### virtualenv 적용
가상환경을 적용할 폴더를 생성한 뒤 `pyenv local 가상환경이름` 의 순서로 입력하여 가상환경을 적용한다.
```
mkdir djangogirls_assignment  # 폴더 생성
```

```
pyenv local django_assignment
```

아래와 같이 콘솔 입력줄의 제일 앞에 가상환경의 이름이 나타나면 적용이 완료된 것이다.
```re
(django_assignment) ~/Projects/Django/djangogirls_assignment >
```

- - -

#### 패키지 설치
`Django` 를 포함하여 프로젝트에 필요한 패키지들을 설치한다. 사실 지금 당장은 `Django` 만 설치하면 된다.
##### django 설치
아래와 같이 입력하여 `Django` 를 설치한다.
```
pip install django
```
##### 패키지 세팅 사항 저장하기
필요한 패키지를 설치한 후 아래와 같이 설치된 패키지 목록을 확인할 수 있다.
```
pip freeze
```
```re
Django==1.11.5
pytz==2017.2
```
이를 `requirements.txt` 에 저장해둔다.
```
pip freeze > requirements.txt
```

이 `requirements.txt` 에 저장된 패키지들을 그대로 다시 설치할 수 있다.
```
pip install -r requirements.txt
```

또, 따로 `README.md` 파일을 생성하여 프로젝트에 사용된 `Python` 버전을 명시해준다.

```
vim README.md
```
```
python-version: 3.6.2
```
- - -

#### git 설정
프로젝트 진행사항을 관리하기 위해서 `git` 을 활용한다.

##### 로컬저장소 초기화
프로젝트 폴더에서 아래와 같이 입력하여 `git` 로컬 저장소를 초기화 한다.
```
git init
```
입력창에 `(master)` 라고 붙으면 완료된 것이다.
```re
(django_assignment) ~/Projects/Django/djangogirls_assignment (master) >
```
##### 리모트저장소 설정

`github` 에서 저장소를 하나 만든 뒤, `git remote add 리모트저장소이름 저장소주소.git` 을 입력하여 리모트저장소와 연결해준다.
```
git remote add origin https://github.com/nachwon/Djangogirls_assignment.git
```
##### .gitignore 파일 만들기
`staging area` 에 파일을 추가할 때 추가되지 말아야 할 파일들을 미리 지정해주는 `.gitignore` 파일을 만들어 준다.
```
vim .gitignore
```

[https://www.gitignore.io/](https://www.gitignore.io/)로 가서 `운영체제`, `사용하는 IDE`, `프로그래밍 언어` 등 자신의 개발환경을 하나씩 입력해준다.  
예를 들면, `Linux`, `Python`, `Django`, `Pycharm` 등...  
그 후 `create` 를 클릭하여 나타난 결과를 `.gitignore` 파일에 복사한다.  
이어서 파일의 가장 아래에 다음과 같이 추가해준 뒤 저장한다.
```
# Custom
.idea
```

지금까지 과정이 끝나면 프로젝트 폴더는 아래와 같은 상태가 된다.
```
.git
.gitignore
.idea
.python-version
README.md
requirements.txt
```
##### github 저장소에 push하기
이 상태로 `commit` 을 해준다.
```
git add -A
```
```
git commit -m 'initial commit'
```

그런 다음 온라인 `github` 저장소에 올린다.

```
git push origin master
```

이제 `Django` 를 시작할 준비를 끝마쳤다.
- - -

###### Reference

이한영 강사님 강의자료  
[Djangogirls_Tutorial](https://tutorial.djangogirls.org/ko/)
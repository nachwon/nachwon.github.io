---
layout: post
title: pyenv 설치하기(Ubuntu 환경)
excerpt: Python 버전 관리 툴인 pyenv 설치하기.
tags:
  - Python
  - Pyenv
  - Linux
  - How to install
category: Python
---

# pyenv

- - -

#### pyenv란?

**Python 버전 관리 프로그램**  
프로젝트에 따라 서로 다른 버전의 Python이 필요한 경우 각각의 프로젝트에 다른 버전의 Python 개발 환경을 적용할 수 있게 해주는 프로그램.  
github : <a href="https://github.com/pyenv/pyenv">https://github.com/pyenv/pyenv</a>

- - -

#### pyenv 설치

shell에서 아래의 커맨드 입력
```
curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
```

- - -

#### pyenv 환경변수 설정

shell에서 바로 pyenv 명령어를 실행할 수 있도록 환경변수를 설정해준다.


bash-shell인 경우:
```
vi ~/.bashrc
```

z-shell인 경우:
```
vi ~/.zshrc
```

파일의 가장 아랫부분에 아래의 내용 추가:
```
export PATH="~/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

- - -

#### pyenv 필수 패키지 설치

pyenv를 이용하여 python을 설치하기 위해서는 필수 패키지 몇가지가 필요하다. 그냥 사용할 경우 오류가 날 수 있다.  
shell에서 아래 명령어를 실행하여 필수 패키지를 설치한다.

```
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev
```

- - -

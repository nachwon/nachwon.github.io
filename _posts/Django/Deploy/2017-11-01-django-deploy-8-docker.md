---
layout: post
title: '[Deploy] Django 프로젝트 배포하기 - 8. Docker'
subtitle: Setting Up A Server Using Docker
comments: true
category: Django
tags:
  - Django
  - Docker
  - Deploy
---

이번 포스트는 Docker에 대해 알아보고 Docker를 이용하여 서버를 구축하는 방법을 알아본다.

- - -

## Docker 란?

> #### Docker
> 도커(Docker)는 리눅스의 응용 프로그램들을 소프트웨어 컨테이너 안에 배치시키는 일을 자동화하는 오픈 소스 프로젝트이다. 도커 웹 페이지의 기능을 인용하면 다음과 같다:  
> 
> 도커 컨테이너는 일종의 소프트웨어를 소프트웨어의 실행에 필요한 모든 것을 포함하는 완전한 파일 시스템 안에 감싼다. 여기에는 코드, 런타임, 시스템 도구, 시스템 라이브러리 등 서버에 설치되는 무엇이든 아우른다. 이는 실행 중인 환경에 관계 없이 언제나 동일하게 실행될 것을 보증한다.  
> 출처: [위키피디아](https://ko.wikipedia.org/wiki/%EB%8F%84%EC%BB%A4_(%EC%86%8C%ED%94%84%ED%8A%B8%EC%9B%A8%EC%96%B4))

- - -

## 컨테이너와 이미지

`Docker` 는 **컨테이너 기반의 오픈소스 가상화 플랫폼** 이다.  

Docker는 **`컨테이너`**라는 독립된 가상 공간에 운영체제와 응용 프로그램들을 설치하여 어떤 외부 환경에서도 컨테이너 안에서는 동일한 환경으로 프로세스들이 실행되도록 한다.  

<img width="500px" src="/img/AWS_deploy/docker/docker-container.png" style="box-shadow:none;">

어떤 프로그램이든 컨테이너 안에 설치해놓을 수 있으며 미리 설정한 컨테이너를 서버에서 실행시키기만 하면 환경 설정이 끝나기 때문에 배포와 관리가 매우 간편해진다.  

컨테이너는 **`이미지`** 를 통해 생성된다. 이미지는 컨테이너를 구성할 파일과 설정값 등을 포함하고 있는 일종의 클래스같은 개념이다. 클래스로 인스턴스를 만들어내듯이 이미지로 컨테이너들을 만들어 사용하는 것이다. 당연히 인스턴스를 삭제하거나 변경한다고 해서 클래스가 바뀌지 않듯이 컨테이너를 삭제하거나 변경해도 이미지는 변하지 않는다.  

<img width="700px" src="/img/AWS_deploy/docker/docker-image.png" style="box-shadow:none;">

이미지를 미리 만들어놓기만 하면 언제든지 해당 이미지에 구성된 환경과 동일한 환경을 가진 컨테이너들을 만들어내서 운영할 수 있게 된다.  

Docker 이미지는 `Docker hub` 이라는 플랫폼 서비스에서 사용자끼리 서로 공유할 수 있다.

- - -

## Docker 설치하기

이제 Docker를 설치해서 사용해보자.  
아래 명령으로 Docker를 설치한다.

```
curl -s https://get.docker.com/ | sudo sh
```

**리눅스 운영체제**에서 설치하는 경우 docker는 sudo 권한을 필요로하기 때문에 항상 `sudo docker ...` 로 실행해야한다.  
번거로우므로 아래 명령을 통해 docker를 항상 sudo 권한으로 실행하도록 한다.

```
# 현재 접속중인 사용자에게 권한 주기
sudo usermod -aG docker $USER

# 지정한 유저에 권한 주기
sudo usermod -aG docker 유저명
```

권한 적용은 다음 로그인한 시점부터 적용된다.  

설치를 마쳤으면 아래 명령을 통해 설치가 잘 되었는지 확인한다.

```
docker run hello-world
```

```
Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://cloud.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/engine/userguide/

```

위와 같이 설치가 잘되었다는 메세지를 받으면 된다.

- - -

## 컨테이너 실행

컨테이너를 실행하는 명령은 아래와 같다.

```
docker run [OPTIONS] IMAGE[:TAG|@DIGEST] [COMMAND] [ARG...]
```


<table class="table table-striped table-bordered">
  <thead>
    <tr>
      <th>옵션</th>
      <th>설명</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>-d</td>
      <td>detached mode 흔히 말하는 백그라운드 모드</td>
    </tr>
    <tr>
      <td>-p</td>
      <td>호스트와 컨테이너의 포트를 연결 (포워딩)</td>
    </tr>
    <tr>
      <td>-v</td>
      <td>호스트와 컨테이너의 디렉토리를 연결 (마운트)</td>
    </tr>
    <tr>
      <td>-e</td>
      <td>컨테이너 내에서 사용할 환경변수 설정</td>
    </tr>
    <tr>
      <td>–name</td>
      <td>컨테이너 이름 설정</td>
    </tr>
    <tr>
      <td>–rm</td>
      <td>프로세스 종료시 컨테이너 자동 제거</td>
    </tr>
    <tr>
      <td>-it</td>
      <td>-i와 -t를 동시에 사용한 것으로 터미널 입력을 위한 옵션</td>
    </tr>
    <tr>
      <td>–link</td>
      <td>컨테이너 연결 [컨테이너명:별칭]</td>
    </tr>
  </tbody>
</table>


아래 명령어를 입력하여 우분투 컨테이너를 생성해서 들어가보자.  

```
docker run ubuntu:16.04
```

```
Unable to find image 'ubuntu:16.04' locally
16.04: Pulling from library/ubuntu
ae79f2514705: pull complete
5ad56d5fc149: pull complete
170e558760e8: pull complete
395460e233f5: pull complete
6f01dc62e444: pull complete
Digest: sha256:506e2d5852de1d7c90d538c5332bd3cc33b9cbd26f6ca653875899c505c82687
Status: Downloaded newer image for ubuntu:16.04
```

컨테이너는 이미지를 통해 만들어지므로 먼저 로컬에서 `ubuntu:16.04` 라는 이미지를 검색한다.  
로컬에 이미지가 없으면 온라인 저장소에서 가져온다.  

<img width="500px" src="/img/AWS_deploy/docker/image-url.png" style="box-shadow:none;">

이미지는 URL 방식으로 관리되고 태그를 붙일 수 있다.  
예를 들어 `ubuntu:16.04` 는 `docker.io/library/ubuntu:16.04` 에 저장되어 있는 이미지이다.  
`docker.io/library/` 는 공통적인 부분으로 생략가능하며, `:` 뒤의 부분이 태그이다.  
따라서 위 명령은 `library/ubuntu` 라는 저장소에서 `16.04` 태그가 붙은 이미지를 가져온 다음 그 이미지를 이용해서 컨테이너를 생성하는 것이다.  

컨테이너는 프로세스이기 때문에 실행중인 프로세스가 없으면 종료된다.  
위 명령은 컨테이너를 실행만하고 아무 명령을 지정해주지 않았기 때문에 컨테이너가 알아서 종료된다.  

아래 명령을 통해 컨테이너 내의 우분투 운영체제에서 `bash` 셸을 실행해보자.

```
docker run --rm -it ubuntu:16.04 bin/bash
```

```
root@d9e034cb5947:/# 
```

위와 같이 사용자 입력을 대기하는 셸이 실행된 것을 볼 수 있다.  

지금까지 우분투 이미지를 다운받아서 컨테이너를 생성하고 실행하는 것까지 해보았다.

- - -

## 이미지 생성하기

이제부터는 다운받은 우분투 이미지에 우리가 필요한 여러가지 응용 프로그램들을 쌓아서 새로운 이미지를 생성하고 그 이미지로 컨테이너를 만들어 쓸 것이다.  

Docker는 이미지를 생성할 때 `Dockerfile` 이라는 파일을 사용한다.  
`Dockerfile` 은 Docker 자체 언어로 작성되어야한다.  
Pycharm에서는 `Docker Integration` 플러그인을 설치하면 Dockerfile 작성시 자동완성 등의 편의 기능을 제공한다.  

`Dockerfile.base` 라는 이름으로 파일을 하나 만들고 작성을 시작해보자.  
먼저 어떤 이미지를 기반으로 이미지를 생성할 것인지를 `FROM` 으로 명시해준다.  
`MAINTAINER` 에는 본인의 이메일 주소를 입력하면 된다.

```dockerfile
# Dockerfile.base

FROM        ubuntu:16.04
MAINTAINER  nachwon@naver.com
```

지금까지의 이미지는 우분투 운영체제만 있는 상태이다.  
이제 여기서부터 우리가 EC2 서버에 처음 해주었던 환경 세팅을 똑같이 해주면 된다.  
예를 들어, EC2에서는 가장 먼저 `apt-get update` 명령으로 패키지들을 업데이트 해주었다.  
그 작업을 동일하게 수행하도록 아래와 같이 작성한다.  

```dockerfile
# Dockerfile.base

FROM        ubuntu:16.04
MAINTAINER  nachwon@naver.com

RUN         apt-get -y update
```

`-y` 옵션은 설치 과정 중 사용자의 확인을 요청하는 부분에 모두 `yes` 로 대답하도록 하는 옵션이다.  
`Dockerfile` 을 통해 설치를 하는 과정에서는 응답을 직접해줄 수 없으므로 이 옵션을 추가해준 것이다.  

이 `Dockerfile` 로 이미지를 생성한다면 우분투 운영체제에 `apt-get update` 명령이 실행된 상태까지의 이미지가 생성된다.  
마치 필요한 운영체제 환경을 미리 시나리오로 짜두는 것이라고 생각하면 된다.  

위와 같은 방식으로 필요한 환경 설정, 프로그램 설치 등등을 작성해주면 된다.  
Dockerfile을 작성할 때는 컨테이너를 하나 실행해서 직접 명령을 실행해보면서 작성하는 것이 정확한 Dockerfile 작성에 도움이 된다.  
예를 들어 지금과 같은 경우는 `docker run --rm -it ubuntu:16.04 bin/bash` 명령으로 우분투 컨테이너를 하나 실행한 다음, `apt-get -y update` 명령을 실행해보고 실행되는 것이 확인되면 `Dockerfile.base` 파일에 작성하는 것이다.

그리하여 필요한 세팅을 쭉 적어보면 아래와 같이 된다.  

```dockerfile
# Dockerfile.base

FROM        ubuntu:16.04
MAINTAINER  nachwon@naver.com

# 우분투 환경 업데이트 및 기본 패키지 설치
RUN         apt-get -y update
RUN         apt-get -y dist-upgrade
RUN         apt-get install -y python-pip git vim

# pyenv
RUN         apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev
RUN         curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
ENV         PATH /root/.pyenv/bin:$PATH
RUN         pyenv install 3.6.3

# zsh
RUN         apt-get install -y zsh
RUN         wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh || true
RUN         chsh -s /usr/bin/zsh

# pyenv settings
RUN         echo 'export PATH="/root/.pyenv/bin:$PATH"' >> ~/.zshrc
RUN         echo 'eval "$(pyenv init -)"' >> ~/.zshrc
RUN         echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.zshrc

# pyenv virtualenv
RUN         pyenv virtualenv 3.6.3 app

# uWGSI install
RUN         /root/.pyenv/versions/app/bin/pip install uwsgi

# Nginx install
RUN         apt-get -y install nginx

# supervisord install
RUN         apt-get -y install supervisor
```

- - -

이제 이 Dockerfile을 가지고 이미지를 생성해보자.  
Dockerfile.base 파일이 있는 폴더로 이동한 후 아래 명령을 입력하여 이미지를 생성한다.  

```
docker build -t base -f Dockerfile.base .
```

`-t` 다음에는 생성될 이미지의 이름을 지정해주고,  
`-f` 다음에는 이미지 생성에 사용할 Dockerfile을 지정해주면 된다.
마지막의 `.` 은 이미지를 생성할 경로를 뜻한다.  

여러 응용프로그램을 설치해야하므로 오랜 시간이 걸린다.  
아래의 메세지가 뜨면 빌드가 성공적으로 끝난 것이다.

```
.
.
.
Successfully built 975e4869f7c3
Successfully tagged base:latest
```

빌드가 끝나면 완성된 이미지를 다음의 명령을 통해 이미지 목록에서 확인해볼 수 있다.

```
docker images
```

```
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
base                latest              975e4869f7c3        3 minutes ago       1.11GB
ubuntu              16.04               747cb2d60bbe        3 weeks ago         122MB
```

- - -

#### 이미지 레이어

Dockerfile을 실행하면 뜨는 로그를 살펴보자

```
Sending build context to Docker daemon  18.11MB  #1
Step 1/19 : FROM ubuntu:16.04                    #2    
 ---> 747cb2d60bbe                               #3
Step 2/19 : MAINTAINER nachwon@naver.com         #4
 ---> Running in 4fd03f3be194                    #5
 ---> feabda9f3e02                               #6
Removing intermediate container 4fd03f3be194     #7
.
.
.
Successfully built 975e4869f7c3                  #8
Successfully tagged base:latest                  #9
```

- **`#1`**: 처음 빌드를 시작하면 명령을 실행한 디렉토리의 파일들 (Build contest) 을 Docker 서버로 전송한다.  
- **`#2`**: FROM ubuntu:16.04 명령을 실행한다.
- **`#3`**: 위 명령의 실행 결과를 이미지 747cb2d60bbe 로 만든다. 이 경우에는 ubuntu:16.04 이미지를 가져오는 것이므로 우분투 이미지의 ID인 747cb2d60bbe이 그대로 표시된다.
- **`#4`**: MAINTAINER 명령을 실행한다.
- **`#5`**: 위 명령을 4fd03f3be194 라는 임시 컨테이너를 만들어 그 안에서 실행한다.
- **`#6`**: 명령의 실행 결과를 이미지 feabda9f3e02 로 저장한다.
- **`#7`**: 명령 실행을 위해 만들었던 임시 컨테이너 4fd03f3be194를 삭제한다.
- **`#8`**: 가장 마지막 명령을 실행한 결과로 생성된 이미지는 975e4869f7c3 이다. 이 이미지가 최종 결과인 base 이미지인 것이다.
- **`#9`**: base 이미지에 latest 라는 태그를 붙여준다.  

이 과정을 통해 알 수 있듯이 이미지는  

`임시 컨테이너 생성` > `다음 명령 실행` > `실행 결과를 이미지로 저장` > `임시 컨테이너 삭제` 

의 과정을 반복하여 생성된다.  

한 번의 반복으로 생성되는 이미지를 **`이미지 레이어`**라고 한다.

<img width="700px" src="/img/AWS_deploy/docker/image-layer.png" style="box-shadow:none;">

각 명령의 실행 결과는 레이어로 저장되기 때문에 이미지를 생성할 때마다 모든 설치과정을 처음부터 다시 실행할 필요가 없다.  
필요하다면 깃헙처럼 특정 시점의 레이어로 돌아가는 것도 가능하다.  
레이어 개념을 잘 알고 있다면 좀 더 최적화된 이미지를 만들 수 있을 것이다.

- - -

## 기본적인 Docker 명령어

#### `ps`: 컨테이너 목록 확인

```
docker ps [OPTIONS]
```

현재 실행중인 컨테이너 목록을 보여준다.  
명령을 실행하면 실행중인 컨테이너의 아래와 같은 정보들을 보여준다. 

- `CONTAINER ID`: 컨테이너의 ID. 어떤 컨테이너를 특정할 때 ID 값을 사용한다.
- `IMAGE`:  컨테이너 빌드에 사용된 이미지를 나타낸다.
- `COMMAND`: 현재 컨테이너 내에서 실행 중인 명령을 보여준다.
- `CREATED`: 컨테이너가 실행 시작된 시점을 보여준다.
- `STATUS`: 컨테이너 실행 상태를 보여준다.
- `PORTS`: -p 옵션으로 포트를 추가해주었다면 포트 번호를 보여준다.
- `NAMES`: 컨테이너의 이름을 보여준다.  

옵션으로는 아래와 같은 것들이 있다.  

`-a`: 종료된 컨테이너 목록까지 보여준다.

- - -

#### `rm`: 컨테이너 삭제



- - -

###### Reference

subicura 블로그: [https://subicura.com/2017/01/19/docker-guide-for-beginners-1.html](https://subicura.com/2017/01/19/docker-guide-for-beginners-1.html)  
이한영 강사님 블로그: [https://lhy.kr/eb-docker](https://lhy.kr/eb-docker)  
Docker 공식 문서: [https://docs.docker.com/](https://docs.docker.com/)
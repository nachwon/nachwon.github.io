---
layout: post
title: '[Deploy] Django 프로젝트 배포하기 - 1. AWS'
excerpt: AWS EC2에 장고 프로젝트 올리기
comments: true
category: Django
tags:
  - Django
  - AWS
  - Deploy
---

이 포스트는 **Ubuntu 16.04**에서 작성되었음.

- - -



## AWS 시작하기


> ### Amazon Web Services
> 아마존 웹 서비스(영어: Amazon Web Services; AWS)는 아마존닷컴이 제공하는 각종 원격 컴퓨팅 서비스(웹 서비스)이다.  
아마존 웹 서비스는 다른 웹 사이트나 클라이언트측 응용 프로그램에 대해 온라인 서비스를 제공하고 있다. 이러한 서비스의 상당수는 최종 사용자에 직접 공개되는 것이 아니고, 다른 개발자가 사용 가능한 기능을 제공하는 플랫폼을 제공하는 PaaS이다.  
아마존 웹 서비스의 각종 서비스는 REST 프로토콜 및 SOAP 프로토콜을 통해 접근, 이용 및 관리가 가능하다. 비용은 실제 사용량에 따라 결정되며, 일부 서비스의 경우 미리 고정된 금액을 지불하는 형태도 있다.  
> 출처: [위키피디아](https://ko.wikipedia.org/wiki/%EC%95%84%EB%A7%88%EC%A1%B4_%EC%9B%B9_%EC%84%9C%EB%B9%84%EC%8A%A4)



AWS: [https://aws.amazon.com/ko/?nc2=h_lg](https://aws.amazon.com/ko/?nc2=h_lg)

먼저 위의 사이트에서 AWS에 가입한 다음 로그인하여 관리 페이지로 접속한다.


<img width="950px" src="/img/AWS_deploy/console_main.png">

- - -
오른쪽 상단의 지역 설정 메뉴에서 `서울` 을 선택한다.

<img width="950px" src="/img/AWS_deploy/region_seoul.png">

- - -

#### 새 유저 만들기

가입한 계정은 루트계정이며 모든 권한을 다 가지고 있기 때문에 보안이 뚫릴 경우 공격자가 모든 권한을 가지는 문제가 생길 수 있다. 따라서 제한된 권한을 가지는 유저를 생성하여 그 유저로 서버를 운영하면 보안이 뚫리더라도 안전할 수 있다.

- - -

메인 화면의 서비스 검색 창에 `IAM` 이라고 입력한 뒤 나타나는 창을 클릭하여 `사용자 및 엑세스 키 관리` 메뉴로 이동한다.

<img width="600px" src="/img/AWS_deploy/search_iam.png">

- - -

`사용자 및 엑세스 키 관리` 화면에서 `Users` 탭으로 이동하여 `Add User` 버튼을 누른다.

<img width="600px" src="/img/AWS_deploy/add_users.png">

- - -

Add User 버튼을 누른 다음 유저 이름을 입력해주고, 엑세스 타입을 `Programmatic access` 로 설정한다.

- Access type:
    - Programmatic access: 개발 환경에만 엑세스를 허용함
    - AWS management console access: AWS 콘솔에 엑세스를 허용함

<img width="600px" src="/img/AWS_deploy/add_user_detail.png">

- - -

`next` 를 눌러 `Permission` 설정 창으로 넘어간 다음 `attach existing policies directly` 를 클릭하여 권한 목록을 불러온다.  
검색창에 `ec2full` 를 검색한 다음 `AmazonEC2FullAccess` 정책에 체크한 후 `next` 를 눌러 넘어간다.

<img width="800px" src="/img/AWS_deploy/add_user_permission.png">


> ###### Amazon EC2란?
>
>[http://docs.aws.amazon.com/ko_kr/AWSEC2/latest/UserGuide/concepts.html](http://docs.aws.amazon.com/ko_kr/AWSEC2/latest/UserGuide/concepts.html)

- - -

다음 화면에서 `Create user` 를 눌러 유저를 생성한다.

<img width="800px" src="/img/AWS_deploy/add_user_complete.png">

유저 생성 완료 창에 뜨는 `Access key ID` 와 `Secret access key` 는 이 창을 닫으면 다시는 볼 수 없으므로 `download.csv` 버튼을 눌러서 `csv` 파일로 다운로드하여 저장하거나 직접 ID와 secret key를 따로 저장해두어야 한다.  
다운로드를 하면 기본적으로 `Download` 폴더에 `credentials.csv` 파일로 ID와 Secret key가 저장된다.  
**`Secret access key` 는 절대로 외부에 노출되어서는 안된다.**

- - -

#### 키 페어 생성하기

Amazon EC2는 공개키 암호화 방식을 사용하여 로그인 정보를 암호화 및 해독한다.  
공개키 암호화 방식은 공개키로 암호화한 데이터를 유저가 가진 개인키로 해독하는 방식이다.  
이 공개키와 개인키 쌍을 `키 페어` 라고 한다.  

상단 메뉴의 `서비스` 를 클릭하여 나온 메뉴 중 `컴퓨팅` 항목 아래의 `EC2` 를 클릭한다.

<img width="300px" src="/img/AWS_deploy/computing_ec2.png">

- - -

메인 화면의 `리소스` 항목 아래의 `키 페어` 를 클릭한다.

<img width="500px" src="/img/AWS_deploy/key_pair.png">

- - -

`키 페어 생성` 을 클릭한다음 이름을 입력하면 `pem` 파일이 다운로드 된다.

<img width="950px" src="/img/AWS_deploy/key_pair_created.png">

다운로드한 pem 파일은 `~/.ssh` 폴더에 보관한다.

다음 명령어를 입력하여 `pem` 파일의 권한을 소유주만 읽을 수 있도록 해준다.

```
chmod 400 pem파일
```

`chmod` 명령에 대한 설명은 [여기](/etc/2017/10/28/shell-chmod.html)를 참고한다.

- - -

#### 인스턴스 시작하기

인스턴스는 AWS에서 제공하는 가상 컴퓨팅 환경을 뜻한다.

`EC2` 관리 메인 화면에서 `인스턴스 시작` 버튼을 클릭한다.

<img width="950px" src="/img/AWS_deploy/instance_start.png">

- - -

`단계 1: AMI` 선택에서 `Ubuntu Server 16.04` 를 선택해준다. 

<img width="950px" src="/img/AWS_deploy/AMI_ubuntu.png">

- - -

`다음` 을 계속 클릭하여 `단계 6: 보안 그룹 구성` 으로 이동한다음 `보안 그룹 이름` 과 `설명`을 입력한다.  

<img width="950px" src="/img/AWS_deploy/security_group.png">

`검토 및 시작` 버튼을 클릭하여 `단계: 7` 로 넘어간다.

- - -

`시작` 버튼을 눌러 나타나는 창에서 생성한 키 페어를 선택하고 체크박스에 체크를 한 뒤 `인스턴스 시작` 버튼을 누른다.

<img width="950px" src="/img/AWS_deploy/choose_key_pair.png">

- - -

`인스턴스 보기` 버튼을 눌러 생성한 인스턴스를 확인한다.

<img width="950px" src="/img/AWS_deploy/instance_created.png">

인스턴스를 생성하면 가상 컴퓨터 환경내의 유저가 자동생성된다.  
자동생성된 유저의 이름은 **`ubuntu`** 이다.

- - -

## 인스턴스에 접속하기

생성한 가상 컴퓨터 인스턴스에 `ssh` 를 사용하여 접속한다. 

```
ssh -i 키페어경로 유저명@EC2퍼블릭DNS주소
```

키 페어 경로는 `pem` 파일의 경로를 지정해주면 된다.  
`EC2 퍼블릭 DNS` 주소는 인스턴스 관리화면에서 확인할 수 있다.

<img width="950px" src="/img/AWS_deploy/public_dns.png">

```
ssh -i ~/.ssh/EC2-CH1.pem ubuntu@ec2-13-124-186-240.ap-northeast-2.compute.amazonaws.com
```
```re
The authenticity of host 'ec2-13-124-186-240.ap-northeast-2.compute.amazonaws.com (13.124.186.240)' can't be established.
ECDSA key fingerprint is SHA256:F6G+EOXm92kZYD8V7XNIUeTaOatVfaqmM0pLhfnk0mw.
Are you sure you want to continue connecting (yes/no)?    
```

`yes` 를 입력하여 접속한다.

만약 아래와 같은 에러가 발생할 경우,

```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Permissions 0664 for '/home/che1/.ssh/EC2-Che1.pem' are too open.
It is required that your private key files are NOT accessible by others.
This private key will be ignored.
Load key "/home/che1/.ssh/EC2-Che1.pem": bad permissions
Permission denied (publickey).
```
다음의 명령어로 `pem` 파일의 권한을 제한해준다.

```
chmod 400 pem파일
```

```re
Welcome to Ubuntu 16.04.2 LTS (GNU/Linux 4.4.0-1022-aws x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  Get cloud support with Ubuntu Advantage Cloud Guest:
    http://www.ubuntu.com/business/services/cloud

0 packages can be updated.
0 updates are security updates.



The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

_____________________________________________________________________
WARNING! Your environment specifies an invalid locale.
 The unknown environment variables are:
   LC_CTYPE=ko_KR.UTF-8 LC_ALL=
 This can affect your user experience significantly, including the
 ability to manage packages. You may install the locales by running:

   sudo apt-get install language-pack-ko
     or
   sudo locale-gen ko_KR.UTF-8

To see all available language packs, run:
   apt-cache search "^language-pack-[a-z][a-z]$"
To disable this message for all users, run:
   sudo touch /var/lib/cloud/instance/locale-check.skip
_____________________________________________________________________

ubuntu@ip-172-31-13-223:~$
```

위와 같이 표시되면 접속된 것이다.
- - -

## 서버 환경 설정

AWS 서버에 처음 접속한 뒤 다음의 기본 설정들을 세팅한다.

- - -

#### locale 설정

```
sudo vi /etc/default/locale
```

다음을 추가한 뒤 서버에 재접속한다.

```
LC_CTYPE="en_US.UTF-8"
LC_ALL="en_US.UTF-8"
LANG="en_US.UTF-8"
```

- - -

#### 기본 설정들

- 패키지 정보 업데이트
```
sudo apt-get update
```

- 패키지 의존성 검사 및 업그레이드
```
sudo apt-get dist-upgrade
```
아래와 같은 화면이 나올 경우, 기본 상태 그대로 엔터를 쳐준다.
<img width="800px" src="/img/AWS_deploy/dist_upgrade.png">


- Python 패키지 매니저 설치
```
sudo apt-get install python-pip
```

- zsh 설치
```
sudo apt-get install zsh
```

- oh my zsh 설치
```
sudo curl -L http://install.ohmyz.sh | sh
```

- 기본 쉘을 zsh로 변경한 뒤 재접속 (chsh 다음에 유저명을 입력해주어야한다.)
```
sudo chsh ubuntu -s /usr/bin/zsh
```

- - -

#### Python 환경 설정

- pyenv 설치 및 환경 설정   
[pyenv 설치하기(Ubuntu 환경)](/python/2017/09/12/pyenv-virtualenv.html) 포스트를 참고하여 pyenv를 설치하고, `~/.zshrc` 의 pyenv 환경변수 설정은 아래와 같이 입력해준다.
```
export PATH="/home/ubuntu/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

- Python 설치  
pyenv를 통해서 Python을 설치한다.
```
pyenv install 3.6.2
```

- Pillow를 위한 Python 라이브러리 설치
```
sudo apt-get install python-dev python-setuptools
```

- - -

#### Django 환경 설정

장고 프로젝트는 `root` 디렉토리의 `srv` 폴더에 업로드한다.  
`srv` 폴더의 소유자를 `ubuntu` 로 변경한다.

```
sudo chown -R ubuntu:ubuntu /srv/
```

<img width="600px" src="/img/AWS_deploy/srv_chown.png">

위와 같이 `srv` 폴더의 소유자와 그룹이 `ubuntu` 로 설정된 것을 확인한다.

- - -

## Django 프로젝트 서버에 업로드하기

간단한 장고 프로젝트를 시작하여 AWS 가상 컴퓨팅 환경에 업로드 해본다.

- - -

#### Django 프로젝트 시작

아래 두 포스트를 참고하여 **로컬 서버**에 장고 프로젝트를 시작한다.  
가상환경 이름은 `ec2_deploy`, python 버전은 3.6.3 버전으로 한다.  
장고 프로젝트 폴더 이름은 `EC2_Deploy_Project`, 프로젝트 이름은 `mysite` 로 한다.  

[[Django Tutorial] Blog 만들기 - 1. 환경설정](/django/2017/09/28/django-1-setting.html)  
[[Django Tutorial] Blog 만들기 - 2. 프로젝트 시작](/django/2017/09/30/django-2-start.html)

`config` 폴더의 `settings.py` 의 `ALLOWED_HOSTS` 에 다음과 같이 추가하여 접속을 허용해준다.
```py
# settings.py

ALLOWED_HOSTS = [
    'localhost',
    '.ap-northeast-2.compute.amazonaws.com',
]
``` 
- - -

#### scp를 사용하여 업로드하기

```
scp -i 키페어경로 -r 보낼폴더경로 유저명@퍼블릭DNS:받을폴더경로
```

아래의 명령어를 이용해서 `EC2_Deploy_Project` 폴더를 AWS 서버의 `srv` 폴더 아래로 복사한다.  
(아래의 경우는 `EC2_Deploy_Project` 폴더의 상위 폴더에서 실행할 경우임.)

```
scp -i ~/.ssh/EC2-Che1.pem -r EC2_Deploy_Project ubuntu@ec2-13-124-186-240.ap-northeast-2.compute.amazonaws.com:/srv/ 
```

- - -

#### 서버에서 Python 가상환경 설치하기

AWS 서버에 로컬 서버에서 생성했던 pyenv 가상환경 이름과 동일한 이름으로 가상환경을 생성한다.

``` 
pyenv virtualenv 3.6.3 ec2_deploy
```

AWS 서버에서 `/srv/EC2_Deploy_Project` 로 이동하면 자동으로 pyenv 가상환경이 `ec2_deploy` 로 설정되어 있는 것을 확인 할 수 있다.  
다음의 명령어를 입력하여 `requirements.txt` 에 기재되어있는 패키지들을 설치해준다.

```
pip install -r requirements.txt
```

만약 pip 버전이 최신버전이 아니라는 에러가 날 경우 아래 명령어를 입력해준 다음 다시 설치한다.

```
pip install --upgrade pip
```

- - -

#### 보안 그룹에 포트 추가하기

EC2 관리 화면으로 접속한 뒤, `보안 그룹` 화면으로 이동한다.  
보안 그룹 목록에서 생성한 보안 그룹을 체크하고 `인바운드` 탭의 `편집` 버튼을 누른다.

<img width="950px" src="/img/AWS_deploy/security_group_add.png">

- - -

`규칙 추가` 버튼을 누른 다음, 포트 범위에 `8080` 을 입력하고 저장을 누른다.

<img width="950px" src="/img/AWS_deploy/inbound_edit.png">

- - -

#### runserver 실행하기

`srv` 폴더안의 프로젝트 폴더로 이동하여 `runserver` 를 포트 8080에 실행한다.

```
./manage.py runserver 0:8080
```

브라우저에서 포트번호 8080으로 퍼블릭 DNS 주소에 접속해서 `runserver` 가 실행되고 있는 것을 확인하자.

```
ec2-13-124-186-240.ap-northeast-2.compute.amazonaws.com:8080
```

<img width="950px" src="/img/AWS_deploy/runserver.png">

- - -

{% include /deploy/deploy-toc-base.html %}

- - -

###### Reference

이한영 강사님 블로그: [https://lhy.kr/ec2-ubuntu-deploy](https://lhy.kr/ec2-ubuntu-deploy)  
AWS 유저 가이드: [http://docs.aws.amazon.com/ko_kr/AWSEC2/latest/UserGuide/concepts.html](http://docs.aws.amazon.com/ko_kr/AWSEC2/latest/UserGuide/concepts.html)

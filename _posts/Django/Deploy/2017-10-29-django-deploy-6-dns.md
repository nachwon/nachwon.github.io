---
layout: post
title: '[Deploy] Django 프로젝트 배포하기 - 6. DNS'
subtitle: Setting Up A Domain Name
comments: true
category: Django
tags:
  - Django
  - DNS
  - Deploy
---



이번 포스트에서는 배포한 웹서비스에 도메인 네임으로 접속할 수 있도록 하는 방법을 알아볼 것이다.

- - -

> #### Domain Name System
>
> 도메인 네임 시스템(Domain Name System, DNS)은 호스트의 도메인 이름을 호스트의 네트워크 주소로 바꾸거나 그 반대의 변환을 수행할 수 있도록 하기 위해 개발되었다. 특정 컴퓨터(또는 네트워크로 연결된 임의의 장치)의 주소를 찾기 위해, 사람이 이해하기 쉬운 도메인 이름을 숫자로 된 식별 번호(IP 주소)로 변환해준다. 도메인 네임 시스템은 흔히 "전화번호부"에 비유된다. 인터넷 도메인 주소 체계로서 TCP/IP의 응용에서, www.example.com과 같은 주 컴퓨터의 도메인 이름을 192.168.1.0과 같은 IP 주소로 변환하고 라우팅 정보를 제공하는 분산형 데이터베이스 시스템이다.
> 출처: [위키피디아](https://ko.wikipedia.org/wiki/%EB%8F%84%EB%A9%94%EC%9D%B8_%EB%84%A4%EC%9E%84_%EC%8B%9C%EC%8A%A4%ED%85%9C)

DNS는 IP 주소에 도메인 이름을 부여해서 외우기 힘든 IP 주소 대신 알아보기 쉬운 도메인 이름을 통해서 특정 서버에 접속할 수 있도록 해주는 시스템이다.  
지금 우리가 AWS 컴퓨터에 올려놓은 웹 사이트에 접속하기 위해서는 `*.ap-northeast-2.compute.amazonaws.com` 와 같은 주소로 접속해야한다. 이것도 DNS를 통해 부여된 도메인 이름이긴 하지만 차라리 IP 주소를 외우는 것이 더 쉬울 것만 같이 복잡하고 길다.  
이제 웹 사이트에게 간단하고 알아보기 쉬운 DNS를 새로 부여해보자. 

- - -

## 도메인 등록하기

먼저 도메인 이름을 부여하려면 사용가능한 도메인 이름을 확보해야한다.  
도메인 이름은 도메인 이름 호스팅 사이트에서 구매할 수 있으며, `Hosting.kr`, `gabia.com` 등 여러 개의 호스팅 사이트가 있다.  
이 포스트에서는 `Hosting.kr` 에서 도메인을 구매하여 적용해볼 것이다.  

- - -

#### 도메인 구매

Hosting.kr 사이트에 접속하면 보이는 검색창에 원하는 도메인 이름을 검색한다.

<img width="800px" src="/img/AWS_deploy/domain_search.png">

- - -

해당 검색어로 된 도메인 이름의 목록이 나타난다.

<img width="700px" src="/img/AWS_deploy/domain_search_result.png">

- - -

`등록 가능` 이라고 표시된 도메인 중 구매할 도메인 이름에 체크를 하고 `도메인 등록` 버튼을 눌러 도메인을 등록한다.  
결제를 하고 나서 `나의 서비스 관리 > 도메인 관리` 메뉴로 이동하면 구매한 도메인 목록이 나타난다.   

나는 `che1.co.kr` 과 `che1.kr` 을 구매했다.

<img width="800px" src="/img/AWS_deploy/domain_purchased.png">

- - -

이제 사용할 도메인 이름을 체크한 다음 `네임 서버 설정` 항목의 `네임서버(서브도메인) 설정 관리` 에 체크하고 `신청하기` 버튼을 누른다.

<img width="800px" src="/img/AWS_deploy/subdomain_submit.png">

- - -

네임서버 설정 관리 화면에서 `서브도메인`, `레코드 타입`, `IP 주소/레코드 값`, `우선순위` 를 설정하고 `설정 내용 추가` 버튼을 누른다.  

`서브도메인` 은 도메인 이름 앞에 추가로 붙는 이름이다. 예를 들어서 서브도메인을 `test` 로 설정하면, `test.che1.kr` 로 도메인 이름이 설정된다.  
그리고 `test.che1.kr` 로 접속할 때 접속하게 되는 실제 `IP 주소` 가 `IP 주소/레코드 값` 에 입력한 주소이다.  
우리의 웹 사이트로 접속해야하므로 `IP 주소/레코드 값` 에는 AWS 인스턴스의 퍼블릭 DNS 주소를 입력한다. 

<img width="700px" src="/img/AWS_deploy/dns_setting_add.png">

- - -

설정 내용을 추가하고나면 아래의 `적용하기` 버튼을 눌러 적용시킨다.

<img width="700px" src="/img/AWS_deploy/apply_dns.png">

- - -

#### Nginx 설정

이제 `test.che1.kr` 로 접속하면 AWS의 퍼블릭 DNS로 접속하게 된다.  
하지만 Nginx는 `test.che1.kr` 라는 주소로 들어온 요청을 알아듣지 못한다.  
Nginx가 이 주소로 오는 요청을 받을 수 있도록 `mysite.conf` 를 수정해주어야한다.

```conf
# mysite.conf

server {
    listen 80;
    server_name *.compute.amazonaws.com *.che1.kr;
    charset utf-8;
    client_max_body_size 128M;
.
.
.
```

`server_name` 항목에 `*.che1.kr` 를 추가해주면 `che1.kr` 도메인 이름으로 오는 요청을 모두 받을 수 있게 된다.  

- - -

#### Django 설정

이제 Nginx는 `test.che1.kr` 로 오는 요청을 받아 장고에게 전달해줄 수 있게 되었지만, 장고에서 이 요청을 처리하게 하려면 장고에서도 이 도메인 이름을 허가해주어야 한다.  
`settings.py` 를 열고 `ALLOWED_HOSTS` 변수에 아래와 같이 추가하자.  

```py
# settings.py

ALLOWED_HOSTS = [
    'localhost',
    '.ap-northeast-2.compute.amazonaws.com',
    '.che1.kr',
]
```

이제 장고도 `che1.kr` 도메인 이름으로 오는 요청을 처리할 수 있게 되었다.  
`scp` 로 서버에 변경사항을 업로드한 다음, `ssh` 로 서버에 접속하여 Nginx와 uWSGI를 재시작해준다.  

브라우저에서 `test.che1.kr` 로 접속을 해보면 업로드했던 장고 프로젝트가 나타나는 것을 볼 수 있다.

- - -

{% include /deploy/deploy-toc-base.html %}

- - -

###### Reference

이한영 강사님 블로그: [https://lhy.kr/ec2-ubuntu-deploy](https://lhy.kr/ec2-ubuntu-deploy)  

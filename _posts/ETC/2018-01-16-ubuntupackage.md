---
layout: post
title: 'Ubuntu 패키지 관리 명령어'
subtitle: Ubuntu Package Management
category: ETC
tags:
  - Linux
  - Shell
---

## Advanced Packaging Tool, APT

Ubuntu는 데비안 GNU/리눅스에서 파생된 운영체제이다.  

**APT(Advanced Packaging Tool)**는 데비안 GNU/리눅스에서 소프트웨어 설치 또는 제거 작업을 할 때 사용하는 소프트웨어이다.  

Ubuntu는 데비안 계열이므로 APT 패키지 매니저를 사용한다.  

- - -

### 명령어

- 패키지 설치

```
sudo apt-get install 패키지명
```

- - -

- 패키지 제거

```shell
sudo apt-get remove 패키지명
```

- - -

- 패키지 검색

```
sudo apt-cache search 패키지명
```

- 패키지 정보 보기

```
sudo apt-cache show 패키지명
```

- 패키지 목록 업데이트

APT에 등록된 패키지들의 최신 정보를 가져와 저장

```
sudo apt-get update
```

- 패키지 업그레이드

설치된 패키지들을 최신 버전으로 업그레이드함.

```
sudo apt-get upgrade
```

- - -

## Debian Package, dpkg

데비안 계열 리눅스 운영체제는 **.deb** 파일을 사용해서 패키지를 설치한다.

deb 파일 관리는 **dpkg** 명령어를 이용한다.

### 명령어

- 패키지 설치

```
dpkg -i deb파일
```

- 패키지 삭제

```
dpkg -P 패키지명
```

- 설치된 패키지 리스트

```
dpkg -l
```



---
layout: post
title: "zsh 플러그인 설치하기"
excerpt: "zsh에 플러그인을 설치하여 여러가지 편의기능을 추가해보자."
tags:
  - Zsh
  - Plugin
  - How to install
category: ETC
---

zsh에 여러가지 플러그인을 설치해서 편의 기능을 추가해보자.

**Ubuntu 16.04** 환경에서 작성되었음.

- - -

## Plugin 설치 경로

zsh 플러그인의 설치경로는 기본적으로 아래와 같다.

```zsh
/home/유저명/.oh-my-zsh/custom/plugins/플러그인명
```

또는 `$ZSH_CUSTOM` 을 호출하면 zsh 커스텀 폴더의 경로를 출력한다.

```zsh
$ZSH_CUSTOM/plugins/플러그인명
```

웹에서 설치하고 싶은 플러그인을 다운받아 위의 경로에 넣어주면 된다.  

예를 들어, zsh에 자동완성 기능을 추가해주는 `zsh-autosuggestions` 을 설치하려 한다면,   
먼저 터미널에서 아래와 같이 입력한다.  

```zsh
git clone https://github.com/zsh-users/zsh-autosuggestions $ZSH_CUSTOM/plugins/zsh-autosuggestions
```

github에서 플러그인 파일들을 다운로드받아서 `$ZSH_CUSTOM/plugins/zsh-autosuggestions` 의 경로에 저장하는 명령이다.  

- - -

## 설치된 플러그인 연결하기

플러그인을 설치했다면 zsh에 연결을 해주어야한다.  
먼저, zsh 설정파일인 `.zshrc` 파일을 연다.  

```zsh
vim ~/.zshrc
```

그 다음 스크롤을 내려서 `plugins` 라고 적혀있는 부분으로 이동한다.

```
...
plugins=( git )
...
```

이 부분에 설치한 플러그인명을 입력해주면 된다.

```
...
plugins=( git zsh-autosuggestions )
...
```

`:wq` 를 입력해 저장하고 나서 터미널을 재시작해보면 플러그인이 작동하는 것을 확인할 수 있다.

- - -

###### Reference

zsh-autosuggestions : [https://github.com/zsh-users/zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions)
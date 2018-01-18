---
layout: post
title: '[Shell] chmod - 파일 및 폴더의 권한 설정'
subtitle: Shell Script - Change Mode
category: ETC
tags:
  - Linux
  - Shell
  - Shell script
---

`chmod` 셸 명령어는 파일 또는 폴더의 권한을 변경할 때 사용한다.

- - -

### 사용법

8진수 모드를 사용하거나 문자열 모드를 사용하여 권한을 변경할 수 있다.

```
# 8진수 모드의경우
chmod [옵션] [소유자권한][그룹권한][그외사용자권한] [파일또는폴더]

# 문자열 모드의 경우
chmod [옵션] [레퍼런스][연산자][권한] [파일또는폴더]
```

- - -

### 권한 확인

파일 또는 폴더의 권한은 `rwx` 로 표시되며 셸에서 `ls -al` 명령을 통해 확인할 수 있다.  
맨 앞의 `d` 는 해당 항목이 파일인지 폴더인지를 나타내며 `d` 가 있으면 폴더이다.

```
[폴더여부][소유자권한][그룹권한][그외사용자권한]
```

<img width="600px" src="/img/Shell/chmod.png">

권한은 다음과 같은 종류가 있다.

- **`r`**: 읽기 권한

- **`w`**: 쓰기 권한

- **`x`**: 실행 권한

예를 들어, 어떤 폴더의 권한이 `drwxrw-r--` 이라면,  
소유자는 **모든 권한(`rwx`)**을 가지고, 그룹에 속한 사용자는 **읽기와 쓰기(`rw-`)**만 가능하며, 그 외의 사용자는 **읽기(`r--`)**만 가능하다.

- - -

### 8진수 모드


8진수 모드는 파일 또는 폴더의 권한을 8진수를 이용해 부여하는 방식이다.

```
chmod [소유자권한][그룹권한][그외사용자권한] [파일또는폴더]
```


<table class="table table-striped table-bordered" style="width: 500px;">
  <tr>
    <th>8진수</th>
    <th>권한</th>
    <th>rwx 표기</th>
  </tr>
  <tr>
      <td>7</td>
      <td>읽기, 쓰기, 실행 모두 가능</td>
      <td>rwx</td>
  </tr>
  <tr>
      <td>6</td>
      <td>읽기, 쓰기만 가능</td>
      <td>rw-</td>
  </tr>
  <tr>
      <td>5</td>
      <td>읽기, 실행만 가능</td>
      <td>r-x</td>
  </tr>
  <tr>
      <td>4</td>
      <td>읽기만 가능</td>
      <td>r--</td>
  </tr>
  <tr>
      <td>3</td>
      <td>쓰기, 실행만 가능</td>
      <td>-wx</td>
  </tr>
  <tr>
      <td>2</td>
      <td>쓰기만 가능</td>
      <td>-w-</td>
  </tr>
  <tr>
      <td>1</td>
      <td>실행만 가능</td>
      <td>--x</td>
  </tr>
  <tr>
      <td>0</td>
      <td>모든 권한 없음</td>
      <td>---</td>
  </tr>
</table>

- - -

##### 사용 예

예를 들어, `test.txt` 라는 파일의 권한을 `rwxrw-r--` 로 설정하려면 다음과 같이 입력한다.

```
chmod 764 test.txt
```

- - -

### 문자열 모드

문자열 모드는 특정 문자열을 사용해 권한을 설정하는 방법이다.

```
chmod [옵션] [레퍼런스][연산자][권한] [파일또는폴더]
```

- - -

##### 레퍼런스 

레퍼런스는 어떤 사용자에게 권한을 부여하는지를 설정한다.

<table class="table table-bordered table-striped">
    <tbody>
        <tr>
            <th>레퍼런스</th>
            <th>사용자 유형</th>
            <th>설명</th>
        </tr>
        <tr>
            <td>
                <tt>u</tt>
            </td>
            <td>소유자</td>
            <td>파일 또는 폴더의 소유자</td>
        </tr>
        <tr>
            <td>
                <tt>g</tt>
            </td>
            <td>그룹</td>
            <td>파일 또는 폴더의 그룹에 포함된 사용자</td>
        </tr>
        <tr>
            <td>
                <tt>o</tt>
            </td>
            <td>그 외 사용자</td>
            <td>소유자도 아니고 그룹에 포함되지도 않은 사용자</td>
        </tr>
        <tr>
            <td>
                <tt>a</tt>
            </td>
            <td>모든 사용자</td>
            <td>모든 사용자를 뜻하며, 
                <tt>ugo</tt>
                와 동일하다.
            </td>
        </tr>
    </tbody>
</table>

- - -

##### 연산자

<table class="table table-striped table-bordered">
    <tbody>
        <tr>
            <th>연산자</th>
            <th>설명</th>
        </tr>
        <tr>
            <td>
                <tt>+</tt>
            </td>
            <td>기존 권한에 권한 추가</td>
        </tr>
        <tr>
            <td>
                <tt>-</tt>
            </td>
            <td>기존 권한에서 권한 제거</td>
        </tr>
        <tr>
            <td>
                <tt>=</tt>
            </td>
            <td>지정한 권한으로 변경</td>
        </tr>
    </tbody>
</table>

- - -

##### 사용 예

`test.txt` 파일의 권한이 `rwxrw-r--` 이라면,

- 소유자의 실행 권한 삭제
```
chmod u-x test.txt
```
```re
rw-rw-r--
```

- 외부사용자에 쓰기, 실행 권한 부여
```
chmod o+wx test.txt
```
```re
rwx-rw-rwx
```

- 모든 사용자에게 읽기 권한만 부여
```
chmod a=r test.txt
```
```re
r--r--r--
```

- - -

### 옵션

`-R`: 권한을 폴더의 하위 경로에도 모두 적용시킨다.


`example_folder` 내의 모든 파일 및 폴더의 권한을 `rwxrwxrwx` 로 설정.
```
chmod -R 777 example_folder
```

- - -

###### Reference

위키피디아: [https://en.wikipedia.org/wiki/Chmod](https://en.wikipedia.org/wiki/Chmod)
---
layout: post
title: '[Python 문법] 정규표현식 (Regular Expressions)'
category: Python
author: Che1
---

## 정규표현식이란?
정규표현식 (Regular expressions) 은 복잡한 문자열을 처리할 때 사용하는 기법으로, Python 뿐만 아니라 문자열을 처리하는 모든 곳에서 사용된다.

- - -

## 메타 문자 (Meta characters)
메타 문자란 문자가 가진 원래의 의미가 아닌 특별한 용도로 사용되는 문자를 말한다.
정규표현식에서 사용되는 메타 문자는 다음과 같다.

```re
. ^ $ * + ? \ | ( ) { } [ ]  
```

- - -

#### 문자 클래스 `[]`

정규표현식에서 대괄호 `[]` 는 **대괄호 안에 포함된 문자들과 매치**를 뜻한다.

```re
[abc] # abc 중 하나와 매치
```
```re
'a' # a와 매치
'boy' # b와 매치
'dye' # a, b, c 중 어느 문자와도 매치되지 않음
```

`[]` 안의 두 문자에 `-`를 사용하면 **두 문자 사이의 범위**를 뜻한다.
```re
[a-c] # [abc]와 같음
[0-5] # [012345]와 같음
[a-zA-Z] # 모든 알파벳
[0-9] # 숫자
```

`^`는 **반대**를 뜻한다.

```re
[^0-9] # 숫자를 제외한 문자만 매치
[^abc] # a, b, c를 제외한 모든 문자와 매치
```

- - -

#### 모든 문자 `.`

`.`은 줄바꿈 문자인 `\n` 을 제외한 **모든 문자**와 매치된다.
```re
a.b # 'a + 모든 문자 + b'를 뜻함
```
```re
aab # a와 b 사이의 a는 모든 문자에 포함되므로 매치
a0b # a와 b 사이의 0은 모든 문자에 포함되므로 매치
abc # a와 b 사이에 문자가 없기 때문에 매치되지 않음
```

**※** `[]` 사이에서 `.`을 사용할 경우 문자 원래의 의미인 마침표가 된다.
```re
a[.]b
```
```re
a.b # a와 b 사이에 마침표가 있으므로 매치
a0b # a와 b 사이에 마침표가 없으므로 매치 안됨
```

- - -

#### 반복 `*`
`*` 앞에 오는 문자가 **0개를 포함하여 몇 개가 오든** 모두 매치된다.
```re
lo*l
```
```re
ll # 매치
lol # 매치
looool # 매치
looooooooooooooooooooool # 매치
lbl # 매치 안됨
loooooooooooobooooooool # 매치 안됨
```
- - -

#### 최소 한 번 이상 반복 `+`

`+` 앞에 있는 문자가 **최소 한 번 이상 반복**되어야 매치된다.

```re
lo+l
```
```re
ll # 매치 안됨
lol # 매치
looooool # 매치
```

- - -

#### 없거나 하나 있거나 `?`

`?` 앞에 있는 문자가 **없거나 하나** 있을 때 매치된다.
```re
lo?l
```
```re
ll # 매치
lol # 매치
lool # 매치 안됨
```

- - -

#### 반복 제어 `{m, n}`

 `{m, n}` 앞에 있는 문자가 **`m` 번에서 `n` 번까지 반복**될 때 매치된다.

 ```re
 lo{3, 5}l
 ```
 ```re
 ll # 매치 안됨
 lol # 매치 안됨
 loool # 매치
 loooool # 매치
 looooool # 매치 안됨
 ```

 `{m}`의 형태로 사용하면 반드시 `m` 번 반복인 경우만 매치된다.

 `{0,}` 는 `*`, `{1,}` 는 `+`, `{0,1}` 는 `?` 와 각각 동일하다.

- - -


## `re`: Python 정규표현식 모듈

Python 에서는 `re` 모듈을 통해 정규표현식을 사용한다.

```python
import re
```

`re.compile()` 명령을 통해 정규표현식을 컴파일하여 변수에 저장한 후 사용한다.
```python
p = re.compile('[a-z]')
```

변수 `p`의 타입을 확인해보면 `_sre.SRE_Pattern` 이라는 이름의 **클래스 객체**인 것을 볼 수 있다.

```python
print(type(p))
```
```result
<class '_sre.SRE_Pattern'>
```

- - -
## 패턴 객체의 메서드

패턴 객체는 매치를 검색할 수 있는 네 가지 메서드를 제공한다.  
다음의 정규표현식으로 각각의 메서드를 비교해본다.
```python
p = re.compile('[a-z]+')
```
- - -

#### `match`: 시작부터 일치하는 패턴 찾기

문자열의 처음 시작부터 검색하여 일치하지 않는 부분이 나올 때까지 찾는다.

```python
p.match('aaaaa')
<_sre.SRE_Match object; span=(0, 5), match='aaaaa'>

p.match('bbbbbbbbb')
<_sre.SRE_Match object; span=(0, 9), match='bbbbbbbbb'>

p.match('1aaaa')
None

p.match('aaa1aaa')
<_sre.SRE_Match object; span=(0, 3), match='aaa'>
```

검색의 결과로 `_sre.SRE_Match` 객체를 리턴하며 동시에 매치된 문자열의 인덱스값과 내용을 출력해준다.
```python
<_sre.SRE_Match object; span=(매치 시작지점 인덱스, 매치 끝지점 인덱스), match='매치된 문자열'>
```

- - -
#### `search`: 전체 문자열에서 첫 번째 매치 찾기

문자열 전체에서 검색하여 처음으로 매치되는 문자열을 찾는다.

```python
p.search('aaaaa')
<_sre.SRE_Match object; span=(0, 5), match='aaaaa'>

p.search('11aaaa')
<_sre.SRE_Match object; span=(2, 6), match='aaaa'>

p.search('aaa11aaa')
<_sre.SRE_Match object; span=(0, 3), match='aaa'>

p.search('1aaa11aaa1')
<_sre.SRE_Match object; span=(1, 4), match='aaa'>
```
`match`와 동일한 형태로 결과를 출력해준다.

- - -

#### `findall`: 모든 매치를 찾아 리스트로 반환

문자열 내에서 일치하는 모든 패턴을 찾아 **리스트**로 반환한다.

```python
p.findall('aaa')
['aaa']

p.findall('11aaa')
['aaa']

p.findall('1a1a1a1a1a')
['a', 'a', 'a', 'a', 'a']

p.findall('1aa1aaa1a1aa1aaa')
['aa', 'aaa', 'a', 'aa', 'aaa']
```

- - -

#### `finditer`: 모든 매치를 찾아 반복가능 객체로 반환

```python
p.finditer('a1bb1ccc')
<callable_iterator object at 0x7f850c4285f8>
```

`callable_iterator`라는 객체가 반환되었다. `for`을 사용하여 하나씩 출력해보자.

```python
f_iter = p.finditer('a1bb1ccc')
for i in f_iter:
    print(i)
```
```result
<_sre.SRE_Match object; span=(0, 1), match='a'>
<_sre.SRE_Match object; span=(2, 4), match='bb'>
<_sre.SRE_Match object; span=(5, 8), match='ccc'>
```

반복가능 객체는 각 매치의 결과인 매치 객체를 포함하고 있다.

- - -

###### Reference

- 이한영 강사님 github : [12.정규표현식.md](https://github.com/Fastcampus-WPS-6th/Python/blob/master/12.%20%EC%A0%95%EA%B7%9C%ED%91%9C%ED%98%84%EC%8B%9D.md)
- 점프 투 파이썬 : [https://wikidocs.net/4308](https://wikidocs.net/4308)
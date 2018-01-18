---
layout: post
title: 마크다운 문법 정리
tags:
  - Markdown
category: ETC
---

# <img width="300px" src="/img/markdown.png">

HOW TO USE MARKDOWN(KRAMDOWN)


## 1. 헤더(Header)
- - -
#### 1.1. `=`, `-`  사용

- 큰 제목으로 만들 텍스트 아랫줄에 `=`을 입력한다.

```
This is H1!
========
```

결과:

This is H1!
========
- - -

- 작은 제목으로 만들려면 `-`을 입력한다.
```
This is H2!
-------------
```
결과:

This is H2!
-------------
※ 꼭 여러줄 안쳐도 되는 듯

- - -
#### 1.2. `#`사용

- 헤더로 만들 텍스트의 앞에 `#`를 입력한다.
```
# This is H1!
```
결과:
# This is H1!

- - - 

- `#`의 갯수에 따라 H1 에서  H6까지 지원된다.
# # This is H1!
## ## This is H2!
### ### This is H3!
#### #### This is H4!
##### ##### This is H5!
###### ###### This is H6!
####### ####### This doesn't work!

- - -


## 2. 인용(Blockquote) 
- `>`를 사용해서 인용문을 표시한다.
```
> This is Blockquote!
```
결과:
>This is Blockquote!

- - -

- `>`를 여러개 입력하여 인용문의 레벨을 설정해줄 수 있다. 
- 같은 레벨의 인용문 안에 텍스트를 추가하려면 같은 수의 `>`를 입력해주어야 한다.
```
>This is 1st level Blockquote!
>>This is 2nd level Blockquote!
>>I am on the 2nd floor!
>>>This is 3rd level Blockquote!
```
결과:
>This is 1st level Blockquote!
>>This is 2nd level Blockquote!
>>I'm on the 2nd floor!
>>>This is 3rd level Blockquote!

- - - 

- 인용문 안에서는 마크다운 문법이 그대로 적용된다.
```
>This is Blockquote!
># This is H1 inside the blockquote!
>>This is another Blockquote inside the blockquote!
```

결과: 
>This is Blockquote!
># This is H1 inside the blockquote!
>>This is another Blockquote inside the blockquote!

- - -


## 3. 목록(List)

- - -

#### 3.1. 순서가 있는 목록(Ordered list)
- `[숫자].`의 형태로 순서가 있는 목록을 작성한다.
```
1. fisrt
2. second
3. third
```
결과:

<ol class="list1">
<li>first</li>
<li>second</li>
<li>third</li>
</ol>

- - -

- `[tab]` 또는 `[spacebar]` 네 칸으로 하위 목록을 입력해줄 수 있다.

```
1. fisrt
	1. first-first
	2. first-second
2. second
3. third
```

결과:

1. first
    1. first-first
    2. first-second
2. second
3. third

- - -

- 번호의 순서가 바뀌어도 결과는 항상 내림차순으로 나타난다.

```
1. fisrt
3. second
2. third
```
결과:

1. fisrt
3. second
2. third

- - -


#### 3.2. 순서가 없는 목록(Unordered list)
- `+`, `-`, `*`를 이용해 순서가 없는 목록을 만들 수 있다. 혼합하여 사용할 수 도 있다.


```
* item1
* item2
* item3

+ item1
+ item2
	+ item2.1
		
+ item1
	- item1.1
		* item1.1.1
```

결과:

* item1
	* item2
	* item3

+ item1
+ item2
	+ item2.1

+ item1
	- item1.1
		* item1.1.1

- - -

- 순서가 있는 목록과도 혼합하여 사용할 수 있다.

```
1. item
	* item
	* item
```

결과:

1. item
	* item
	* item
<br>

- - -
※ 목록의 기본 넘버링 스타일을 바꾸는 것은 마크다운에서는 지원하지 않 것 같다. 아래 코드를 추가하여 바꿔 줄 수 있다. (전체 목록에 동시 적용.)
```
<style>
ol{list-style-type: [스타일값];}
</style>
```

적용 예:

 - 숫자 : [스타일 값] = decimal

<style>
ol.list2{list-style-type: decimal;}
</style>

<ol class="list2">
<li>first</li>
<li>second</li>
<li>third</li>
</ol>

- 영어 소문자 : [스타일 값] = lower-alpha

<style>
ol.list3{list-style-type: lower-alpha;}
</style>

<ol class="list3">
<li>first</li>
<li>second</li>
<li>third</li>
</ol>

- 두자리 숫자 : [스타일 값] = decimal-leading-zero

<style>
ol.list4{list-style-type: decimal-leading-zero;}
</style>

<ol class="list4">
<li>first</li>
<li>second</li>
<li>third</li>
</ol>
- - -


## 4. 줄바꾸기(line break) 

- 줄을 바꾸고 싶을 때는 줄을 나누고 싶은 부분에 `[Spacebar]`를 두 번 넣고 줄을 바꾼다.

```
this is a line  
this is next line
```

결과:

this is a line  
this is next line

- - -

- 빈 줄을 추가할 때는 `[Enter]`를 삽입한다.

```
this is a line

this is next line
```

결과:

this is a line

this is next line

- - -

## 5. 이미지 삽입(Insert images)

- 이미지를 삽입하기 위해서는 아래와 같이 입력한다.

```
![gras](이미지 경로){:[스타일 옵션]}
```
적용 예:

```
markdown logo:  
![gras](/img/markdown.png){:width="300px"}
```
markdown logo:   
![gras](/img/markdown.png){:width="300px"}

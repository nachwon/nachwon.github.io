---
layout: post
title: 마크다운 문법 정리
author: Che1
---

Lorem ipsum dolor sit amet consectetur adipisicing elit. Adipisci, nemo eius quos laborum, necessitatibus culpa in commodi nam cupiditate, rerum neque nostrum quibusdam placeat voluptatibus iusto saepe! Voluptas, velit praesentium.
Lorem ipsum dolor sit amet consectetur adipisicing elit. Adipisci, nemo eius quos laborum, necessitatibus culpa in commodi nam cupiditate, rerum neque nostrum quibusdam placeat voluptatibus iusto saepe! Voluptas, velit praesentium.


<!-- # <img width="150px" src="~./Projects/Che1-blog/img/markdown.png"> -->

HOW TO USE MARKDOWN


## 1. 헤더(Header)
#### 1.1. `=`, `-`  사용

- 큰 제목으로 만들 텍스트 아랫줄에 `=`을 입력한다.

```
This is H1!
========
```
결과:

This is H1!
========

<br>

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
<br>
#### 1.2. `#`사용

- 헤더로 만들 텍스트의 앞에 `#`를 입력한다.
```
# This is H1!
```
결과:
# This is H1!

<br>

- `#`의 갯수에 따라 H1 에서  H6까지 지원된다.
# # This is H1!
## ## This is H2!
### ### This is H3!
#### #### This is H4!
##### ##### This is H5!
###### ###### This is H6!
####### ####### This doesn't work!
- - -

<br>

## 2. 인용(Blockquote) 
- `>`를 사용해서 인용문을 표시한다.
```
> This is Blockquote!
```
결과:
>This is Blockquote!

<br>

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

<br>

- 인용문 안에서는 마크다운 문법이 그대로 적용된다.
```
>This is Blockquote!
># This is H1 inside the blockquote!
>>This is another Blockquote inside the blockquote!
```
>This is Blockquote!
># This is H1 inside the blockquote!
>>This is another Blockquote inside the blockquote!
- - -
<br>

## 3. 목록(List)
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

<br>

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

<br>

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

<br>

#### 3.2. 순서가 없는 목록(Unordered list)
- `+`, `-`, `*`를 이용해 순서가 없는 목록을 만들 수 있다. 혼합하여 사용할 수 도 있다.

```
* item
* item
* item

+ item
+ item
	+ item
		
+ item
	- item
		* item
```

결과:

* item
* item
* item
<br>

+ item
+ item
	+ item
<br>

+ item
	- item
		* item
<br>

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



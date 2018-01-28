---
layout: post
title: '[HTML]Emmet 사용법'
tags:
  - HTML
category: Front-end
---

## Emmet이란?

강력한 자동완성 기능 등으로 HTML 작성 속도를 크게 향상시켜주는 플러그인

- - -
## Emmet 문법
- - -
#### 요소 (Elements) 생성

생성하려는 요소의 이름을 입력한 뒤 `tab`을 누르면 태그가 자동 생성된다.  
Emmet에는 **미리 정해진 태그 이름이 없다**. 즉, 아무 이름으로나 태그를 생성할 수 있다.(에디터에 따라 그렇지 않은 경우도 있다.)

```
html:5[tab]
```
결과:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
    
</body>
</html>
```
```
helloworld[tab]
```
결과:
```html
<helloworld></helloworld>
```

- - -

## 구조화 하기 (Nesting operators)

Emmet의 문법을 활용하여  **요소들의 구조**를 간편히 생성할 수 있다.

- - -

#### 자식 요소: `>`

`>`를 사용하여 **자식 요소**를 생성할 수 있다. :
```
div>ul>li
```
결과 :

```html
<div>
    <ul>
        <li></li>
    <ul>
<div>
```
- - -

#### 형제 요소: `+`

`+`를 사용하여 한 요소와 **같은 단계**에 위치한 요소를 생성할 수 있다.
```
div+p+bq
```
결과 :

```html
<div></div>
<p></p>
<blockquote></blockquote>
```

- - -

#### 한 단계 올리기: `^`

`^`를 사용하여 **한 단계 위**에 요소를 배치할 수 있다.

```
div+div>p>span+em^bq
```
*span+em은 p태그의 하위 단계에 위치하지만 bq는 ^로 인해 p태그와 같은 단계에 위치하게 된다.*

결과 : 

```html
<div></div>
<div>
    <p>
        <span></span>
        <em></em>
    </p>
    <blockquote></blockquote>
</div>
```


Use as many **^** as needed to **move up more levels**.

```
div+div>p>span+em^bq
```

```html
<div></div>
<div>
  <span>
    <p><span></span><em></em></p>
    <blockquote></blockquote>
  </span>
</div>
```

```
div+div>p>span+em^^bq
```

```html
<div></div>
<div>
  <span>
    <p><span></span><em></em></p>
  </span>
  <blockquote></blockquote>
</div>
```

```
div+div>p>span+em^^^bq
```

```html
<div></div>
<div>
  <span>
    <p><span></span><em></em></p>
  </span>
</div>
<blockquote></blockquote>
```

### Multiplication: *

Use ** * ** operator to define **how many times** element should be outputted.

```
ul>li*5
```

...outputs to

```html
<ul>
  <li></li>
  <li></li>
  <li></li>
  <li></li>
  <li></li>
</ul>
```

```
ul>li*3
```

...outputs to

```html
<ul>
  <li></li>
  <li></li>
  <li></li>
</ul>
```

### Grouping: ()

Use **()** to group subtrees in complex abbreviations.

```
div>(header>ul>li*2>a)+footer>p
```

...expands to

```html
<div>
    <header>
        <ul>
            <li><a href=""></a></li>
            <li><a href=""></a></li>
        </ul>
    </header>
    <footer>
        <p></p>
    </footer>
</div>
```
            

Each group contains abbreviation subtree and all the following elements are inserted at the same level as **the first element of group.**

It is possible to nest groups inside each other and combine them with ** * ** operator.

```
(div>dl>(dt+dd)*3)+footer>p
```

```html
<div>
  <dl>
    <dt></dt>
    <dd></dd>
    <dt></dt>
    <dd></dd>
    <dt></dt>
    <dd></dd>
  </dl>
</div>
<footer>
  <p></p>
</footer>
```

## Attribute operators

### ID and CLASS

Use *elem*#id and *elem*.class notation to **reach the elements with specified id or class attributes.**

```
div#header+div.page+div#footer.class1.class2.class3
```

...will output

```html
<div id="header"></div>
<div class="page"></div>
<div id="footer" class="class1 class2 class3"></div>
```

### Custom attributes

Use **[attr]** notation to **add custom attributes** to element.

```
td[title="Hello world!" colspan=3]
```

...outputs

```html
<td title="Hello world!" colspan="3"></td>
```

- Place as many attributes as necessary.
- It is not required to specify attribute values:

```
td[colspan title]
```

```html
<td colspan="" title=""></td>
```
    
  In this case, **tabstops are available** for each empty attribute.
- Single or double quotes can be used for quoting attribute values.
- If attribute values have **no space**, it is not needed to quote values.

```
td[title=hello colspan=3]
```
```html
<td title="hello" colspan="3"></td>
```

### Item numbering: $

Use **$** operator with ** * ** operator to ** repeat elements with numbers**. Place ```$``` operator inside element's name, attribute's name or attribute's value to output current number of repeated element.
```
ul>li.item$*5
```
...outputs to

```html
<ul>
  <li class="item1"></li>
  <li class="item2"></li>
  <li class="item3"></li>
  <li class="item4"></li>
  <li class="item5"></li>
</ul>
```

Use multiple $ in a row to **pad** number with zeroes.

```
ul>li.item$$$*4
```

```html
<ul>
  <li class="item001"></li>
  <li class="item002"></li>
  <li class="item003"></li>
  <li class="item004"></li>
</ul>
```

### Changing numbering base and direction

Use **@** modifier to **change numbering direction** (ascending or decending) and base (start value).

```
ul>li.item$@-*5
```

...outputs to

```html
<ul>
  <li class="item5"></li>
  <li class="item4"></li>
  <li class="item3"></li>
  <li class="item2"></li>
  <li class="item1"></li>
</ul>
```

To change counter base value, add **@N** to $.
```
ul>li.item$@2*4
```
...transforms to

```html
<ul>
  <li class="item2"></li>
  <li class="item3"></li>
  <li class="item4"></li>
  <li class="item5"></li>
</ul>
```

```
ul>li.item$@-3*4
```
...is transformed to

```html
<ul>
  <li class="item6"></li>
  <li class="item5"></li>
  <li class="item4"></li>
  <li class="item3"></li>
</ul>
```

### Text: {}

Use **{}** to **add text** to element.

```
a{Click me}
```
... will produce

```html
<a href="">Click me</a>
```

When {text} is written right after elemnet, **it doesn't change parent context.**

```
p>{Click}+a{here}+{to continue}
```

...produces


```html
<p>Click<a href="">here</a>to continue</p>
```

```
p{Click}+a{here}+{to continue}
```

...produces

```html
<p>Click</p>
<a href="">here</a>to continue
```

### Notes on abbreviation formatting

- Do not use spaces between elements and operators to make abbreviations more readable. **Space is a stop symbol where Emmet stops abbreviation parsing.**
- Expanding abbreviation is possible **anywhere in the text.**


- - -

###### Reference

Emmet Document: [https://docs.emmet.io/abbreviations/syntax/](https://docs.emmet.io/abbreviations/syntax/)

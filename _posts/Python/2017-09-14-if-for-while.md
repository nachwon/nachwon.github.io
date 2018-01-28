---
layout: post
title: '[Python 문법] 제어문 - if, for, while'
excerpt: 제어문을 사용하여 좀 더 다이나믹한 Python 프로그램을 만들어보자.
category: Python
tags:
  - Python
  - Statement
---

## `if` 문

- 여러 조건에 따라 각각 다른 명령을 실행할 수 있도록 해준다.

- - -

#### 기본구조

```python
if 조건1:
    조건1이 True일 경우
else:
    조건1이 False일 경우
```
- - -

#### `elif`: 추가조건이 필요한 경우

- 2개 이상의 조건이 필요한 경우, `elif`를 사용하여 추가해준다.

```python
if 조건1:
    조건1이 True일 경우
elif 조건2:
    조건2가 True일 경우
    .
    .
    .
elif 조건n:
    조건n이 True일 경우
else 모든 조건이 False일 경우
```

- - -

#### 조건표현식
- 간단한 `if`문은 조건표현식으로 한 줄에 작성할 수 있다.

```python
True일 경우 if 조건식 else False일 경우
```

- 조건표현식을 중첩하여 여러 개의 조건을 가진 `if`문을 한줄로 작성할 수 있다.    

*조건표현식은 가독성의 문제로 두 개 이상 중첩하여 사용하지 않는 것을 권장한다.*

```python
True일 경우 if 조건1 else 조건1은 False, 조건2는 True일 경우 if 조건2 else 모두 False인 경우
```

- - -

## `for` 문

- 순회가능 객체(Iterable object)를 매개로 같은 명령을 반복하여 실행해준다.

- - -
#### 기본구조

```python
for 변수이름 in 순회가능 객체:
    반복 실행할 코드
```

- - -

#### `for`문과 `if`문

- `for`문과 `if`문을 혼합하여 좀 더 복잡한 명령을 반복할 수 있다.

```python
for i in [1, 2, 3, 4, 5]:
    if i % 2 == 0:
        print(i, '는 2의 배수')
    elif i % 3 == 0:
        print(i, '는 3의 배수')
    else:
        pass
```
결과:
```
2 는 2의 배수
3 는 3의 배수
4 는 2의 배수
```

- - -

#### `continue`: 다음 반복 실행

- `for`문안의 명령이 실행되는 중에 `continue`를 만나면 `for`문의 처음으로 돌아가 다음 순서의 반복을 수행한다.

```python
for i in [1, 2, 3, 4, 5]:
    if i % 2 == 0:
        print(i, '는 2의 배수')
    elif i % 3 == 0:
        continue
        print(i, '는 3의 배수') # 이 명령은 실행되지 않는다.
    else:
        pass
```
결과:
```
2 는 2의 배수
4 는 2의 배수
```
- - -

#### `break`: 반복 강제 종료

- `for`문안의 명령이 실행되는 중에 `break`를 만나면 즉시 반복을 멈춘다.

```python
for i in [1, 2, 3, 4, 5]:
    if i % 2 == 0:
        print(i, '는 2의 배수')
    elif i % 3 == 0:
        break # i가 3이 되는 순간 for 루프가 멈추게 된다.
        print(i, '는 3의 배수') # 이 명령은 실행되지 못하고 루프가 종료된다.
    else:
        pass
```
결과:
```
2 는 2의 배수
```
- - -

#### 리스트 컴프리헨션 (Comprehension)

- `for` 문을 활용하여 한 줄로 리스트를 생성할 수 있다.

- 기본 형태
```python
[표현식 for 항목 in 순회가능객체]
```
- if문을 포함한 형태

```python
[표현식 for 항목 in 순회가능객체 if 조건문]
```

- 중첩된 형태

```python
[표현식 for 항목1 in 순회가능객체1 for 항목2 in 순회가능객체2]
```

- 셋(set)이나 딕셔너리(dictionary) 자료형에도 적용가능하다.

셋 컴프리헨션
```python
(표현식 for 항목 in 순회가능객체)
```

딕셔너리 컴프리헨션 적용 예
```python
>>> a = [['a', 1], ['b', 2], ['c', 3]]
>>> {i: j for i, j in a}
{'a': 1, 'b': 2, 'c': 3}
```
- - -

## `while` 문

- 주어진 조건이 거짓이 될 때까지 명령을 반복 실행한다.

```python
while 조건:
    조건이 True일 경우 실행
    조건이 False가 될 때까지 계속해서 반복
```

- `for` 문과 마찬가지로 `if`, `continue`, `break`를 사용할 수 있다.

<br>

##### 무한 루프

- `while` 문으로 무한히 반복되는 루프를 구현할 수 있다.

```python
while True:
    명령1
    명령2
    명령3
    .
    .
    .
```

- - -


## 연습 문제
- 구구단의 단 이름을 'title'키의 값으로, 단 내용을 'item'키의 값으로 가지는 딕셔너리들의 리스트 만들기.

```python
d_list = [
    {
        'title': f'{x}단', 
        'items': [f'{x} X {y} = {x * y}' for y in range(1, 10)]
        } for x in range(2, 10)
    ]
```

- - -

###### Reference

- 이한영 강사님 github: [https://github.com/Fastcampus-WPS-6th/Python/blob/master/08.%20%EC%A0%9C%EC%96%B4%EB%AC%B8.md](https://github.com/Fastcampus-WPS-6th/Python/blob/master/08.%20%EC%A0%9C%EC%96%B4%EB%AC%B8.md)  
- 점프 투 파이썬: [https://wikidocs.net/20](https://wikidocs.net/20)
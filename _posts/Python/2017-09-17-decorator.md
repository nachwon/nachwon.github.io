---
layout: post
title: '[Python 문법] 데코레이터 (Decorator)'
excerpt: Pyton으로 데코레이터를 만들고 사용하는 방법에 대해 알아본다.
category: Python
tags:
  - Python
  - Closure
  - Decorator
---

## 데코레이터란?

- 어떤 함수를 받아 명령을 추가한 뒤 이를 다시 함수의 형태로 반환하는 함수.
- 어떤 함수의 내부를 수정하지 않고 기능에 변화를 주고 싶을 때 사용한다.
- 말그대로 다른 함수를 꾸며주는 함수.

- - -

## 데코레이터의 구조

데코레이터의 기본 구조는 아래와 같다.

```python
def 데코레이터이름(func):  # 기능을 추가할 함수를 인자로 받아온다.
    def 내부함수이름(*args, **kwargs):
        기존 함수에 추가할 명령
        return func(*args, **kwargs)
    return 내부함수이름
```

클로저와 매우 흡사하게 생겼다는 것을 알 수 있다. 차이점이라면 데코레이터는 **다른 함수를 인자로 받는다**는 점이다.

간단한 데코레이터를 만들어보자. 아래 함수는 이름을 인자로 받아 자기소개를 출력해주는 함수이다.

```python
def introduce(name):
    print(f'My name is {name}!')
```
```python
introduce('Chaewon')
```
```re
My name is Chaewon!
```

그런데 인사도 없이 대뜸 자기 이름을 말해버리니까 버릇이 없어보여서 자기이름을 말하기 전에 인사를 먼저 하도록 바꿔주고 싶어졌다.  
그래서 아래의 함수를 만들었다.

```python
def decorator(func):
    def wrapper(*args, **kwargs):
        print('Hello')
        return func(*args, **kwargs)
    return wrapper
```

이 함수는 어떤 함수가 실행될 때 `Hello`라는 문자열을 출력해주도록 꾸며주는 데코레이터이다.

- - -

## 데코레이터의 적용

만든 데코레이터를 적용시켜서 `introduce` 함수를 꾸며보자.

```python
decorated_introduce = decorator(introduce)  # decorator 함수에 호출하지 않은 introduce 함수 자체를 인자로 전달한다.
```
`decorator` 함수에 `introduce` 함수를 인자로 전달한 것을 `decorated_introduce` 라는 변수에 할당하였다.  
이제 업그레이드 된 `introduce` 함수인 `decorated_introduce` 함수에 이름을 전달하여 잘 작동하는지 살펴보자.
```python
decorated_introduce('Chaewon')
```
```re
Hello
My name is Chaewon!
```

오오 이제 예의범절을 갖춘 개념찬 사람이 되었다!

- - -

어떤 과정을 통해 `decorator` 함수가 `introduce` 에 인사하는 기능을 추가해주는 것인지 살펴보자.

```python
def decorator(func):                        # 1
    def wrapper(*args, **kwargs):           # 4
        print('Hello')                      # 7
        return func(*args, **kwargs)        # 8
    return wrapper                          # 5


def introduce(name):                        # 2
    print(f'My name is {name}!')            # 9


decorated_introduce = decorator(introduce)  # 3
decorated_introduce('Chaewon')              # 6
```
- **#1** : `decorator` 라는 함수가 정의되었다.  
- **#2** : `introduce` 라는 함수가 정의되었다.  
- **#3** : `decorator` 함수에 `introduce` 함수를 인자로 전달하여 호출하였다. 그 출력값을 `decorated_introduce` 라는 변수에 할당하기로 한다.  
- **#4** : `decorator` 함수가 호출되어 내부 명령이 실행된다. `wrapper` 라는 함수가 정의되었다.  
- **#5** : `wrapper` 함수가 호출되지 않은 함수 자체의 상태로 리턴되었다. 따라서 아직 `wrapper` 함수 내의 명령들은 실행되지 않는다.  
- **#6** : `decorated_introduce` 변수에는 `decorator` 함수의 리턴값 즉, 호출되지 않은 `wrapper` 함수가 할당된다.  
따라서 `decorated_introduce('Chaewon')` 는 `wrapper('Chaewon')` 과 같아진다.  
실제로 아래와 같이 확인해보면 `decorated_introduce` 함수에는 `decorator` 함수의 로컬 스콥에 있는 `wrapper` 함수가 할당되어 있는 것을 볼 수 있다.

```python
print(decorated_introduce)
```
```re
<function decorator.<locals>.wrapper at 0x7f769c79f7b8>
```

- **#7** : `wrapper` 함수가 호출되었기 때문에 `wrapper` 함수의 내부 명령이 실행된다. `'Hello'`가 출력된다.
- **#8** : `wrapper` 함수는 자신이 받은 인자를 `decorator` 함수가 받은 함수에 전달하여 호출한 결과를 리턴한다. 즉, `introduce` 함수에 자신이 받은 인자인 `'Chaewon'`을 전달하여 호출한다. 이는 `introduce('Chaewon')` 을 실행하는 것과 같다.
- **#9** : `introduce` 함수가 호출되었으므로 `introduce` 함수의 내부 명령이 실행된다. `My name is Chaewon!` 이 출력된다.

- - -

위의 과정에서는 데코레이터를 적용하기 위해  
`decorated_introduce` 라는 새로운 변수를 만들어 `decorator` 함수에 `introduce` 함수를 전달한 값을 저장하였다.

```python
decorated_introduce = decorator(introduce)
```

이것은 아래와 같이 세련되게 바꿔줄 수 있다.

```python
@데코레이터 함수 이름
def 꾸미고싶은함수이름(args):
```

```python
def decorator(func):                      
    def wrapper(*args, **kwargs):          
        print('Hello')                    
        return func(*args, **kwargs)        
    return wrapper                        

@decorator  # 데코레이터 함수를 적용할 함수 바로 위에 '@데코레이터이름'을 붙여준다.
def introduce(name):                     
    print(f'My name is {name}!')
```

이것은 아래의 명령을 실행하는 것과 동일하다.

```python
introduce = decorator(introduce)
```

이렇게하면 원래의 함수를 호출할 때 데코레이터 함수가 적용된 결과를 출력한다.

```python
introduce('Chaewon')
```

```re
Hello
My name is Chaewon!
```

- - -
## 데코레이터의 활용

- - -

나중에 실제로 데코레이터를 써보면 그 때 예제 추가

- - -

## 여러 개의 데코레이터 중첩 적용

한 함수에 여러 개의 기능을 추가하고 싶을 경우 여러 개의 데코레이터를 적용할 수 있다.

```python
def say_hello(func):
    def wrapper(*args, **kwargs):
        print('Hello')            
        return func(*args, **kwargs) 
    return wrapper


def say_hi(func):                      
    def wrapper(*args, **kwargs):          
        print('Hi')                    
        return func(*args, **kwargs)        
    return wrapper


@say_hello
@say_hi
def introduce(name):                     
    print(f'My name is {name}!')

introduce('Chaewon')
```
```re
Hello
Hi
My name is Chaewon!
```

이 경우 `introduce` 함수에서 가까운 데코레이터부터 `@say_hi`->`@say_hello`의 순서로 실행된다. 아래의 명령을 실행하는 것과 같은 결과를 낸다.

```python
introduce = say_hi(introduce)
introduce = say_hello(introduce)
```

중첩된 데코레이터가 적용되는 과정을 살펴보자. 좀 복잡하다.

```python
def say_hello(func):                    # 1
    def wrapper2(*args, **kwargs):      # 8
        print('Hello')                  # 11
        return func(*args, **kwargs)    # 12
    return wrapper2                     # 9


def say_hi(func):                       # 2
    def wrapper1(*args, **kwargs):      # 5   
        print('Hi')                     # 13
        return func(*args, **kwargs)    # 14    
    return wrapper1                     # 6


@say_hello                              # 7
@say_hi                                 # 4
def introduce(name):                    # 3
    print(f'My name is {name}!')        # 15

introduce('Chaewon')                    # 10
```
- **#1** : `say_hello` 함수 정의

- **#2** : `say_hi` 함수 정의

- **#3** : `introduce` 함수 정의

- **#4** : `say_hi` 함수에 `introduce` 함수를 인자로 전달하면서 호출 

```python
introduce = say_hi(introduce)
```
- **#5** : `say_hi` 함수 내에서 `wrapper1` 함수 정의

- **#6** : `wrapper1` 함수를 호출하지 않고 리턴

```python
introduce = wrapper1(introduce)
```
- **#7** : `say_hello` 함수에 `say_hi` 함수의 출력값 `wrapper1` 을 인자로 전달하면서 호출

```python
introduce = say_hello(wrapper1(introduce))
```

- **#8** : `say_hello` 함수 내에서 `wrapper2` 함수 정의

- **#9** : `wrapper2` 함수를 호출하지 않고 리턴

```python
introduce = wrapper2(wrapper1(introduce))
```
- **#10** : `introduce`에 `'Chaewon'` 을 인자로 전달하면서 호출

```python
introduce('Chaewon')  # 이 introduce는 가장 처음 정의되었던 introduce와 다르다
```

위의 과정들에서 `introduce` 함수가 계속 덮어씌어 졌기 때문에 `introduce('Chaewon')` 은 아래와 같다고 할 수 있다.

```python
wrapper2(wrapper1(introduce))('Chaewon')  # introduce 자리에 wrapper2(wrapper1(introduce))를 그대로 대입
# 여기의 introduce는 가장 처음 정의되었던 introduce이다.
```

- **#11** : `wrapper2` 가 먼저 호출되면서 내부 명령인 `print('Hello')` 실행

```re
Hello
```

- **#12** : `wrapper2` 함수는 자신이 받은 func 즉, `wrapper1(introduce)`에 `'Chaewon'` 을 인자로 전달하여 호출한 뒤 종료된다.

```python
|-------func------|---args---|
wrapper1(introduce)('Chaewon')
```

- **#13** : `wrapper1` 이 호출되면서 내부 명령인 `print('Hi')` 

```re
Hello
Hi
```

- **#14** : `wrapper1` 함수는 자신이 받은 func 즉, `introduce`에 `'Chaewon'` 을 인자로 전달하여 호출한 뒤 종료된다.

```python
|--func--|---args--|
introduce('Chaewon')
```

- **#15** : 드디어 `introduce` 함수에 `'Chaewon'` 이 인자로 전달되면서 내부 명령이 실행된다.

```re
Hello
Hi
My name is Chaewon!
```

- 실제로 아래와 같이 실행해보면 동일한 결과가 출력되는 것을 볼 수 있다.

```python
say_hello(say_hi(introduce))('Chaewon')
```

```re
Hello
Hi
My name is Chaewon!
```

- - -

## @Wraps

아래의 코드를 보자. `decorator1` 과 `decorator2` 는 자신이 받은 함수의 이름과 함께 메세지를 출력해준다.

```python
def decorator2(func):  # 받은 func의 이름을 출력하면서 데코레이터가 적용되었다는 메세지를 출력 
    def wrapper2(*args, **kwargs):
        print(f'{func.__name__} has been decorated again by decorator2')
        return func(*args, **kwargs)
    return wrapper2


def decorator1(func):  # 받은 func의 이름을 출력하면서 데코레이터가 '또' 적용되었다는 메세지를 출력 
    def wrapper1(*args, **kwargs):
        print(f'{func.__name__} has been decorated by decorator1')
        return func(*args, **kwargs)
    return wrapper1


@decorator2
@decorator1
def function():  # 데코레이터를 적용할 함수
    print(f'This is original function')
```

위의 예제에서 `decorator1` 과 `decorator2` 는 모두 `function` 함수에 적용되었다. 그런데 출력 결과가 좀 이상하다. 

```python
function()
```
```re
wrapper1 has been decorated again by decorator2
function has been decorated by decorator1
This is original function
```

분명 두 개의 데코레이터 함수 모두 `function` 함수를 꾸미고 있는데 `decorator2` 의 실행결과에 `function` 함수의 이름이 아닌 `wrapper1` 함수의 이름이 나타난 것을 볼 수 있다. 이는 위의 적용 과정 중 **#7** 에서 보았듯이 두 번째 데코레이터인 `decorator2` 에는 실제로는 `wrapper1(function)` 이 전달되기 때문이다.  
이러한 현상을 방지하기 위해 **`functools` 모듈의 `wraps`** 데코레이터를 사용한다.

```python
from functools import wraps  # functools 모듈로부터 wraps 데코레이터를 가져온다.


def decorator2(func):
    @wraps(func)  # wrapper2에 붙여준다.
    def wrapper2(*args, **kwargs):
        print(f'{func.__name__} has been decorated again by decorator2')
        return func(*args, **kwargs)
    return wrapper2


def decorator1(func):
    @wraps(func)  # wrapper1에 붙여준다.
    def wrapper1(*args, **kwargs):
        print(f'{func.__name__} has been decorated by decorator1')
        return func(*args, **kwargs)
    return wrapper1

@decorator2
@decorator1
def function():
    print(f'This is original function')
```

이렇게 하고나면 아래와 같이 원하던 결과가 나타나는 것을 볼 수 있다.

```python
function()
```
```re
function has been decorated again by decorator2
function has been decorated by decorator1
This is original function
```

`wraps` 데코레이터의 자세한 동작 원리는 잘 모르겠지만 데코레이터가 적용되는 원래의 함수가 가진 네임스페이스의 정보들을 가져와서 `wrapper1` 과 `wrapper2` 에 전달해주는 역할을 하는 것 같다.  
위와 같이 데코레이터를 적용한 `function` 함수의 내부를 살펴보자.
```python
print(dir(function))
```
```re
['__annotations__', '__call__', '__class__', '__closure__', '__code__', '__defaults__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__get__', '__getattribute__', '__globals__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__kwdefaults__', '__le__', '__lt__', '__module__', '__name__', '__ne__', '__new__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__wrapped__']
```

그러면 원래는 없던 `__wrapped__` 라는 속성이 새로 생겨있는 것을 볼 수 있다. 이 속성을 호출해보자.
```python
print(function.__wrapped__)
```
```re
<function function at 0x7fe2ac546400>
```

그 안에는 `function` 함수가 또 있었다. 이 `function` 함수의 내부를 또 살펴보자.
```python
print(dir(function.__wrapped__))
```
```re
['__annotations__', '__call__', '__class__', '__closure__', '__code__', '__defaults__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__get__', '__getattribute__', '__globals__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__kwdefaults__', '__le__', '__lt__', '__module__', '__name__', '__ne__', '__new__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__wrapped__']
```

그 안에는 또 `__wrapped__` 속성이 있다. 이 속성도 한번 호출해보자.

```python
print(function.__wrapped__.__wrapped__)
```
```re
<function function at 0x7fcf1f081378>
```

그 안에는 또 `function` 함수가 들어있었다. 하지만 바로 전의 `function` 함수와는 주소값이 다르다. 이 함수의 내부 영역을 다시 한 번 들여다보자.

```python
print(dir(function.__wrapped__.__wrapped__))
```
```
['__annotations__', '__call__', '__class__', '__closure__', '__code__', '__defaults__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__get__', '__getattribute__', '__globals__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__kwdefaults__', '__le__', '__lt__', '__module__', '__name__', '__ne__', '__new__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__']
```

앗 이번에는 `__wrapped__` 라는 속성이 없다. 이로 미루어보아 `__wrapped__` 속성은 `wraps` 데코레이터를 사용할 때마다 원래 함수의 정보를 가져오기 위해 만들어지는 속성인 것 같다. `wraps` 데코레이터가 두 번 사용되었으므로 `__wrapped__` 함수도 두 겹이 생겨있었던 것 같다. 실제로 `wraps` 데코레이터를 사용하지 않을 경우 `__wrapped__` 속성이 없는 것을 확인 할 수 있다. 나중에 좀 더 자세히 동작 원리를 알고나면 내용 추가를 해야겠다.

- - -

## 데코레이터는 클로저일까?

데코레이터와 클로저는 서로 매우 비슷한 구조를 가지고 있다. 이 둘의 차이점은 데코레이터는 **함수를 인자**로 전달받는다는 점이다.  
그렇다면 클로저 포스트에서 살펴봤던 것처럼 데코레이터도 `cell object` 를 가지고 있을까? 
[클로저 포스트 참고](https://nachwon.github.io/python/2017/09/17/closure.html)

위의 예제를 그대로 사용하여 알아보자. `function` 함수를 열어보면 아래와 같다.
```python
print(dir(function))
```
```
['__annotations__', '__call__', '__class__', '__closure__', '__code__', '__defaults__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__get__', '__getattribute__', '__globals__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__kwdefaults__', '__le__', '__lt__', '__module__', '__name__', '__ne__', '__new__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__','__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__wrapped__']
```

`__closure__` 속성을 호출해보자.
```python
print(function.__closure__)
```
```
(<cell at 0x7f89316ea588: function object at 0x7f893027e400>,)
```

오오 역시나 이번에도 `cell` 오브젝트가 튜플안에 들어있는 것을 볼 수 있다. 이것을 열어보자.
```python
print(dir(function.__closure__[0]))
```
```
['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'cell_contents']
```

역시나 `cell_contents` 라는 속성이 보인다. 이것을 가져와보자.
```python
print(function.__closure__[0].cell_contents)
```
```
<function function at 0x7fd1226bb488>
```

그 안에는 `function` 함수가 들어있었다! 그렇다면 이 함수안에도 `cell_contents` 가 있을까?
```python
print(function.__closure__[0].cell_contents.__closure__[0].cell_contents)
```
```re
<function function at 0x7fd1226bb400>
```

있다! 그런데 위의 `function` 함수와는 다른 함수인 것을 알 수 있다. 혹시 이 `function` 함수도 `cell_contents` 를 가지고 있을까?
```python
print(function.__closure__[0].cell_contents.__closure__[0].cell_contents.__closure__)
```
```re
None
```

`__closure__` 속성이 비어있는 것을 볼 수 있다. 그렇다면 이 `function` 함수가 아무 데코레이터도 적용되지 않은 원래의 `function` 함수 일 것이다.  


따라서 아래의 세 `function` 함수는 모두 다른 함수이다.

```python
print(function)
print(function.__closure__[0].cell_contents)
print(function.__closure__[0].cell_contents.__closure__[0].cell_contents)
```
```re
<function function at 0x7fd1226bb510>
<function function at 0x7fd1226bb488>
<function function at 0x7fd1226bb400>
```

세 `function` 함수들을 다 호출해보면 아래와 같다.

```python
function()
print('')
function.__closure__[0].cell_contents()
print('')
function.__closure__[0].cell_contents.__closure__[0].cell_contents()
```
```re
function has been decorated again by decorator2
function has been decorated by decorator1
This is original function

function has been decorated by decorator1
This is original function

This is original function
```

첫 번째 `function` 이 두 개의 데코레이터가 모두 적용된 `function` 이고  
두 번째 `function` 이 하나의 데코레이터 즉, `decorator1` 만 적용된 단계의 `function` 이고  
마지막 이 원래 처음 정의된 `function` 임을 알 수 있다.  
이는 데코레이터가 적용될 때마다 `function` 함수를 덮어쓰기 때문인 것 같다.  
어쨋든 데코레이터는 함수를 받아서 기억하고 있는 클로저 쯤 되는 것으로 생각할 수 있을 것 같다.

- - -

###### Reference

- 이한영 강사님 github: [https://github.com/Fastcampus-WPS-6th/Python/blob/master/09.%20%ED%95%A8%EC%88%98.md](https://github.com/Fastcampus-WPS-6th/Python/blob/master/09.%20%ED%95%A8%EC%88%98.md)
- School of Web: [http://schoolofweb.net/blog/posts/%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EB%8D%B0%EC%BD%94%EB%A0%88%EC%9D%B4%ED%84%B0-decorator/](http://schoolofweb.net/blog/posts/%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EB%8D%B0%EC%BD%94%EB%A0%88%EC%9D%B4%ED%84%B0-decorator/)
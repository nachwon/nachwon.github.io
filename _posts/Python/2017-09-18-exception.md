---
layout: post
title: '[Python 문법] 예외처리 (Exception)'
excerpt: 예외처리를 통해 좀 더 유연한 Python 프로그램을 만들어보자!
category: Python
tags:
  - Python
  - Exception
---

프로그래밍을 하다보면 뭔가 잘못되었을 때 에러가 나면서 프로그램이 멈춰버린다. 이럴 때 예외처리를 활용하면 프로그램이 멈춰버리지 않고 다른 대응을 하게 하는 것이 가능하다. 에러를 무시하고 계속 진행하거나 특정 에러가 발생하면 특정 명령이 실행되게 할 수도 있고, 심지어는 특정 상황에 일부러 에러를 발생시킬 수도 있다.

- - -

#### 기본적인 형태

Python에서 예외처리에는 `try` 와 `except` 를 사용한다.

```python
try:
    실행 시도할 명령
except:
    에러 발생시 실행할 명령
```

`try` 문 내의 에러들을 실행하던 중 에러가 발생하면 `except` 문 내의 명령들이 실행된다.  
에러 발생이 조건인 `if` 문이라고 생각할 수 있다.  
다음과 같이 에러를 발생시켜 확인해보자.

```python
my_list = [1, 2, 3, 4, 5]
print(my_list[5])
```
```re
Traceback (most recent call last):
  File "/home/che1/Projects/python/python-practice/test.py", line 2, in <module>
    print(my_list[5])
IndexError: list index out of range
```

`IndexError` 는 어떤 시퀀스 자료형을 인덱싱 할 때 범위를 넘어선 인덱스 값이 주어졌을 경우 발생하는 에러이다.  
`my_list` 는 `0` 에서 `4` 까지의 인덱스 값을 가지는데 `5` 가 주어졌으므로 `IndexError` 가 발생한 것이다.  
이를 `try` 와 `except` 로 감싸서 예외처리를 해보자.

```python
try:
    my_list = [1, 2, 3, 4, 5]
    print(my_list[5])
except:
    print('Hello Error!')
```
```re
Hello Error!
```

에러가 발생하면 `Hello Error!` 라는 메세지를 출력하도록 하였다. `IndexError` 가 발생하지 않고 메세지가 출력된 것을 볼 수 있다.  
이렇게 예외처리를 해주면 프로그램이 종료되지 않고 다음 명령들이 실행된다.  
아래와 같이 `try`, `except` 문 다음에 다른 명령을 추가해보자.

```python
try:
    my_list = [1, 2, 3, 4, 5]
    print(my_list[5])
except:
    print('Hello Error!')

print('Program is still running!')
```
```re
Hello Error!
Program is still running!
```

`try`, `except` 문이 끝난 후에도 명령이 계속 실행되는 것을 볼 수 있다.

- - -

#### 특정 에러 처리

아래와 같이 특정 에러가 발생했을 때만 실행할 명령을 지정해줄 수 있다.

```python
try:
    실행 시도할 명령
except 에러이름:
    명시된 이름의 에러가 발생했을 때 실행할 명령
```

위의 예제와 같이 `IndexError` 가 발생하는 상황에서는 아래와 같이 해주면 된다.

```python
try:
    my_list = [1, 2, 3, 4, 5]
    print(my_list[5])
    
except IndexError:
    print('Hello Error!')
```
```re
Hello Error!
```

`except` 옆에 다른 에러의 이름을 입력하면 예외처리가 되지 않는 것을 볼 수 있다.
```python
try:
    my_list = [1, 2, 3, 4, 5]
    print(my_list[5])
    
except ZeroDivisionError:
    print('Hello Error!')
```
```re
Traceback (most recent call last):
  File "/home/che1/Projects/python/python-practice/test.py", line 3, in <module>
    print(my_list[5])
IndexError: list index out of range
```

프로그램은 에러가 발생하면 바로 강제종료되므로 아래와 같이 지정한 에러가 발생하기 전에 다른 에러가 발생한다면 예외처리가 작동하지 않고 프로그램이 종료된다.

```python
try:
    a = 4 // 0
    my_list = [1, 2, 3, 4, 5]
    print(my_list[5])

except IndexError:
    print('Hello Error!')
```
```re
Traceback (most recent call last):
  File "/home/che1/Projects/python/python-practice/test.py", line 2, in <module>
    a = 4 // 0
ZeroDivisionError: integer division or modulo by zero
``` 

`IndexError` 가 발생하기 전에 어떤 수를 0으로 나누면 발생하는 에러인 `ZeroDivisionError` 가 발생해서 예외처리가 작동하지 않고 바로 프로그램이 종료된 것을 볼 수 있다.

- - -

#### 여러 개의 에러 처리


서로 다른 여러 개의 에러가 발생할 것으로 예상되는 경우 `except` 문을 사용해서 각각의 에러에 모두 대처할 수 있다.

```python
try:
    실행 시도할 명령
except 에러1이름:
    에러1 발생시 실행할 명령
except 에러2이름:
    에러2 발생시 실행할 명령
```

`try` 문 안에 서로 다른 두 가지 에러가 발생하도록 한 다음, 두 개의 `except` 문으로 모두 예외처리 해보자.

```python
try:
    a = 4 // 0  # ZeroDivisionError 발생
    my_list = [1, 2, 3, 4, 5]
    print(my_list[5])  # IndexError 발생

except IndexError:
    print('Hello IndexError!')

except ZeroDivisionError:
    print('Hello ZeroDivisionError!')

print('Program is still running!')
```
```re
Hello ZeroDivisionError!
Program is still running!
```

위의 예제의 경우, `ZeroDivisionError` 가 먼저 발생하였고 그 순간 `try` 문이 종료되어 `except ZeroDivisionError:` 아래의 명령이 실행된다. `a = 4 // 0` 아래의 명령들은 아예 실행되지 않았다.  
에러가 발생하는 순서를 바꿔보면 아래와 같이 `IndexError` 가 발생한 시점에 `try` 문을 빠져나온다.
```python
try:
    my_list = [1, 2, 3, 4, 5]
    print(my_list[5])
    a = 4 // 0

except IndexError:
    print('Hello IndexError!')

except ZeroDivisionError:
    print('Hello ZeroDivisionError!')

print('Program is still running!')
```
```re
Hello IndexError!
Program is still running!
```


여러 개의 에러에 대해 같은 명령으로 예외처리를 하고 싶으면 아래와 같이 에러이름을 묶어줄 수 있다.
```python
try:
    my_list = [1, 2, 3, 4, 5]
    print(my_list[5])
    a = 4 // 0

except (ZeroDivisionError, IndexError):
    print('Hello Error!')
```

아무 에러이름도 입력하지 않을 경우 모든 에러에 대해 예외처리가 실행되므로 가능하면 예외처리할 에러를 특정하는 것이 권장된다.

- - -
#### 에러메세지 저장

`as` 를 사용하여 특정 에러가 발생했을 때 발생한 에러의 에러 메세지를 변수에 저정할 수 있다.

```python
try:
    실행 시도할 명령
except 에러이름 as 변수이름:
    명시된 이름의 에러가 발생했을 때 실행할 명령
```

`ZeroDivisionError` 의 에러메세지를 변수 `e` 에 저장하여 출력해보자.

```python
try:
    a = 4 // 0

except ZeroDivisionError as e:
    print(e)
```
```re
integer division or modulo by zero
```

정수를 `0` 으로 나누었다는 메세지가 출력된다.  
실수를 `0` 으로 나누면 어떻게 될까?

```python
try:
    a = 4.0 // 0  # 실수를 0으로 나누어보았다.

except ZeroDivisionError as e:
    print(e)
```
```re
float divmod()
```

똑같이 `ZeroDivisionError` 가 발생했지만 다른 에러메세지가 출력된 것을 볼 수 있다.  
에러메세지 변수 `e` 의 타입을 확인해보면 `ZeroDivisionError` 이라는 클래스의 인스턴스인 것을 볼 수 있다.

```python
try:
    a = 4 // 0

except ZeroDivisionError as e:
    print(type(e))
```
```re
<class 'ZeroDivisionError'>
```

- - -

#### `try` & `else`

예외처리에 `else` 를 사용하여 아무 에러도 발생하지 않았을 경우 실행할 명령을 지정해줄 수 있다.

```python
try:
    a = 4 // 1

except ZeroDivisionError as e:
    print(e)

else:
    print('No Error Found!')
```
```re
No Error Found!
```

`else` 는 예외가 발생하면 실행되지 않는다.

```python
try:
    a = 4 // 0

except ZeroDivisionError as e:
    print(e)

else:
    print('No Error Found!')
```
```re
integer division or modulo by zero
```

- - -

#### `try` & `finally`

예외처리에 `finally` 를 사용하여 에러 발생 여부에 관계없이 예외처리가 끝날 때 항상 실행될 명령을 지정할 수 있다.

```python
try:
    a = 4 // 0

except ZeroDivisionError as e:
    print(e)

finally:
    print('Finally!')
```
```re
integer division or modulo by zero
Finally!
```
`else` 문과는 달리 에러가 발생해도 실행되는 것을 볼 수 있다.

- - -

#### `raise` 에러 발생시키기

`raise` 문을 사용하면 일부러 에러를 발생시킬 수 있다.  
다음은 `my_list` 내의 요소들을 하나씩 돌면서 출력해주는 `for` 문이다. 리스트 내의 요소가 `3` 일 경우 `ZeroDivisionError` 가 나도록 해보았다.

```python
my_list = [1, 2, 3, 4, 5]

for i in my_list:
    print(i)
    if i == 3:
        raise ZeroDivisionError
```
```re
1
2
3
Traceback (most recent call last):
  File "/home/che1/Projects/python/python-practice/test.py", line 6, in <module>
    raise ZeroDivisionError
ZeroDivisionError
```

실제로 어떤 수를 `0`으로 나눈 적이 없지만 `ZeroDivisionError` 가 발생한 것을 볼 수 있다.  
이렇게 일부러 에러를 발생시키고 예외처리하여 특정 상황에 대해 실행할 명령을 사용자의 입맛에 맞게 구성할 수 있다.

- - -

#### 에러 만들기

프로그램을 짜면서 딱히 에러는 아니지만 발생하기 원하지 않는 특정한 상황이 있다면, 그 상황이 발생했음을 알려주는 에러를 직접 만들어 발생시킬 수 있다.  
에러는 아래와 같이 `Exception` 클래스를 상속받는 클래스를 정의하여 만들 수 있다.

```python
class 에러이름(Exception):
    pass
```

오버워치의 영웅이름을 입력하면 그 영웅이 선택되었다는 메세지를 출력하는 함수를 만들어보았다.  
단, 한조를 선택하면 직접 만든 에러인 `HanzoSelected` 에러를 발생시킨다.

```python
class HanzoSelected(Exception):  # HanzoSelected 에러 정의
    pass


def overwatch(hero):
    if hero == '한조':
        raise HanzoSelected
    else:
        print(f'{hero}가 선택되었습니다.')

overwatch('겐지')
overwatch('한조') # HanzoSelected 에러 발생
```
```re
겐지가 선택되었습니다.
Traceback (most recent call last):
  File "/home/che1/Projects/python/python-practice/test.py", line 12, in <module>
    overwatch('한조')
  File "/home/che1/Projects/python/python-practice/test.py", line 7, in overwatch
    raise HanzoSelected
__main__.HanzoSelected
```

한조를 입력하면 `HanzoSelected` 가 발생한 것을 볼 수 있다.
직접 만든 에러를 예외처리 해보자.

```python
try:
    overwatch('겐지')
    overwatch('한조')

except HanzoSelected as e:
    print(e)
```
```re
겐지가 선택되었습니다.
```

음? 분명히 한조를 선택했는데 아무 에러메세지가 나타나지 않는다.  
직접 만든 에러의 오류메세지를 설정하지 않았기 때문이다. 오류메세지를 설정하려면 `HanzoSelected` 클래스 안에 `__str__` 이라는 메서드를 만들어주어야 한다. `__str__` 메서드는 `print` 문으로 출력하였을 때 보여질 것을 정의한다.

```python
class HanzoSelected(Exception):
    def __str__(self):
        return '한조는 안된다 이 악마야!'
```
```python
try:
    overwatch('겐지')
    overwatch('한조')

except HanzoSelected as e:
    print(e)
```
```re
겐지가 선택되었습니다.
한조는 안된다 이 악마야!
```

같은 에러이지만 상황에 따라 다른 에러메세지를 출력하고 싶을 때, 직접 에러 발생시점에서 에러메세지를 정해줄 수 있다.

```python
class HanzoSelected(Exception):
    def __init__(self, msg):  # msg 매개변수로 인자를 하나 받아
        self.msg = msg  # self.msg에 할당하고

    def __str__(self):
        return self.msg  # print 문으로 출력될 때 보여지도록 한다.
```

`위도우` 를 선택해도 에러를 발생하도록 해보자.
```python
def overwatch(hero):
    if hero == '한조':
        raise HanzoSelected('한조는 안된다 이 악마야!')  # 한조를 선택했을 경우 에러메세지
    elif hero == '위도우':
        raise HanzoSelected('위도우도 안된다 이 악마야!')  # 위도우를 선택했을 경우 에러메세지
    else:
        print(f'{hero}가 선택되었습니다.')
```
```python
try:
    overwatch('한조')
except HanzoSelected as e:
    print(e)
```
```re
한조는 안된다 이 악마야!
```

```python
try:
    overwatch('위도우')
except HanzoSelected as e:
    print(e)
```
```re
위도우도 안된다 이 악마야!
```

같은 `HanzoSelected` 에러가 발생했지만 서로 다른 에러메세지가 출력되는 것을 볼 수 있다. 이는 실수를 `0` 으로 나누었을 때와 정수를 `0` 으로 나누었을 때의 `ZeroDivisionError` 에러 메세지가 달랐던 것과 같은 맥락으로 이해하면 될 듯 하다.

- - -

#### 에러의 종류

Python의 모든 내장 에러들은 `BaseException` 클래스의 서브클래스들이다.

>*exception* **BaseException**
>
>: The base class for all built-in exceptions. It is not meant to be directly inherited by user-defined classes (for that, use Exception). If str() is called on an instance of this class, the representation of the argument(s) to the instance are returned, or the empty string when there were no arguments.


시스템 에러를 제외한 모든 내장 에러들은 `Exception` 클래스의 서브클래스들이다. 에러를 만들 때는 이 클래스를 상속받아 오는 것이다. 

>*exception* **Exception**
>
>: All built-in, non-system-exiting exceptions are derived from this class. All user-defined exceptions should also be derived from this class.

아래는 Python 내장 에러들을 트리 구조로 나타낸 것이다.

```
BaseException
 +-- SystemExit
 +-- KeyboardInterrupt
 +-- GeneratorExit
 +-- Exception
      +-- StopIteration
      +-- StopAsyncIteration
      +-- ArithmeticError
      |    +-- FloatingPointError
      |    +-- OverflowError
      |    +-- ZeroDivisionError
      +-- AssertionError
      +-- AttributeError
      +-- BufferError
      +-- EOFError
      +-- ImportError
           +-- ModuleNotFoundError
      +-- LookupError
      |    +-- IndexError
      |    +-- KeyError
      +-- MemoryError
      +-- NameError
      |    +-- UnboundLocalError
      +-- OSError
      |    +-- BlockingIOError
      |    +-- ChildProcessError
      |    +-- ConnectionError
      |    |    +-- BrokenPipeError
      |    |    +-- ConnectionAbortedError
      |    |    +-- ConnectionRefusedError
      |    |    +-- ConnectionResetError
      |    +-- FileExistsError
      |    +-- FileNotFoundError
      |    +-- InterruptedError
      |    +-- IsADirectoryError
      |    +-- NotADirectoryError
      |    +-- PermissionError
      |    +-- ProcessLookupError
      |    +-- TimeoutError
      +-- ReferenceError
      +-- RuntimeError
      |    +-- NotImplementedError
      |    +-- RecursionError
      +-- SyntaxError
      |    +-- IndentationError
      |         +-- TabError
      +-- SystemError
      +-- TypeError
      +-- ValueError
      |    +-- UnicodeError
      |         +-- UnicodeDecodeError
      |         +-- UnicodeEncodeError
      |         +-- UnicodeTranslateError
      +-- Warning
           +-- DeprecationWarning
           +-- PendingDeprecationWarning
           +-- RuntimeWarning
           +-- SyntaxWarning
           +-- UserWarning
           +-- FutureWarning
           +-- ImportWarning
           +-- UnicodeWarning
           +-- BytesWarning
           +-- ResourceWarning
```

각 에러들의 자세한 사항은 [공식문서](https://docs.python.org/3/library/exceptions.html)를 참고하면 된다.
- - -

###### Reference
이한영 강사님 github: [https://github.com/Fastcampus-WPS-6th/Python/blob/master/13.%20%EC%98%88%EC%99%B8%EC%B2%98%EB%A6%AC.md](https://github.com/Fastcampus-WPS-6th/Python/blob/master/13.%20%EC%98%88%EC%99%B8%EC%B2%98%EB%A6%AC.md)  
점프 투 파이썬: [https://wikidocs.net/30](https://wikidocs.net/30)  
Python 에러 공식문서: [https://docs.python.org/3/library/exceptions.html](https://docs.python.org/3/library/exceptions.html)
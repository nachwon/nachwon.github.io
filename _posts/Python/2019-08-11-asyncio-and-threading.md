---
layout: post
title: '[Python] asyncio 를 활용한 동시성 - 1. threading 과의 비교'
excerpt: asyncio 라이브러리에 대해서 알아보자.
project: false
tags:
  - Python
  - asyncio
  - threading
  - concurrency
category: Python
---

*Fluent Python 18장 내용의 일부를 요약한 것임.*  
*Python 3.6 버전을 사용함.*

파이썬에는 동시적인 처리를 위한 몇 가지 라이브러리들이 있는데, 그 중 코루틴을 활용하는 asyncio 에 대해서 알아보고자 한다.

- - -
# Thread 를 사용한 동시성과의 비교

보통 동시에 여러가지 작업을 처리하게 하려면 별도의 쓰레드를 생성해서 작업을 할당하는데, 파이썬에서는 GIL(Global Interpreter Lock)으로 인해 한 번에 한 쓰레드만 파이썬 코드를 실행할 수 있기 때문에 여러 쓰레드를 쓰는 것이 오히려 비효율적이다.  

단, 위 내용은 CPU bound 작업을 할 때에만 해당하는데, 파이썬은 I/O bound 작업들을 할 때에는 GIL 을 해제하여 다른 쓰레드가 이어서 작업을 진행할 수 있도록 되어있어 I/O bound 작업들에 대해서는 여러 개의 쓰레드를 사용해서 효율적인 동시 처리가 가능하기 때문이다.

파이썬에서는 `threading` 라이브러리나 `concurrent` 라이브러리를 이용한 멀티쓰레딩이 가능하고, 3.4 부터는 generator 에서 부터 진화해 오던 코루틴을 이용한 비동기 라이브러리인 `asyncio` 가 추가되어서 좀 더 쉬운 동시적인 처리를 지원하게 되었다.

asyncio 는 threading 과는 달리 하나의 쓰레드를 사용하여 작업들을 동시적으로 처리한다.

---

## threading을 사용한 예제

asyncio 와 기존의 threading 과의 비교를 위해서 어떤 오랜 시간이 걸리는 I/O bound 작업을 처리하는 동안에 문자열 `|/-\` 을 순차적으로 보여주는 spinner 를 띄워주는 간단한 프로그램을 만들어 볼 것이다.

```python
import threading
import itertools
import time
import sys

class Signal:  # 1
    go = True

def spin(msg, signal):  # 2
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):  # 3
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))
        time.sleep(.1)
        if not signal.go:  # 4
            break
    write(' ' * len(status) + '\x08' * len(status))

def slow_function():  # 5
    # pretend waiting a long time for I/O
    time.sleep(3)  # 6
    return 42

def supervisor():  # 7
    signal = Signal()
    spinner = threading.Thread(target=spin,
                               args=('thinking!', signal))
    print('spinner object:', spinner)  # 8
    spinner.start()  # 9
    result = slow_function()  # 10
    signal.go = False  # 11
    spinner.join()  # 12
    return result

def main():
    result = supervisor()  # 13
    print('Answer:', result)

if __name__ == '__main__':
    main()

```

1. `Signal` 클래스는 쓰레드 외부에서 쓰레드를 제어하기 위한 용도로 사용될 클래스이다.
2. `spinner` 함수는 별도의 쓰레드에서 실행할 함수이다.
3. `spinner` 함수는 문자열 `|/-\` 을 순차적으로 `thinking` 이라는 문자열과 함께 무한히 출력한다. 기존 출력을 지우고 새로 출력하기 때문에 막대기가 회전하는 것처럼 보이게 된다.
4. `signal.go` 값이 `False` 이면 루프를 멈추고 나온다.
5. 가상의 시간이 오래걸리는 I/O bound 작업을 처리하는 함수이다.
6. `time.sleep` 을 호출하면 주어진 시간동안 메인 쓰레드는 블락된다. 하지만 그 동안 GIL이 해제되어 다른 쓰레드가 작업을 진행할 수 있게 된다.
7. `supervisor` 함수는 별도의 쓰레드를 생성해서 `spinner` 를 처리하도록 하고, 이어서 `slow_function` 작업을 처리한다. `slow_function` 의 처리가 끝나면 별도의 쓰레드에서 돌고있는 `spinner` 함수의 루프도 종료시킨다.
8. 별도로 생성된 thread 오브젝트를 출력한다. 대략 `<Thread(Thread-1,
initial)>` 와 같이 출력된다.
9. 별도로 생성된 쓰레드를 실행시킨다.
10. `slow_function` 을 실행시킨다. 이 부분에서 메인 쓰레드는 result 값을 받을 때까지 블락되어 있다. 이 동안 별도의 쓰레드에 넘겨진 `spinner` 함수가 실행된다.
11. `slow_function` 의 실행이 끝나면 `signal.go` 의 값을 `False` 로 바꾸어주어서 `spinner` 함수의 루프가 종료되도록 한다.
12. 별도로 생성했던 쓰레드가 종료되는 것을 기다린다.
13. `supervisor` 함수를 실행하는 엔트리 포인트.

threading 라이브러리의 Thread 객체에는 외부에서 쓰레드를 제어할 수 있는 API가 없기 때문에, 위 예제에서는 직접 `Signal` 이라는 객체를 만들어서 쓰레드를 종료시켜주었다.

---

## asyncio를 사용한 예제

이제 위 예제와 똑같은 일을 하는 프로그램을 `asyncio` 로 만들어보자.

```python
import asyncio
import itertools
import sys

async def spin(msg):
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))
        try:
            await asyncio.sleep(.1)  # 1
        except asyncio.CancelledError:  # 2
            break
    write(' ' * len(status) + '\x08' * len(status))

async def slow_function():  # 3
    await asyncio.sleep(3)  # 4
    return 42

async def supervisor():  # 5
    spinner = asyncio.ensure_future(spin('thinking!'))  # 6
    print('spinner object:', spinner)  # 7
    result = await slow_function()  # 8
    spinner.cancel()  # 9
    return result

def main():
    loop = asyncio.get_event_loop()  # 10
    result = loop.run_until_complete(supervisor())  # 11
    loop.close()
    print('Answer:', result)

if __name__ == '__main__':
    main()
```

1. `time.sleep` 대신 `asyncio.sleep` 을 활용하면 이벤트 루프를 블락하지 않고 sleep 할 수 있다.
2. sleep 이 끝난 시점에 `asyncio.CancelledError` 가 발생하면, 이는 테스크가 취소된 것이며, 따라서 루프를 종료해준다.
3. `slow_function` 은 이제 코루틴이 되었다. `await` 문을 사용해서 I/O bound 작업을 하는 동안 이벤트 루프를 진행시킨다.
4. `await asyncio.sleep(3)` 부분에서는 3초동안 I/O 작업(sleep)이 끝나기를 기다린다. 그 동안 이벤트 루프는 계속 진행되며, 작업이 끝나고 나면 `slow_function `코루틴이 이 부분에서 이어서 진행된다.
5. `supervisor` 함수도 코루틴이 되었다.
6. `asyncio.ensure_future` 는 코루틴이 실행되도록 등록하고 `Task` 객체를 즉시 반환 한다.
7. `spin` 함수를 실행하도록 등록한 `Task` 객체의 정보를 출력한다. 다음과 비슷하게 출력된다.  
`<Task pending coro=<spin() running at spinner_asyncio.py:12>>`
8. `slow_function` 을 실행한다. 이 부분 또한 `await` 를 사용하기 때문에 `slow_function` 안의 `asyncio.sleep` 의 실행이 종료될 때까지 이벤트 루프가 진행되도록 한다.
9. `asyncio.sleep(3)` 의 실행이 끝나면 `await asynciio.sleep(3)` 부분에서 코루틴이 재개하며, result 를 리턴해서 `slow_function` 의 실행이 끝나면, 마찬가지로 `result = await slow_function()` 부분에서 `supervisor` 코루틴이 재개된다. `spinner.cancel` 로 인해서 `spin` 코루틴의 `await asyncio.sleep(.1)` 부분에서 `CancelledError` 가 발생한다. 이 에러를 잡아서 처리하여 취소를 거부하도록 만들 수도 있다.
10. 이벤트 루프를 가져온다.
11. 이벤트 루프에 `superviser` 를 넣어서 끝날 때까지 실행시킨다.

- - -

## asyncio 와 threading 의 차이점

위 두 예제를 통해서 알 수 있는 `asyncio` 와 `threading` 라이브러리의 차이점을 요약하면 다음과 같다.

- `asyncio.Task` 와 `threading.Thread` 는 거의 대등하다. `Task` 객체는 `gevent` 와 같은 협업적 멀티태스킹을 구현하는 라이브러리에서의 그린 쓰레드와 같다.
- `asyncio` 의 `Task` 객체는 코루틴을 구동(drive)하고, `threading` 의 `Thread` 객체는 콜러블을 실행시킨다.
- `Thread` 객체는 직접 생성할 수 있는 반면, `Task` 객체는 직접 생성하지 않고, `ensure_futuer` 함수를 사용해서 생성해야한다.
- `Task` 객체가 생성되면, 이 객체는 이미 `ensure_future` 등에 의해서 실행이 예약되어 있는 상태이지만, `Thread` 객체는 `start()` 메서드를 호출해야 실행된다.
- 쓰레드 버전의 `slow_function` 은 그냥 보통 함수이고, 스레드가 직접 호출하지만, 코루틴 버전의 `slow_function` 은 `await` 로 구동하는 코루틴 객체이다.
- `Thread` 객체는 외부에서 쓰레드 내부를 제어할 수 있도록 해주는 API가 없다. 스레드를 아무 때나 중단시키면 시스템 상태의 무결성이 훼손될 수 있기 때문이다. 반면 `Task` 객체는 코루틴 안에서 `CancelledError` 를 발생시키는 `Task.cancel()` 메서드가 있다. 코루틴은 중단되었던 `await` 문에서 예외를 처리할 수 있다.
- `supervisor` 코루틴은 반드시 `loop.run_until_complete()` 에 의해서 실행되어야 한다.

쓰레드를 사용해서 여러 작업을 동시에 처리하려고 할 때에는 여러가지 어려움이 많이 따른다. 디버깅의 어려움도 있고, 서로 다른 쓰레드들이 같은 자원에 접근할 때 발생할 수 있는 레이스 컨디션이나 데드락과 같은 문제들을 모두 고려하면서 프로그래밍을 하는 것은 매우 힘든 일이다. 파이썬에 GIL이 있는 것도 이런 문제들 때문인데, 코루틴 기반 동시 처리에서는 이런 문제를 걱정할 필요가 없다.

코루틴은 항상 반드시 하나의 코루틴만 실행되기 때문에, 여러 쓰레드들을 사용할 때처럼 락을 관리할 필요가 없다. 다른 코루틴으로 제어권을 넘겨주려면 `await` 문을 사용하여 언제든지 넘겨줄 수 있다. 그렇기 때문에 코루틴은 안전하게 취소할 수 있다. 코루틴이 멈춰있던 `await` 문에서 `CancelledError` 를 처리해서 마무리하면 된다.

---
#### Reference
Fluent Python Chapter 18 - concurrency with asyncio
---
layout: post
title: '[Python] Python 동시 프로그래밍'
excerpt: threading, asyncio, multiprocessing 의 비교
project: false
tags:
  - Python
  - asyncio
  - threading
  - multiprocessing
  - concurrency
category: Python
---

이 포스트는 [원문](https://realpython.com/python-concurrency/#what-is-concurrency)을 번역 및 요약한 것임.

- - -

# 파이썬의 동시성

파이썬에서는 쓰래드, 태스크, 프로세스를 사용해서 동시적으로 작업들을 처리할 수 있다. 고수준에서보면 세 가지 방법 모두 어떤 작업들을 동시에 처리한다는 점이서 비슷해보이지만, 내부를 파보면 서로 조금씩 다른점이 있다.

파이썬에는 쓰래드를 사용하는 `threading` 모듈, 태스크를 사용하는 `asyncio` 모듈, 그리고 프로세스를 사용하는 `multiprocessing` 모듈이 있는데 이 중 정말로 완전히 동시에 `병렬적으로` 작업을 처리하는 것은 multiprocessing 뿐이다. threading과 asyncio 모듈은 모두 하나의 프로세서를 사용하기 때문에 한 번에 하나씩 실행할 수 밖에없다. 다만, 서로 돌아가면서 교묘하게 진행 순서를 겹쳐서 전체 작업 시간을 줄이는 것이다. 이런 방법은 엄밀하게는 여러 작업들을 한꺼번에 같은 시간에 처리하는 것은 아니지만, 여전히 동시적인 작업 처리라고 부른다.

threading과 asyncio는 동시적인 작업을 할 때 쓰래드 또는 작업들간에 서로 돌아가면서 처리하는 방법에서 큰 차이가 있다. threading 모듈에서는 실행되고 있는 각 쓰레드를 운영체제가 언제든지 멈추고 다른 쓰레드를 진행시킬 수 있다. 운영체제가 쓰래드를 선점할 수 있기 때문에, 이걸 `선점형 멀티태스킹(pre-emptive multitasking)` 이라고 한다.

선점형 멀티태스킹은 쓰래드안의 코드가 아무것도 안해도 알아서 스위칭이 일어나기 때문에 편한점도 있지만, 언제든지 스위칭이 일어날 수 있다는 점에서는 다루기 어려워질 수 있다. `x = x + 1` 같은 코드를 돌리다가도 스위칭이 일어날 수 있기 때문이다.

반면에, asyncio 모듈은 `협력식 멀티태스킹(cooperative multitasking)` 방식을 사용한다. 이 방식은 각 태스크가 직접 언제 스위칭될 준비가 되었는지 명시해주어야 한다. 이 말은 결국 asyncio를 사용하려면 코드를 좀 수정해줘야한다는 뜻이기도 하다.

이 방식의 장점은 언제 다른 태스크로 넘어갈지를 항상 알 수 있다는 점이다. 다른 태스크로 넘어갈 수 있는 지점에 이르기 전까지는 절대로 넘어갈일이 없다. 

- - -

# 병렬성?

지금까지 한 프로세서에서 이루어지는 동시성에 대해서 잠깐 살펴보았는데, 그렇다면 나머지 놀고 있는 다른 프로세서들은 어떻게 써먹을 수 있을까? 이런 경우에는 `multiprocessing` 모듈이 답이다.

multiproccessing 모듈을 사용하면, 파이썬은 완전히 새로운 프로세스를 생성한다. 새로운 프로세스를 생성한다는 것은 완전히 별개의 자원들을 할당받은 새로운 파이썬 인터프리터를 실행하는 것으로 볼 수 있다.

완전히 다른 프로세스이기 때문에 다른 CPU 코어를 사용해서 실행할 수 있고, 이 말은 즉, 완전히 같은 시간에 `병렬적으로` 실행할 수 있다는 뜻이다. 이런 식으로 실행하는데에는 몇 가지 복잡한 문제들이 따르긴 하는데, 파이썬은 이 문제들을 대체로 잘 처리하는 편이다.

이제 동시성과 병렬성에 대해 알았으니 그 차이를 정리해보자.

| 동시성 유형                     | 스위칭 결정 방법                                       | 프로세서 수 |
|---------------------------------|--------------------------------------------------------|-------------|
| 선점형 멀티태스킹 ( threading)  | 운영체제가 언제 스위칭할지를 결정함.                   | 1           |
| 협력식 멀티태스킹 ( asyncio)    | 태스크가 언제 스위칭할지를 결정함.                     | 1           |
| 멀티프로세싱 ( multiprocessing) | 프로세스들이 서로 다른 프로세서에서 병렬적으로 실행됨. | 다수        |

이 서로 다른 방법들을 적절히 잘 어울리는 곳에 사용하면 프로그램의 성능을 크게 올릴 수 있다!

- - -

# 언제 동시성이 빛을 발하는가?

동시성은 두 가지 경우에 큰 변화를 가져올 수 있는데, 바로 `CPU 바운드 작업` 과 `I/O 바운드 작업` 이 그 두 경우이다.

I/O 바운드 작업은 프로그램 외부에서 이루어지는 input/output 작업이 이루어질 때까지 프로그램 내부에서는 기다리고 있어야하기 때문에 프로그램이 느려지게 만들 수 있다. 이런 문제는 프로그램이 CPU 보다 훨씬 느린 것들을 사용해야할 때 주로 발생하는데, 그런 느린 것들의 대부분을 차지하는 것은 바로 파일 시스템과 네트워크 연결이다.

![iobound](/img/python/iobound.png)

위 그림에서 파란색 박스는 프로그램이 진행 중인 시간을 나타내고, 빨간색 박스는 I/O 바운드 작업이 끝날 때까지 대기하는 시간을 나타낸다. 실제로 빨간색 박스는 저 파란색 박스보다 훨씬 크며 프로그램은 대부분의 시간을 I/O 바운드 작업을 대기하는데 보내게 된다.

반대로, 네트워크나 파일에 엑세스하는 작업 없이 계산 작업만 하는 프로그램들도 있는데 이런 작업들을 CPU 바운드 작업이라고 한다. 왜냐하면 프로그램의 속도를 결정짓는 자원이 CPU이기 때문이다.

![cpubound](/img/python/cpubound.png)

좀 있다 살펴볼 예제를 통해 알게되겠지만, 여러가지 동시적 처리방법들은 CPU 바운드이냐, I/O 바운드이냐에 따라 프로그램에 도움이 될 수도 있고, 오히려 악화시킬 수도 있다. 동시성을 프로그램에 도입하는 것은 추가적인 공수가 들고, 프로그램의 복잡도를 올리는 작업이기 때문에 이렇게 해서 도입한 동시성이 실제로 프로그램의 성능을 개선하는데 도움이 되는지 잘 따져보아야한다.

| I/O 바운드 프로세스                                                                               | CPU 바운드 프로세스                                             |
|---------------------------------------------------------------------------------------------------|-----------------------------------------------------------------|
| 프로그램이 네트워크 커넥션, 하드디스크 등과 같은 외부 장치들과 통신하는데 대부분의 시간을 보낸다. | 프로그램이 CPU를 사용하는 계산작업에 대부분의 시간을 쓴다.      |
| 외부 장치의 응답을 기다리는 대기시간들을 어떻게 잘 겹치면 전체적인 속도를 개선할 수 있다.         | 같은 시간에 더 많은 계산을 하게 만들어서 속도를 개선할 수 있다. |

- - -

# I/O 바운드 프로그램 속도 개선하기

먼저 I/O 바운드 프로그램의 속도를 개선하는 방법을 알아보기 위해서 웹사이트 몇개로부터 페이지를 다운로드하는 프로그램을 만들어보자.

### 순차적 버전

먼저 동시성이 전혀 없는 프로그램으로 웹페이지를 다운로드 해보자.

```python
import requests
import time


def download_site(url, session):
    with session.get(url) as response:
        print(f"Read {len(response.content)} from {url}")


def download_all_sites(sites):
    with requests.Session() as session:
        for url in sites:
            download_site(url, session)


if __name__ == "__main__":
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 80
    start_time = time.time()
    download_all_sites(sites)
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} in {duration} seconds")
```

굉장히 간단한 프로그램이다. `download_site` 함수가 그냥 주어진 URL로부터 내용을 다운받아와서 그 크기를 출력한다. 네트워크 통신을 위해서 `requests` 모듈의 `Session` 객체를 사용하였다. 그냥 바로 `get()` 메서드를 사용할 수도 있지만, Session 객체를 만들어서 사용하면 몇 가지 네트워킹 트릭들을 내부적으로 수행해주기도 하고, 속도를 높이는데도 유용하다.

`download_all_sites` 함수는 사이트 URL 목록을 받고, Session 객체를 생성하여 `download_site` 함수에 넘겨주어 목록을 하나씩 돌면서 순차적으로 데이터를 다운받게 한다. 비교를 위해 작업이 모두 끝나면 시간이 얼마나 걸렸는지 출력하도록 하였다.

이 프로그램은 위에서 보았던 I/O 바운드 작업을 시각화한 그림과 거의 흡사한 과정으로 실행된다.

- - -

#### 순차적 버전의 장점
무엇보다도 읽고 이해하기 쉽다. 그렇기 때문에 당연히 디버깅도 쉽다. 단 하나의 흐름이 있기 때문에 생각하기도 쉽고, 어떻게 작동할지 예측하기도 쉽다.

- - -

#### 순차적 버전의 문제
가장 큰 문제는 느리다는 점이다. 아래는 위 프로그램을 실행한 결과의 예이다.

```shell
$ ./io_non_concurrent.py
   [most output skipped]
Downloaded 160 in 14.289619207382202 seconds
```

느리다는 것이 항상 문제가 되는건 아니다. 예를 들어 한 번 돌리는데 2초 정도 걸리는 프로그램이 자주 실행되는 것도 아니라면, 동시성이 별로 필요 없다고 봐도 될 것이다.

그런데 만약 자주 실행되어야 하는 프로그램이라면? 또는 한 번 실행하는데 몇 시간이 걸리는 프로그램이라면? 이런 경우에는 동시성을 도입하는 것을 고려해보아야 한다.


- - -

### threading 버전

threading 모듈을 사용해서 위의 프로그램을 개선시켜보자. threading 버전으로 프로그램을 만드는 데는 그냥 순차적인 프로그램을 만드는 것 보다 좀 더 많은 노력이 들어간다. 그렇지만 놀랍게도 정말 약간의 추가적인 코딩만 있으면 된다.

다음은 위의 프로그램을 threading 모듈을 사용해서 개선한 버전이다.

```python
import concurrent.futures
import requests
import threading
import time


thread_local = threading.local()


def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def download_site(url):
    session = get_session()
    with session.get(url) as response:
        print(f"Read {len(response.content)} from {url}")


def download_all_sites(sites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(download_site, sites)


if __name__ == "__main__":
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 80
    start_time = time.time()
    download_all_sites(sites)
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} in {duration} seconds")
```

threading 모듈을 추가하려면, 큰 틀은 그대로 가져가면서 몇 가지만 약간 바꿔주면 된다. `download_all_sites()` 함수가 사이트 목록에 있는 사이트 하나마다 `download_site` 함수를 실행하는 대신, 뭔가 더 복잡한 구조로 바뀌었다.

이 버전에서는 `ThreadPoopExecutor` 라는 뭔가 복잡해보이는 것을 생성하였는데, 이걸 쪼개보면 `Thread` + `Pool` + `Executor` 이다.

`Thread` 가 뭔지는 이미 안다. 하나의 흐름이라고 생각할 수 있다. `Pool` 부분이 흥미로워지기 시작하는 부분인데, 이 객체는 각각 동시에 실행될 수 있는 쓰래드의 묶음 같은 것을 만들어 낸다. 마지막으로 `Executor` 는 풀에 있는 각각의 쓰래드가 언제 어떻게 실행될지를 제어한다.

`ThreadPoolExecutor` 는 컨텍스트 매니저로 구현되어 있어서 `with` 문을 사용하여 간편하게 쓰래드들을 생성하고 해제할 수 있다.

ThreadPoolExecutor를 만들고나면 `map()` 메서드를 사용할 수 있다. 이 메서드는 iterable 객체 하나와 객체 안의 각 항목에 적용시킬 함수 하나를 받는다. 여기서 멋진 점은, 각 항목에 함수를 실행시키는 작업이 쓰래드들을 이용하여 동시적으로 실행된다는 점이다.

다른 언어를 쓰던 사람이나 Python 2 버전을 사용하던 사람들은 `Queue`나 `Thread.start()`, `Thread.join()` 같은 평소에 쓰래드를 사용할 때 자주 쓰던 객체나 메서드들은 어디있는지 의아해 할 것이다.

그런 도구들은 여전히 그대로 있으며, 쓰래드에 대한 정밀한 제어가 필요하다면 그것들을 직접 사용해서 구현할 수도 있다. 하지만 파이썬 3.2 버전에서 `Executors` 라는 고수준의 추상화된 객체가 추가되었으며, 정밀한 제어가 필요한 경우가 아니라면 그냥 이 객체를 사용하면 된다.

또 다른 흥미로운 차이점은 각각의 쓰래드가 각자의 `request.Session()` 객체를 생성해서 써야한다는 점이다. 확실하지는 않지만, 이 [이슈](https://github.com/requests/requests/issues/2766)에 의하면 각 쓰래드마다 별도의 Session 객체를 생성해주어야 하는 것으로 보인다.

threading 을 사용하는데 따르는 흥미로우면서도 어려운 부분이 이런 부분인데, 위에서 알아보았듯이 선점형 멀티태스킹에서는 운영체제가 한 작업을 멈추고 다른 작업을 진행시키는 등의 제어를 하다보니, 쓰레드들이 공유하는 데이터들이 `쓰래드안전(thread-safe)`하거나 그게 아니라면, 보호되어야 할 필요가 있다. 불행히도 requests의 Session 객체는 쓰래드안전하지 않다.

데이터가 어떤 데이터인지, 어떻게 쓰이는지에 따라 쓰래드안전하게 데이터를 가져오는 다양한 방법들이 있다. 그 중 하나는 파이썬의 `queue` 모듈에 있는 `Queue` 객체 같은 쓰래드안전한 데이터 구조를 사용하는 것이다.

이런 객체들은 `threading.Lock` 같은 저수준 요소들을 사용해서 한 번에 한 쓰래드만 코드 조각 또는 메모리 조각에 접근할 수 있게 제한한다. 그리고 `ThreadPoolExecutor` 를 사용하면 이 방법을 간접적으로 사용하게 된다.

예제에서 사용한 또다른 방법은 `thread local storage` 라는 것을 사용하는 방법이다. `Threading.Local()` 은 글로벌 변수처럼 생겼지만 각 쓰래드에 특정된 어떤 객체를 만들어낸다. 예제에서는 `threadLocal` 변수와 `get_session()` 함수를 사용해서 이 부분을 구현하였다.

```python
threadLocal = threading.local()


def get_session():
    if not hasattr(threadLocal, "session"):
        threadLocal.session = requests.Session()
    return threadLocal.session
```

`ThreadLocal` 객체는 `threading` 모듈에 포함되어 있으며, 딱 이러한 용도로 사용되기 위해 만들어졌다. 좀 이상하게 보이겠지만, 전역적으로 하나만 만들어 놓으면 내부적으로 각각의 쓰래드마다 서로 다른 데이터에 접근하도록 처리해준다.

`get_session` 함수가 실행되면, `session` 어트리뷰트를 `threadLocal` 객체로 부터 찾아 가져오는데, 각 쓰래드마다 별도의 객체를 가져오게 된다. 그래서 각 쓰래드는 처음 한번 session 어트리뷰트에 requests.Session 객체를 만들어 넣어 놓으면, 이에서 실행되는 작업들에서는 각각 만들어 놓았던 Session 객체를 다시 가져와 재사용하게 된다.

마지막으로 짚고 넘어갈 점은 쓰래드의 갯수를 정하는 것이다. 예제에서는 5 개의 쓰래드를 사용하는 것을 볼 수 있는데, 이 숫자를 조정하면서 전체적인 성능이 어떻게 변하는지 실험해보면 좋다. 다운로드할 사이트 하나마다 하나씩 쓰래드를 생성하는게 제일 좋지 않을까 생각할 수 도 있는데, 적어도 내 컴퓨터에서는 아니었다. 대략 5개에서 10개 사이가 가장 높은 성능 향상을 가져왔다. 10개보다 더 많이 생성하면, 쓰래드를 만들고 없애는데 드는 오버헤드 때문에 실행 속도가 상쇄된다.

적절한 쓰래드 수는 태스크에 따라 다르며, 몇 번의 실험을 통해서 정해야 한다.

- - -

#### threading 버전의 장점

가장 눈에 띄게 바뀐 점은 바로 속도이다. 순차적 버전이 14초 정도 걸린 것에 비하면 엄청난 발전이다.

```shell
$ ./io_threading.py
   [most output skipped]
Downloaded 160 in 3.7238826751708984 seconds
```

다음은 threading 버전의 실행 시간을 나타낸 다이어그램이다.

![threading](/img/python/threading.png)

여러 개의 웹사이트에 요청을 보내기 위해 여러 개의 쓰래드를 사용해서, 각 쓰래드가 I/O 작업을 대기하는 시간을 겹치게 만들었다. 이는 결국 전체적인 속도 향상으로 이어진다.

- - -

#### threading 버전의 문제점

일단 예제에서 봤듯이 코드를 좀 더 써야하고, 쓰래드간에 공유되는 데이터가 어떤게 있는지 잘 생각해야한다.

쓰래드들은 미묘하고 알아차리기 어려운 방법으로 서로 상호작용한다. 이런 상호작용은 무작위로, 간헐적으로 일어나는 버그의 원인이 되는 `경쟁 상태(Race Condition)` 을 발생시킬 수 있다. 이런 버그는 굉장히 디버깅하기 어렵다.

- - -

### Asyncio 버전

- - -

#### Asyncio의 원리

Asyncio의 전반적인 컨셉은 `이벤트 루프 (event loop)` 라고 하는 하나의 파이썬 객체가 각 태스크를 언제 어떻게 실행시킬지를 제어하는 것이다. 이벤트 루프는 각 태스크가 어떤 상태에 있는지 알고 있다. 실제로는 태스크들이 여러가지 상태에 있을 수 있지만, 지금은 좀 단순화해서 두 가지 상태만 있다고 가정해보자.

하나는 준비 상태이며, 이 상태에 있는 태스크는 해야할 작업이 있으며, 그 작업을 실행할 준비가 되어있다는 뜻이다. 또 하나는 대기 상태인데 이 상태에 있는 태스크는 네트워크 통신 같은 외부 작업이 끝나기를 대기하는 상태이라는 뜻이다.  

(단순화 한)이벤트 루프는 각 상태별 태스크 목록을 관리한다. 준비 상태에 있는 태스크를 하나 꺼내서 실행시키는데, 이 태스크는 직접 이벤트 루프에게 다시 제어권을 반환할 때까지 완전한 제어권을 가지게 된다.

실행 중이던 래스크가 이벤트 루프에 제어권을 넘기면, 이벤트 루프는 그 테스크를 준비 또는 대기 목록에 다시 추가하고, 대기 목록의 태스크들을 확인하여 I/O 작업이 끝나서 준비 상태인 태스크가 있는지 확인한다. 준비 목록에 있는 태스크들은 아직 실행된 적이 없으므로 그대로 준비 상태이다.

모든 태스크가 상태별로 재분류되었으면, 이벤트 루프가 다음 실행할 테스크를 뽑는다. 새로 뽑은 태스크에 대해서 앞의 과정들을 반복하게된다. 이벤트 루프는 가장 오랫동안 대기 상태였던 태스크를 뽑아서 실행시킨다. 이벤트 루프가 끝날 때까지 이 과정이 계속 반복된다.

asyncio의 중요한 포인트는, 태스크가 직접 의도적으로 제어권을 넘길 때까지 절대로 스위칭이 일어나지 않는다는 점이다. 절대로 실행 중에 방해받지 않는다. 이 점으로 인해서 threading 모듈을 사용할 때보다 자원 공유 문제를 해결하기가 훨씬 쉬워진다. 코드를 쓰래드안전하게 짤 필요가 없어지기 때문이다.

고수준 관점에서 바라본 asyncio 모듈에 대해 잠시 알아보았는데, 더 깊은 내용이 알고 싶다면, [Stackoverflow 질문](https://stackoverflow.com/questions/49005651/how-does-asyncio-actually-work/51116910#51116910) 을 참고하면 도움 될 것이다. 

- - -

#### async 와 await

이제 파이썬에 추가된 두 가지 키워드 `async` 와 `await` 을 살펴보자. await 키워드는 위에서 알아본 내용들 중에 태스크가 이벤트 루프에게 다시 제어권을 반환하는 일을 가능하게 하는 마법 같은 키워드이다. 코드가 어떤 함수 실행을 await 한다면, 그 함수 실행이 어느 정도 시간이 걸리니까 태스크가 제어권을 넘겨줘야 한다는 신호이다.

async 키워드는 지금 정의하려는 이 함수가 내부에서 await 키워드를 사용한다는 의미로 간단히 생각할 수 있다. 엄밀히 따지면 `비동기 제너레이터` 처럼 그렇지 않은 경우도 있지만, 대부분의 경우에는 맞기 때문에 처음 이해하는데 도움 될 것이다.

한 가지 예외는, 곧 보게될 `async with` 문인데, await 해야할 객체로 부터 컨텍스트 매니저를 생성하는 기능을 한다. 의미는 조금 다르지만, 그래도 저변에 깔린 아이디어는 똑같다. 이 컨텍스트 매니저가 실행하는 도중에 멈추고 다른 태스크로 넘어갈 수 있음을 의미한다.

당연하게도 이벤트 루프와 태스크들 간의 상호작용을 관리하는 것은 꽤나 복잡한 일이지만, asyncio 를 처음 사용하는 개발자들에게는 크게 중요한 부분은 아니다. 일단은 await 를 내부에서 사용하는 함수는 꼭 async def 로 정의되어야 한다는 사실만 알고 시작하면 된다.

- - -

#### 다시 코드로

이제 asyncio 의 기본적인 원리에 대해 알았으니, 앞의 예제를 asyncio 버전으로 리펙토링 해보자. 이 버전에서는 `aiohttp` 라이브러리를 사용하니 `pip install aiohttp` 를 실행하여 먼저 설치하도록 하자.

```python
import asyncio
import time
import aiohttp


async def download_site(session, url):
    async with session.get(url) as response:
        print("Read {0} from {1}".format(response.content_length, url))


async def download_all_sites(sites):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in sites:
            task = asyncio.ensure_future(download_site(session, url))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 80
    start_time = time.time()
    asyncio.get_event_loop().run_until_complete(download_all_sites(sites))
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} sites in {duration} seconds")
```

이 버전은 앞의 두 버전보다 좀 더 복잡하다. 비슷한 구조를 가지고는 있지만, ThreadPoolExecutor를 쓰는 것보다는 더 많은 작업이 들어갔다. 위에서 하나씩 살펴보자.

- `download_site()`

download_site 함수는 threading 버전과 거의 동일하지만, 함수 정의 부분에 async 키워드를 사용한 점과 내부에서 session.get() 을 호출할 때 async with 문을 사용했다는 점이 다르다. 왜 thread local storage 대신 Session 객체가 async with 문에 사용될 수 있는 것인지는 좀 있다 살펴볼 것이다.

- `download_all_sites()`

download_all_sites 함수는 threading 버전과 비교해서 가장 크게 바뀐 부분이다.  

모든 태스크에게 session 객체를 공유시킬 수 있도록 컨텍스트 매니저를 사용하여 session 을 생성하였다. 태스크들이 같은 session 객체를 공유할 수 있는 이유는 모든 태스크들이 같은 쓰래드에서 돌기 때문이다. session이 나쁜 상태(bad state)에 있는 동안 한 태스크가 다른 태스크를 방해할 방법이 전혀 없다.

컨택스트 매니저 내부에서는, 태스크들을 시작시키는 일에도 관여하는 `asyncio.ensure_future()` 를 사용하여 태스크의 목록을 만든다. 모든 태스크가 생성되고 나면, `asyncio.gather()` 를 사용하여 모든 태스크가 끝날 때까지 session 컨텍스트를 사용한다.

threading 버전에서도 이와 비슷한 과정을 거치지만, 세부적인 동작들은 ThreadPoolExecutor 내부에서 알아서 진행된다. 아직까지는 AsyncioPoolExecutor 같은 건 없다.  

작지만 큰 차이점이 하나 더 있는데, threading 모듈에서는 쓰래드 풀에 들어갈 쓰래드를 몇 개로 지정해주어야 하는지가 분명하지 않았다. threading 모듈과 비교해서 asyncio 모듈이 가지는 가장 큰 강점은 각 태스크가 쓰래드를 만드는 것보다 훨씬 더 적은 자원과 시간을 소모한다는 것이다. 그렇기 때문에 쓰래드를 사용할 때보다 더 많은 태스크를 만들어 동시에 실행하는 것이 가능하다. 이 예제에서는 한 사이트마다 각각 별도의 태스크를 만들어 주는데 잘 작동한다.  

- `__main__`

마지막으로, asyncio의 본질 상 이벤트 루프를 시작시키고 이벤트 루프에게 태스크들을 실행하라고 명령해주어야 한다. 맨 아래에 있는 `__main__` 부분에서 `get_event_loop()` 를 사용하여 이벤트 루프를 가져오고, `run_until_complete()` 를 사용하여 태스크들을 실행시킨다. 메서드들 이름을 아주 잘지은 것 같다.  

파이썬 3.7 을 사용한다면, `asyncio.run()` 을 사용하면 위의 두 과정을 알아서 수행해준다.  

- - -

#### asyncio 버전의 장점

정말 빠르다. 테스트 해본 결과 지금까지 중에 가장 빠른 버전이다.

```shell
$ ./io_asyncio.py
   [most output skipped]
Downloaded 160 in 2.5727896690368652 seconds
```

실행 시간 다이어그램을 보면 threading 모듈과 비슷한 것을 볼 수 있다. 단지 I/O 요청들이 하나의 쓰래드에 의해 이루어진다는 점만 다르다.

![async](/img/python/asyncio.png)

작동은 비슷하지만 ThreadPoolExecutor 같은 고수준 객체가 없는 점은 threading 모듈에 비해서 코드 복잡도를 높게 만든다. 이 시점이 바로 더 나은 성능을 위해 추가 작업이 필요한 시점이다.

거기에 더해서 async 와 await 문을 적절한 곳에 넣어주는 것도 필요하기 때문에 더 복잡해진다는 의견도 있다. 어느 정도는 맞는 말인데, 반대로 생각하면 태스크가 언제 교체될지를 생각하면서 코드를 짜야하기 때문에 더 빠르고 더 좋은 디자인을 만드는데 도움이 되기도 한다.  

스케일링 문제도 크게 개선되는데, 위의 threading 버전에서 각 사이트마다 하나 씩 쓰래드를 할당하는 것은 적당한 수의 쓰래드를 할당하는 것보다 훨씬 눈에 띄게 느렸었다. 하지만 asyncio 버전에서는 수백개의 태스크를 만들어도 전혀 느려지지 않았다.

- - -

#### asyncio 버전의 문제점

asyncio 버전도 역시 몇 가지 문제점이 있다. 일단 asyncio를 최대한 활용하려면 동시성을 지원하는 라이브러리들이 필요하다는 점이다. requests 라이브러리는 이벤트 루프에 블락되었다는 신호를 주도록 디자인 되어있지 않으므로, 사이트를 다운로드하는데 그냥 requsets 모듈을 사용했다면 훨씬 느리게 작동하였을 것이다. 이 문제점은 점점 더 많은 라이브러리들이 asyncio와 호환되도록 작성되고 있기 때문에 시간이 지날 수록 해결되고 있다.  

또 다른 문제는 어느 한 태스크가 협력하지 않으면 협력적 멀티태스킹의 이점이 모두 사라진다는 점이다. 실수로 한 태스크가 프로세서를 오랫동안 붙잡고 있게 만든다면, 다른 태스크들은 절대로 진행되지 못하고 묶여있게 된다. 한 태스크가 제어권을 이벤트 루프에 넘겨주지 않으면 외부에서 뚫고 들어갈 방법이 전혀 없기 때문이다.

- - -

### multiprocessing 버전

앞의 예제들과는 다르게, multiprocessing 버전은 컴퓨터가 가진 여러 개의 CPU 코어들을 모두 사용할 수 있다는 점이다.

```python
import requests
import multiprocessing
import time

session = None


def set_global_session():
    global session
    if not session:
        session = requests.Session()


def download_site(url):
    with session.get(url) as response:
        name = multiprocessing.current_process().name
        print(f"{name}:Read {len(response.content)} from {url}")


def download_all_sites(sites):
    with multiprocessing.Pool(initializer=set_global_session) as pool:
        pool.map(download_site, sites)


if __name__ == "__main__":
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 80
    start_time = time.time()
    download_all_sites(sites)
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} in {duration} seconds")
```

asyncio 버전보다는 훨씬 짧고 threading 버전과 상당히 흡사해보인다. 코드를 자세히 살펴보기 전에 잠깐 multiprocessing 이 어떤 일을 하는지 살펴보자.

- - -

#### multiprocessing 간단히 살펴보기

지금까지 살펴본 동시성 프로그래밍 예제들은 하나의 CPU 만을 사용하는 예제들이었다. 그 이유는 현재 CPython의 디자인과 `Global Interpreter Lock(GIL)` 이라는 것 때문이다.

이 글에서는 GIL을 왜 쓰는지, 어떻게 쓰이는지에 대해서는 다루지 않을 것이다. 지금은 순차적버전, threading 버전, asyncio 버전 모두 하나의 CPU를 사용한다는 것을 아는걸로 충분하다.  

multiprocessing 은 GIL을 우회해서 코드를 여러 CPU에 걸쳐서 사용할 수 있도록 만들어졌다. 새로운 파이썬 인터프리터를 각 CPU에서 실행할 수 있도록 만들어주어 프로그램의 일부를 실행하도록 한다.

아직까지는 새로운 인터프리터를 띄우는게 쓰래드를 생성하는 것 보다는 훨씬 무겁고 제한적이며 어려움도 많지만, 올바르게 사용된다면 프로그램의 성능을 크게 개선할 수 있다.

- - -

#### multiprocessing 코드

multiprocessing 버전 코드는 순차적 버전에 비해서 몇 가지 작은 변화가 있다. download_all_sites 함수에서 download_site 함수를 반복적으로 호출하기 보다는 `multiprocessing.Pool` 객체를 생성해서 threading 버전과 비슷하게 download_site 함수를 sites 리스트에 맵핑한다.

여기서 무슨 일이 일어나냐면, Pool 객체가 여러 개의 파이썬 인터프리터 프로세스들을 생성하고 각각이 download_site 함수를 sites 리스트의 항목 중 몇몇에 실행되도록 한다. 메인 프로세스와 다른 프로세스들 간의 통신은 multiprocessing 모듈이 알아서 해결해준다.  

Pool 객체를 생성하는 부분이 유심히 볼만한데, 먼저, 몇 개의 프로세스를 풀에 생성해야하는지 명시하는 부분이 없다. 이걸 직접 지정해줄 수 있는 선택적인 파라미터가 있긴 하지만 기본적으로 multiprocessing.Pool() 을 실행하면 CPU 갯수대로 알아서 프로세스들을 생성한다. 이렇게 하는 것이 보통의 경우 최적이며, 이 예제에서도 그렇다.  

이 예제에서는 프로세스의 갯수를 늘리는게 속도 개선에 별 도움이 되지 않았다. 오히려 더 느리게 만들었는데 이는 I/O 요청들을 병렬적으로 하는데서 오는 이득보다 프로세스들을 생성하고 정리하는데 드는 비용이 더 크기 때문이다.

다음으로 `initializer=set_global_sesion` 부분을 보자. 각 프로세스는 각자의 메모리 공간을 가진다는 점을 기억하자. 이 말은 즉, Session 객체같은 걸 서로 공유할 수 없다는 말이 된다. 함수가 실행될 때마다 Session 객체를 새로 만드는 건 별로 좋은 방법이 아니다. 각 프로세스 마다 하나씩 만들어 주는것이 최적이다.  

initializer 파라미터는 이 경우를 위해서 있는 것이다. initializer에 넘겨준 함수의 리턴 값을 download_site() 에 넘겨줄 방법은 없지만, 대신 전역 session 변수를 만들어서 각 프로세스가 같은 session 객체를 사용하도록 해줄 수 있다. 각 프로세스는 별도의 메모리 공간을 가지고 있기 때문에, 각 프로세스가 가지는 전역변수는 서로 다르게 된다.

이게 다이다. 나머지는 이 앞에서 본 것과 비슷하다.

- - -

#### multiprocessing 버전의 장점

multiprocessing 버전은 비교적 구현하기 쉽고, 조금의 추가적인 코딩이 필요하기 때문에 좋다. 또 모든 CPU를 사용할 수 있는데서 오는 장점을 누릴 수 있다. 이 버전의 실행 시간 다이어그램은 아래와 같다.

![multiprocessing](/img/python/multiprocessing.png)

- - -

#### multiprocessing 버전의 문제점

이 버전은 약간이긴 하지만 몇몇 추가 작업이 필요하고 전역 변수로 할당한 session 은 못생겼다. 어떤 변수들이 각 프로세스에서 쓰일지 생각을 좀 해야한다.

결과적으로 asyncio 와 threading 버전에 비해 느리다.

```shell
$ ./io_mp.py
    [most output skipped]
Downloaded 160 in 5.718175172805786 seconds
```

놀라운 점은 아닌데, muliprocessing 은 I/O 바운드 작업을 위해 있는게 아니기 때문이다.

- - -

# CPU 바운드 작업의 성능 개선하기

지금까지 본 예제들은 모두 I/O 바운드 작업을 가지고 한 예제들이었다. 이제 CPU 바운드 작업을 살펴보자. 지금까지 보았듯이, I/O 바운드 작업은 대부분의 시간을 외부 장치가 작업을 처리할 때까지 대기하는데 보냈다. 반면 CPU 바운드 작업은 필요한 데이터를 얼마나 빠르게 처리하느냐에 따라 전체 실행시간이 달라진다.

예제를 위해서 CPU를 오래 사용하는 간단한 함수를 하나 사용할 것이다. 이 함수는 0 부터 받은 수까지의 모든 수를 제곱하여 전부 더하는 함수이다.

```python
def cpu_bound(number):
    return sum(i * i for i in range(number))
```

매우 큰 수를 넘겨주면 이 작업은 꽤나 걸릴 것이다. 이 함수는 단지 예제용일 뿐이고 실제로는 계산식을 계산하거나 거대한 데이터를 정렬하는 등의 처리 시간이 굉장히 긴 작업들이 이 함수를 대체하게 될 것이다.

- - -

### CPU 바운드 순차적 버전

```python
import time


def cpu_bound(number):
    return sum(i * i for i in range(number))


def find_sums(numbers):
    for number in numbers:
        cpu_bound(number)


if __name__ == "__main__":
    numbers = [5_000_000 + x for x in range(20)]

    start_time = time.time()
    find_sums(numbers)
    duration = time.time() - start_time
    print(f"Duration {duration} seconds")
```

이 코드는 서로 다른 큰 수를 사용하여 cpu_bound 함수를 20번 호출한다. 이 모든 작업을 하나의 CPU 안의 하나의 프로세스 안의 하나의 쓰래드로 실행한다.

![cpusync](/img/python/cpusync.png)

I/O 바운드 예제들과는 다르게 CPU 바운드 작업들은 실행시간이 어느정도 일정한 편이다. 이 예제는 7.8초 정도 걸렸다.

```shell
$ ./cpu_non_concurrent.py
Duration 7.834432125091553 seconds
```

이 버전은 CPU 하나를 써서 순차적적으로 처리한 버전이기 때문에, 확실히 이것보단 빠르게 돌도록 개선할 수 있을 것이다. 

- - -

### threading 과 asyncio 버전

위 예제를 threading 과 asyncio 버전으로 다시 작성하면 얼마나 빨라질까?

전혀 빨라지지 않는다고 대답했으면 잘한거고, 더 느려진다고 대답했으면 참 잘한거다.

I/O 바운드 예제들에서는 대부분의 시간이 느린 외부 작업을 대기하는데 사용되었다. threading 과 asyncio 버전은 이 대기 시간을 순차적으로 가지는 대신 서로 겹쳐서 전체 대기 시간을 줄인다.

그런데 CPU 바운드 버전에서는, 대기 시간이 없다. 작업을 처리하기 위해 CPU는 계속 돌아가고 있다. 파이썬에서는 쓰래드와 태스크가 같은 CPU의 같은 프로세스에서 실행된다. 이 말은 하나의 CPU가 모든 동시적이지 않은 코드들을 실행하는 것뿐만 아니라 쓰래드 또는 태스크를 세팅하는 것까지 함께 한다는 뜻이다. 돌려본 결과 10초 이상이 걸렸다.

```shell
$ ./cpu_threading.py
Duration 10.407078266143799 seconds
```

threading 버전의 예제를 [GitHub 저장소](https://github.com/realpython/materials/tree/master/concurrency-overview) 에 올려두었으니 궁금하면 직접 테스트 해보자.

- - -

### CPU 바운드 multiprocessing 버전

드디어 multiprocessing 버전이 빛을 발할 때가 되었다. 다른 동시성 라이브러리들과는 다르게 multiprocessing 은 무거운 CPU 작업을 여러 CPU에 나눠서 처리하기 위해 고안되었다. 실행 시간 다이어그램은 아래와 같다.

![cpumulti](/img/python/cpumulti.png)

```python
import multiprocessing
import time


def cpu_bound(number):
    return sum(i * i for i in range(number))


def find_sums(numbers):
    with multiprocessing.Pool() as pool:
        pool.map(cpu_bound, numbers)


if __name__ == "__main__":
    numbers = [5_000_000 + x for x in range(20)]

    start_time = time.time()
    find_sums(numbers)
    duration = time.time() - start_time
    print(f"Duration {duration} seconds")
```

위의 순차적 버전에서 크게 달라진건 없다. multiprocessing 을 임포트하고 숫자들을 루프로 반복하는 대신 multiprocessing.Pool 의 map 메서드를 사용해서 cpu_bound 함수에 각 숫자들을 맵핑해주었다. 이렇게 하면 각 숫자들을 각 워커 프로세스가 작업을 끝내는 대로 이어서 넘겨주게 된다.

I/O 바운드 multiprocessing 버전의 코드와 거의 똑같은 걸 해준 것이지만 여기서는 Session 에 대해 걱정할 필요가 없다.

- - -

#### multiprocessing 버전의 장점

multiprocessing 버전은 비교적 구현하기 쉽고, 조금의 추가적인 코딩이 필요하기 때문에 좋다. 또 모든 CPU를 사용할 수 있는데서 오는 장점을 누릴 수 있다.

I/O 바운드 버전에서 했던 얘기와 똑같다. 큰 차이점은 이번엔 확실히 크게 성능을 개선시켜준다는 점이다.

```shell
$ ./cpu_mp.py
Duration 2.5175397396087646 seconds
```

다른 버전들에 비해서 훨씬 빨라졌다.

- - -

#### multiprocessing 버전의 문제점

multiprocessing 을 사용하는데는 몇가지 어려움이 있을 수 있다. 이 예제에는 크게 드러나지 않았지만 작업을 분할시켜서 각 프로세서가 작업하도록 하는 것은 때때로 상당히 어려울 수 있다.

또한 대부분의 경우 프로세스들 간 통신을 필요로 할 것이다. 이 점으로 인해 순차적인 프로그램에서는 고민하지 않아도 될 추가적인 복잡성이 발생하게 된다.

- - -

# 언제 동시성을 사용하면 좋을까?

지금까지 많은 것을 알아보았는데, 한 번 전체적으로 정리를 하면서, 어떤 동시성 모듈을 사용하면 좋을지에 대한 의사결정 포인트들을 짚어보도록 하자.

첫 단계는 동시성 모듈이 필요한지부터 정하는 것이다. 예제들에서는 간단해 보였지만, 동시성을 프로그램에 추가하는 일은 항상 추가적인 복잡성을 발생시키고 찾기 힘든 버그들을 발생시키게 된다.

동시성을 추가하는 것을 보류하다가 성능 이슈가 발생하면 그 때 어떤 방식으로 동시성을 추가할지를 결정하면 된다. [Donald Knuth](https://en.wikipedia.org/wiki/Donald_Knuth) 에 의하면, "조기 최적화는 프로그래밍에서 모든 (또는 적어도 대부분의) 악의 근원이다."

프로그램을 개선하기로 결정했다면, 프로그램이 CPU 바운드인지, I/O 바운드인지를 파악하는 것이 다음 큰 스텝이다. I/O 바운드 프로그램은 외부 장치를 대기하는데 대부분의 시간을 쓰는 프로그램이고, CPU 바운드 프로그램은 데이터를 최대한 빠르게 처리하는데 시간을 쓰는 프로그램임을 기억하자.

예제를 통해 알아보았듯이, CPU 바운드 프로그램들은 오직 multiprocessing 을 사용해서 개선할 수 있었다. threading 과 asyncio 는 별 도움이 되지 않았다.  

I/O 바운드 프로그램들에 대해서는, 파이썬 커뮤니티에서 제시하는 일반적인 규칙이 있다.  "가능하면 asycnio를 쓰고, threading은 꼭 필요할 때 써라." asyncio는 이런 프로그램에 대해서 최고의 효율을 뽑아낼 수 있지만, 주요 라이브러리가 asyncio와 호환되도록 되어있지 않다면 곤란해질 수도 있다. 이벤트 루프로 제어권을 넘겨주지 않는 태스크가 있다면 그 태스크가 전체 프로그램을 블락할 수도 있다는 점을 기억하자.

- - -

# 결론

지금까지 파이썬의 기본적인 동시성 타입들을 알아보았다.

- threading
- asyncio
- multiprocessing

동시성을 도입해야한다면 어떤 방법의 동시성을 어떤 상황에서 사용해야하는지 배웠고, 동시성을 사용하면서 따라올 수 있는 몇 가지 문제점들에 대해서도 알게 되었다.

이 글을 통해서 많이 배웠길 바라며, 배운 걸 토대로 스스로의 프로젝트에 동시성을 잘 사용해보길 바란다.

- - -

##### Reference
https://realpython.com/python-concurrency/#what-is-concurrency

##### 함께보면 좋을만한 글들
[데이비드 비즐리의 강의 자료](https://speakerdeck.com/dabeaz/an-introduction-to-python-concurrency?slide=163)
[asyncio에 대한 자세한 stac koverflow 답변](https://stackoverflow.com/questions/49005651/how-does-asyncio-actually-work/51116910#51116910)
[asyncio 라이브러리 소스코드](https://github.com/python/cpython/tree/bec2372b7e1da5dfdbadaf242aa8e994b164cace/Lib/asyncio)
[GIL에 관한 글](https://emptysqua.re/blog/grok-the-gil-fast-thread-safe-python/)
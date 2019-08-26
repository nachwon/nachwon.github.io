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
  - Future
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

### 동기 버전

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

#### 동기 버전의 장점
무엇보다도 읽고 이해하기 쉽다. 그렇기 때문에 당연히 디버깅도 쉽다. 단 하나의 흐름이 있기 때문에 생각하기도 쉽고, 어떻게 작동할지 예측하기도 쉽다.

- - -

#### 동기 버전의 문제
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

threading 모듈을 사용해서 위의 프로그램을 개선시켜보자. threading 버전으로 프로그램을 만드는 데는 그냥 동기적인 프로그램을 만드는 것 보다 좀 더 많은 노력이 들어간다. 그렇지만 놀랍게도 정말 약간의 추가적인 코딩만 있으면 된다.

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

가장 눈에 띄게 바뀐 점은 바로 속도이다. 동기 버전이 14초 정도 걸린 것에 비하면 엄청난 발전이다.

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
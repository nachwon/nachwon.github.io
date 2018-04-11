---
layout: post
title: '[Codility] Lv5 - GenomicRangeQuery'
excerpt: Codility Lesson Level 5 - Prefix Sums
category: Algorithm
tags:
  - Algorithm
  - Codility
  - Prefix Sums
---

이 문제는 확실히 Prefix Sums 의 원리를 사용해서 풀어야 time complexity 제한을 맞출수 있을 것 같은데 문제는 슬라이스 배열의 총 합이아니라 최소값을 알아내야한다는 점이다...  

일단 단순 접근으로 풀어본 결과 O(N*M) 시간이 걸렸고 correctness는 100% 였지만 performance 에서 점수를 받지 못했다... 그래서 총 62% 를 받았다. 

```py
def solution(S, P, Q):
    M = len(P)
    impact_array = [0] * len(S)
    result = []
    
    for i in range(len(S)):
        if S[i] == "A":
            impact_array[i] = 1
        elif S[i] == "C":
            impact_array[i] = 2
        elif S[i] == "G":
            impact_array[i] = 3
        elif S[i] == "T":
            impact_array[i] = 4

    for i in range(M):
        result.append(min(impact_array[P[i]:Q[i]+1]))

    return result
```

O(N+M) 시간을 맞춰볼려고 했지만 방법이 잘 떠오르지 않았다... 그냥 최대한으로 좀 더 줄여보고자 다음과 같이 바꾸었더니 그래도 performance 테스트 하나는 통과했다.  
그래서 총 75%... 하지만 근본적인 문제는 여전히 해결하지 못한다.

```py
def solution(S, P, Q):
    M = len(P)
    query = []
    result = []
    
    for i in range(M):
        query.append(S[P[i]:Q[i]+1])
    
    for i in query:
        if "A" in i:
            impact = 1
        elif "C" in i:
            impact = 2
        elif "G" in i:
            impact = 3
        else:
            impact = 4
        
        result.append(impact)
        
    return result
```

인터넷에서 다른 사람이 이 문제를 설명해놓은 글에서 힌트를 얻어서 Prefix 배열에 각 문자들의 카운터를 집어넣어 보았다.  
예를 들어, `S = "CAGCCTA"` 이라면, `Prefix 배열 A` 는 다음과 같다.

```py
[[0, 0, 0, 0]]  # 초기 상태
[[0, 0, 0, 0], [0, 1, 0, 0]]  # C 등장
[[0, 0, 0, 0], [0, 1, 0, 0], [1, 1, 0, 0]]  # A 등장
.
.
.
[[0, 0, 0, 0]...[2, 3, 1, 1]]  # 가장 마지막, 즉, S 전체에 대한 카운터
```

이런 Prefix 배열이 있다면 S 의 특정 슬라이스 배열에 대한 카운터를 구할 수 있게 된다.  
예를 들어, `S[2:4]` 인 `"GC"` 는 `A[4]` 의 각 요소에서 `A[2]` 의 각 요소를 빼면 된다.  

```
아래는 Python 연산이 아님

A[4] = [1, 2, 1, 0]
A[2] = [1, 1, 0, 0]

A[4] - A[2] = [0, 1, 1, 0]
```

결과는 `[0, 1, 1, 0]` 으로 `S[2:4]` 에는 `C` 1 번, `G` 1 번이 들어간다는 것을 한 번의 계산으로 바로 알 수 있다.  
그러고나면 최소 값은 그냥 0 이 아닌 요소의 인덱스 값 + 1 을 리턴하면 된다.  

- - -

## 최종 답안

위 내용을 반영하여 아래와 같이 코드를 수정했더니 100%가 나왔다.  
Counter 와 Prefix 가 결합된 어렵고 재미있는 문제였다...

Detected time complexity:

```
O(N + M)
```

```py
def solution(S, P, Q):
    M = len(P)
    N = len(S)
    A = [[0, 0, 0, 0]]
    counter = [0] * 4
    result = []
    for i in S:
        if i == "A":
            counter[0] += 1
            A.append(counter[:])
        elif i == "C":
            counter[1] += 1
            A.append(counter[:])
        elif i == "G":
            counter[2] += 1
            A.append(counter[:])
        elif i == "T":
            counter[3] += 1
            A.append(counter[:])
    
    for i in range(M):
        for j in range(4):
            val = A[Q[i]+1][j] - A[P[i]][j]
            if val != 0:
                result.append(j + 1)
                break
    
    return result
```

- - -

#### Reference

[Codility](https://app.codility.com/programmers/lessons/5-prefix_sums/genomic_range_query/)
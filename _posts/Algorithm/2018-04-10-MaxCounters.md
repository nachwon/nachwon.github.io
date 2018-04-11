---
layout: post
title: '[Codility] Lv4 - MaxCounters'
excerpt: Codility Lesson Level 4 - Counting Elements
category: Algorithm
tags:
  - Algorithm
  - Codility
  - Counting Elements
---

44%...

```py
def solution(N, A):
    counter = [0] * (N + 1)

    for i in A:
        if i == N + 1:
            for i in range(len(counter)):
                counter[i] = max(counter)
        else:
            counter[i] += 1
    
    del counter[0]
    
    return counter
```

66%...

```py
def solution(N, A):
    counter = [0] * (N + 1)
    
    for i in A:
        if i == N + 1:
            counter = [max(counter)] * (N + 1)
        else:
            counter[i] += 1
    
    del counter[0]
    
    return counter
```

77%...

```py
def solution(N, A):
    counter = [0] * (N + 1)
    max_num = 0
    
    for i in A:
        if i == N + 1:
            counter = [max_num] * (N + 1)
        else:
            counter[i] += 1
            if counter[i] > max_num:
                max_num = counter[i]
    
    del counter[0]
    
    return counter
```

- - -

## 최종 답안

결과 보니까 max_counter 가 매우 많이 발생할 때 time out 에러가 발생해서 점수가 깎이는 것 같다.
그래서 max_num 이 업데이트 될 때만 max_counter 를 실행하도록 바꿔주었다.

Detected time complexity:
```
O(N + M)
```
```py
def solution(N, A):
    counter = [0] * (N + 1)
    prev_max = 0
    max_num = 0
    
    for i in A:
        if i == N + 1 and prev_max != max_num:
            counter = [max_num] * (N + 1)
            
        elif i == N + 1 and prev_max == max_num:
            continue

        else:
            counter[i] += 1
            if counter[i] > max_num:
                prev_max = max_num
                max_num = counter[i]
    
    del counter[0]
    
    return counter
```

이렇게 해주니까 100%가 나왔다!

- - -

#### Reference

[Codility](https://app.codility.com/programmers/lessons/4-counting_elements/max_counters/)
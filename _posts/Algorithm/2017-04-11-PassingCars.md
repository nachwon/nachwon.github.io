---
layout: post
title: '[Codility] Lv5 - PassingCars'
excerpt: Codility Lesson Level 5 - Prefix Sums
category: Algorithm
tags:
  - Algorithm
  - Codility
  - Prefix Sums
---

## 최종 답안

오예~ Prefix Sums 를 활용해서 한 번에 100%를 받았다!

Detected time complexity:

```
O(N)
```

```py
def prefix_sums(A):
    n = len(A)
    P = [0] * (n + 1)
    for i in range(1, n + 1):
        P[i] = P[i - 1] + A[i - 1]
    return P

def solution(A):
    P = prefix_sums(A)
    res = 0
    for i in range(len(A)):
        if A[i] == 0:
            res += P[-1] - P[i]
            
    if res > 1000000000:
        return -1
    return res
```

- - -

#### Reference

[Codility](https://app.codility.com/programmers/lessons/5-prefix_sums/passing_cars/)
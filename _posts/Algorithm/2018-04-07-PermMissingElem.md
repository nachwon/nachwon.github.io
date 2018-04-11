---
layout: post
title: '[Codility] Lv3 - PermMissingElem'
excerpt: Codility Lesson Level 3 - Time Complexity
category: Algorithm
tags:
  - Algorithm
  - Codility
  - Time Complexity
---

## 최종 답안

처음엔 펙토리얼로 풀려고 했는데 생각해보니 그렇게 어려운 문제가 아니었다. 다만 그걸 알아내는데 시간이 한참 걸렸다.

```py
def solution(A):
    a = 0
    for i in range(len(A)+2):
        a += i

    return a - sum(A)
```

아래는 다른 사람의 풀이를 파이썬으로 써본 것

```py
def solution(A):
    a = (len(A)+1)*((len(A))+1)+1) / 2
    for i in A:
        a -= i

    return int(a)
```

- - -

#### Reference

[Codility](https://app.codility.com/programmers/lessons/3-time_complexity/perm_missing_elem/)
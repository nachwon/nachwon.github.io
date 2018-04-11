---
layout: post
title: '[Codility] Lv4 - FrogRiverOne'
excerpt: Codility Lesson Level 4 - Counting Elements
category: Algorithm
tags:
  - Algorithm
  - Codility
  - Counting Elements
---

```py
def solution(X, A):
    leaves = [0] * (X + 1)
    expected = [0] + [1] * (X)

    for i in range(len(A)):
        leaves[A[i]] = 1
        if leaves == expected:
            return i
    return -1
```

- - -

## 최종 답안

위의 방법으로는 81% 정도가 한계였다. 그 원인이 무엇인지 생각해보다가 왠지 리스트를 두개나 써서 공간 복잡도 문제인 것 같아 아래와 같이 수정해보았더니 100%가 나왔다. 
근데 사실 정말 공간복잡도 때문인건지 잘 모르겠다...

```py
def solution(X, A):
    leaves = [0] * (X + 1)
    total_leaves = 0

    for i in range(len(A)):
        if leaves[A[i]] == 0:
            leaves[A[i]] = 1
            total_leaves += 1
            if total_leaves == X:
                return i
    return -1
```

- - -

#### Reference

[Codility](https://app.codility.com/programmers/lessons/4-counting_elements/frog_river_one/)
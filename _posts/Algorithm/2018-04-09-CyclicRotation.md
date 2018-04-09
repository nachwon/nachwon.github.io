---
layout: post
title: '[Codility] Lv2 - CyclicRotation'
excerpt: Codility Lesson Level 2 - Arrays
category: Algorithm
tags:
  - Algorithm
  - Codility
  - Arrays
---

```py
def solution(A, K):
    if len(A) == K or len(A) == 0:
        return A
    elif len(A) < K:
        K = K % len(A)
    
    for i in range(K):
        item = A.pop()
        A.insert(0, item)
    return A
```

- - -

#### Reference

[Codility](https://app.codility.com/programmers/lessons/2-arrays/cyclic_rotation/)
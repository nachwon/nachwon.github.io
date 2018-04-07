---
layout: post
title: '[Codility] Lv3 - Tape Equilibrium'
excerpt: Codility Lesson Level 3 - Time Complexity
category: Algorithm
tags:
  - Algorithm
  - Codility
  - Time Complexity
---

50% 밖에 못 받음...

```py
def solution(A):
    total = sum(A)
    total_L = 0
    min_diff = 1000000

    for i in range(len(A)):
        total_L += A[i]
        total -= A[i]
        diff = abs(total_L - total)

        if diff < min_diff:
            min_diff = diff
        
        if diff != min_diff:
            break
        
    return min_diff
```
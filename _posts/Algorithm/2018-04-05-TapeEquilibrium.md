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

## 최종 답안

```py
def solution(A):
    total = sum(A)
    total_L = 0
    min_diff = None

    for i in range(len(A) - 1):
        total_L += A[i]
        total -= A[i]
        diff = abs(total_L - total)

        if min_diff is None:
            min_diff = diff
        else:
            min_diff = min(min_diff, diff)
        
    return min_diff
```

- - -

#### Reference

[Codility](https://app.codility.com/programmers/lessons/3-time_complexity/tape_equilibrium/)
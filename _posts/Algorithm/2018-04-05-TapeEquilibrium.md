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

```py
def diff(A, P):
    LHS = abs(sum(A[:P]))
    RHS = abs(sum(A[P:]))
    diff = abs(LHS - RHS)
    return diff

def solution(A):
    P = len(A) // 2
    min_diff = 10000000000000
    d = 0
    
    while True:
        LHS = abs(sum(A[:P]))
        RHS = abs(sum(A[P:]))
        
        if LHS > RHS:
            P -= 1
            d = diff(A, P)
    
        elif LHS < RHS:
            P += 1
            d = diff(A, P)

        # print(min_diff, d)
        if d < min_diff:
            min_diff = d
        elif d >= min_diff:
            break
    
    return min_diff
```
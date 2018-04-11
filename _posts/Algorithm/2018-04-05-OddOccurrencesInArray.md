---
layout: post
title: '[Codility] Lv2 - OddOccurrencesInArray'
excerpt: Codility Lesson Level 2 - Arrays
category: Algorithm
tags:
  - Algorithm
  - Codility
  - Arrays
---

## 최종 답안

```py
def solution(A):
    sorted_A = sorted(A)
    
    for i in range(0, len(sorted_A), 2):
        if i + 1 == len(sorted_A):
            return sorted_A[-1]
        if sorted_A[i] != sorted_A[i+1]:
            return sorted_A[i]
```

- - -

#### Reference

[Codility](https://app.codility.com/programmers/lessons/2-arrays/odd_occurrences_in_array/)
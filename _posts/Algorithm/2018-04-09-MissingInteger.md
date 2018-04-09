---
layout: post
title: '[Codility] Lv4 - MissingInteger'
excerpt: Codility Lesson Level 4 - Counting Elements
category: Algorithm
tags:
  - Algorithm
  - Codility
  - Counting Elements
---

Detected time complexity:
```
O(N) or O(N * log(N))
```

```py
def solution(A):
    max_value = max(A)
    count = [0] * max_value
    
    if count == []:
        return 1

    for i in range(len(A)):
        
        count[A[i]-1] = 1

    for index, item in enumerate(count):
        if item == 0:
            return index + 1

    return max_value + 1
```

77% 밖에 못받음...

- - -

#### Reference

[Codility](https://app.codility.com/programmers/lessons/4-counting_elements/missing_integer/)
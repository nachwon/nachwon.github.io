---
layout: post
title: '[Codility] Lv4 - PermCheck'
excerpt: Codility Lesson Level 4 - Counting Elements
category: Algorithm
tags:
  - Algorithm
  - Codility
  - Counting Elements
---

## 최종 답안

알고리즘 풀이에 대한 새로운 접근 법을 배웠다. 특정 요소가 배열에 몇 번 나타나는지를 세어서 별도의 충분한 길이의 배열에 저장하는 방법이다.  
어떤 숫자들의 배열이 주어졌을 때 1 에서 부터 N 까지 중복 없고 빠짐 없이 숫자들이 모두 들어있지를 확인하는 문제를 이 방법으로 풀어보았다.

```py
def solution(A):
    count = [0] * (len(A) + 1)
    expected = [1] * len(A)
    
    for i in A:
        try:
            count[i] += 1
        except IndexError:
            return 0
            
    del count[0]
    
    if count == expected:
        return 1
    else: 
        return 0
```

- - -

#### Reference
[Codility](https://app.codility.com/programmers/lessons/4-counting_elements/perm_check/)
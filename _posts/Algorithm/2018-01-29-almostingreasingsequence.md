---
layout: post
title: 'almostIncreasingSequence'
category: Algorithm
excerpt: codefights.com/arcade
comment: true
tags:
    - Algorithm
---

Given a sequence of integers as an array, determine whether it is possible to obtain a strictly increasing sequence by removing no more than one element from the array.  

Example  

For sequence = [1, 3, 2, 1], the output should be
almostIncreasingSequence(sequence) = false;  

There is no one element in this array that can be removed in order to get a strictly increasing sequence.  

For sequence = [1, 3, 2], the output should be
almostIncreasingSequence(sequence) = true.  

You can remove 3 from the array to get the strictly increasing sequence [1, 2]. Alternately, you can remove 2 to get the strictly increasing sequence [1, 3].  

- - -

### 허접한 풀이

```py
def almostIncreasingSequence(sequence):
    s = sequence
    s2 = s[:]
    deleted = 0
    if (len(s) - len(set(s))) > 1:
        return False
    elif len(set(s)) == 1:
        return True
    
    for i in range(len(s)-1):
        if s2[i] < s2[i+1]:
            continue
        else:
            del s[i:i+2]
            deleted += 1
            
    for i in range(len(s)-1):
        if s[i] > s[i+1]:
            return False
        
    if deleted > 1:
        return False
    else:
        return True
```

- - -

### 고수의 깔끔한 풀이

```py
def almostIncreasingSequence(sequence):
    droppped = False
    last = prev = min(sequence) - 1
    for elm in sequence:
        if elm <= last:
            if droppped:
                return False
            else:
                droppped = True
            if elm <= prev:
                prev = last
            elif elm >= prev:
                prev = last = elm
        else:
            prev, last = last, elm
    return True
```

- - - 

### 굇수의 미친 풀이

```py
def almostIncreasingSequence(s):
    return 3> sum((i >= j) + (i >= k) for i, j, k in zip(s, s[1:], s[2:] + [10**6]))
```

세상에 맙소사 이게뭐람

<img src="/img/algorithm/fuuu.png">
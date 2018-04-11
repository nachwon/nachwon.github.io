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

아래의 방법으로는 77% 밖에 못받음...

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

- - -

## 최종 답안

위 코드에서 count 리스트를 생성할 때 max 값으로 생성했던 이유는 예를 들어 인풋 배열에 100이 있을 경우 count[100] 에 1의 값을 집어 넣어 주어야 하기 때문에 충분한 길이를 가질 수 있도록 해주기 위해서였다.  
그런데 생각해보니까 어차피 엄청 큰 값이 있던 말던 간에 배열 내에 나타나지 않은 가장 작은 값을 찾으면 되므로 count 함수를 인풋 배열의 길이 만큼만 만들어도 된다. 그리고 count 배열에 값을 넣어 줄 때 count 배열의 길이를 넘어서는 index 값을 받은 경우는 제외시켜주면 된다. 왜냐하면 count 함수의 100 번째 값을 넣을 필요가 있는 경우는 1에서 부터 99까지 모든 수가 있는 경우, 즉, 인풋 배열의 길이로 count 배열을 생성해도 충분할 경우이기 때문이다.  
따라서 코드를 아래와 같이 바꾸어 보았더니 100%가 나왔다.

```py
def solution(A):
    A = set(A)
    A = sorted(A)
    count = [0] * (len(A) + 1)
    
    if count == [] or len(count) == 1:
        return 1
        
    for i in A:
        if 0 < i < len(A) + 1:
            count[i] = 1
    
    del count[0]

    for index, item in enumerate(count):
        if item == 0:
            return index + 1
            
    return A[-1] + 1
```


- - -

#### Reference

[Codility](https://app.codility.com/programmers/lessons/4-counting_elements/missing_integer/)
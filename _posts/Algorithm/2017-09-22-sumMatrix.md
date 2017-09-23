---
layout: post
title: 행렬의 덧셈
category: Algorithm
author: Che1
---

```python
a = [[1, 1, 1], 
     [2, 2, 2],
     [3, 3, 3], 
     [4, 4, 4]]
     
b = [[1, 1, 1], 
     [2, 2, 2],
     [3, 3, 3], 
     [4, 4, 4]]
```

```python
def sumMatrix(A, B):
    result = [[sum(x) for x in zip(A[i], B[i])] for i in range(len(A))]
    return result

print(sumMatrix(a, b))
```

```re
[[2, 2, 2], [4, 4, 4], [6, 6, 6], [8, 8, 8]]
```

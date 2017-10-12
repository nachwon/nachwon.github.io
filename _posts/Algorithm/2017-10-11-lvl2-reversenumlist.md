---
layout: post
title: '[Level 1] 같은 숫자는 싫어'
category: Algorithm
author: Che1
---

digit_reverse함수는 양의 정수 n을 매개변수로 입력받습니다.
n을 뒤집어 숫자 하나하나를 list로 표현해주세요
예를들어 n이 12345이면 [5,4,3,2,1]을 리턴하면 됩니다.

```py
def digit_reverse(n):
    return [int(i) for i in list(str(n))[::-1]]

print("결과 : {}".format(digit_reverse(12345)));
```

```re
결과 : [5, 4, 3, 2, 1]
```
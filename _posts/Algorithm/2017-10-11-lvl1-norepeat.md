---
layout: post
title: '[Level 1] 같은 숫자는 싫어'
category: Algorithm
excerpt: 
comment: true
tags:
    - Algorithm
---
no_continuous함수는 스트링 s를 매개변수로 입력받습니다.

s의 글자들의 순서를 유지하면서, 글자들 중 연속적으로 나타나는 아이템은 제거된 배열(파이썬은 list)을 리턴하도록 함수를 완성하세요.
예를들어 다음과 같이 동작하면 됩니다.

s가 '133303'이라면 ['1', '3', '0', '3']를 리턴
s가 '47330'이라면 [4, 7, 3, 0]을 리턴

- - -
#### 내 풀이

```py
def no_continuous(s):
    my_list = []
    if len(s) == 0:
        return my_list
    for i in range(len(s)-1):
        if s[i] != s[i+1]:
            my_list.append(s[i])
        else:
            continue
    my_list.append(s[-1])
    return my_list

print(no_continuous("4444433337776699999666"))
```
```re
['4', '3', '7', '6', '9', '6']
```
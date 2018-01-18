---
layout: post
title: '[Level 2] 가장 긴 펠린드롬'
category: Algorithm
excerpt: 
comment: true
tags:
    - Algorithm
---
앞뒤를 뒤집어도 똑같은 문자열을 palindrome이라고 합니다.
longest_palindrom함수는 문자열 s를 매개변수로 입력받습니다.
s의 부분문자열중 가장 긴 palindrom의 길이를 리턴하는 함수를 완성하세요.
예를들어 s가 "토마토맛토마토"이면 7을 리턴하고 "토마토맛있어"이면 3을 리턴합니다.

- - -

#### 내 풀이

```py
def longest_palindrom(s):
    l = []
    for i in range(len(s)):
        for j in range(i+1, len(s)+1):
            a = s[i:j]
            if a == a[::-1]:
                l.append(len(a))
    if l != []:
        return max(l)

print(longest_palindrom("토마토맛토마토"))
print(longest_palindrom("맛있어토마토"))
```
```re
7
3
```
- - -

#### 모범답안

```py
def longest_palindrom(s):
    return len(s) if s[::-1] == s else max(longest_palindrom(s[:-1]), longest_palindrom(s[1:]))
```

재귀를 활용한 풀이
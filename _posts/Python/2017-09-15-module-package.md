---
layout: post
title: '[Python 문법] 모듈과 패키지 (Module and Package)'
category: Python
tags:
  - Python
  - Module
  - Package
---

## 모듈

#### module/game.py

```python
def play_game():
    print('Play game!')
```

#### module/shop.py

```python
def buy_item():
    print('Buy item!')
```

#### module/lol.py

```python
import game
import shop

print('= Turn on game =')
game.play_game()
shop.buy_item()
```
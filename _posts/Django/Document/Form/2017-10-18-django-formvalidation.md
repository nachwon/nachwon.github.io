---
layout: post
title: '[Form] 폼 데이터의 검증'
subtitle: Using Forms to Validate Data
category: Django
tags:
  - Django
  - Form
---

폼 객체를 사용하기 전에 가장 먼저 해야할 일은 폼으로 전달된 데이터가 유효한 데이터인지 **검증**하는 작업이다.  
여기서 폼 데이터가 유효하다는 것은 폼의 형식에 맞는 데이터가 전달되었음을 의미한다.

- - -

### is_valid()

폼 데이터가 유효한지 검사하려면 폼 인스턴스에 `is_valid()` 메서드를 호출해준다.

```py
data = {'subject': 'hello',
        'message': 'Hi there',
        'sender': 'foo@example.com',
        'cc_myself': True}
f = ContactForm(data)
f.is_valid()
```
```re
Ture
```
is_valid() 메서드는 폼이 유효한지에 따라 부울값을 리턴한다. 그리고 폼이 유효하다면 폼 인스턴스의 `cleaned_data` 라는 속성에 딕셔너리 형태로 데이터들을 저장한다.

is_valid() 가 호출되면 다음의 몇 가지 절차를 통해서 폼 데이터를 검사한다.

- - -

#### to_python()

가장 먼저 실행되는 검증절차로 각 폼 필드에 대해 **필드** 인스턴스의 `to_python()` 메서드가 실행된다.  
`to_python()` 메서드는 필드에 입력된 로우 데이터를 필드 유형에 맞는 Python 자료형으로 변환해보고 불가능하면 `ValidationError` 를 발생시킨다.  
예를 들어, `FloatField` 에 입력된 값은 `float` 자료형으로, `CharField` 에 입력된 값은 `string` 자료형으로 변환시킨다. 만약 `FloatField` 에 입력된 값이 문자열인 경우 `float` 자료형으로 변환이 불가능하며, 이 때, `ValidationError` 를 발생시킨다.

- - -

#### validate()

각 필드가 `to_python()` 메서드를 통과했다면, `validate()` 메서드가 실행된다. 각 필드 유형에 맞는 Python 자료형으로 변환된 데이터들이 폼 필드의 다른 제약사항을 위배하는지를 판단한다. 
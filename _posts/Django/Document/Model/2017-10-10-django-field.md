---
layout: post
title: '[Model] 필드'
subtitle: Fields
category: Django
tags:
  - Django
  - Model
---

### 필드란?

필드는 데이터베이스의 테이블에서 열(column)을 의미한다. `Django` 에서 필드는 모델을 생성할 때 필수적인 요소이며, 모델클래스의 속성으로 나타낸다. 필드를 `clean`, `save`, `delete` 등과 같이 `모델 API` 와 동일한 이름으로 생성하지 않도록 주의해야 한다.

```py
class 모델이름(models.Model):
    필드이름1 = models.필드타입(필드옵션)
    필드이름2 = models.필드타입(필드옵션)
    .
    .
```

- - -

##### 모델이름 테이블

<table class="table table-striped table-bordered">
    <tr>
        <th>필드이름1</th>
        <th>필드이름2</th>
        <th>...</th>
    </tr>
    <tr>
        <td><p></p></td>
        <td><p></p></td>
        <td><p></p></td>
    </tr>
    <tr>
        <td><p></p></td>
        <td><p></p></td>
        <td><p></p></td>
    </tr>
</table>


- - -

### 필드 타입

필드는 `Field` 클래스의 인스턴스이다. `Django` 는 필드를 통해 다음과 같은 사항을 정의한다.

- 테이블의 열 저장할 데이터의 유형 (문자열, 정수 등)
- 폼 필드를 렌더링할 때 사용할 기본 `HTML 위젯`
- 관리자 페이지와 자동생성 되는 폼들에 적용될 최소 요구사항

`Django` 는 기본적으로 아래와 같은 필드 타입들을 제공한다.


<table class="table table-striped table-bordered">
    <tr>
        <th>필드타입</th>
        <th>HTML 위젯</th>
        <th>필수 옵션</th>
        <th>설명</th>
    </tr>
    <tr>
        <td style="vertical-align: middle;">
            <a href="https://docs.djangoproject.com/en/1.11/ref/models/fields/#booleanfield">
                BooleanField
            </a>
        </td>
        <td style="vertical-align: middle;">CheckboxInput</td>
        <td style="vertical-align: middle;"> - </td>
        <td>`True/False` 값을 가지는 필드.</td>
    </tr>
    <tr>
        <td style="vertical-align: middle;">
            <a href="https://docs.djangoproject.com/en/1.11/ref/models/fields/#charfield">
                CharField
            </a>
        </td>
        <td style="vertical-align: middle;">TextInput</td>
        <td style="vertical-align: middle;">max_length</td>
        <td>문자열 데이터를 저장하는 필드. 최대 글자 수를 반드시 지정해주어야 한다.</td>
    </tr>
    <tr>
        <td style="vertical-align: middle;">
            <a href="https://docs.djangoproject.com/en/1.11/ref/models/fields/#datefield">
                DateField
            </a>
        </td>
        <td style="vertical-align: middle;">TextInput</td>
        <td style="vertical-align: middle;"> - </td>
        <td>datetime.date 인스턴스인 날짜 데이터를 저장하는 필드. <br>달력 위젯과 오늘 날짜 입력 기능을 기본제공한다.</td>
    </tr>
    <tr>
        <td style="vertical-align: middle;">
             <a href="https://docs.djangoproject.com/en/1.11/ref/models/fields/#datetimefield">
                DateTimeField
            </a>
        </td>
        <td style="vertical-align: middle;">TextInput</td>
        <td style="vertical-align: middle;"> - </td>
        <td>datetime.datetime 인스턴스인 날짜와 시간 데이터를 저장하는 필드. <br>두 개의 TextInput, 달력 위젯, 오늘 날짜 입력 기능을 기본제공한다.</td>
    </tr>
    <tr>
        <td style="vertical-align: middle;">
            <a href="https://docs.djangoproject.com/en/1.11/ref/models/fields/#floatfield">
                FloatField
            </a>
        </td>
        <td style="vertical-align: middle;">NumberInput</td>
        <td style="vertical-align: middle;"> - </td>
        <td>Python의 float과 같은 실수 데이터를 저장하는 필드.</td>
    </tr>
    <tr>
        <td style="vertical-align: middle;">
            <a href="https://docs.djangoproject.com/en/1.11/ref/models/fields/#integerfield">
                IntegerField
            </a>
        </td>
        <td style="vertical-align: middle;">NumberInput</td>
        <td style="vertical-align: middle;"> - </td>
        <td>Python의 integer과 같은 정수 데이터를 저장하는 필드. <br>-2147483648과 2147483647 사이의 값을 저장할 수 있다.</td>
    </tr>
    <tr>
        <td style="vertical-align: middle;">
            <a href="https://docs.djangoproject.com/en/1.11/ref/models/fields/#textfield">
                TextField
            </a>
        </td>
        <td style="vertical-align: middle;">Textarea</td>
        <td style="vertical-align: middle;"> - </td>
        <td>글자 수 제한이 없는 문자열 데이터를 저장하는 필드. <br>max_length 값을 지정하면 폼에서는 제한이 되지만, 데이터베이스에는 영향을 주지 않음.</td>
    </tr>
    <tr>
        <th colspan="4">관계 정의 필드</th>
    </tr>
    <tr>
        <td style="vertical-align: middle;">
            <a href="https://docs.djangoproject.com/en/1.11/ref/models/fields/#foreignkey">
                Forignkey
            </a>
        </td>
        <td style="vertical-align: middle;"> - </td>
        <td style="vertical-align: middle;">to, on_delete</td>
        <td>필드를 외래키로 설정한다. 다른 테이블의 레코드와 일대다 관계를 형성한다. <br>관계 설정 대상이 되는 모델과 레코드 삭제 시 처리 방식을 필수로 설정해주어야 한다.</td>
    </tr>
    <tr>
        <td style="vertical-align: middle;">
            <a href="https://docs.djangoproject.com/en/1.11/ref/models/fields/#manytomanyfield">
                ManytoManyField
            </a>
        </td>
        <td style="vertical-align: middle;"> - </td>
        <td style="vertical-align: middle;">to</td>
        <td>필드가 대상 테이블과 다대다 관계를 형성하도록 설정한다.<br>관계 설정 대상이 되는 모델을 필수로 설정해주어야 한다.</td>
    </tr>
    <tr>
        <td style="vertical-align: middle;">
            <a href="https://docs.djangoproject.com/en/1.11/ref/models/fields/#onetoonefield">
                OneToOneField
            </a>
        </td>
        <td style="vertical-align: middle;"> - </td>
        <td style="vertical-align: middle;">to, on_delete</td>
        <td>필드가 대상 테이블과 일대일 관계를 형성하도록 설정한다.<br>관계 설정 대상이 되는 모델과 레코드 삭제 시 처리 방식을 필수로 설정해주어야 한다.</td>
    </tr>
</table>

모든 기본 제공 필드 타입들에 대한 정보는 [Django 공식 문서](https://docs.djangoproject.com/en/1.11/ref/models/fields/)에서 확인할 수 있다.

- - -
### 필드 옵션

모든 필드에는 여러가지 설정을 변경할 수 있는 필드 옵션을 지정해줄 수 있다.
- - -

#### 자주 사용하는 필드 옵션

아래는 주로 사용하는 필드 옵션들이다. 모두 선택 옵션이다.

- `null`: `True` 이면 데이터베이스에 빈 값을 `null` 값으로 저장한다. 기본값은 `False` 이다.
```py
field = models.IntegerField(null=True)
```

- `blank`: `True` 이면 필드가 빈 값을 받을 수 있게 된다. 기본값은 `False`.
```py
field = models.IntegerField(blank=True)
```

- `choices`: 길이가 2인 튜플들의 리스트 혹은 튜플을 선택지 변수로 지정할 수 있다. `choices` 옵션에 선택지 변수를 지정해주면 된다.
```py
# 선택지 변수 예
SHIRT_SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )
field = models.CharField(max_length=1, choices=SHIRT_SIZES)
```

- `default`: 필드의 기본값을 지정해준다. 필드에 아무것도 입력하지 않을 경우 기본값이 들어간다.
```py
field = models.IntegerField(default=0)
```

- `help_text`: 필드에 대한 설명을 추가할 수 있다. 관리자 페이지에서 확인 가능.
```py
company_name = models.CharField(max_length=10, help_text='Type company name here')
```

- `primary_key`: 필드를 기본키로 설정한다. 기본키를 설정하지 않으면 자동적으로 고유한 정수값을 가지는 `id` 기본키 필드가 생성된다. 기본키 필드는 읽기전용이며, 값을 바꾸면 기존 레코드의 기본키 필드 값이 바뀌는 것이 아니고 바꾸려는 값을 기본키 값으로 가지는 레코드가 새로 생성된다.  
```py
name = models.CharField(max_length=100, primary_key=True)
```

- `unique`: 필드가 항상 고유한 값만 가지도록 설정한다. 동일한 필드 값을 가지는 레코드를 생성하려고 할 경우 `IntegrityError` 가 난다. `ManyToManyField` 와 `OneToOneField` 에는 사용할 수 없다.

- `verbose_name`: 관계설정 필드를 제외한 모든 필드타입들은 첫 번째 위치 인자로 문자열을 받을 수 있다. 이 문자열은 필드를 좀 더 구체적으로 나타내는 이름이 된다. `verbose_name` 을 설정하지 않는 경우, 기본값으로 `_` 를 공백문자로 치환한 변수이름이 `verbose_name` 이 된다.  
```py
# verbose_name 은 'person's first name' 이 된다.
# 문자열을 전달하지 않는 경우 verbose_name 은 'first name' 이 된다.
first_name = models.CharField("person's first name", max_length=20)
```
`ForignKey`, `OneToOneField`, `ManyToManyField` 는 첫 번째 위치인자로 관계 대상 모델을 받으므로 `verbose_name` 이라는 키워드 인자로 전달해주어야한다.
```py
poll = models.ForignKey(Poll, on_delete=models.CASCADE, verbose_name='the related poll')
```
관례적으로 `verbose_name` 의 첫 글자를 대문자로 표기하지 않는다. `Django` 는 이 이름을 사용할 때 자동으로 첫 글자를 대문자 표기한다.

- `db_colmn`: 필드 이름을 사용자 지정해줄 수 있다. 이 옵션이 주어지지 않는 경우 기본적으로는 모델의 속성 이름이 테이블의 필드 이름이 된다. 이 옵션을 사용하면 Python 예약어 및 변수명 제약, 하이픈(`-`), SQL 예약어 등을 필드 이름으로 사용할 수 있게 된다.
```py
# 데이터베이스의 필드 이름은 db-field-name 로 표시된다.
field_name = models.CharField(max_length=30, db_colmn='db-field-name')
```

모든 필드 옵션들에 대한 정보는 [Django 공식 문서](https://docs.djangoproject.com/en/1.11/ref/models/fields/#module-django.db.models.fields)에서 확인할 수 있다.

- - -

### 필드 이름 제약사항

필드 이름의 정의에는 다음의 두 가지 제약사항이 있다.

- Python 예약어는 필드 이름으로 사용할 수 없다.
```py
class Example(models.Model):
    pass = models.CharField(max_length=100)  # pass 는 Python 예약어이다.
```

- 필드 이름에 언더스코어(`_`) 두 개를 연속으로 쓸 수 없다. `Django` 의 쿼리 룩업 문법과 겹치기 때문이다.
```py
class Example(model.Model):
    ex__field = models.CharField(max_length=100)  # ex__field 는 연속된 언더스코어 두 개를 가지고 있다.
``` 

위의 제약사항들은 `db_colmn` 옵션을 통해서 우회될 수 있다.

- - -

###### Reference

Django 공식 문서: [https://docs.djangoproject.com/en/1.11/ref/models/fields/](https://docs.djangoproject.com/en/1.11/ref/models/fields/)
---
layout: post
title: '[Query] 쿼리 보내기'
subtitle: Making Queries
category: Django
tags:
  - Django
  - Database
  - Query
  - ORM
---

데이터 모델을 만들어주고 나면, `Django` 는 데이터베이스에 데이터 객체를 입력, 삭제, 또는 데이터베이스로부터 데이터 객체를 추출하도록 해주는 `API` 를 자동적으로 생성해준다.  
이번 포스트에서는 아래의 예제 모델을 사용해 데이터베이스 `API` 의 사용법을 알아본다.

- - -

#### 예제 모델

```py
from django.db import models

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    authors = models.ManyToManyField(Author)
    n_comments = models.IntegerField()
    n_pingbacks = models.IntegerField()
    rating = models.IntegerField()

    def __str__(self):              # __unicode__ on Python 2
        return self.headline
```

- - -

### 레코드 생성하기

모델 클래스는 데이터베이스에서 테이블이되고, 모델 클래스의 인스턴스는 해당 테이블의 한 레코드가 된다.  
새로운 레코드를 테이블에 추가하려면, 각 필드의 값들을 모델 클래스에 키워드 인자로 전달하여 인스턴스를 생성한 다음, `save()` 를 호출해주면 된다.

`Blog` 모델의 인스턴스를 아래와 같이 생성한 다음, `save()` 를 호출해준다.

```py
b = Blog(name='This is name.', tagline='This is tagline.')
b.save()
```

위 명령을 실행하면 내부적으로 데이터베이스에 SQL의 `INSERT` 문을 사용하게 된다.  
`save()` 를 호출하기 전까지는 데이터베이스를 직접 건들이지 않는다.

- - -

### 레코드 수정하기

이미 데이터베이스에 존재하는 한 레코드를 수정하려면 아래와 같이 할 수 있다.

```py
b.name = 'New name'
b.save()
```

Post 인스턴스인 `b` 의 `name` 속성값에 직접 새로운 값을 대입한 다음, `save()` 를 호출하여 데이터베이스에 기록한다.  
위 명령은 내부적으로 데이터베이스에 SQL의 `UPDATE` 문을 사용한다.  
이 경우에도 마찬가지로 `save()` 를 호출하기 전까지는 데이터베이스에 접촉하지 않는다.  

- - -

### ForignKey와 ManyToManyField 수정하기

- `ForignKey` 필드 값의 수정은 보통의 필드 수정과 동일하다. 단, 필드가 받을 수 있는 타입의 객체를 전달해주어야만 한다.  
```py
# pk가 1인 Entry 객체 하나를 가져온다.
entry = Entry.objects.get(pk=1)  
# name이 Dream theater 인 Blog 객체 하나를 가져온다.
dt_blog = Blog.objects.get(name='Dream theater')  
# Entry 인스턴스의 ForignKey 필드인 blog 속성값에 Blog 객체를 대입한다.
entry.blog = dt_blog  
# 데이터베이스에 변경사항 기록
entry.save()  
```
`Entry` 모델의 `blog` 속성은 `ForignKey` 필드이기 때문에 이 필드에 연결된 모델인 `Blog` 모델의 인스턴스를 값으로 가진다. 따라서 값을 수정할 때에도 `blog` 속성에 `Blog` 모델의 인스턴스를 대입해주어야 한다.  

- `ManyToManyField` 필드에 새 값을 추가하려면 `add()` 를 사용한다. `ManyToManyField` 는 다대다 관계이므로 여러 개의 필드 값을 가질 수 있다. 따라서 `add()` 를 사용하면 기존의 값에 새로운 값을 추가하게 된다.  
```py
entry = Entry.objects.get(pk=1)
a1 = Author.objects.get(name='John')
entry.authors.add(a1)
```
아래와 같이 한꺼번에 여러 값을 추가할 수도 있다.
```py
a1 = Author.objects.get(name='John')
a2 = Author.objects.get(name='Mike')
a3 = Author.objects.get(name='James')
entry.authors.add(a1, a2, a3)
```
`add()` 함수에 전달하는 값이 `ManyToManyField` 속성에 연결된 모델의 인스턴스가 아닐 경우, 에러가 난다.

- - -

### 레코드 가져오기

데이터베이스로부터 레코드들을 가져오려면, 모델 클래스의 `매니저 (Manager)` 를 통해 `Queryset` 객체를 생성한다.  
`쿼리셋 (Queryset)` 은 데이터베이스로부터 추출된 객체들의 한 묶음이다. 쿼리셋은 하나 이상의 필터를 가질 수 있으며, 필터는 주어진 조건에 맞는 결과들로만 구성된 쿼리셋을 반환하도록 해준다. 쿼리셋은 SQL에서 하나의 `SELECT` 문과 같으며, 필터들은 `WHERE` 또는 `LIMIT` 절과 같은 역할을 한다.  

쿼리셋은 매니저를 통해 가져올 수 있으며, 각 모델 클래스는 최소한 하나 이상의 매니저를 가지고 있다. 기본적으로 설정되어있는 매니저는 `objects` 이다.  
매니저는 모델 클래스의 인스턴스가 아닌 클래스 자체를 통해서만 접근할 수 있다.

```py
b = Blog(name='Blog name', tagline='Blog tagline)
b.objects
```
```re
Traceback:
    ...
AttributeError: "Manager isn't accessible via Blog instances."
```

- - -

#### 모든 레코드 가져오기

한 테이블의 모든 레코드를 가져오려면 아래와 같이 `all()` 을 사용한다.

```py
all_blogs = Blog.objects.all()
```

`Blog` 테이블의 모든 레코드들의 쿼리셋이 반환된다.

- - -

#### 필터: 특정 레코드 가져오기

한 테이블의 특정 레코드를 가져오려면 필터를 사용할 수 있다.  
다음의 두 명령은 가장 자주 사용하는 필터 기능이다.

- `filter(**kwargs)`: 키워드 인자로 주어진 `lookup` 조건에 **일치하는** 레코드들의 쿼리셋을 반환한다.
```py
# 게시날짜의 년도가 2006년인 모든 Entry 인스턴스의 쿼리셋 반환
e = Entry.objects.filter(pub_date__year=2006)
```

- `exclude(**kwargs)`: 키워드 인자로 주어진 `lookup` 조건에 **일치하지 않는** 레코드들의 쿼리셋을 반환한다.
```py
# 게시날짜의 년도가 2006년이 아닌 모든 Entry 인스턴스의 쿼리셋 반환
e = Entry.objects.exclude(pub_date__year=2006)
```

- - -

##### 필터 연결

여러개의 필터를 이어 붙여서 여러 조건을 동시에 만족하는 레코드들을 가져올 수 있다.

```py
e = Entry.objects.filter(
    headline__startswith='What'
).exclude(
    pub_date__gte=datetime.date.today()  # gte: Greater than or equal to
).filter(
    pub_date__gte=datetime.date(2005, 1, 5)
)
```

위의 명령은 `2005년 1월 5일` 과 현재 날짜 사이에 발행된 `headline` 이 `What` 으로 시작하는 모든 레코드들의 쿼리셋을 반환한다. 


- - -

##### 쿼리셋은 서로 독립적이다

쿼리셋은 생성될 때마다 항상 새로운 객체로 리턴된다.

```py
e1 = Entry.objects.filter(headline__startswith='What')
e2 = e1.exclude(pub_date__gte=datetime.date.today())
e3 = e1.filter(pub_date__gte=datetime.date(2005, 1, 5))
```

`e2` 는 `e1` 쿼리셋에 `exclude` 필터를 적용한 결과에 해당하는 레코드들의 쿼리셋을 새로 생성하여 반환한다. `e3` 의 경우도 마찬가지이다. 위의 과정에서 기존의 `e1` 쿼리셋은 아무 영향을 받지 않는다.  
이는 Python 에서 불변한 (immutable) 객체들을 다룰 때와 비슷하게 생각할 수 있다.

- - -

##### 쿼리셋은 게으르다

쿼리셋을 가져오는 것은 데이터베이스에 아무런 영향을 미치지 않는다. 무수히 많은 필터들을 수 없이 적용하여 쿼리셋을 불러와도 `Django` 는 쿼리셋이 **평가(evaluate)** 되기 전까지는 데이터베이스에 단 한번도 실제로 쿼리를 보내지 않는다.  

```py
q = Entry.objects.filter(headline__startswith="What")
q = q.filter(pub_date__lte=datetime.date.today())
q = q.exclude(body_text__icontains="food")
print(q)
```

위의 명령에서 실제로 데이터베이스에 쿼리를 실행해 데이터를 가져오는 시점은 `print(q)` 가 실행될 때이다. 실제로 데이터베이스에 쿼리를 보내 쿼리셋을 가져오는 것을 쿼리셋이 **평가**되었다고 한다.  
쿼리셋이 언제 평가되는지에 대한 자세한 사항은 [여기](/django/2017/10/15/django-evaluation.html)를 참고하기 바란다.

- - -

#### 하나의 레코드 가져오기

필터는 항상 쿼리셋 객체를 리턴한다. 심지어 조건에 매치되는 레코드가 단 하나일 경우도, 길이가 1인 쿼리셋 객체를 리턴한다.  
만약 특정 조건에 매치되는 레코드가 단 하나임을 알고 있다면, `get()` 을 사용하여 쿼리셋이 아닌 단일 객체 자체를 가져올 수 있다.  

```py
one_entry = Entry.objects.get(pk=1)
```

`get()` 에는 `filter()` 와 같이 `lookup` 조건을 전달할 수 있다.  
`get()` 을 이용한 경우와 `filter()[0]` 을 이용해 하나의 객체를 가져온 경우의 차이점은 `get()` 을 이용할 경우 매치되는 값이 없으면 `DoesNotExist` 예외가 발생하며, `filter()[0]` 의 경우는 `IndexError` 가 발생한다.  
`DoesNotExist` 는 모델 클래스의 속성이다. 따라서, 위의 코드에서 매치되는 결과가 없다면 `Entry.DoesNotExist` 가 발생하게 된다.  

`get()` 에 매치된 결과가 여러 개일 경우에도 에러가 발생한다. 이 경우 발생하는 에러는 `MultipleObjectsReturned` 이며, 이 에러 역시 모델 클래스의 속성이다.

- - -

### 쿼리 제한하기

Python의 슬라이싱 문법을 통해서 쿼리셋에 들어갈 데이터를 제한할 수 있다. SQL의 `LIMIT` 과 `OFFSET` 문과 같은 역할을 한다.  

- 처음 5 개의 레코드의 쿼리셋(`LIMIT 5`)
```py
Entry.objects.all()[:5]
```

- 여섯번째 레코드부터 열번째 레코드까지의 쿼리셋(`OFFSET 5 LIMIT 5`)
```py
Entry.objects.all()[5:10]
```

음수 슬라이싱은 지원하지 않는다.  

기본적으로 슬라이싱을 실행하면 그 결과를 평가되지 않은 새로운 쿼리셋으로 반환하게 되는데, **스텝**을 사용하면 쿼리셋을 평가하여 데이터베이스에서 데이터를 가져오게 되며 그 결과를 리스트로 반환한다.  

- 처음부터 열번째 레코드 중 매 두번째 레코드들의 쿼리셋
```py
Entry.objects.all()[:10:2]
```

하나의 값을 가져오려면 인덱싱을 해준다. 가져오려는 인덱스의 값이 없을 경우 `IndexError` 를 일으킨다.

- `headline` 필드를 기준으로 오름차순 정렬한 레코드들 중 첫번째 레코드
```py
Entry.objects.order_by('headline')[0]
```

- - -

###### Reference
Django 공식문서: [https://docs.djangoproject.com/en/1.11/topics/db/queries/#making-queries](https://docs.djangoproject.com/en/1.11/topics/db/queries/#making-queries)
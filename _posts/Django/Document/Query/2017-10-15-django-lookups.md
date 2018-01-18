---
layout: post
title: '[Query] 필드 룩업 (내용 추가 필요)'
subtitle: Field Lookups
category: Django
tags:
  - Django
  - Database
  - Query
  - ORM
---

`필드 룩업 (Field lookups)` 은 SQL의 `WHERE` 절에 해당하는 부분이다.  
쿼리셋 메서드인 `filter()`, `exclude()`, `get()` 에 키워드 인자의 형태로 전달된다.  
필드 룩업의 기본적인 형태는 아래와 같다.

```py
필드이름__룩업타입=조건값
```

예를 들면, 2006년 이전에 발행된 `Entry` 객체들의 쿼리셋을 가져오려면 다음과 같이 할 수 있다.

```py
Entry.objects.filter(pub_date__lte='2006-01-01')  # lte: less than or equal to
```

이것은 대략 다음의 SQL 문과 같은 동작을 한다.

```sql
SELECT * 
FROM blog_entry 
WHERE pub_date <= '2006-01-01';
```

룩업에 들어가는 필드이름은 검색하려는 모델의 필드이름이며, 예외적으로 `ForignKey` 필드의 경우에는 필드이름에 `_id` 가 들어간다. 외래키 필드를 검색하는 경우에는 조건값으로 외래키 필드가 참조하고 있는 레코드의 기본키 필드 값을 전달해주어야 한다.  

예를 들어, 다음은 `Blog` 테이블의 기본키 값이 4인 레코드를 참조하고 있는 모든 `Entry` 테이블의 레코드들의 쿼리셋을 반환한다.

```py
Entry.objects.filter(blog_id=4)
```

잘못된 룩업 타입을 전달한 경우, `TypeError` 가 발생한다.

- - -

### 자주 사용하는 룩업 타입


- **`exact`**: 완전히 일치하는 값 검색.
```py
Entry.objects.get(headline__exact="Cat bites dog")
```
위 명령은 `Entry` 테이블에서 `headline` 변수가 정확히 `"Cat bites dong"` 인 레코드를 가져온다.  
필드 룩업을 사용할 때, 룩업 타입, 즉, `__` 와 그 이후 부분을 지정하지 않으면, 자동으로 `exact` 를 사용한 매치를 실행한다.
```py
Blog.objects.get(id__exact=4)
Blog.objects.get(id=4)
``` 
위 두 명령의 결과는 동일하다. 상당히 자주 사용하는 룩업타입이기 때문에 편의성을 위해 이렇게 되어있다.  

- **`iexact`**: 대소문자 구분을 하지 않는 `exact`.
```py
Blog.objects.get(name__iexact="beatles blog")
```
`Beatles blog`, `beatles Blog`, `BEAtles BlOg` 등등이 모두 매치됨.

- **`contains`**: 조건값을 포함한 값과 매치됨. 대소문자 구분함.
```py
Entry.objects.get(headline__contains='Lennon')
```
위 명령은 아래 SQL 문과 같다.
```sql
SELECT * 
FROM Entry 
WHERE headline 
LIKE '%Lennon%';
```
`headline` 값에 `Lennon` 이 포함된 레코드들을 가져온다.

- **`icontains`**: `contains` 의 대소문자 무시 버전.

- **`startswith`, `endswith`**: 각각 조건값으로 시작, 끝나면 매치된다. 대소문자 구분함.

- **`istartswith`, `iendswith`**: `startswith`, `endswith` 의 대소문자 무시 버전.

- - -

###### Reference

Django 공식문서: [https://docs.djangoproject.com/en/1.11/topics/db/queries/#field-lookups](https://docs.djangoproject.com/en/1.11/topics/db/queries/#field-lookups)
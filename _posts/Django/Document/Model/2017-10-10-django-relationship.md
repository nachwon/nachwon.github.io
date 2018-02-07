---
layout: post
title: '[Model] 관계'
subtitle: Relationships
category: Django
tags:
  - Django
  - Model
  - Database
---

<span id="list"></span>
관계형 데이터베이스 시스템의 핵심은 테이블 간의 관계 설정이라고 할 수 있다. `Django` 는 데이터베이스 관계의 가장 흔한 유형인  

- **[`다대일 (Many-to-One)`](#mto)**
- **[`다대다 (Many-to-Many)`](#mtm)**
- **[`일대일 (One-to-One)`](#oto)**

관계를 구현할 수 있는 기능을 제공한다.

- - -

<span id='mto'></span>
### 다대일 관계 (Many-to-one relationships)

한 테이블에 있는 두 개 이상의 레코드가 다른 테이블에 있는 하나의 레코드를 참조할 때, 두 모델간의 관계를 **다대일 관계**라고 한다. 

- - -
<span id='order-customer'></span>
##### Customers 테이블

<table class="table table-striped table-bordered">
    <tr>
        <th>ID</th>
        <th>Name</th>
    </tr>
    <tr>
        <td>1</td>
        <td>James Hetfield</td>
    </tr>
</table>

##### Orders 테이블

<table class="table table-striped table-bordered">
    <tr>
        <th>ID</th>
        <th>Product</th>
        <th>Customer_ID</th>
    </tr>
    <tr>
        <td>1</td>
        <td>ESP Guitar</td>
        <td>1</td>
    </tr>
    <tr>
        <td>2</td>
        <td>Mesaboogie Amplifier</td>
        <td>1</td>
    </tr>
    <tr>
        <td>3</td>
        <td>Guitar Pick</td>
        <td>1</td>
    </tr>
</table>
- - -

`Orders` 테이블의 `Customer_ID` 필드는 `Customers` 테이블의 기본키 (Primary Key) 인 `ID` 필드를 참조하고 있다. 이 때, `Orders` 테이블의 `Customer_ID` 필드를 **외래키 (Forign Key)** 필드라고 한다.  


- - -

#### ForignKey

`Django` 에서 다대일 관계를 설정할 때는 아래와 같이 `ForignKey` 를 사용한다. 다른 필드 타입과 마찬가지로 모델 클래스의 속성으로 입력하며, 연결대상이 될 모델 객체를 위치인자로 전달해주어야 하고, `on_delete` 옵션을 필수로 입력해주어야 한다.

```py
class 모델이름(models.Model):
    필드이름 = models.ForeignKey(연결대상모델, on_delete=삭제옵션)
``` 

```py
# Customers Table
class Customer(models.Model):
    name = models.CharField(max_length=50)


# Orders Table
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # 외래키 설정
    product = models.CharField(max_length=50)
```

>**ForignKey 필드의 이름**
>
>`ForignKey` 필드의 필드이름은 자유롭게 설정할 수 있지만, 연결대상 모델명의 소문자로 정하는 것을 >권장한다.  
>
>```py
>customer = models.ForeignKey(Customer)
>manufacturer = models.ForignKey(Manufacturer)
>```

- - -

##### on_delete 옵션

`on_delete` 은 레코드를 삭제했을 때, 그 레코드를 참조하는 레코드들에 대한 행동을 정의한다. 현재는 반드시 명시하지 않아도 되지만, `Django 2.0` 버전부터는 필수 옵션이 된다. 
다음과 같은 옵션값들이 있다.

- `models.CASCADE`: 레코드가 삭제되면, 그 레코드를 외래키로 참조하고 있는 모든 레코드들을 함께 삭제한다. 현재 `Django` 버전에서 `on_delete` 값을 명시하지 않았을 경우의 기본값이다.

- `models.PROTECT`: 외래키가 참조하고 있는 레코드를 삭제하지 못하게 만든다. 삭제를 시도하면 `ProtectedError` 를 발생시킨다.

- `models.SET_NULL`: 외래키가 참조하고 있는 레코드가 삭제되면, 외래키 필드의 값이 `null` 이 된다. 외래키 필드에 `null=True` 옵션이 있을 때만 가능함.

- `models.SET_DEFAULT`: 외래키가 참조하고 있는 레코드가 삭제되면, 외래키 필드의 값이 기본값으로 바뀐다. `default` 옵션이 설정되어 있을 때만 가능함.

- `models.SET()`: `SET()` 함수에  값이나 호출가능한 객체를 전달할 수 있으며,외래키가 참조하고 있는 레코드가 삭제되면 전달된 값 또는 객체를 호출한 결과로 외래키 필드를 채운다.

- - -

#### 재귀적 관계 (Recursive relationship)

한 테이블의 레코드들이 같은 테이블의 다른 레코드들과 관계를 형성하는 것을 `재귀적 관계` 라고 한다.  
예를 들어, 그룹스터디에서 멤버 한 명이 다른 멤버들을 가르치는 경우를 아래와 같이 표현할 수 있다.

- - -
##### StudyGroup 테이블

<table class="table table-striped table-bordered">
    <tr>
        <th>ID</th>
        <th>Name</th>
        <th>Tutor_ID</th>
    </tr>
    <tr>
        <td>1</td>
        <td>Joe Satriani</td>
        <td>1</td>
    </tr>
    <tr>
        <td>2</td>
        <td>John Petrucci</td>
        <td>1</td>
    </tr>
    <tr>
        <td>3</td>
        <td>Steve Vai</td>
        <td>1</td>
    </tr>
</table>

`StudyGroup` 테이블의 `Tutor_ID` 필드는 `StudyGroup` 테이블의 기본키인 `ID` 필드를 참조한다.

- - -

재귀적 관계는 아래와 같이 연결대상 위치인자로 `'self'` 를 전달하여 설정할 수 있다.  

```py
class StudyGroup(models.Model):
    name = models.CharField(max_length=30)
    tutor = models.ForeignKey('self', on_delete=models.SET_NULL)  # 'self' 를 위치인자로 전달
```

- - -

#### 아직 정의되지 않은 테이블과의 관계

아직 정의되지 않은 테이블과의 관계를 설정해야할 때는, 연결대상 위치인자로 모델 객체 대신 문자열로 `'모델명'` 을 전달하면 된다.

```py
class Car(models.Model):
    name = models.CharField(max_length=50)
    manufacturer = models.ForignKey('Manufacturer', on_delete=models.CASCADE)
    # 이 시점에는 아직 Manufacturer 모델이 정의되지 않음


class Manufacturer(models.Model):
    name = models.CharField(max_length=50)
```

[위로](#list)

- - -
<span id='mtm'></span>
### 다대다 관계 (Many-to-many relationship)

한 테이블의 하나 이상의 레코드가 다른 테이블의 하나 이상의 레코드를 참조할 때, 두 모델간의 관계를 `다대다 관계` 라고 한다.  
다대다 관계를 표현할 때는, 두 테이블 사이의 관계를 표현하기 위해 참조 정보를 담은 새로운 테이블을 생성하게된다.  
아래는 다대다 관계를 표현한 예제이다.

- - -

##### Pizza 테이블

<table class="table table-striped table-bordered">
    <tr>
        <th>ID</th>
        <th>PizzaName</th>
    </tr>
    <tr>
        <td>1</td>
        <td>Pepperoni Pizza</td>
    </tr>
    <tr>
        <td>2</td>
        <td>Sausage Pizza</td>
    </tr>
    <tr>
        <td>3</td>
        <td>Cheeze Pizza</td>
    </tr>
</table>    

##### Topping 테이블

<table class="table table-striped table-bordered">
    <tr>
        <th>ID</th>
        <th>ToppingName</th>
    </tr>
    <tr>
        <td>1</td>
        <td>Pepperoni</td>
    </tr>
    <tr>
        <td>2</td>
        <td>Cheeze</td>
    </tr>
    <tr>
        <td>3</td>
        <td>Sausage</td>
    </tr>
</table>

##### Pizza_Topping 테이블

<table class="table table-striped table-bordered">
    <tr>
        <th>ID</th>
        <th>Pizza_ID</th>
        <th>Topping_ID</th>
    </tr>
    <tr>
        <td>1</td>
        <td>1</td>
        <td>1</td>
    </tr>
    <tr>
        <td>2</td>
        <td>1</td>
        <td>2</td>
    </tr>
    <tr>
        <td>3</td>
        <td>2</td>
        <td>2</td>
    </tr>
    <tr>
        <td>4</td>
        <td>2</td>
        <td>3</td>
    </tr>
    <tr>
        <td>5</td>
        <td>3</td>
        <td>2</td>
    </tr>
</table>

피자는 여러개의 토핑을 가질 수 있고, 토핑도 여러개의 피자에 올라갈 수 있기 때문에 서로 다대다 관계를 가지고 있다.  
`Pizza_Topping` 테이블은 두 테이블 간의 다대다 관계를 나타내주는 **중개 모델 (intermediary model)** 이다.  
`Pizza_Topping` 테이블은 자동 생성되며, `Pizza` 테이블과 `Topping` 테이블의 `ID` 필드를 각각 참조하는 `Pizza_ID` 와 `Topping_ID` 를 외래키 필드로 가지고 있다.

- - -

#### ManyToManyField

`Django` 에서 테이블 간 다대다 관계를 설정해주려면 아래와 같이 `ManyToManyField` 를 사용해서 필드를 만들어준다.

```py
class 모델이름(models.Model):
    필드이름 = models.ManyToManyField(연결대상모델)
```
```py
class Topping(models.Model):
    name = models.CharField(max_length=10)


class Pizza(models.Model):
    name = models.CharField(max_length=10)
    toppings = models.ManyToManyField(Topping)
```

`ForignKey` 와 마찬가지로 `ManyToManyField` 도 동일한 방법으로 재귀적 관계와 아직 정의되지 않은 테이블에 대한 관계를 설정할 수 있다.  

> **ManyToManyField 필드 권장사항**
>
> - `ManyToManyField` 필드의 필드이름은 복수형으로 설정하는 것을 권장한다.  
>
> ```py
> toppings = models.ManyToManyField(Topping)
> ```
>
> - 서로 관계된 모델들 중 어느 곳에 `ManyToManyField` 를 선언하든 상관이 없지만 반드시 한 모델에만 선언해야하며, 의미적으로 자연스러운 관계가 되도록 선언해주는 것을 권장한다.  
> - 예를 들어, 피자에 들어갈 토핑을 선택하는 것이 토핑이 들어갈 피자를 선택하는 것보다 자연스러우므로 `ManyToManyField` 를 `Pizza` 모델에 선언해주는 것이 더 자연스럽다.  


- - -

#### 중개 모델 직접 생성하기

다대다 관계에서는 두 테이블 간의 관계를 표현하는 테이블이 자동적으로 생성된다. 하지만 사용자가 직접 중개 모델을 생성해줄 수도 있으며, 이 때 추가적인 정보를 담은 필드들을 중개 모델에 삽입할 수도 있다.

- - -

##### Artist 테이블

<table class="table table-striped table-bordered">
    <tr>
        <th>ID</th>
        <th>ArtistName</th>
    </tr>
    <tr>
        <td>1</td>
        <td>John Petrucci</td>
    </tr>
    <tr>
        <td>2</td>
        <td>Jordan Rudess</td>
    </tr>
    <tr>
        <td>3</td>
        <td>John Myung</td>
    </tr>
</table>

##### Band 테이블

<table class="table table-striped table-bordered">
    <tr>
        <th>ID</th>
        <th>BandName</th>
    </tr>
    <tr>
        <td>1</td>
        <td>Dream Theater</td>
    </tr>
    <tr>
        <td>2</td>
        <td>Liquid Tension Experiment</td>
    </tr>
</table>

##### Membership 테이블

<table class="table table-striped table-bordered">
    <tr>
        <th>ID</th>
        <th>Artist_ID</th>
        <th>Band_ID</th>
        <th>Is_Founding_Member</th>
    </tr>
    <tr>
        <td>1</td>
        <td>1</td>
        <td>1</td>
        <td>True</td>
    </tr>
    <tr>
        <td>2</td>
        <td>1</td>
        <td>2</td>
        <td>True</td>
    </tr>
    <tr>
        <td>3</td>
        <td>2</td>
        <td>1</td>
        <td>False</td>
    </tr>
    <tr>
        <td>4</td>
        <td>2</td>
        <td>2</td>
        <td>True</td>
    </tr>
    <tr>
        <td>5</td>
        <td>3</td>
        <td>1</td>
        <td>True</td>
    </tr>
</table>

`Membership` 테이블은 `Artist` 테이블과 `Band` 테이블 사이의 관계를 나타내는 중개 모델이며, 추가적으로 해당 아티스트가 해당 밴드의 창립멤버인지에 대한 정보를 담은 필드도 포함하고있다.

- - -

#### through

중개 모델을 직접 생성하려면 `ManyToManyField` 필드의 옵션으로 `through` 값을 넣어주면 된다.

```py
class 모델이름(models.Model):
    필드이름 = models.ManyToManyField(연결대상모델, through='관계모델')
```

```py
class Artist(models.Model):
    name = models.CharField(max_length=50)


class Band(models.Model):
    name = models.CharField(max_length=50)
    members = models.ManyToManyField(Artist, through='Membership')


class Membership(models.Model):
    artist = models.ForignKey(Artist, on_delete=models.CASCADE)
    band = models.ForignKey(Band, on_delete=models.CASCADE)
    is_founding_member = models.BooleanField()
```

- - -

#### 중개 모델의 제약사항

중개 모델을 직접 생성하는 경우, 관계를 가지는 두 테이블을 각각 참조하는 외래키 필드를 명확히 선언해주어야 한다. 중개 모델을 직접 생성할 때에는 아래와 같은 제약사항이 따른다.

- 중개 모델에는 다대다 관계의 **소스모델(Source model)**과 **타겟모델(Target model)**을 참조하는 외래키가 반드시 **각각 하나씩** 있어야 한다.  

    - **소스모델**은 `ManyToManyField` 필드가 있는 모델을 말한다.
    - **타겟모델**은 `ManyToManyField` 에 인자로 전달되는 모델을 말한다.
    
    만약 중개 모델에서 하나 이상의 외래키 필드가 소스모델 혹은 타겟모델을 참조한다면, **`through_field`** 옵션을 통해 관계 형성에 사용할 외래키를 반드시 설정해주어야 한다. 그렇지 않으면 `ValidationError` 가 발생한다.

- 재귀적 다대다 관계를 맺을 경우, 중개 모델이 하나의 모델을 참조하는 두 개의 외래키 필드를 가지는 것이 허용된다. 그러나 같은 모델을 참조하는 외래키 필드가 두 개를 초과한 경우, 마찬가지로 `through_field` 옵션을 통해 관계 형성에 사용될 외래키 필드 두 개를 명확히 지정해주어야 한다.

- 중개 모델을 직접 생성하여 재귀적 다대다 관계를 설정할 경우, `symmetrical=False` 옵션을 반드시 추가해주어야 한다.

아래의 예제 테이블을 보자.
- - -

##### Artist 테이블

<table class="table table-striped table-bordered">
    <tr>
        <th>ID</th>
        <th>ArtistName</th>
    </tr>
    <tr>
        <td>1</td>
        <td>John Petrucci</td>
    </tr>
    <tr>
        <td>2</td>
        <td>Jordan Rudess</td>
    </tr>
    <tr>
        <td>3</td>
        <td>John Myung</td>
    </tr>
</table>

##### Band 테이블

<table class="table table-striped table-bordered">
    <tr>
        <th>ID</th>
        <th>BandName</th>
    </tr>
    <tr>
        <td>1</td>
        <td>Dream Theater</td>
    </tr>
    <tr>
        <td>2</td>
        <td>Liquid Tension Experiment</td>
    </tr>
</table>

##### Membership 테이블

<table class="table table-striped table-bordered">
    <tr>
        <th>ID</th>
        <th>Artist_ID</th>
        <th>Band_ID</th>
        <th>Inviter_ID</th>
    </tr>
    <tr>
        <td>1</td>
        <td>1</td>
        <td>1</td>
        <td>1</td>
    </tr>
    <tr>
        <td>2</td>
        <td>1</td>
        <td>2</td>
        <td>1</td>
    </tr>
    <tr>
        <td>3</td>
        <td>2</td>
        <td>1</td>
        <td>1</td>
    </tr>
    <tr>
        <td>4</td>
        <td>2</td>
        <td>2</td>
        <td>1</td>
    </tr>
    <tr>
        <td>5</td>
        <td>3</td>
        <td>1</td>
        <td>1</td>
    </tr>
</table>

중개 테이블인 `Membership` 테이블의 `Artist_ID` 필드는 `Artist` 테이블의 기본키를 참조하고 있는 외래키 필드이다.  
`Band_ID` 필드는 `Band` 테이블의 기본키를 참조하고 있는 외래키 필드이다.
`Inviter_ID` 필드는 `Artist` 테이블의 기본키 필드를 참조하고 있으며, 해당 아티스트를 밴드에 초대한 아티스트가 누군지에 대한 정보를 담고있다.  

이러한 경우 다대다 관계를 형성하기 위해 어떤 외래키 필드를 사용할지 명시해주어야 한다.  
`Artist_ID` 필드와 `Band_ID` 필드를 연결할지, `Artist_ID` 필드와 `Inviter_ID` 필드를 연결할지, 아니면 `Band_ID` 필드와 `Inviter_ID` 필드를 연결할지 명확히 정해주어야 한다.  

다대다 관계를 형성해야할 필드는 `Artist_ID` 필드와 `Band_ID` 필드이므로 이것을 `Django` 에 알려주기위해 `through_fields` 를 사용한다.

- - -

#### through_fields


중개모델을 직접 생성할 때, `through_fields` 옵션을 사용해서 관계를 형성하는 두 모델을 명시해줄 경우 아래와 같이 할 수 있다.

```py
class 타겟모델(models.Model):
    필드1
    필드2
    ...


class 소스모델(models.Model):
    필드이름 = models.ManyToManyField(
        타겟모델, 
        through=중개모델, 
        through_fields=('소스필드', '타겟필드',)  # 반드시 소스필드, 타겟필드 순서로 된 튜플로 전달
        )
    필드2
    필드3
    ...


class 중개모델(models.Model):
    # through_fields 옵션에는 소스 및 타겟모델이 아닌 중개모델에 선언된 소스 및 타겟 "필드"의 이름을 문자열로 전달해야한다.
    타겟필드 = models.ForignKey(타겟모델)
    소스필드 = models.ForignKey(소스모델)
    추가외래키필드 = models.ForignKey(관계대상모델)
    ...
```

```py
class Artist(models.Model):
    name = models.CharField(max_length=50)


class Band(models.Model):
    name = models.CharField(max_length=50)
    members = models.ManyToManyField(
        Artist, 
        through='Membership',
        through_fields=('band', 'artist',)
    )


class Membership(models.Model):
    artist = models.ForignKey(Artist, on_delete=models.CASCADE)
    band = models.ForignKey(Band, on_delete=models.CASCADE)
    inviter = models.ForignKey(Artist, on_delete=models.CASCADE)
```

`through_fields` 옵션에 `Band`, `Artist` 모델이 아닌 `'band'`, `'artist'` 필드를 전달하였다.  
그 결과로 중개 모델에서 `Band` 와 `Artist` 모델간의 다대다 관계를 형성하는데에 `artist` 와 `band` 필드를 사용한다.  
중개 모델의 `inviter` 필드 역시 `Artist` 모델을 참조하지만 다대다 관계 형성에는 아무 역할을 하지 않는다.

- - -

#### 관계의 역참조

그런데 위의 예제 코드를 작성한 뒤 `migrate` 를 시켜보면 아래와 같은 에러가 난다.

```error
ERRORS:
model.Membership.artist: (fields.E304) Reverse accessor for 'Membership.artist' clashes with reverse accessor for 'Membership.inviter'.
        HINT: Add or change a related_name argument to the definition for 'Membership.artist' or 'Membership.inviter'.
model.Membership.inviter: (fields.E304) Reverse accessor for 'Membership.inviter' clashes with reverse accessor for 'Membership.artist'.
        HINT: Add or change a related_name argument to the definition for 'Membership.inviter' or 'Membership.artist'.
```

`Membership` 모델의 `artist` 필드의 `Reverse accessor` 가 `Membership` 모델의 `inviter` 필드의 `Reverse accessor` 와 충돌이 난다는 내용이다. `Reverse accessor` 가 무엇일까?

외래키 필드를 가진 소스모델에 연결된 타겟모델의 인스턴스들은 자신과 연결된 소스모델의 인스턴스들을 가져올 수 있는 `Manager` 를 가지게 된다.  
기본적으로 이 `Manager` 는 `FOO_set` 의 형태로 이름지어지며, 여기서 `FOO` 는 소문자로 변환된 소스모델 이름(예를 들어, 소스모델 이름이 `Order` 라면, `order_set`)이다.  
`Reverse accessor` 는 관계를 역참조할 수 있는 이 `Manager` 를 가리킨다.  

- - -

##### 다대일 관계의 역참조

위의 `Orders, Customers 테이블`[[테이블 보기]](#order-customer) 을 예로 들면, `Customer` 모델은 `Order` 모델의 타겟모델이다.  
소스모델의 인스턴스에서 타겟모델의 인스턴스를 가져오려면 아래와 같이 관계가 정의된 속성의 이름을 붙여준다.

```py
o = Order.objects.get(id=1)
o.customer  # 1번 주문을 한 고객을 가져온다.
```

여기서 반대로 타겟 인스턴스에서 소스 인스턴스를 역참조하려면 아래와 같이 한다.

```py
c = Customer.objects.get(id=1)
c.order_set.all()  # 소스모델의 이름은 Order 이므로, 역참조 매니저의 이름은 order_set 이 된다.
```

이것의 결과로 1번 고객에 연결된 모든 `Order` 모델의 인스턴스들이 쿼리셋으로 리턴된다.

- - -

##### 다대다 관계의 역참조

다대다 관계에서의 역참조는 `Artist, Group 테이블` 을 예로 들어 설명한다.
먼저 소스 인스턴스에서 타겟 인스턴스를 참조할 때는 아래와 같이 타겟필드 이름을 사용한다.

```py
g = Group.objects.first()
g.members.all()  # 그룹에 속한 모든 멤버들의 쿼리셋을 리턴
```

반대로 타겟 인스턴스에서 소스 인스턴스를 역참조할 때는 아래와 같이 역참조 매니저를 사용한다.

```py
a = Artist.objects.first()
a.group_set.all()  # 아티스트가 속한 모든 그룹의 쿼리셋을 리턴
```

다대다 관계에서는 `Membership` 중개 모델이 있기 때문에 이 중개 모델을 역참조하는 `membership_set` 매니저 또한 생성된다.  
`Membership` 모델의 인스턴스는 아래와 같이 필드이름을 사용하여 연결된 각 모델들의 인스턴스들을 참조할 수 있다.   

```py
m = Membership.objects.first()
m.artist  # 해당 멤버쉽의 아티스트 참조
m.group  # 해당 멤버쉽의 그룹 참조
```

`Artist` 의 인스턴스와 `Group` 의 인스턴스는 각각 역참조 매니저를 통해 `Membership` 모델의 인스턴스들을 역참조 할 수 있다.  

```py
g = Group.objects.first()
g.membership_set.all()  # 그룹이 멤버쉽에서 참조되는 곳들을 모두 조회

a = Artist.objects.first()
a.membership_set.all()  # 아티스트가 멤버쉽에서 참조되는 곳들을 모두 조회..??????
```

그런데 바로 여기서 위의 에러가 발생한 것이다. `Membership` 모델에는 `Artist` 를 참조하고 있는 외래키 필드가 두 개 (`artist`, `inviter`) 이다. `membership_set` 을 통해 `Artist` 의 인스턴스가 참조되는 곳을 조회하도록 하면, `Artist` 모델을 참조하고 있는 두 외래키 필드 중 어느 필드의 값을 가져와야 하는지 알지 못한다.

- - -

##### related_name

역참조 매니저의 이름은 `FOO_set` 의 형태로 자동 생성된다고 했다. 위와 같은 에러를 해결하기 위해서는 `inviter` 필드를 역참조할 때 사용하는 역참조 매니저의 이름을 바꿔주어야 한다. 이 때 사용하는 옵션이 `related_name` 이다. 아래와 같이 사용한다.

```py
class Artist(models.Model):
    name = models.CharField(max_length=50)


class Band(models.Model):
    name = models.CharField(max_length=50)
    members = models.ManyToManyField(
        Artist, 
        through='Membership',
        through_fields=('band', 'artist',)
    )


class Membership(models.Model):
    artist = models.ForignKey(Artist, on_delete=models.CASCADE)
    band = models.ForignKey(Band, on_delete=models.CASCADE)
    inviter = models.ForignKey(
        Artist, 
        on_delete=models.CASCADE,
        related_name='membership_inviter_set'
        )  # 역참조 매니저 이름을 직접 만들어 줄 필드에 입력한다.
```

이렇게 하면 `Artist` 의 인스턴스에서 `Membership` 의 인스턴스를 역참조할 때 아래와 같이 해줄 수 있게 된다.

```py
a = Artist.objects.first()
a.membership_set.all()  # 해당 아티스트의 기본키값을 aritst_id 필드에서 참조하는 모든 레코드
a.membership_inviter_set.all()  # 해당 아티스트의 기본키값을 inviter_id 필드에서 참조하는 모든 레코드
```

어떤 관계를 역참조할지 구별할 수 있게 된다.

[위로](#list)


- - -

<span id='oto'></span>
### 일대일 관계 (One-to-one relationship)

한 테이블의 하나의 레코드가 다른 테이블의 단 하나의 레코드만을 참조할 때, 이 두 모델간의 관계를 `일대일 관계` 라고 한다. 일대일 관계는 어떤 테이블을 구조적으로 **확장**시킬 때 가장 유용하게 쓰인다.  
다음의 예를 보자.

- - -

##### Place 테이블

<table class="table table-bordered table-striped">
    <tr>
        <th>Name</th>
        <th>Address</th>
    </tr>
    <tr>
        <td>손중헌 논메기매운탕</td>
        <td>대구시 달성군 다사읍</td>
    </tr>
    <tr>
        <td>논골집 논현점</td>
        <td>서울특별시 강남구 논현동</td>
    </tr>
    <tr>
        <td>우리집</td>
        <td>경기도 안산시 상록구</td>
    </tr>
</table>

##### Restaurant 테이블

<table class="table table-striped table-bordered">
    <tr>
        <th>Place_ID</th>
        <th>Menu</th>
        <th>Rating</th>
    </tr>
    <tr>
        <td>1</td>
        <td>메기매운탕</td>
        <td>9.5</td>
    </tr>
    <tr>
        <td>2</td>
        <td>갈비탕</td>
        <td>8</td>
    </tr>
</table>

`Restaurant` 테이블의 각 레코드는 `Place` 테이블의 한 레코드만을 참조한다.  
`Restaurant` 테이블은 `Place` 테이블의 레코드들 중 식당인 레코드에 `Menu` 와 `Rating` 이라는 추가적인 정보를 제공하여 테이블을 확장시키고 있다고 볼 수 있다.  
다시 말해, 식당의 정보를 담은 테이블을 만들려고 할 때, 완전히 별개의 테이블에 장소 이름과, 주소를 또다시 반복하여 입력할 필요없이, 기존에 존재하는 장소들 중 식당인 장소에 추가 정보를 덧붙여 식당 정보 테이블을 만드는 것이다.  
아래는 위 관계를 하나의 테이블에 표시한 것이다.

##### Place-Restaurant 테이블

<table class="table table-bordered table-striped">
    <tr>
        <th>Name</th>
        <th>Address</th>
        <th>Menu</th>
        <th>Rating</th>
    </tr>
    <tr>
        <td>손중헌 논메기매운탕</td>
        <td>대구시 달성군 다사읍</td>
        <td>메기매운탕</td>
        <td>9.5</td>
    </tr>
    <tr>
        <td>논골집 논현점</td>
        <td>서울특별시 강남구 논현동</td>
        <td>갈비탕</td>
        <td>8</td>
    </tr>
    <tr>
        <td>우리집</td>
        <td>경기도 안산시 상록구</td>
        <td><i>null</i></td>
        <td><i>null</i></td>
    </tr>
</table>

- - -

#### OneToOneField

`Django` 에서 모델에 일대일 관계 필드를 추가하려면 `OneToOneField` 를 사용한다.  
`OneToOneField` 는 `ForignKey` 필드에 `unique=True` 옵션을 준 것과 동일하게 동작한다. 즉, 외래키 필드의 값은 반드시 고유한 값이어야 한다.  
재귀적 관계와 아직 정의되지 않은 관계 또한 `ForignKey` 필드와 동일한 방식으로 설정한다.

```py
class 모델이름(models.Model):
    필드이름 = models.OneToOneField(관계대상모델)
```

```py
class Place(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=100)


class Restaurant(models.Model):
    place = models.OneToOneField(Place)
    menu = models.CharField(max_length=50, blank=True, null=True)
    rating = models.FloatField(default=0, blank=True, null=True)
```

- - -

##### 일대일 관계의 역참조

일대일 관계에서 소스모델 (`Restaurant`) 이 타겟모델 (`Place`) 을 참조할 때는, 다대일 관계의 경우와 같이 관계가 정의된 속성이름을 사용한다.

```py
r = Restaurant.objects.first()
r.place
```

이 경우, 다대일 관계와 동일하게 하나의 모델 객체를 돌려받는다.

반대로 타겟모델에서 소스모델을 역참조할 때는, `모델이름소문자_set` 을 사용했던 다대일 관계의 경우와 달리 `소문자소스모델이름` 를 사용한다.

```py
p = Place.objects.first()
p.restaurant
```

이 경우에도 마찬가지로 하나의 모델 객체를 돌려받는다. 하나의 레코드는 단 하나의 레코드를 참조하기 때문이다.

- - -

##### 참조-역참조 요약

<table class="table table-bordered table-striped">
    <tr>
        <th></th>
        <th>OneToOneField</th>
        <th>ManyToOneField</th>
        <th>ManyToManyField</th>
    </tr>
    <tr>
        <td rowspan="2" style="vertical-align: middle; text-align:center;"><b>참조<br>(소스 > 타겟)</b></td>
        <td>source.attname</td>
        <td>source.attname</td>
        <td>source.attname</td>
    </tr>
    <tr>
        <td>단일 객체 리턴</td>
        <td>단일 객체 리턴</td>
        <td>다수의 객체 리턴</td>
    </tr>
    <tr>
        <td rowspan="2" style="vertical-align: middle; text-align:center;"><b>역참조<br>(타겟 > 소스)</b></td>
        <td>target.lowersource</td>
        <td>target.lowersource_set</td>
        <td>target.lowersource_set</td>
    </tr>
    <tr>
        <td>단일 객체 리턴</td>
        <td>다수의 객체 리턴</td>
        <td>다수의 객체 리턴</td>
    </tr>
</table>

[위로](#list)

- - -

###### Reference

Django 공식문서: [https://docs.djangoproject.com/en/1.11/topics/db/models/#relationships](https://docs.djangoproject.com/en/1.11/topics/db/models/#relationships)
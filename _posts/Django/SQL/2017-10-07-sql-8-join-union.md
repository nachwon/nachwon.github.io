--- 
layout: post 
title: '[SQL] JOIN, UNION'
category: Django 
tags:
  - SQL 
--- 



### 예제 테이블

{% include /sql/sql-customers-table.html %}

{% include /sql/sql-orders-table.html %}

{% include /sql/sql-suppliers-table.html %}

- - -

<span id="join"></span>

### JOIN

`JOIN` 절은 서로 다른 테이블에서 가져온 레코드들을 공통된 필드를 기준으로 합쳐준다.  

```sql
SELECT 필드이름1, 필드이름2, ...
FROM 테이블이름1
옵션 JOIN 테이블이름2 ON 테이블이름1.필드이름 = 테이블이름2.필드이름
```

`JOIN` 절의 옵션은 아래와 같다.

- `INNER`: 두 테이블 모두에 기준 필드의 값이 있는 레코드만 가져온다.

<img src="/img/SQL/inner_join.gif" style="display: block; margin-left: 150px;">

- `LEFT`: 왼쪽 테이블(테이블이름1)에 있는 모든 레코드를 가져오고, 기준 필드의 값과 매치되는 레코드들을 오른쪽 테이블(테이블이름2)에서 가져온다.  
왼쪽 테이블의 기준 필드 값과 매치되는 값이 오른쪽 테이블에 없으면 `null` 값을 가져온다.

<img src="/img/SQL/left_join.gif" style="display: block; margin-left: 150px;">

- `RIGHT`: 오른쪽 테이블(테이블이름2)에 있는 모든 레코드를 가져오고, 기준 필드의 값과 매치되는 레코드들을 왼쪽 테이블(테이블이름1)에서 가져온다.  
오른쪽 테이블의 기준 필드 값과 매치되는 값이 왼쪽 테이블에 없으면 `null` 값을 가져온다.

<img src="/img/SQL/right_join.gif" style="display: block; margin-left: 150px;">

- `FULL OUTER`: 기준 필드의 값과 매치되는 레코드가 어느 한쪽 테이블에라도 있으면 해당 레코드를 해당 테이블에서 가져온다.  
결과 테이블이 매우 커질 수 있으므로 주의해야한다.

<img src="/img/SQL/full_join.gif" style="display: block; margin-left: 150px;">

- - -

예제 테이블을 보면 `Orders` 테이블의 `CustomerID` 필드는 `Customers` 테이블의 `CustomerID` 필드를 참조하고 있다.  
아래는 `Orders`, `Customers` 테이블 양쪽 모두에 동일한 `CustomerID` 필드 값을 가지는 레코드들을 모두 가져오는 `INNER JOIN` 의 예이다.  

```sql
SELECT Orders.OrderID, Customers.CustomerName, Orders.OrderDate
FROM Orders
INNER JOIN Customers
ON Orders.CustomerID=Customers.CustomerID;
```
- - -

##### Result

<table class="table table-striped table-bordered">
    <tbody>
        <tr>
            <th>OrderID</th>
            <th>CustomerName</th>
            <th>OrderDate</th>
        </tr>
        <tr>
            <td>10278</td>
            <td>Berglunds snabbköp</td>
            <td>1996-08-12</td>
        </tr>
        <tr>
            <td>10280</td>
            <td>Berglunds snabbköp</td>
            <td>1996-08-14</td>
        </tr>
        <tr>
            <td>10308</td>
            <td>Ana Trujillo Emparedados y helados</td>
            <td>1996-09-18</td>
        </tr>
        <tr>
            <td>10355</td>
            <td>Around the Horn</td>
            <td>1996-11-15</td>
        </tr>
        <tr>
            <td>10365</td>
            <td>Antonio Moreno Taquería</td>
            <td>1996-11-27</td>
        </tr>
        <tr>
            <td>10383</td>
            <td>Around the Horn</td>
            <td>1996-12-16</td>
        </tr>
        <tr>
            <td>10384</td>
            <td>Berglunds snabbköp</td>
            <td>1996-12-16</td>
        </tr>
    </tbody>
</table>

`Orders` 테이블과 `Customers` 테이블 양쪽 모두에서 동일한 `CustomerID` 값을 가지는 레코드들을 모두 가져와서, `OrderID`, `CustomerName`, `OrderDate` 필드의 순서로 나타내었다.

- - -

#### Self JOIN

`Self JOIN` 은 테이블을 자기 스스로와 결합시킨다.  

```sql
SELECT 필드이름1, 필드이름2, ...
FROM 테이블이름 예명1, 테이블이름 예명2
WHERE 조건;
```

아래 명령은 `Customers` 테이블에서 `City` 필드의 값이 같은 레코드들을 가져온다.

```sql
SELECT A.CustomerName AS CustomerName1, B.CustomerName AS CustomerName2
FROM Customers A, Customers B
WHERE A.CustomerID <> B.CustomerID AND A.City=B.City
ORDER BY A.City;
```

- - -
##### Result

<table class="table table-striped table-bordered">
    <tbody>
        <tr>
            <th>CustomerName1</th>
            <th>CustomerName2</th>
            <th>City</th>
        </tr>
        <tr>
            <td>Ana Trujillo Emparedados y helados</td>
            <td>Antonio Moreno Taquería</td>
            <td>México D.F.</td>
        </tr>
        <tr>
            <td>Antonio Moreno Taquería</td>
            <td>Ana Trujillo Emparedados y helados</td>
            <td>México D.F.</td>
        </tr>
    </tbody>
</table>

<a href="#top">위로</a>

- - -
<span id="union"></span>

### UNION

`UNION` 은 두 개 이상의 `SELECT` 문으로 얻어진 결과 테이블을 합칠 때 사용한다.  
`UNION` 은 아래와 같은 조건이 갖추어져야 실행할 수 있다.

- `UNION` 이 적용되는 각각의 `SELECT` 문은 동일한 개수의 필드를 가져와야한다.
- 필드들은 같은 데이터 타입을 가져야한다.
- 각각의 `SELECT` 문은 같은 순서로 필드들을 가져와야한다.

```sql
SELECT 필드이름1, 필드이름2, ...
FROM 테이블이름1
UNION
SELECT 필드이름1, 필드이름2, ...
FROM 테이블이름2;
```

아래는 `Customers` 테이블과 `Suppliers` 테이블의 모든 레코드를 합친 뒤, `Customers` 테이블의 레코드는 `Customer` 를, `Suppliers` 테이블의 레코드는 `Supplier` 를 값으로 가지는 `Type` 필드와 `ContactName`, `City`, `Country` 필드를 가져와 결과 테이블을 구성하는 명령이다.

```sql
SELECT 'Supplier' AS type, ContactName, City, Country
FROM Suppliers
UNION
Select 'Customer', ContactName, City, Country
From Customers;
```

- - -
##### Result

<table class="table table-striped table-bordered">
    <tbody>
        <tr>
            <th>type</th>
            <th>ContactName</th>
            <th>City</th>
            <th>Country</th>
        </tr>
        <tr>
            <td>Customer</td>
            <td>Ana Trujillo</td>
            <td>México D.F.</td>
            <td>Mexico</td>
        </tr>
        <tr>
            <td>Customer</td>
            <td>Antonio Moreno</td>
            <td>México D.F.</td>
            <td>Mexico</td>
        </tr>
        <tr>
            <td>Customer</td>
            <td>Christina Berglund</td>
            <td>Luleå</td>
            <td>Sweden</td>
        </tr>
        <tr>
            <td>Customer</td>
            <td>Maria Anders</td>
            <td>Berlin</td>
            <td>Germany</td>
        </tr>
        <tr>
            <td>Customer</td>
            <td>Thomas Hardy</td>
            <td>London</td>
            <td>UK</td>
        </tr>
        <tr>
            <td>Supplier</td>
            <td>Antonio del Valle Saavedra </td>
            <td>Oviedo</td>
            <td>Spain</td>
        </tr>
        <tr>
            <td>Supplier</td>
            <td>Charlotte Cooper</td>
            <td>Londona</td>
            <td>UK</td>
        </tr>
        <tr>
            <td>Supplier</td>
            <td>Regina Murphy</td>
            <td>Ann Arbor</td>
            <td>USA</td>
        </tr>
        <tr>
            <td>Supplier</td>
            <td>Shelley Burke</td>
            <td>New Orleans</td>
            <td>USA</td>
        </tr>
        <tr>
            <td>Supplier</td>
            <td>Yoshi Nagase</td>
            <td>Tokyo</td>
            <td>Japan</td>
        </tr>
    </tbody>
</table>

- - -

#### UNION ALL

`UNION` 은 기본적으로 두 테이블을 합칠 때, 고유한 값만을 남긴다. 중복되는 값을 남기고 싶으면 `UNION ALL` 을 사용한다.

```sql
SELECT 필드이름1, 필드이름2, ...
FROM 테이블이름1
UNION ALL
SELECT 필드이름1, 필드이름2, ...
FROM 테이블이름2;
```

아래 명령은 `Customers` 과 `Suppliers` 테이블의 모든 레코드들의 `City` 필드 값을 보여주는 `UNION` 명령이다.

```sql
SELECT City
FROM Customers
UNION
SELECT City
FROM Suppliers
```

- - -

##### Result

<table class="table table-striped table-bordered">
    <tbody>
        <tr>
            <th>City</th>
        </tr>
        <tr>
            <td>Ann Arbor</td>
        </tr>
        <tr>
            <td>Berlin</td>
        </tr>
        <tr>
            <td>London</td>
        </tr>
        <tr>
            <td>Londona</td>
        </tr>
        <tr>
            <td>Luleå</td>
        </tr>
        <tr>
            <td>México D.F.</td>
        </tr>
        <tr>
            <td>New Orleans</td>
        </tr>
        <tr>
            <td>Oviedo</td>
        </tr>
        <tr>
            <td>Tokyo</td>
        </tr>
    </tbody>
</table>


- - -

아래는 똑같은 명령을 `UNION ALL` 으로 수행한 결과이다.

```sql
SELECT City
FROM Customers
UNION ALL
SELECT City
FROM Suppliers
```

- - -
##### Result


<table class="table table-striped table-bordered">
    <tbody>
        <tr>
            <th>City</th>
        </tr>
        <tr>
            <td>Berlin</td>
        </tr>
        <tr>
            <td>México D.F.</td>
        </tr>
        <tr>
            <td>México D.F.</td>
        </tr>
        <tr>
            <td>London</td>
        </tr>
        <tr>
            <td>Luleå</td>
        </tr>
        <tr>
            <td>Londona</td>
        </tr>
        <tr>
            <td>New Orleans</td>
        </tr>
        <tr>
            <td>Ann Arbor</td>
        </tr>
        <tr>
            <td>Tokyo</td>
        </tr>
        <tr>
            <td>Oviedo</td>
        </tr>
    </tbody>
</table>

중복되는 값이 나타나는 것을 볼 수 있다.

<a href="#top">위로</a>

- - -

{% include /sql/sql-toc-base.html %}

- - -

<span id="reference"></span>
###### Reference

W3School: [https://www.w3schools.com/sql/](https://www.w3schools.com/sql/)

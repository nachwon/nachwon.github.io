--- 
layout: post 
title: '[SQL] INSERT INTO'
category: Django 
tags:
  - SQL
--- 


### 예제 테이블

{% include /sql/sql-customers-table.html %}

- - -

`INSERT INTO` 는 테이블에 새 레코드를 삽입할 때 사용한다.  

데이터를 삽입할 필드 이름과 해당 필드에 들어갈 값을 아래와 같이 입력한다.

```sql
INSERT INTO 테이블이름 (필드이름1, 필드이름2, 필드이름3, ...)
VALUES (값1, 값2, 값3, ...);
```

모든 필드에 값을 삽입하는 경우 필드이름을 생략할 수 있다. 이 때, 값들의 입력 순서는 테이블의 필드 순서에 맞춰서 입력해주어야 한다.

```sql
INSERT INTO 테이블이름
VALUES (값1, 값2, 값3, ...);
```

아래의 명령은 새로운 레코드를 추가한다.

```sql
INSERT INTO Customers (CustomerName, ContactName, Address, City, PostalCode, Country)
VALUES  ('Cardinal', 'Tom B. Erichsen', 'Skagen 21', 'Stavanger', '4006', 'Norway');
```
```re
You have made changes to the database. Rows affected: 1
```

아래의 명령으로 전체 테이블을 확인해본다.

```sql
SELECT *
FROM Customers;
```

- - -

##### Result
<table class="table table-striped table-bordered">
    <tbody>
        <tr>
            <th>CustomerID</th>
            <th>CustomerName</th>
            <th>ContactName</th>
            <th>Address</th>
            <th>City</th>
            <th>PostalCode</th>
            <th>Country</th>
        </tr>
        <tr>
            <td>1</td>
            <td>Alfreds Futterkiste</td>
            <td>Maria Anders</td>
            <td>Obere Str. 57</td>
            <td>Berlin</td>
            <td>12209</td>
            <td>Germany</td>
        </tr>
        <tr>
            <td>2</td>
            <td>Ana Trujillo Emparedados y helados</td>
            <td>Ana Trujillo</td>
            <td>Avda. de la Constitución 2222</td>
            <td>México D.F.</td>
            <td>05021</td>
            <td>Mexico</td>
        </tr>
        <tr>
            <td>3</td>
            <td>Antonio Moreno Taquería</td>
            <td>Antonio Moreno</td>
            <td>Mataderos 2312</td>
            <td>México D.F.</td>
            <td>05023</td>
            <td>Mexico</td>
        </tr>
        <tr>
            <td>4</td>
            <td>Around the Horn</td>
            <td>Thomas Hardy</td>
            <td>120 Hanover Sq.</td>
            <td>London</td>
            <td>WA1 1DP</td>
            <td>UK</td>
        </tr>
        <tr>
            <td>5</td>
            <td>Berglunds snabbköp</td>
            <td>Christina Berglund</td>
            <td>Berguvsvägen 8</td>
            <td>Luleå</td>
            <td>S-958 22</td>
            <td>Sweden</td>
        </tr>
        <tr>
            <td>6</td>
            <td>Cardinal</td>
            <td>Tom B. Erichsen</td>
            <td>Skagen 21</td>
            <td>Stavanger</td>
            <td>4006</td>
            <td>Norway</td>
        </tr>
    </tbody>
</table>

6 번째 레코드가 추가되었다.  

`CustomerID` 필드는 자동으로 추가되는 필드이므로 따로 추가해주지 않는다.

- - -

특정 필드에만 값을 지정해주는 경우, 값을 지정하지 않은 필드에는 `null` 값이 들어간다.

```sql
INSERT INTO Customers (CustomerName, PostalCode, Country)
VALUES ('Cardinal',  '4006', 'Norway');
```

- - -

##### Result
<table class="table table-striped table-bordered">
    <tbody>
        <tr>
            <th>CustomerID</th>
            <th>CustomerName</th>
            <th>ContactName</th>
            <th>Address</th>
            <th>City</th>
            <th>PostalCode</th>
            <th>Country</th>
        </tr>
        <tr>
            <td>1</td>
            <td>Alfreds Futterkiste</td>
            <td>Maria Anders</td>
            <td>Obere Str. 57</td>
            <td>Berlin</td>
            <td>12209</td>
            <td>Germany</td>
        </tr>
        <tr>
            <td>2</td>
            <td>Ana Trujillo Emparedados y helados</td>
            <td>Ana Trujillo</td>
            <td>Avda. de la Constitución 2222</td>
            <td>México D.F.</td>
            <td>05021</td>
            <td>Mexico</td>
        </tr>
        <tr>
            <td>3</td>
            <td>Antonio Moreno Taquería</td>
            <td>Antonio Moreno</td>
            <td>Mataderos 2312</td>
            <td>México D.F.</td>
            <td>05023</td>
            <td>Mexico</td>
        </tr>
        <tr>
            <td>4</td>
            <td>Around the Horn</td>
            <td>Thomas Hardy</td>
            <td>120 Hanover Sq.</td>
            <td>London</td>
            <td>WA1 1DP</td>
            <td>UK</td>
        </tr>
        <tr>
            <td>5</td>
            <td>Berglunds snabbköp</td>
            <td>Christina Berglund</td>
            <td>Berguvsvägen 8</td>
            <td>Luleå</td>
            <td>S-958 22</td>
            <td>Sweden</td>
        </tr>
        <tr>
            <td>6</td>
            <td>Cardinal</td>
            <td><i>null</i></td>
            <td><i>null</i></td>
            <td><i>null</i></td>
            <td>4006</td>
            <td>Norway</td>
        </tr>
    </tbody>
</table>

- - -

#### NULL 값

필드의 값이 `NULL` 인 경우 필드에 값이 없음을 의미한다.

필드에 값이 필수적이지 않은 경우 필드 값이 `NULL` 이 될 수 있다.  

필드에 값이 없다는 것은 필드가 완전히 비어있다는 뜻이며 **필드의 값이 0 이거나 "" 인 것과는 다르다**. 

`NULL` 값을 테스트 할 때는 일반적인 연산자를 사용하지 않고 `IS NULL` 또는 `IS NOT NULL` 을 사용한다.

아래 명령은 `Customer` 테이블에서 `Address` 필드가 비어있는 레코드의 `CustomerName`, `Country`, `Address` 필드 값을 가져온다.

- - -

##### IS NULL

```sql
SELECT CustomerName, Country, Address
FROM Customers
WHERE Address IS NULL;
```

- - -

##### Result

<table class="table table-striped table-bordered">
    <tbody>
        <tr>
            <th>CustomerName</th>
            <th>Country</th>
            <th>Address</th>
        </tr>
        <tr>
            <td>Cardinal</td>
            <td>Norway</td>
            <td><i>null</i></td>
        </tr>
    </tbody>
</table>

- - -

##### IS NOT NULL

아래 명령은 `Customers` 테이블에서 `Address` 필드 값이 비어있지 않은 레코드들의 `CustomerName`, `Country`, `Address` 필드 값을 가져온다.

```sql
SELECT CustomerName, Country, Address
FROM Customers
WHERE Address IS NOT NULL;
```

- - -

##### Result

<table class="table table-striped table-bordered">
    <tbody>
        <tr>
            <th>CustomerName</th>
            <th>Country</th>
            <th>Address</th>
        </tr>
        <tr>
            <td>Alfreds Futterkiste</td>
            <td>Germany</td>
            <td>Obere Str. 57</td>
        </tr>
        <tr>
            <td>Ana Trujillo Emparedados y helados</td>
            <td>Mexico</td>
            <td>Avda. de la Constitución 2222</td>
        </tr>
        <tr>
            <td>Antonio Moreno Taquería</td>
            <td>Mexico</td>
            <td>Mataderos 2312</td>
        </tr>
        <tr>
            <td>Around the Horn</td>
            <td>UK</td>
            <td>120 Hanover Sq.</td>
        </tr>
        <tr>
            <td>Berglunds snabbköp</td>
            <td>Sweden</td>
            <td>Berguvsvägen 8</td>
        </tr>
    </tbody>
</table>

<a href="#top">위로</a>

- - -

{% include /sql/sql-toc-base.html %}

- - -

<span id="reference"></span>
###### Reference

W3School: [https://www.w3schools.com/sql/](https://www.w3schools.com/sql/)

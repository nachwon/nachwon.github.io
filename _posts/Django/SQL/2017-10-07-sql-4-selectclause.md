--- 
layout: post 
title: '[SQL] SELECT를 꾸며주는 옵션 모음'
category: Django 
tags:
  - SQL
--- 


### 예제 테이블

{% include /sql/sql-customers-table.html %}

{% include /sql/sql-products-table.html %}

{% include /sql/sql-orderdetails-table.html %}

{% include /sql/sql-orders-table.html %}

- - -

<span id="top-limit-rownum"></span>
#### TOP, LIMIT, ROWNUM

`TOP`, `LIMIT`, `ROWNUM` 절은 `SELECT` 로 가져올 레코드의 개수를 지정할 때 사용한다. 레코드의 수가 아주 클 때 사용하면 유용하다.  
모든 데이터베이스 시스템이 `TOP` 절을 지원하지 않는다. 데이터베이스 종류에 따라 아래와 같이 사용한다.

##### SQL Server / MS Access:
```sql
SELECT TOP 레코드개수 |PERCENT 필
FROM Customers
```드이름1, 필드이름2, ...
FROM 테이블이름;
```

##### MySQL:
```sql
SELECT 필드이름1, 필드이름2, ...
FROM 테이블이름
WHERE 조건
LIMIT 레코드개수;
```

##### Oracle:
```sql
SELECT 필드이름1, 필드이름2, ...
FROM 테이블이름
WHERE ROWNUM <= 레코드개수;
```

아래 명령은 `SQL Server / MS Access` 데이터베이스에서 `Customer` 테이블의 레코드를 3개까지 가져온다. 

```sql
SELECT TOP 3 *
FROM Customers;
```
- - -
##### Result

<table class="table table-striped table-bordered">
    <tbody>
        <tr>
            <th align="left">CustomerID</th>
            <th align="left">CustomerName</th>
            <th align="left">ContactName</th>
            <th align="left">Address</th>
            <th align="left">City</th>
            <th align="left">PostalCode</th>
            <th align="left">Country</th>
        </tr>
        <tr>
            <td valign="top">1&nbsp;</td>
            <td valign="top">Alfreds Futterkiste&nbsp;</td>
            <td valign="top">Maria Anders&nbsp;</td>
            <td valign="top">Obere Str. 57&nbsp;</td>
            <td valign="top">Berlin&nbsp;</td>
            <td valign="top">12209&nbsp;</td>
            <td valign="top">Germany&nbsp;</td>
        </tr>
        <tr>
            <td valign="top">2&nbsp;</td>
            <td valign="top">Ana Trujillo Emparedados y helados&nbsp;</td>
            <td valign="top">Ana Trujillo&nbsp;</td>
            <td valign="top">Avda. de la Constitución 2222&nbsp;</td>
            <td valign="top">México D.F.&nbsp;</td>
            <td valign="top">05021&nbsp;</td>
            <td valign="top">Mexico&nbsp;</td>
        </tr>
        <tr>
            <td valign="top">3&nbsp;</td>
            <td valign="top">Antonio Moreno Taquería&nbsp;</td>
            <td valign="top">Antonio Moreno&nbsp;</td>
            <td valign="top">Mataderos 2312&nbsp;</td>
            <td valign="top">México D.F.&nbsp;</td>
            <td valign="top">05023&nbsp;</td>
            <td valign="top">Mexico&nbsp;</td>
        </tr>
    </tbody>
</table>


아래 명령은 `MySQL` 데이터베이스에서 위의 명령과 똑같은 작업을 실행한다.

```sql
SELECT * FROM Customers LIMIT 3;
```

아래 명령은 `Oracle` 데이터베이스에서 위의 명령과 똑같은 작업을 실행한다.

```sql
SELECT * FROM Customers
WHERE ROWNUM <= 3;
```

- - -

`TOP` 절에는 `PERCENT` 옵션을 줄 수 있다.  

아래 명령은 `Customers` 테이블의 상위 50% 레코드들을 가져온다.

```sql
SELECT TOP 50 PERCENT *
FROM Customers
```

- - -
##### Result

<table class="table table-striped table-bordered">
    <tbody>
        <tr>
            <th align="left">CustomerID</th>
            <th align="left">CustomerName</th>
            <th align="left">ContactName</th>
            <th align="left">Address</th>
            <th align="left">City</th>
            <th align="left">PostalCode</th>
            <th align="left">Country</th>
        </tr>
        <tr>
            <td valign="top">1&nbsp;</td>
            <td valign="top">Alfreds Futterkiste&nbsp;</td>
            <td valign="top">Maria Anders&nbsp;</td>
            <td valign="top">Obere Str. 57&nbsp;</td>
            <td valign="top">Berlin&nbsp;</td>
            <td valign="top">12209&nbsp;</td>
            <td valign="top">Germany&nbsp;</td>
        </tr>
        <tr>
            <td valign="top">2&nbsp;</td>
            <td valign="top">Ana Trujillo Emparedados y helados&nbsp;</td>
            <td valign="top">Ana Trujillo&nbsp;</td>
            <td valign="top">Avda. de la Constitución 2222&nbsp;</td>
            <td valign="top">México D.F.&nbsp;</td>
            <td valign="top">05021&nbsp;</td>
            <td valign="top">Mexico&nbsp;</td>
        </tr>
        <tr>
            <td valign="top">3&nbsp;</td>
            <td valign="top">Antonio Moreno Taquería&nbsp;</td>
            <td valign="top">Antonio Moreno&nbsp;</td>
            <td valign="top">Mataderos 2312&nbsp;</td>
            <td valign="top">México D.F.&nbsp;</td>
            <td valign="top">05023&nbsp;</td>
            <td valign="top">Mexico&nbsp;</td>
        </tr>
    </tbody>
</table>

<a href="#top">위로</a>

- - -

<span id="min-max"></span>
#### MIN, MAX

`MIN()` 과 `MAX()` 함수는 필드를 전달받으며 전달 받은 필드에서 최소값과 최대값을 결과테이블로 돌려준다.

```sql
SELECT MIN(필드이름) AS 결과필드이름
FROM 테이블이름
WHERE 조건;
```

```sql
SELECT MAX(필드이름) AS 결과필드이름
FROM 테이블이름
WHERE 조건;
```

`MIN` 과 `MAX` 의 예제는 `Products` 테이블에서 실행해보겠다.

- - -

아래 명령은 `Products` 테이블에서 `Price` 필드의 값들 중 가장 작은 값을 `SmallestPrice` 라는 필드에 담아 보여준다.

```sql
SELECT MIN(Price) AS SmallestPrice
FROM Products;
```

- - -

##### Result

<table class="table table-striped table-bordered">
    <tbody>
        <tr>
            <th>SmallestPrice</th>
        </tr>
        <tr>
            <td>10</td>
        </tr>
    </tbody>
</table>

- - -

아래의 명령은 `Products` 테이블에서 `Price` 필드의 값들 중 가장 큰 값을 `LargestPrice` 라는 필드에 담아 보여준다.

```sql
SELECT MAX(Price) AS LargestPrice
FROM Products;
```

- - -

##### Result

<table class="table table-striped table-bordered">
    <tbody>
        <tr>
            <th>LargestPrice</th>
        </tr>
        <tr>
            <td>22</td>
        </tr>
    </tbody>
</table>

<a href="#top">위로</a>

- - -

<span id='count-average-sum'></span>

#### COUNT, AVG, SUM

`COUNT()` 는 조건을 만족하는 레코드의 개수를 돌려준다.

```sql
SELECT COUNT(필드이름)
FROM 테이블이름
WHERE 조건;
```

아래는 `Products` 테이블에서 `ProductID` 필드의 레코드 개수를 돌려주는 명령이다.

```sql
SELECT COUNT(ProductID)
FROM Products;
```

- - -

##### Result

<table class="table table-striped table-bordered">
    <tbody>
        <tr>
            <th>COUNT(ProductID)</th>
        </tr>
        <tr>
            <td>5</td>
        </tr>
    </tbody>
</table>

- - -

`AVG()` 는 숫자 필드의 평균을 돌려준다.

```sql
SELECT AVG(필드이름)
FROM 테이블이름
WHERE 조건;
```

아래 명령은 `Products` 테이블의 `Price` 필드의 모든 값의 평균을 돌려준다.

```sql
SELECT AVG(Price)
FROM Products;
```

- - -

##### Result

<table class="table table-striped table-bordered">
    <tbody>
        <tr>
            <th>AVG(Price)</th>
        </tr>
        <tr>
            <td>18.07</td>
        </tr>
    </tbody>
</table>

- - -

`SUM()` 은 숫자 필드의 총 합을 돌려준다.

```sql
SELECT SUM(필드이름)
FROM 테이블이름
WHERE 조건;
```

아래 명령은 `OrderDetails` 테이블에서 `Quantity` 필드의 모든 값의 합을 돌려준다.
```sql
SELECT SUM(Quantity)
FROM OrderDetails;
```

- - -

##### Result

<table class="table table-striped table-bordered">
    <tbody>
        <tr>
            <th>SUM(Quantity)</th>
        </tr>
        <tr>
            <td>76</td>
        </tr>
    </tbody>
</table>

<a href="#top">위로</a>

- - -

<span id="alias"></span>

#### AS

`AS` 는 테이블이나 필드에 예명을 붙여줄 때 사용한다. 주로 필드명을 좀 더 알아보기 쉽게 해줄 때 사용한다.  
`AS` 로 붙인 예명은 질의가 진행되는 동안에만 유효하다.  

필드에 예명을 붙일 때
```sql
SELECT 필드이름 AS 예명
FROM 테이블이름
``` 

테이블에 예명을 붙일 때
```sql
SELECT 필드이름
FROM 테이블이름 AS 예명
```

아래 명령은 `Customers` 테이블의 `CustomerID` 필드를 `ID` 라는 예명으로, `CustomerName` 필드를 `Customer` 라는 예명으로 가져온다.

```sql
SELECT CustomerID AS ID, CustomerName AS Customer
FROM Customers
```

- - -

##### Result

<table class="table table-striped table-bordered">
    <tbody>
        <tr>
            <th>ID</th>
            <th>Customer</th>
        </tr>
        <tr>
            <td>1</td>
            <td>Alfreds Futterkiste</td>
        </tr>
        <tr>
            <td>2</td>
            <td>Ana Trujillo Emparedados y helados</td>
        </tr>
        <tr>
            <td>3</td>
            <td>Antonio Moreno Taquería</td>
        </tr>
        <tr>
            <td>4</td>
            <td>Around the Horn</td>
        </tr>
        <tr>
            <td>5</td>
            <td>Berglunds snabbköp</td>
        </tr>
    </tbody>
</table>

- - -



아래 명령은 `Customer` 테이블을 `c` 로, `Orders` 테이블을 `o` 로 이름 붙인 다음, 이 예명들을 사용해서 각 테이블의 필드들을 불러온다.  
`Customers` 테이블에서는 `CustomerID`, `CustomerName` 필드를 불러와 각각 `ID`, `Customer` 라는 예명을 붙여주었다.  
`Orders` 테이블에서는 `OrderDate` 필드를 불러와서 `Order Date` 라는 예명을 붙였다. 예명에 공백문자가 있으면 `[]` 로 감싸준다.  
불러온 필드들 중  서로 같은 `CustomerID` 값을 가진 레코드들만 가져온다.  
`CustomerID` 를 기준으로 오름차순 정렬한다.

```sql
SELECT c.CustomerID as ID, c.CustomerName As Customer, o.OrderDate AS [Order Date]
FROM Customers As c, Orders as o
WHERE c.CustomerID=o.CustomerID
Order By c.CustomerID;
```

- - -

##### Result

<table class="table table-striped table-bordered">
    <tbody>
        <tr>
            <th>ID</th>
            <th>Customer</th>
            <th>Order Date</th>
        </tr>
        <tr>
            <td>2</td>
            <td>Ana Trujillo Emparedados y helados</td>
            <td>1996-09-18</td>
        </tr>
        <tr>
            <td>3</td>
            <td>Antonio Moreno Taquería</td>
            <td>1996-11-27</td>
        </tr>
        <tr>
            <td>4</td>
            <td>Around the Horn</td>
            <td>1996-11-15</td>
        </tr>
        <tr>
            <td>4</td>
            <td>Around the Horn</td>
            <td>1996-12-16</td>
        </tr>
        <tr>
            <td>5</td>
            <td>Berglunds snabbköp</td>
            <td>1996-08-12</td>
        </tr>
        <tr>
            <td>5</td>
            <td>Berglunds snabbköp</td>
            <td>1996-08-14</td>
        </tr>
        <tr>
            <td>5</td>
            <td>Berglunds snabbköp</td>
            <td>1996-12-16</td>
        </tr>
    </tbody>
</table>

- - -


여러 필드들의 값을 하나의 필드로 묶어서 불러올 수 도 있다.

```sql
SELECT CustomerName AS Name, Address + ', ' + PostalCode + ' ' + City + ', ' + Country AS Address
FROM Customers;
```

- - -

##### Result

<table class="table table-striped table-bordered">
    <tbody>
        <tr>
            <th align="left">Name</th>
            <th align="left">Address</th>
        </tr>
        <tr>
            <td valign="top">Alfreds Futterkiste&nbsp;</td>
            <td valign="top">Obere Str. 57, 12209 Berlin, Germany&nbsp;</td>
        </tr>
        <tr>
            <td valign="top">Ana Trujillo Emparedados y helados&nbsp;</td>
            <td valign="top">Avda. de la Constitución 2222, 05021 México D.F., Mexico&nbsp;</td>
        </tr>
        <tr>
            <td valign="top">Antonio Moreno Taquería&nbsp;</td>
            <td valign="top">Mataderos 2312, 05023 México D.F., Mexico&nbsp;</td>
        </tr>
        <tr>
            <td valign="top">Around the Horn&nbsp;</td>
            <td valign="top">120 Hanover Sq., WA1 1DP London, UK&nbsp;</td>
        </tr>
        <tr>
            <td valign="top">Berglunds snabbköp&nbsp;</td>
            <td valign="top">Berguvsvägen 8, S-958 22 Luleå, Sweden&nbsp;</td>
        </tr>
    </tbody>
</table>

<a href="#top">위로</a>
- - -

<span id="group-by"></span>

#### GROUP BY

`GROUP BY` 는 계산 함수(COUNT, AVG, SUM, MIN, MAX)의 결과를 필드별로 나타낼 때 주로 사용한다.

```sql
SELECT 필드이름1, 필드이름2, ...
FROM 테이블이름
WHERE 조건
GROUP BY 필드이름1, 필드이름2,...;
```

아래는 `Customers` 테이블의 레코드들 중 같은 `Country` 값을 가지는 레코드들의 `CustomerID` 값을 세어서 `Country` 값 별로 나타내는 명령이다.

```sql
SELECT COUNT(CustomerID), Country
FROM Customers
GROUP BY Country;
```

- - -

##### Result

<table class="table table-striped table-bordered">
    <tbody>
        <tr>
            <th>COUNT(CustomerID)</th>
            <th>Country</th>
        </tr>
        <tr>
            <td>1</td>
            <td>Germany</td>
        </tr>
        <tr>
            <td>2</td>
            <td>Mexico</td>
        </tr>
        <tr>
            <td>1</td>
            <td>Sweden</td>
        </tr>
        <tr>
            <td>1</td>
            <td>UK</td>
        </tr>
    </tbody>
</table>


<a href="#top">위로</a>

- - -

<span id="having"></span>

#### HAVING

`HAVING` 절은 계산 함수(COUNT, AVG, SUM, MIN, MAX)를 `WHERE` 절과 함께 사용하지 못하는 점을 보완하기 위해 도입되었다.  

```sql
SELECT 필드이름1, 필드이름2, ...
FROM 테이블이름
WHERE 조건
GROUP BY 필드이름1, 필드이름2, ...
HAVING 조건;
```

아래는 `Customers` 테이블에서 `Country` 필드의 값 별로 레코드 수를 세어서 그 수가 2 이상인 `Country` 값 만 나타내는 명령이다.


```sql
SELECT COUNT(CustomerID), Country
FROM Customers
GROUP BY Country
HAVING COUNT(CustomerID) >= 2;
```
- - -
##### Result

<table class="table table-striped table-bordered">
    <tbody>
        <tr>
            <th>COUNT(CustomerID)</th>
            <th>Country</th>
        </tr>
        <tr>
            <td>2</td>
            <td>Mexico</td>
        </tr>
    </tbody>
</table>

<a href="#top">위로</a>

- - -

{% include /sql/sql-toc-base.html %}

- - -

<h5>[SQL] SELECT를 꾸며주는 옵션 모음</h5>
<ul>
    <li><a href="#top-limit-rownum">TOP, LIMIT, ROWNUM</a></li>
    <li><a href="#min-max">MIN, MAX</a></li>
    <li><a href="#count-avg-sum">COUNT, AVG, SUM</a></li>
    <li><a href="#alias">AS</a></li>
    <li><a href="#group-by">GROUP BY</a></li>
    <li><a href="#having">HAVING</a></li>
    <li><a href="#reference">참고 문헌</a></li>
</ul>

- - -

<span id="reference"></span>
###### Reference

W3School: [https://www.w3schools.com/sql/](https://www.w3schools.com/sql/)

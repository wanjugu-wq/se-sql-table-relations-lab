# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# STEP 1
# Replace None with your code
df_boston = pd.read_sql("""
SELECT
    employees.firstName,
    employees.lastName
FROM employees 
INNER JOIN offices
ON employees.officeCode = offices.officeCode                                                                                      
WHERE offices.city = 'Boston';                       
""", conn)
print(df_boston)

# STEP 2
# Replace None with your code
df_zero_emp = pd.read_sql("""
SELECT 
    offices.officeCode,
    employees.employeeNumber
FROM offices
LEFT JOIN employees
ON employees.officeCode = offices.officeCode
WHERE employees.employeeNumber IS NULL;
""",conn)
print(df_zero_emp)

# STEP 3
# Replace None with your code
df_employee = pd.read_sql('''
SELECT 
    employees.firstName,
    employees.lastName,
    offices.city,
    offices.state
FROM employees
LEFT JOIN offices
ON offices.officeCode = employees.officeCode
ORDER BY employees.firstName ASC,employees.lastName;
''', conn)

print(df_employee)

# STEP 4
# Replace None with your code
df_contacts = pd.read_sql('''
SELECT
    customers.contactFirstName,
    customers.contactLastName,
    customers.phone,
    customers.salesRepEmployeeNumber
FROM customers
LEFT JOIN orders
ON customers.customerNumber = orders.customerNumber
WHERE orders.customerNumber IS NULL
ORDER BY customers.contactLastName ASC;
''', conn)

print(df_contacts)

# STEP 5
# Replace None with your code
df_payment = pd.read_sql('''
SELECT 
    customers.contactFirstName,
    customers.contactLastName,
    customers.phone,
    payments.amount
FROM customers
INNER JOIN payments
ON customers.customerNumber = payments.customerNumber
ORDER BY CAST(payments.amount AS REAL) DESC;
''',conn)

print(df_payment)

# STEP 6
# Replace None with your code
df_credit = pd.read_sql('''
SELECT 
    employees.firstName,
    employees.lastName,
    customers.creditLimit,
    COUNT(customers.customerNumber) AS numberOfCustomers
FROM employees            
LEFT JOIN customers
ON employees.employeeNumber = customers.salesRepEmployeeNumber
GROUP BY
    employees.employeeNumber,
    employees.firstName,
    employees.lastName
HAVING AVG(customers.creditLimit) > 90000
ORDER BY numberOfCustomers DESC
LIMIT 4;
''',conn)

print(df_credit)

# STEP 7
# Replace None with your code
df_product_sold = pd.read_sql('''
SELECT 
    products.productName,
    products.productCode,
    SUM(orderdetails.quantityOrdered) AS totalunits
FROM products
INNER JOIN orderdetails
ON products.productCode = orderdetails.productCode
GROUP BY
    products.productCode,
    products.productName
ORDER BY totalunits DESC;
''', conn)

print(df_product_sold)

# STEP 8
# Replace None with your code
df_total_customers = pd.read_sql('''
SELECT
    products.productName,
    products.productCode,
    COUNT(DISTINCT orders.customerNumber) AS numpurchasers
FROM products
INNER JOIN orderdetails ON products.productCode = orderdetails.productCode
INNER JOIN orders ON orderdetails.orderNumber = orders.orderNumber
GROUP BY
    products.productCode,
    products.productName
ORDER BY numpurchasers DESC;
''', conn)

# STEP 9
# Replace None with your code
df_customers = pd.read_sql('''
SELECT
    offices.officeCode,
    offices.city,
    COUNT(DISTINCT customers.customerNumber) AS n_customers
FROM offices
LEFT JOIN employees ON offices.officeCode = employees.officeCode
LEFT JOIN customers ON employees.employeeNumber = customers.salesRepEmployeeNumber
GROUP BY
    offices.officeCode,
    offices.city
ORDER BY offices.officeCode ASC;
''', conn)

# STEP 10
# Replace None with your code
df_under_20 = pd.read_sql('''
WITH low_products AS (
    SELECT
        orderdetails.productCode
    FROM orderdetails
    JOIN orders ON orderdetails.orderNumber = orders.orderNumber
    GROUP BY orderdetails.productCode
    HAVING COUNT(DISTINCT orders.customerNumber) < 20
)
SELECT DISTINCT
    employees.employeeNumber,
    employees.firstName,
    employees.lastName,
    offices.city,
    employees.officeCode
FROM employees
LEFT JOIN offices ON employees.officeCode = offices.officeCode
LEFT JOIN customers ON employees.employeeNumber = customers.salesRepEmployeeNumber
LEFT JOIN orders ON customers.customerNumber = orders.customerNumber
LEFT JOIN orderdetails ON orders.orderNumber = orderdetails.orderNumber
WHERE orderdetails.productCode IN (SELECT productCode FROM low_products)
ORDER BY employees.lastName ASC, employees.firstName ASC;
''', conn)

conn.close()
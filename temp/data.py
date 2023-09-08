from faker import Faker
import cx_Oracle

fake = Faker()

# Connect to the Oracle database
connection = cx_Oracle.connect('testuser/testuser@192.168.1.40:1521/oralabpdb')
cursor = connection.cursor()

def create_tables():
    cursor.execute("""
        CREATE TABLE HR_Employees (
            employee_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            last_name VARCHAR2(50) NOT NULL,
            first_name VARCHAR2(50) NOT NULL,
            email VARCHAR2(100) NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE Managers (
            manager_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            employee_id NUMBER NOT NULL,
            manager_name VARCHAR2(100) NOT NULL,
            FOREIGN KEY (employee_id) REFERENCES HR_Employees(employee_id)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE Titles (
            title_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            employee_id NUMBER NOT NULL,
            title VARCHAR2(100) NOT NULL,
            FOREIGN KEY (employee_id) REFERENCES HR_Employees(employee_id)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE Organizations (
            organization_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            employee_id NUMBER NOT NULL,
            organization VARCHAR2(100) NOT NULL,
            FOREIGN KEY (employee_id) REFERENCES HR_Employees(employee_id)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE Salary_Level (
            salary_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            employee_id NUMBER NOT NULL,
            salary NUMBER(10,2) NOT NULL,
            FOREIGN KEY (employee_id) REFERENCES HR_Employees(employee_id)
        )
    """)
    connection.commit()

# Function to generate random data for HR_Employees table
def generate_hr_employees(n):
    data = [(fake.last_name(), fake.first_name(), fake.email()) for _ in range(n)]
    cursor.executemany("""
        INSERT INTO HR_Employees (last_name, first_name, email)
        VALUES (:1, :2, :3)
    """, data)
    connection.commit()

# Function to generate random data for Managers table
def generate_managers(n):
    data = [(i+1, fake.name()) for i in range(n)]
    cursor.executemany("""
        INSERT INTO Managers (employee_id, manager_name)
        VALUES (:1, :2)
    """, data)
    connection.commit()

# Function to generate random data for Titles table
def generate_titles(n):
    data = [(i+1, fake.job()) for i in range(n)]
    cursor.executemany("""
        INSERT INTO Titles (employee_id, title)
        VALUES (:1, :2)
    """, data)
    connection.commit()

# Function to generate random data for Organizations table
def generate_organizations(n):
    data = [(i+1, fake.company()) for i in range(n)]
    cursor.executemany("""
        INSERT INTO Organizations (employee_id, organization)
        VALUES (:1, :2)
    """, data)
    connection.commit()

# Function to generate random data for Salary_Level table
def generate_salary_level(n):
    data = [(i+1, fake.random_number(digits=5, fix_len=True)) for i in range(n)]
    cursor.executemany("""
        INSERT INTO Salary_Level (employee_id, salary)
        VALUES (:1, :2)
    """, data)
    connection.commit()

# Generate random data for each table
create_tables()
num_records = 100
generate_hr_employees(num_records)
generate_managers(num_records)
generate_titles(num_records)
generate_organizations(num_records)
generate_salary_level(num_records)

# Close the cursor and connection
cursor.close()
connection.close()


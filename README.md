# Student-Management-System-Using-Python-And-MySQL

The Student Management System is a user-friendly desktop application developed with Python and Tkinter, aimed at efficiently managing student information. It allows users to easily add, modify, delete, and search for student records stored in a MySQL database. This application streamlines student administration tasks, making data management straightforward and accessible.

Before running the application, ensure that all necessary modules are installed as outlined in the requirements.txt file.

To set up the project, follow these essential steps:

Create a database named "studentmanagement".

    CREATE DATABASE studentmanagement;
    
Use the newly created database.
    
    USE studentmanagement;

Within this database, establish a table called "student".

use this code to create the table under the "studentmanagement" database

    CREATE TABLE student (
         Roll_no INT PRIMARY KEY,
         Name VARCHAR(100) NOT NULL, 
         Email_ID VARCHAR(100) NOT NULL UNIQUE,
         Gender ENUM('Male', 'Female', 'Others') NOT NULL,
         Bdate DATE NOT NULL,
         Address TEXT NOT NULL,
         Phone VARCHAR(10) NOT NULL,
         Course ENUM('IT', 'CS') NOT NULL,
         Enrollment_Year INT NOT NULL,
         CONSTRAINT chk_phone_length CHECK (CHAR_LENGTH(Phone) = 10)
     );

# OUTPUT

![Screenshot 2024-10-21 144546](https://github.com/user-attachments/assets/93b61389-9dd0-4b39-b9e9-97f448c0e38e)

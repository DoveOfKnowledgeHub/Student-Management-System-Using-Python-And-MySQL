import mysql.connector
from datetime import datetime
import re
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# Validations
def valid_roll_no(roll_no):
    return roll_no.isdigit() and int(roll_no) > 0 and ' ' not in roll_no

def valid_name(name):
    return name.isalpha()  # Only letters, no spaces or special characters

def valid_date(dateStr, Date_Format="%Y-%m-%d"):
    try:
        datetime.strptime(dateStr, Date_Format)
        return True
    except ValueError:
        return False

def valid_email(email):
    regex = r'^[a-zA-Z0-9]+@gmail\.com$'   # Allows letters, digits, no spaces or special characters
    return re.match(regex, email) is not None

def valid_phone(phone):
    return phone.isdigit() and len(phone) == 10 and ' ' not in phone

def valid_address(address):
    return any(char.isalpha() for char in address)  # Must contain letters, can have numbers/special chars

def valid_course(course):
    return course in ("IT", "CS")  # Only allows specified values

def valid_enrollment_year(year):
    return year.isdigit() and len(year) == 4  # Must be a 4-digit number

# Database connection
def create_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='P@y@L-29',
        database='studentmanagement'
    )

# Add a student
def Add():
    Roll_no = entry_roll.get().strip()
    Name = entry_name.get().strip()
    Email_ID = entry_email.get().strip()
    Gender = entry_gender.get().strip()
    Bdate = entry_dob.get().strip()
    Address = entry_address.get().strip()
    Phone = entry_phone.get().strip()
    Course = entry_course.get().strip()
    Enrollment_Year = entry_enrollment.get().strip()

    if not all([Roll_no, Name, Email_ID, Gender, Bdate, Address, Phone, Course, Enrollment_Year]):
        messagebox.showerror("Error", "All fields must be filled!")
        return

    if not valid_roll_no(Roll_no):
        messagebox.showerror("Error", "Roll No must be a positive integer with no spaces!")
        return

    if not valid_name(Name):
        messagebox.showerror("Error", "Name must contain only alphabetic characters with no spaces!")
        return

    if Gender not in ("Male", "Female", "Others"):
        messagebox.showerror("Error", "Gender must be Male, Female, or Others!")
        return

    if Bdate and not valid_date(Bdate):
        messagebox.showerror("INPUT ERROR", "Invalid Format, please use YYYY-MM-DD")
        return

    if Email_ID and not valid_email(Email_ID):
        messagebox.showerror("INPUT ERROR", "Invalid Email, please use valid format")
        return

    if not valid_phone(Phone):
        messagebox.showerror("Error", "Phone number must be 10 digits with no spaces!")
        return

    if not valid_address(Address):
        messagebox.showerror("Error", "Address must contain at least one alphabetic character!")
        return

    if not valid_course(Course):
        messagebox.showerror("Error", "Course must be either IT or CS!")
        return

    if not valid_enrollment_year(Enrollment_Year):
        messagebox.showerror("Error", "Enrollment Year must be a 4-digit year!")
        return

    try:
        conn = create_connection()
        cursor = conn.cursor()
        query = "SELECT COUNT(*) FROM student WHERE Roll_no = %s OR Email_ID = %s"
        cursor.execute(query, (Roll_no, Email_ID))
        exists = cursor.fetchone()[0]

        if exists > 0:
            messagebox.showerror("Error", "Student with the same Roll No or Email ID already exists")
            return

        insert_query = """
        INSERT INTO student (Roll_no, Name, Email_ID, Gender, Bdate, Address, Phone, Course, Enrollment_Year)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (Roll_no, Name, Email_ID, Gender, Bdate, Address, Phone, Course, Enrollment_Year))
        conn.commit()
        messagebox.showinfo("Success", "Student added successfully")
        clear_fields()

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f'Error: {err}')
    finally:
        cursor.close()
        conn.close()

# Clear input fields
def clear_fields():
    entry_roll.delete(0, END)
    entry_name.delete(0, END)
    entry_email.delete(0, END)
    entry_gender.set('')
    entry_dob.delete(0, END)
    entry_address.delete(0, END)
    entry_phone.delete(0, END)
    entry_course.set('')
    entry_enrollment.delete(0, END)

# Delete a student
def Delete():
    Roll_no = entry_roll.get().strip()
    if not Roll_no:
        messagebox.showerror("Error", "Roll No must be provided to delete a student!")
        return

    try:
        conn = create_connection()
        cursor = conn.cursor()
        delete_query = "DELETE FROM student WHERE Roll_no = %s"
        cursor.execute(delete_query, (Roll_no,))
        conn.commit()

        if cursor.rowcount > 0:
            messagebox.showinfo("Success", "Student deleted successfully")
            clear_fields()
        else:
            messagebox.showerror("Error", "No student found with that Roll No")

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f'Error: {err}')
    finally:
        cursor.close()
        conn.close()

# Update a student
def Update():
    Roll_no = entry_roll.get().strip()
    Name = entry_name.get().strip()
    Email_ID = entry_email.get().strip()
    Gender = entry_gender.get().strip()
    Bdate = entry_dob.get().strip()
    Address = entry_address.get().strip()
    Phone = entry_phone.get().strip()
    Course = entry_course.get().strip()
    Enrollment_Year = entry_enrollment.get().strip()

    if not Roll_no:
        messagebox.showerror("Error", "Roll No must be provided to update a student!")
        return

    if not valid_roll_no(Roll_no):
        messagebox.showerror("Error", "Roll No must be a positive integer with no spaces!")
        return

    if not valid_name(Name):
        messagebox.showerror("Error", "Name must contain only alphabetic characters with no spaces!")
        return

    if Gender not in ("Male", "Female", "Others"):
        messagebox.showerror("Error", "Gender must be Male, Female, or Others!")
        return

    if Bdate and not valid_date(Bdate):
        messagebox.showerror("INPUT ERROR", "Invalid Format, please use YYYY-MM-DD")
        return

    if Email_ID and not valid_email(Email_ID):
        messagebox.showerror("INPUT ERROR", "Invalid Email, please use valid format")
        return

    if not valid_phone(Phone):
        messagebox.showerror("Error", "Phone number must be 10 digits with no spaces!")
        return

    if not valid_address(Address):
        messagebox.showerror("Error", "Address must contain at least one alphabetic character!")
        return

    if not valid_course(Course):
        messagebox.showerror("Error", "Course must be either IT or CS!")
        return

    if not valid_enrollment_year(Enrollment_Year):
        messagebox.showerror("Error", "Enrollment Year must be a 4-digit year!")
        return

    try:
        conn = create_connection()
        cursor = conn.cursor()

        update_query = """
        UPDATE student
        SET Name = %s, Email_ID = %s, Gender = %s, Bdate = %s, Address = %s, Phone = %s, Course = %s, Enrollment_Year = %s
        WHERE Roll_no = %s
        """
        cursor.execute(update_query, (Name, Email_ID, Gender, Bdate, Address, Phone, Course, Enrollment_Year, Roll_no))
        conn.commit()

        if cursor.rowcount > 0:
            messagebox.showinfo("Success", "Student updated successfully")
            clear_fields()
        else:
            messagebox.showerror("Error", "No student found with that Roll No")

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f'Error: {err}')
    finally:
        cursor.close()
        conn.close()

# Search for students
def Search():
    search_by = entry_search_by.get()
    search_value = entry_search_value.get().strip()

    if not search_value:
        messagebox.showerror("Error", "Please enter a search value!")
        return

    if search_by not in ["Roll No", "Name", "Gender"]:
        messagebox.showerror("Error", "Please select a valid search option!")
        return

    try:
        conn = create_connection()
        cursor = conn.cursor()
        query = ""

        if search_by == "Roll No":
            query = "SELECT * FROM student WHERE Roll_no = %s"
        elif search_by == "Name":
            query = "SELECT * FROM student WHERE Name LIKE %s"
            search_value = f"%{search_value}%"
        else:
            query = "SELECT * FROM student WHERE Gender = %s"

        cursor.execute(query, (search_value,))
        results = cursor.fetchall()

        text_display.delete(1.0, END)

        if results:
            result_string = "\n".join([f"{row[0]} - {row[1]} - {row[2]} - {row[3]} - {row[4]} - {row[5]} - {row[6]} - {row[7]} - {row[8]}" for row in results])
            text_display.insert(END, result_string)
        else:
            text_display.insert(END, "No results found.")

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f'Error: {err}')
    finally:
        cursor.close()
        conn.close()

# Display all students
def DisplayAll():
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM student")
        results = cursor.fetchall()

        text_display.delete(1.0, END)

        if results:
            display_text = "\n".join([f"{row[0]} - {row[1]} - {row[2]} - {row[3]} - {row[4]} - {row[5]} - {row[6]} - {row[7]} - {row[8]}" for row in results])
            text_display.insert(END, display_text)
        else:
            text_display.insert(END, "No students found.")

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f'Error: {err}')
    finally:
        cursor.close()
        conn.close()

# UI Setup
root = Tk()
root.title("Student Management System")
root.geometry('900x450')
root.configure(bg='white')

# Main Frame
main_frame = Frame(root, bg="white")
main_frame.pack(pady=10, padx=10, fill=BOTH, expand=True)

# Left Frame with Gray Background
left_box = Frame(main_frame, bg="lightgray", padx=10, pady=10)
left_box.pack(side=LEFT, padx=10, fill=BOTH, expand=True)

# Left Frame for Inputs
left_frame = Frame(left_box, bg="lightgray")
left_frame.pack(fill=BOTH, expand=True)

# Input Fields
fields = [
    ("Roll No", "entry_roll"),
    ("Name", "entry_name"),
    ("Email ID", "entry_email"),
    ("Gender", "entry_gender"),
    ("DOB (YYYY-MM-DD)", "entry_dob"),
    ("Address", "entry_address"),
    ("Phone", "entry_phone"),
    ("Course", "entry_course"),
    ("Enrollment Year", "entry_enrollment")
]

for i, (label_text, var_name) in enumerate(fields):
    Label(left_frame, text=label_text, font=("Arial", 10), bg="lightgray").grid(row=i, column=0, padx=5, pady=5, sticky=W)
    if var_name == "entry_gender":
        entry_gender = ttk.Combobox(left_frame, values=("Male", "Female", "Others"), font=("Arial", 8), width=20)
        entry_gender.grid(row=i, column=1)
    elif var_name == "entry_course":
        entry_course = ttk.Combobox(left_frame, values=("IT", "CS"), font=("Arial", 8), width=20)
        entry_course.grid(row=i, column=1)
    else:
        globals()[var_name] = Entry(left_frame, font=("Arial", 10), width=20, bg="white")
        globals()[var_name].grid(row=i, column=1)

# Buttons
button_frame = Frame(left_frame, bg="lightgray")
button_frame.grid(row=len(fields), column=0, columnspan=2, pady=10)

Button(button_frame, text="Add", font=("Arial", 10), command=Add, bg="gray", fg="black", activebackground="gray").pack(side=LEFT, padx=5)
Button(button_frame, text="Update", font=("Arial", 10), command=Update, bg="gray", fg="black", activebackground="gray").pack(side=LEFT, padx=5)
Button(button_frame, text="Delete", font=("Arial", 10), command=Delete, bg="gray", fg="black", activebackground="gray").pack(side=LEFT, padx=5)

# Right Frame with Gray Background
right_box = Frame(main_frame, bg="lightgray", padx=10, pady=10)
right_box.pack(side=RIGHT, padx=10, fill=BOTH, expand=True)

# Right Frame for Display and Search
right_frame = Frame(right_box, bg="lightgray")
right_frame.pack(fill=BOTH, expand=True)

# Search Fields in Right Frame
search_frame = Frame(right_frame, bg="lightgray")
search_frame.pack(pady=10)

Label(search_frame, text="Search By:", font=("Arial", 10), bg="lightgray").grid(row=0, column=0, padx=5, pady=5, sticky=W)
entry_search_by = ttk.Combobox(search_frame, values=("Roll No", "Name", "Gender"), font=("Arial", 10), width=15)
entry_search_by.grid(row=0, column=1, padx=5)
entry_search_by.current(0)

Label(search_frame, text="Value:", font=("Arial", 10), bg="lightgray").grid(row=1, column=0, padx=5, pady=5, sticky=W)
entry_search_value = Entry(search_frame, font=("Arial", 10), width=20, bg="white")
entry_search_value.grid(row=1, column=1, padx=5)

# Search and Display Buttons
search_button_frame = Frame(search_frame, bg="lightgray")
search_button_frame.grid(row=2, column=0, columnspan=2, pady=10)

Button(search_button_frame, text="Search", font=("Arial", 10), command=Search, bg="gray", fg="black", activebackground="gray").pack(side=LEFT, padx=5)
Button(search_button_frame, text="Display All", font=("Arial", 10), command=DisplayAll, bg="gray", fg="black", activebackground="gray").pack(side=LEFT, padx=5)

# Text Display Area
text_display = Text(right_frame, height=15, width=50, font=("Arial", 10), bg="#f0f0f0")
text_display.pack(pady=10, padx=10)

root.mainloop()

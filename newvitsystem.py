import time
import string
import random

# storage
users = {}
faculty_attendance={}
attendance_records = {}
assigned_tasks = {}
faculty_assigned_tasks_to_students = {}
admin_assigned_tasks = {}
submitted_tasks_to_admin = {}
removed_tasks = {}
submitted_tasks = {}  

unique_codes = {"Administrator": "admin2024", "Teaching": "teach2024", "Non-Teaching": "nonteach2024", "Student": "stud2024"}

chars = " " + string.punctuation + string.digits + string.ascii_letters
chars = list(chars)

def generate_unique_seed(length=10): #generates a random alphanumeric string of the given length (default is 10)
    """Generates a unique random alphanumeric seed."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_key(seed):
    """Generate a consistent key based on the seed."""
    random.seed(seed) #ensuring consistent randomness.
    key = chars.copy()
    random.shuffle(key) #list is shuffled to create the key for encryption.
    return key

def encrypt_password(password, seed):
    """Encrypt a password using the given seed."""
    start_time = time.time()  # start timer for encryption
    key = generate_key(seed)
    cipher_text = ""
    for letter in password: # the index of that character in the chars list and the corresponding character from the shuffled key is added to the encrypted result (cipher text).
        index = chars.index(letter)
        cipher_text += key[index]
    end_time = time.time()  # end timer for encryption
    encrypt_time=end_time - start_time
    return cipher_text, encrypt_time #returns the encrypted password and the time taken to encrypt it.

def decrypt_password(cipher_text, seed):
    """Decrypt a password using the given seed."""
    key = generate_key(seed)
    password = ""
    for letter in cipher_text: #reconstructs
        index = key.index(letter)
        password += chars[index]
    return password

# Validate password
def is_valid_password(password): #password validation
    has_upper = has_lower = has_digit = has_special = False
    special_characters = string.punctuation
    if len(password) >= 8:
        for char in password:
            if char.isupper():
                has_upper = True
            elif char.islower():
                has_lower = True
            elif char.isdigit():
                has_digit = True
            elif char in special_characters:
                has_special = True
    return has_upper and has_lower and has_digit and has_special

# Registration
def register_user():
    reg_no = input("Enter Registration Number: ").strip()
    if reg_no in users:
        print("Registration number already exists. Try again.")
        return

    name = input("Enter your name: ").strip()
    dob = input("Enter Date of Birth (YYYY-MM-DD): ").strip()

    print("Choose your designation: 1) Administrator  2) Teaching Faculty  3) Non-Teaching Faculty  4) Student")
    choice = input("Enter your choice: ").strip()

    if choice == "1":
        designation = "Administrator"
    elif choice == "2":
        designation = "Teaching"
    elif choice == "3":
        designation = "Non-Teaching"
    elif choice == "4":
        designation = "Student"
    else:
        print("Invalid choice. Registration failed.")
        return

    unique_code = input(f"Enter unique code for {designation}: ").strip()

    if designation.lower() == "administrator" and unique_code != "admin2024":
        print("Invalid unique code for Administrator. Registration failed.")
        return
    elif designation.lower() == "teaching" and unique_code != "teach2024":
        print("Invalid unique code for Teaching. Registration failed.")
        return
    elif designation.lower() == "non-teaching" and unique_code != "nonteach2024":
        print("Invalid unique code for Non-Teaching. Registration failed.")
        return
    elif designation.lower() == "student" and unique_code != "stud2024":
        print("Invalid unique code for Student. Registration failed.")
        return

    unique_seed = generate_unique_seed() #unique seed generated for specific user to view/reset password later.
    password = input("Create a password (at least 8 chars, with uppercase, lowercase, digits, special chars): ").strip()
    while not is_valid_password(password):
        print("Invalid password. Try again.")
        password = input("Create a password: ").strip()
    encrypted_password,encrypt_time = encrypt_password(password, unique_seed)
    
    # storing data
    users[reg_no] = {
        "Name": name,
        "DOB": dob,
        "Designation": designation,
        "EncryptedPassword": encrypted_password,
        "Seed": unique_seed, 
    }

    print("-" * 40)
    print("Registration Successful!")
    print(f"Name: {name}")
    print(f"Designation: {designation}")
    print(f"Encrypted Password: {encrypted_password}")
    print(f"Seed Value (Keep this safe!): {unique_seed}")
    print(f"Time taken for encryption: {encrypt_time:.10f}s") #to get more precise time(:.10f)is used
    print("-" * 40)


def view_all_users(): 
    if not users:
        print("No users found.")
        return
    
    print("\nAll Registered Users:")
    print("-" * 40)
    for reg_no, user_info in users.items():
        print(f"Registration Number: {reg_no}")
        print(f"Name: {user_info['Name']}")
        print(f"Date of Birth: {user_info['DOB']}")
        print(f"Designation: {user_info['Designation']}")
        print(f"Encrypted Password: {user_info['EncryptedPassword']}")
        print("-" * 40)

def login_user():
    print("-" * 40)
    start_time = time.time()  # start timer for login
    attempts = 5  # allowing only 5 attempts to enter the correct reg number

    while attempts > 0:
        reg_no = input("Enter Registration Number: ").strip()
        
        if reg_no not in users:  # checking if the user is  registered
            print("User not found. Please register first.")
            attempts -= 1
            print(f"{attempts} attempts remaining.")
            if attempts == 0:
                print("Too many failed attempts. Exiting.")
                return
        else:
            print(f"User found: {reg_no}")
            break 
    
    user = users[reg_no]
    for _ in range(3):  # allowing only 3 attempts to enter the correct password
        password = input("Enter Password: ").strip()
        decrypted_password = decrypt_password(user["EncryptedPassword"], user["Seed"])

        if password == decrypted_password:
            print(f"Welcome, {user['Name']} ({user['Designation']})!")
            user["last_login"] = time.time()  # recording the current time as the login time

            designation = user["Designation"]
            if designation == "Administrator":
                admin_menu(user)
            elif designation == "Teaching":
                teaching_faculty_menu(user)
            elif designation == "Non-Teaching":
                non_teaching_faculty_menu(user)
            elif designation == "Student":
                student_menu(user)
            else:
                print("Error: Unknown designation. Contact Administrator.")
            return  
        else:
            print("Invalid password.")
            print("Press 1 to try again or 2 to reset your password.")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                continue  
            elif choice == "2":
                # checking if the user is an administrator to allow direct reset
                if user["Designation"] == "Administrator":
                    
                    reset_password_byadmin() 
                else:
                    print("Contact Administrator for password reset.")
                return
            else:
                print("Invalid choice. Exiting.")
                return

    print("Too many failed password attempts. Exiting.")
    return

    # calculating login operation Time
    end_time = time.time()
    elapsed_time = end_time - start_time 
    if elapsed_time < 60:
        print(f"Login operation took {elapsed_time:.4f} seconds.")
    elif elapsed_time < 3600:
        print(f"Login operation took {elapsed_time / 60:.4f} minutes.")
    else:
        print(f"Login operation took {elapsed_time / 3600:.4f} hours.")
    print("-" * 40)

def logout_user(user):
    """ Log out the user and calculate their session duration """
    print("-" * 40)
    if "last_login" in user:
        # calculating the session duration
        session_duration = time.time() - user["last_login"]
        
        # initialize login time if it doesn't exist
        if "login_time" not in user:
            user["login_time"] = 0
        
        # adding ession duration to total login time
        user["login_time"] += session_duration
        
        print(f"Logged out. You were logged in for {session_duration:.2f} seconds.")
        print(f"Total logged-in time: {user['login_time']:.2f} seconds.")
        
        # clearing last login time after logout
        user["last_login"] = None
    else:
        print("No login session found.")
    print("-" * 40)

def mark_attendance(faculty_reg_no):
    print("-" * 40)
    print("Mark Attendance for Students:")
    student_reg_no = input("Enter student's Registration Number: ").strip()
    # checking if the student is registered
    if student_reg_no not in users:
        print("Student not found. Please check the registration number.")
        return
    # getting the attendance status
    attendance_status = input("Enter attendance status (P for Present, A for Absent): ").strip().upper()
    if attendance_status not in ['P', 'A']:
        print("Invalid attendance status. Please enter 'P' for Present or 'A' for Absent.")
        return
    # marking attendance in the attendance records
    if student_reg_no not in attendance_records:
        attendance_records[student_reg_no] = []
    # adding attendance record 
    attendance_records[student_reg_no].append({"faculty_reg_no": faculty_reg_no, "status": attendance_status})
    print(f"Attendance for student {student_reg_no} marked as {attendance_status}.")
    print("-" * 40)

def view_attendance_admintofaculty(faculty_reg_no):
    """Allows the administrator to view attendance records marked by faculty for each faculty member."""
    print("-" * 40)
    print("\n--- View Attendance for Faculty ---")

    faculty_reg_no = input("Enter the faculty's Registration Number: ").strip()

    # checking if the faculty has attendance records
    if faculty_reg_no not in attendance_records:
        print(f"No attendance records found for faculty {faculty_reg_no}.")
        return

    # filtering and displaying attendance records for the faculty
    print(f"\nAttendance records for faculty {faculty_reg_no}:")
    records_found = False

    for record in attendance_records[faculty_reg_no]:
        status = record["status"]
        marked_by = record["marked_by"] 
        # checking if the attendance was marked by admin or another entity
        if marked_by == 'Admin':
            records_found = True
            print(f"- Status: {status} (Marked by Admin)")
        else:
            print(f"- Status: {status} (Marked by {marked_by})")

    if not records_found:
        print(f"No attendance records found marked by Admin for faculty {faculty_reg_no}.")
    print("-" * 40)
            
def view_own_attendance_students(student_reg_no):
    """Allows a student to view their attendance records."""
    print(f"\n--- Attendance Records for Student {student_reg_no} ---")
    
    # checking if the student exists in the attendance records
    if student_reg_no not in attendance_records or not attendance_records[student_reg_no]:
        print("No attendance records found.")
        return
    
    # displaying all attendance records for the student
    print(f"Attendance records for {student_reg_no}:")
    for idx, record in enumerate(attendance_records[student_reg_no], start=1):
        faculty = record["faculty_reg_no"]
        status = record["status"]
        print(f"{idx}. Status: {status} (Marked by Faculty: {faculty})")
    
    print("\n--- End of Records ---")
        
def remove_user():
    reg_no = input("Enter the Registration Number of the user to remove: ").strip()
    print("-" * 40)
    if reg_no in users:
        del users[reg_no]
        print(f"User with Registration Number {reg_no} has been removed.")
    else:
        print("User not found.")
    print("-" * 40)
def assign_task_to_faculty(faculty_reg_no):
    """Assign a task to a faculty member (Teaching or Non-Teaching)."""
    # checking if the faculty exists and has the correct designation
    if faculty_reg_no not in users or users[faculty_reg_no]["Designation"] not in ["Teaching", "Non-Teaching"]:
        print("Faculty not found or has an incorrect designation.")
        return
    print("-" * 40)
    task = input("Enter the task description: ").strip()
    if not task:
        print("Task description cannot be empty.")
        return

    if faculty_reg_no not in admin_assigned_tasks:
        admin_assigned_tasks[faculty_reg_no] = []

    admin_assigned_tasks[faculty_reg_no].append(task)
    print("-" * 40)
    print(f"Task '{task}' has been assigned to faculty {faculty_reg_no}.")
    print(f"Faculty {faculty_reg_no} now has {len(admin_assigned_tasks[faculty_reg_no])} task(s) assigned.")
    print("-" * 40)

def remove_task_from_faculty(faculty_reg_no):
    """Remove a specific task assigned to a faculty member."""
    # checking if the faculty exists in the tasks dictionary
    if faculty_reg_no not in admin_assigned_tasks or not admin_assigned_tasks[faculty_reg_no]:
        print(f"No tasks found for faculty {faculty_reg_no}.")
        return
    print("-" * 40)
    # displaying assigned tasks
    print(f"Tasks for faculty {faculty_reg_no}:")
    for i, task in enumerate(admin_assigned_tasks[faculty_reg_no], 1):
        print(f"{i}. {task}")

    task_index = input("Enter the task number to remove: ").strip()
    if not task_index.isdigit():
        print("Invalid input. Please enter a valid number.")
        return

    task_index = int(task_index) - 1
    if 0 <= task_index < len(admin_assigned_tasks[faculty_reg_no]):
        removed_task = admin_assigned_tasks[faculty_reg_no].pop(task_index)
        print(f"Task '{removed_task}' removed successfully.")
        
        # cleaning up if no tasks are left
        if not admin_assigned_tasks[faculty_reg_no]:
            del admin_assigned_tasks[faculty_reg_no]
    else:
        print("Invalid task number. No task was removed.")
    print("-" * 40)

def remove_task_from_student():
    student_reg_no = input("Enter Student's Registration Number whose task you want to remove: ").strip()

    if student_reg_no not in submitted_tasks:
        print(f"No tasks found for student with Registration Number {student_reg_no}.")
        return
    print("-" * 40)
    print(f"Tasks submitted by student {student_reg_no}:")
    student_tasks = submitted_tasks[student_reg_no]
    
    for i, task in enumerate(student_tasks, start=1):
        print(f"{i}. {task}")

    task_to_remove = int(input("Enter the task number you want to remove: ").strip())
    
    if task_to_remove.isdigit():
        task_to_remove = int(task_to_remove)

    if 1 <= task_to_remove <= len(student_tasks):
        removed_task = student_tasks.pop(task_to_remove - 1) # Removes the task from the list which is entered at the last
        print(f"Task '{removed_task}' removed successfully!")

        # Log the removed task
        if student_reg_no not in removed_tasks:
            removed_tasks[student_reg_no] = []
        removed_tasks[student_reg_no].append(removed_task)
        
        if len(student_tasks) == 0:
            del submitted_tasks[student_reg_no]  # Deletes the student entry if no tasks remain
    else:
        print("Invalid task number. No task removed.")
    print("-" * 40)
        

# Modify user details
def modify_user_details():
    reg_no = input("Enter Registration Number to modify details: ").strip()
    print("-" * 40)
    if reg_no in users:
        new_name = input("Enter new name (leave empty to retain current): ").strip()
        new_dob = input("Enter new Date of Birth (YYYY-MM-DD) (leave empty to retain current): ").strip()
        
        if new_name:
            users[reg_no]["Name"] = new_name
        if new_dob:
            users[reg_no]["DOB"] = new_dob

        print("User details updated.")
    else:
        print("User not found.")
    print("-" * 40) 
# View Tasks
def view_tasks_for_faculty(faculty_reg_no):
    print("-" * 40)
    if faculty_reg_no not in admin_assigned_tasks or not admin_assigned_tasks[faculty_reg_no]:
        print(f"No tasks assigned to faculty {faculty_reg_no}.")
        return

    print(f"Assigned tasks for faculty {faculty_reg_no}:")
    for idx, task in enumerate(admin_assigned_tasks[faculty_reg_no], start=1): # idx is the task number
        print(f"{idx}. {task}")
    print("-" * 40)
        
def assign_review_to_student():
    print("-" * 40)
    student_reg_no = input("Enter the student's registration number: ").strip()
    
    if student_reg_no not in submitted_tasks:
        print(f"No submitted tasks found for student {student_reg_no}.")
        return

    # Display all tasks submitted by the student
    print(f"Tasks submitted by student {student_reg_no}:")
    for idx, task in enumerate(submitted_tasks[student_reg_no], start=1):
        print(f"{idx}. Task Name: {task['task_name']} - Submission Date: {task['submission_date']}")

    # Select the task to assign review to
    task_num = int(input("Enter the task number to review: ").strip())
    if task_num < 1 or task_num > len(submitted_tasks[student_reg_no]):
        print("Invalid task number.")
        return

    # Input the review for the selected task
    review = input("Enter the review for this task: ").strip()

    # Add the review to the task
    submitted_tasks[student_reg_no][task_num - 1]["review"] = review
    print(f"Review for task '{submitted_tasks[student_reg_no][task_num - 1]['task_name']}' added successfully.")

    # Optionally, display the task with the assigned review (if needed)
    print(f"Review added to the task '{submitted_tasks[student_reg_no][task_num - 1]['task_name']}': {review}")
    print("-" * 40)
        
def view_reviews_by_user(user_reg_no):
    print("-" * 40)
    print(f"Tasks, Grades, and Reviews for {user_reg_no}:")

    # Check if the user has any submitted tasks
    if user_reg_no not in submitted_tasks or not submitted_tasks[user_reg_no]:
        print("No submitted tasks found.")
        return

    # Display tasks along with their grades and reviews
    for idx, task in enumerate(submitted_tasks[user_reg_no], start=1): # idx is the task number 
        task_name = task.get('task_name', 'Unnamed Task')
        review = task.get('review', 'No review assigned yet')
        grade = task.get('grade', 'Not Graded')
        
        print(f"{idx}. Task Name: {task_name} - Grade: {grade} - Review: {review}")
    print("-" * 40)


def view_all_submitted_tasks_and_reviews():
    print("-" * 40)
    if not submitted_tasks or not any(submitted_tasks.values()):
        print("No tasks have been submitted by students yet.")
        print("-" * 40)
        return
    
    print("All Submitted Tasks and Reviews:")
    for reg_no, tasks in submitted_tasks.items():
        if tasks:
            print(f"\nStudent {reg_no} has submitted the following tasks:")
            for task in tasks:
                review = task.get("review", "No review assigned yet.")
                print(f"  Task Name: {task['task_name']} - Review: {review}")
        else:
            print(f"\nStudent {reg_no} has not submitted any tasks.")
    print("-" * 40)

def assign_review_by_admin():
    print("-" * 40)
    print("Assign Review by Admin (For Faculty Only)")

    # Check if the user is a Faculty member
    reg_no = input("Enter the Faculty's registration number: ").strip()

    if reg_no not in users:
        print(f"Faculty with registration number {reg_no} not found.")
        return

    if "faculty" not in users[reg_no]["Designation"].lower():
        print("This is not a Faculty member. Reviews can only be assigned to Faculty.")
        return

    if reg_no not in submitted_tasks:
        print(f"No submitted tasks found for Faculty {reg_no}.")
        return

    print(f"Tasks submitted by Faculty {reg_no}:")
    for idx, task in enumerate(submitted_tasks[reg_no], start=1):
        print(f"{idx}. Task Name: {task['task_name']} - Submission Date: {task['submission_date']}")

    task_num = int(input("Enter the task number to review: ").strip())
    if task_num < 1 or task_num > len(submitted_tasks[reg_no]):
        print("Invalid task number.")
        return

    review = input("Enter the review for this task: ").strip()

    # Add the review to the specific task
    submitted_tasks[reg_no][task_num - 1]["review"] = review
    print(f"Review for task '{submitted_tasks[reg_no][task_num - 1]['task_name']}' added successfully.")
    print("-" * 40)  
def admin_mark_faculty_attendance():
    print("-" * 40)
    print("Admin: Mark Attendance for Faculty")
    # Get the faculty registration number
    faculty_reg_no = input("Enter faculty's Registration Number: ").strip()

    # Check if the faculty is registered
    if faculty_reg_no not in users:
        print("Faculty not found. Please check the registration number.")
        return

    # Get the attendance status (Present/Absent)
    attendance_status = input("Enter attendance status (P for Present, A for Absent): ").strip().upper()
    if attendance_status not in ['P', 'A']:
        print("Invalid attendance status. Please enter 'P' for Present or 'A' for Absent.")
        return

    # Mark attendance in the faculty_attendance records
    if faculty_reg_no not in faculty_attendance:
        faculty_attendance[faculty_reg_no] = []

    # Add attendance record for the faculty
    faculty_attendance[faculty_reg_no].append({"status": attendance_status, "marked_by": "Admin"})
    print(f"Attendance for faculty {faculty_reg_no} marked as {attendance_status}.")
    print("-" * 40)
# Faculty function to view their own attendance
def view_faculty_attendance(faculty_reg_no):
    print("-" * 40)
    print(f"View Your Attendance, Faculty {faculty_reg_no}:")
    if faculty_reg_no not in faculty_attendance:
        print("No attendance records found for this faculty.")
        return

    # Display all attendance records for the faculty
    print(f"Attendance records for faculty {faculty_reg_no}:")
    for record in faculty_attendance[faculty_reg_no]:
        status = record["status"]
        marked_by = record["marked_by"]
        print(f"Status: {status} (Marked by: {marked_by})")
    print("-" * 40)
# Admin Menu
def admin_menu(user):
    while True:
        print("-" * 40)
        print("\nAdministrator Menu:")
        print("1. Add User")
        print("2. Remove User")
        print("3. Assign Tasks")
        print("4. Remove Task") #problem
        print("5. View Submitted Tasks")
        print("6. Modify User Details")
        print("7. Mark Attendance")
        print("8. View all Attendance")
        print("9. View assigned tasks")
        print("10. View all users")
        print("11. Assign Review")
        print("12. Reset Password")
        print("13. View Password")
        print("14. View submitted task from faculties")
        print("15. View Reviews")
        print("16. Logout")
        print("-" * 40)
        
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            register_user()  # Admin can add users
        elif choice == "2":
            remove_user()  # Admin can remove users
        elif choice == "3":
            print("-" * 40)
            print("1. Assign Task to Teaching Faculty")
            print("2. Assign Task to Student")
            sub_choice = input("Enter your choice: ").strip()
            if sub_choice == "1":
                faculty_reg_no = input("Enter faculty registration number: ").strip()
                assign_task_to_faculty(faculty_reg_no)  # Admin can assign tasks to teaching faculty
            elif sub_choice == "2":
                student_reg_no = input("Enter student registration number: ").strip()
                assign_task_to_student(student_reg_no)  # Admin can assign tasks to non-teaching faculty
            else:
                print("Invalid choice.")
        elif choice == "4":
            print("-" * 40)
            print("1. Remove Task from Faculty")# Admin can remove tasks
            print("2. Remove Task from Student")
            sub_choice = input("Enter your choice: ").strip()
            if sub_choice == "1":
                remove_task_from_faculty()  # Admin can remove tasks from teaching faculty
            elif sub_choice == "2":
                remove_task_from_student()  # Admin can remove tasks from non-teaching faculty
            else:
                print("Invalid choice.")
        elif choice == "5":
            print("-" * 40)
            print("1. View submitted tasks by faculty")
            print("2. View submitted tasks by students")
            sub_choice = input("Enter your choice: ").strip()
            if sub_choice == "1":
                faculty_reg_no = input("Enter faculty registration number: ").strip()
                view_all_submitted_tasks_to_admin()  # View all tasks submitted by faculties to admin
            elif sub_choice == "2":
                view_all_submitted_tasks_and_reviews()# View all submitted tasks and reviews  
            else:
                print("Invalid choice.")
        elif choice == "6":
            modify_user_details()  # Admin can modify user details
        elif choice == "7":# Admin can mark attendance
            print("-" * 40)
            print("1. Mark Attendance for Faculty")
            print("2. Mark Attendance for Student")
            sub_choice = input("Enter your choice: ").strip()
            if sub_choice == "1":
                admin_mark_faculty_attendance()  # Admin can mark faculty attendance
            elif sub_choice=="2":
                mark_attendance(user["Registration No."])
            else:
                print("Invalid choice.")
        elif choice == "8":
            print("-" * 40)
            print("1. View Attendance for Faculty")
            print("2. View Attendance for Student")
            sub_choice = input("Enter your choice: ").strip()
            if sub_choice == "1":
                view_attendance_admintofaculty()  # View faculty attendance
            elif sub_choice == "2":
                view_own_attendance_students(user["Registration No."])  # Admin can view attendance for students
            else:
                print("Invalid choice.")
        elif choice == "9":
            print("-" * 40)
            print("1. View tasks for faculty")
            print("2. View tasks for students")
            print("3. View all tasks")
            sub_choice = input("Enter your choice: ").strip()
            if sub_choice == "1":
                faculty_reg_no = input("Enter faculty registration number: ").strip()
                view_tasks_for_faculty(faculty_reg_no)  # Admin can view tasks for faculty
            elif sub_choice == "2":
                student_reg_no = input("Enter student registration number: ").strip()
                view_tasks_for_student(student_reg_no)  # Admin can view tasks for students
            elif sub_choice == "3":
                view_all_assigned_tasks()
            else:
                print("Invalid choice.")
        elif choice == "10":
            view_all_users()  # Admin can view all users
        elif choice == "11":
            print("-" * 40)
            print("1. Assign Review to Faculty")
            print("2. Assign Review to Student")
            sub_choice = input("Enter your choice: ").strip()
            if sub_choice == "1":
                assign_review_by_admin()  # Admin can assign reviews to faculties
            elif sub_choice == "2":
                assign_review_to_student()
        elif choice == "12":
            reset_password_byadmin()
        elif choice == "13":
            print("-" * 40)
            reg_no = input("Enter the registration number of the user: ").strip()
            if reg_no in users:
                seed = input("Enter the seed value for the user: ").strip()
                encrypted_password = users[reg_no]["EncryptedPassword"]  # Get the encrypted password

                # Decrypt the password
                decrypted_password = decrypt_password(encrypted_password, seed)  # Decrypt using reg_no and seed
                print(f"Decrypted Password: {decrypted_password}")
            else:
                print("User not found.")
            print("-" * 40)
        elif choice == "14":
            view_submitted_tasks_for_admin()
        elif choice == "15":
            print("-" * 40)
            print("1. View Reviews by Faculty to student")
            print("2. View Reviews by Admin")
            sub_choice = input("Enter your choice: ").strip()
            if sub_choice == "1":
              view_submitted_tasks_and_reviews(user["Registration No."])  
            elif sub_choice == "2":
              view_reviews_by_user()
            else:
                print("Invalid choice.")
        elif choice == "16":
            logout_user(user) 
            break
        else:
            print("Invalid choice. Try again.")


def submit_task_to_faculty(student_reg_no, task):
    print("-" * 40)
    if student_reg_no in users and users[student_reg_no]["Designation"] == "Student":
        faculty_reg_no = users[student_reg_no].get("AssignedFaculty")
        if faculty_reg_no and faculty_reg_no in users:
            if "SubmittedTasksToFaculty" not in users[student_reg_no]:
                users[student_reg_no]["SubmittedTasksToFaculty"] = []
            users[student_reg_no]["SubmittedTasksToFaculty"].append(task)
            print(f"Task '{task}' submitted successfully by {users[student_reg_no]['Name']} to faculty {users[faculty_reg_no]['Name']}.")
        else:
            print("Assigned faculty not found or invalid.")
    else:
        print("Invalid student registration number.")
    print("-" * 40)

def view_all_submitted_tasks_to_admin():
    print("-" * 40)
    print("\n--- All Tasks Submitted to Admin ---")
    all_tasks_to_admin = []

    # Iterate through all users and check for submitted tasks
    for reg_no, user_data in users.items():
        if user_data.get("Designation") in ["Teaching", "Non-Teaching"]:
            tasks = user_data.get("SubmittedTasksToAdmin", [])
            if tasks:  # Ensure there are tasks to add
                for task in tasks:
                    all_tasks_to_admin.append((reg_no, user_data["Name"], task))

    # Display all tasks
    if all_tasks_to_admin:
        for task in all_tasks_to_admin:
            print(f"Faculty: {task[1]}, Task: {task[2]}")
    else:
        print("No tasks have been submitted to the Admin yet.")
    print("-" * 40)
# Function to view all tasks submitted by students to faculties
def view_all_submitted_tasks_by_students():
    print("-" * 40)
    print("\n--- All Tasks Submitted by Students ---")
    all_tasks_by_students = []
    
    # Iterate through all students and the faculty to which they have submitted tasks
    for student_reg_no, student_data in users.items():
        if student_data["Designation"] == "Student":
            faculty_reg_no = student_data.get("AssignedFaculty", None)
            if faculty_reg_no:
                tasks = student_data.get("SubmittedTasksToFaculty", [])
                for task in tasks:
                    all_tasks_by_students.append((student_reg_no, student_data["Name"], task, faculty_reg_no))
    
    # Print all tasks submitted by students to faculty
    if all_tasks_by_students:
        for task in all_tasks_by_students:
            print(f"Student: {task[1]}, Task: {task[2]}, Faculty: {task[3]}")
    else:
        print("No tasks have been submitted by students yet.")
    print("-" * 40)

def view_faculty_submitted_tasks(user):
    print("-" * 40)
    reg_no = user["Registration No."]
    print(f"Submitted Tasks for Faculty {reg_no}:")
    found_tasks = False
    for student_reg_no, tasks_list in submitted_tasks.items():
        for task in tasks_list:
            if task.get("faculty_reg_no") == reg_no:
                found_tasks = True
                print(f"Student: {student_reg_no}, Task: {task['task']}, Status: {task['status']}, Grade: {task.get('grade', 'Not Graded')}, Review: {task.get('review', 'No Review')}")
    if not found_tasks:
        print("No tasks submitted to you.")
    print("-" * 40)
# Function for faculties (Teaching/Non-Teaching) to submit a task to Admin
def submit_task_to_admin(faculty_reg_no, task):
    print("-" * 40)
    if faculty_reg_no in users and users[faculty_reg_no]["Designation"] in ["Teaching", "Non-Teaching"]:
        if "SubmittedTasksToAdmin" not in users[faculty_reg_no]:
            users[faculty_reg_no]["SubmittedTasksToAdmin"] = []
        users[faculty_reg_no]["SubmittedTasksToAdmin"].append(task)
        print(f"Task submitted successfully by {users[faculty_reg_no]['Name']}.")
    else:
        print("Invalid faculty registration number.")

    print("-" * 40)

# View submitted tasks
def view_submitted_tasks_for_faculty(faculty_reg_no):
    print("-" * 40)
    print(f"\n--- Tasks Submitted to Faculty {faculty_reg_no} ---")
    for student_reg_no, tasks_for_faculty in submitted_tasks.items():
        if faculty_reg_no in tasks_for_faculty:
            print(f"\nStudent {student_reg_no}:")
            for task in tasks_for_faculty[faculty_reg_no]:
                print(f"  - {task}")
    print("-" * 40)
def view_all_assigned_tasks():
    print("-" * 40)
    # Administrator views all tasks assigned by them (to faculty) and faculty to students
    print("\n--- Tasks Assigned by Administrator to Faculty ---")
    if not admin_assigned_tasks:
        print("No tasks assigned by the administrator.")
    else:
        for faculty_reg_no, tasks in admin_assigned_tasks.items():
            print(f"\nFaculty {faculty_reg_no}:")
            for task in tasks:
                print(f"  - {task}")

    print("\n--- Tasks Assigned by Faculty to Students ---")
    if not faculty_assigned_tasks_to_students:
        print("No tasks assigned by faculty to students.")
    else:
        for student_reg_no, tasks in faculty_assigned_tasks_to_students.items():
            print(f"\nStudent {student_reg_no}:")
            for task in tasks:
                print(f"  - {task}")        
    print("-" * 40)

# Assign Task to Student
def assign_task_to_student():
    print("-" * 40)
    # Faculty assigns tasks to students
    student_reg_no = input("Enter the student's Registration Number: ").strip()

    if student_reg_no not in users or users[student_reg_no]["Designation"] != "Student":
        print("Student not found.")
        return

    task = input("Enter the task description: ").strip()

    # Assign the task to the student
    if student_reg_no not in faculty_assigned_tasks_to_students:
        faculty_assigned_tasks_to_students[student_reg_no] = []

    faculty_assigned_tasks_to_students[student_reg_no].append(task)
    
    print(f"Task '{task}' has been assigned to student {student_reg_no}.")
    print("-" * 40)

    
def view_tasks_for_student(student_reg_no):
    print("-" * 40)
    if student_reg_no not in assigned_tasks or not assigned_tasks[student_reg_no]:
        print(f"No tasks assigned to student {student_reg_no}.")
        return

    print(f"Assigned tasks for student {student_reg_no}:")
    for idx, task in enumerate(assigned_tasks[student_reg_no], start=1):
        print(f"{idx}. {task}")
    print("-" * 40)    
def view_submitted_tasks(student_reg_no):
    print("-" * 40)
    print(f"\n--- Tasks Submitted by Student {student_reg_no} ---")
    if student_reg_no not in submitted_tasks or not submitted_tasks[student_reg_no]:
        print("No tasks submitted yet.")
    else:
        for faculty_reg_no, tasks in submitted_tasks[student_reg_no].items():
            print(f"\nFaculty {faculty_reg_no}:")
            for task in tasks:
                print(f"  - {task}")
    print("-" * 40)
        
def reset_password_byadmin():
    print("-" * 40)
    print("Reset Password - Admin Access")
    reg_no = input("Enter the registration number of the user to reset the password: ").strip()

    # Check if the user exists
    if reg_no in users:
        user_data = users[reg_no]
        print(f"User found: {user_data['Name']} ({user_data['Designation']})")

        # Input new password
        new_password = input("Enter the new password (at least 8 chars with uppercase, lowercase, digits, special chars): ").strip()
        while not is_valid_password(new_password):  # Use the validation function to ensure strong passwords
            print("Invalid password. Try again.")
            new_password = input("Enter the new password: ").strip()

        # Generate a new seed for password encryption
        new_seed = generate_unique_seed()
        
        # Encrypt the new password
        encrypted_password,encrypt_time = encrypt_password(new_password, new_seed)

        # Update the user's password and seed
        user_data["EncryptedPassword"] = encrypted_password
        user_data["Seed"] = new_seed

        print("-" * 40)
        print(f"Password reset successful for {user_data['Name']} ({reg_no}).")
        print(f"Encrypted Password: {encrypted_password}")
        print(f"New Seed Value (User should note this down): {new_seed}")
        print(f"Time taken for encryption :{encrypt_time:.10f}s")
        print("-" * 40)
    else:
        print("User not found.")
        
def view_submitted_tasks_for_admin():
    print("-" * 40)
    print("\n--- Tasks Submitted to Administrator ---")
    if not submitted_tasks_to_admin:
        print("No tasks submitted yet.")
    else:
        for faculty_reg_no, tasks in submitted_tasks_to_admin.items():
            print(f"\nFaculty {faculty_reg_no}:")
            for task in tasks:
                print(f"  - {task}")
    print("-" * 40)            
def view_submitted_tasks_for_faculty_to_admin(faculty_reg_no):
    print("-" * 40)
    # Check if the faculty is registered
    if faculty_reg_no not in users or users[faculty_reg_no]["Designation"] not in ["Teaching", "Non-Teaching"]:
        print(f"Faculty {faculty_reg_no} not found or not eligible to submit tasks.")
        return

    print(f"\n--- Tasks Submitted by Faculty {faculty_reg_no} ---")
    if faculty_reg_no not in submitted_tasks_to_admin or not submitted_tasks_to_admin[faculty_reg_no]:
        print("No tasks submitted yet.")
    else:
        for task in submitted_tasks_to_admin[faculty_reg_no]:
            print(f"  - {task}")
    print("-" * 40)
def remove_submitted_task_from_student():
    print("-" * 40)
    # Ask for the registration number of the student whose task needs to be removed
    student_reg_no = input("Enter Student's Registration Number whose task you want to remove: ").strip()

    if student_reg_no not in submitted_tasks:
        print(f"No tasks found for student with Registration Number {student_reg_no}.")
        return

    print(f"Tasks submitted by student {student_reg_no}:")
    student_tasks = submitted_tasks[student_reg_no]
    
    # Display submitted tasks
    for i, task in enumerate(student_tasks, start=1):
        print(f"{i}. {task}")

    # Ask for the task to remove
    task_to_remove = int(input("Enter the task number you want to remove: ").strip())

    if 1 <= task_to_remove <= len(student_tasks):
        removed_task = student_tasks.pop(task_to_remove - 1)
        print(f"Task '{removed_task}' removed successfully!")
        
        # Update the dictionary
        if len(student_tasks) == 0:
            del submitted_tasks[student_reg_no]  # Remove the student entry if no tasks remain
    else:
        print("Invalid task number. No task removed.")
    print("-" * 40)
def view_submitted_tasks_and_reviews(student_reg_no):
    print("-" * 40)
    if student_reg_no not in submitted_tasks:
        print("No tasks have been submitted yet.")
        return

    print(f"Submitted Tasks and Reviews for student {student_reg_no}:")
    for task in submitted_tasks[student_reg_no]:
        # Check if the 'review' key exists and assign the value or default to "No review assigned yet."
        review = task["review"] if "review" in task else "No review assigned yet."
        print(f"Task Name: {task['task_name']}, Review: {review}")
    print("-" * 40)
# Teaching Faculty Menu
def teaching_faculty_menu(user):
    while True:
        print("-" * 40)
        print(f"\n{user['Name']} (Teaching Faculty) Menu:")
        print("1. View Tasks")
        print("2. Assign Task to Student")
        print("3. Mark Attendance")
        print("4. View own Attendance")
        print("5. Assign Review")
        print("6. View Grades and Reviews")
        print("7. View Submitted Tasks from Students")
        print("8. Reset Password")
        print("9. Submit task to administrator")
        print("10. View submitted task to administrator")
        print("11. Remove submitted task from student")
        print("12. View attendance given to student")
        print("13. Logout")
        print("-" * 40)
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            faculty_reg_no = user.get("Registration Number")
            if not faculty_reg_no:
              print("Error: Faculty registration number not found.")
              print(f"Debug info: User dictionary is {user}")  
              return
            view_tasks_for_faculty(faculty_reg_no)
        elif choice == "2":
            assign_task_to_student()
        elif choice == "3":
            mark_attendance(user["Registration No."])  # Mark student attendance
        elif choice == "4":
            view_attendance_admintofaculty(faculty_reg_no)  # View faculty attendance
        elif choice == "5":
            assign_review_to_student()
        elif choice == "6":
            view_reviews_by_user(user["Registration No."])
        elif choice == "7":
            view_submitted_tasks_for_faculty(user["Registration No."])  # View tasks submitted to the faculty
        elif choice == "8":
            print("Contact Administrator")
        elif choice == "9":
            submit_task_to_admin(user["Registration No."])  # Submit task to Admin
        elif choice == "10":
            view_submitted_tasks_for_faculty_to_admin(user["Registration No."])  # View tasks submitted to Admin
        elif choice == "11":
            remove_submitted_task_from_student()
        elif choice == "12":
            view_own_attendance_students(user["Registration No."])
        elif choice == "13":
            logout_user(user)
            break
        else:
            print("Invalid choice. Try again.")

def non_teaching_faculty_menu(user):
    while True:
        print("-" * 40)
        print(f"\n{user['Name']} (Non-Teaching Faculty) Menu:")
        print("1. View own Attendance")
        print("2. View Tasks")
        print("3. Submit Task to administrator")
        print("4. View Submitted Tasks")
        print("5. View Grades and Reviews")
        print("6. Reset Password")
        print("7. Logout")
        print("-" * 40)
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_attendance_admintofaculty()  # View faculty attendance
        elif choice == "2":
            view_tasks_for_faculty(user["Registration No."])
        elif choice == "3":
            submit_task_to_admin(user["Registration No."])  # Submit task to Admin
        elif choice == "4":
            view_submitted_tasks_for_faculty_to_admin(user["Registration No."])  # View tasks submitted to Admin
        elif choice == "5":
            view_reviews_by_user(user["Registration No."])
        elif choice == "6":
            print("Contact Administrator")
        elif choice == "7":
            logout_user(user)
            break
        else:
            print("Invalid choice. Try again.")


# Student Menu
def student_menu(user):
    while True:
        print("-" * 40)
        print(f"\n{user['Name']} (Student) Menu:")
        print("1. View own Attendance")
        print("2. View Tasks")
        print("3. Submit Task")
        print("4. View submitted tasks and reviews")
        print("5. Logout")
        print("-" * 40)
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_own_attendance_students(user["Registration No."])  # View attendance
        elif choice == "2":
            view_tasks_for_student(user["Registration No."])  # View assigned tasks
        elif choice == "3":
            print("-" * 40)
            # Let student choose which teaching faculty they want to submit a task to
            faculty_reg_no = input("Enter the Faculty Registration Number to submit the task: ").strip()
            if faculty_reg_no not in users or users[faculty_reg_no]["Designation"] != "Teaching":
                print("Invalid Faculty Registration Number.")
                continue
            submit_task_to_faculty(user['Registration No.'], faculty_reg_no)  # Submit task
            print("-" * 40)
        elif choice == "4":
          view_submitted_tasks_and_reviews(user["Registration No."])  # View submitted tasks and reviews
        elif choice == "5":
            logout_user(user) 
            break
        else:
            print("Invalid choice. Try again.")


# Main
def main():
    while True:
        print("-" * 40)
        print("\nWelcome to the User Management System")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        print("-" * 40)
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            register_user()
        elif choice == "2":
            login_user()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Try again.")

# Run the main menu
if __name__ == "__main__":
    main()

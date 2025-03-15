import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from employee import Empl as employeeapp
from employer import Empl as employerapp
from register__ee import App as ee_App  # Import the Registration class
from register_er import App as er_App  # Import the Registration class
from database import (
    retrieve_employers,
    retrieve_employers_password,
    retrieve_employees_password,
    retrieve_employers_id,
    retrieve_employees_id,
)
import subprocess

# Set appearance mode
ctk.set_appearance_mode("light")


class MainApp(ctk.CTk):
    def __init__(self, master=None):  # Ensure 'master' is passed here
        super().__init__(master)  # Pass 'master' to the parent class constructor
        self.master = master  # Store the parent (App) reference
        self.title("Career Castle")
        self.geometry("1000x667")
        self.iconbitmap(r"C:\Users\Shema\Desktop\version1.0\code\images\castleicon.ico")
        self.resizable(False, False)

        # Background image setup
        img = Image.open(r"C:\Users\Shema\Desktop\version1.0\code\images\bg_img_login.jpg").convert("RGBA")
        alpha = 0.7
        alpha_layer = img.split()[3].point(lambda p: int(p * alpha))
        img.putalpha(alpha_layer)
        bg_image = ctk.CTkImage(light_image=img, dark_image=img, size=(1000, 667))
        self.label = ctk.CTkLabel(self, image=bg_image, text='', width=1000, height=667)
        self.label.place(relwidth=1, relheight=1)

        # Initialize variables
        self.flag = ["employee", "employer"]
        self.choice = self.flag[0]

        # Header Frame
        self.frame1 = Header(self)
        self.frame1.pack(side="top", fill="x")

        # Login Frame
        self.login = ctk.CTkFrame(self, fg_color="#e0e0e0", height=300, width=350)
        self.login.place(relx=0.04, rely=0.37)

        # Initialize Employee View
        self.create_employee_view()

    def update_login_position(self):
        """Update the position of the login frame based on the current choice."""
        if self.choice == "employee":
            self.login.place(relx=0.57, rely=0.37)
        elif self.choice == "employer":
            self.login.place(relx=0.04, rely=0.37)
        else:
            messagebox.showinfo("Error", "Unclear choice")

    def create_employee_view(self):
        """Create and display the Employee Login Form."""
        self.choice = self.flag[0]
        self.update_login_position()
        for widget in self.login.winfo_children():
            widget.destroy()

        # Employee Login Form
        ctk.CTkLabel(self.login, text="Employee Login Form", font=("Verdana", 21, "bold"), text_color="blue").pack(pady=10)
        self.frame_entry1 = frame_entry1(self.login)
        self.frame_entry1.pack(pady=10)

        # Button to switch to Employer Login
        ctk.CTkButton(self.login, text="Switch to Employer View", command=self.create_employer_view).pack(pady=20)

    def create_employer_view(self):
        """Create and display the Employer Login Form."""
        self.choice = self.flag[1]
        self.update_login_position()
        for widget in self.login.winfo_children():
            widget.destroy()

        # Employer Login Form
        ctk.CTkLabel(self.login, text="Employer Login Form", font=("Verdana", 21, "bold"), text_color="blue").pack(pady=10)
        self.frame_entry2 = frame_entry2(self.login)
        self.frame_entry2.pack(pady=10)

        # Button to switch to Employee Login
        ctk.CTkButton(self.login, text="Switch to Employee View", command=self.create_employee_view).pack(pady=20)

class Header(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="#b8d1e8", height=70)
        ctk.CTkLabel(self, text="Career Castle", text_color="black", font=("Arial", 24, "bold")).place(relx=0.37, rely=0)
        ctk.CTkLabel(self, text="A noble connection, built on integrity and trust.",
                     text_color="black", font=("Verdana", 18, "italic")).place(relx=0.2, rely=0.4)

class frame_entry1(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="#b6b6b6", height=280, width=320)

        # Username Entry
        ctk.CTkLabel(self, text="Username:", font=("Arial", 20, "bold")).place(relx=0.06, rely=0.22)
        self.employee_name = ctk.CTkEntry(self, placeholder_text="shema", height=40, width=175)
        self.employee_name.place(relx=0.38, rely=0.2)

        # Password Entry
        ctk.CTkLabel(self, text="Password:", font=("Arial", 20, "bold")).place(relx=0.06, rely=0.42)
        self.employee_password = ctk.CTkEntry(self, placeholder_text="password", height=40, width=175, show='*')
        self.employee_password.place(relx=0.38, rely=0.4)

        # Buttons
        ctk.CTkButton(self, text="Register", font=("Verdana", 20, "bold"), width=90, height=40, cursor="hand2",
                      command=employee_reg).place(relx=0.12, rely=0.65)
        ctk.CTkButton(self, text="Login", font=("Verdana", 20, "bold"), width=90, height=40, cursor="hand2",
                      command=lambda: employee_log(self)).place(relx=0.54, rely=0.65)

class frame_entry2(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="#b6b6b6", height=280, width=320)

        value= retrieve_employers()
        companies=[]
        for i in value:
            companies.append(i[1])
         # Replace with dynamic companies list
        ctk.CTkLabel(self, text="Company:", font=("Arial", 20, "bold")).place(relx=0.06, rely=0.22)
        self.employer_name = ctk.CTkComboBox(self, values=companies, height=40, width=175)
        self.employer_name.place(relx=0.38, rely=0.2)

        # Password Entry
        ctk.CTkLabel(self, text="Password:", font=("Arial", 20, "bold")).place(relx=0.06, rely=0.42)
        self.employer_password = ctk.CTkEntry(self, placeholder_text="password", height=40, width=175, show='*')
        self.employer_password.place(relx=0.38, rely=0.4)

        # Buttons
        ctk.CTkButton(self, text="Register Company", font=("Verdana", 17, "bold"), width=120, height=40,
                      cursor="hand2", command=employer_reg).place(relx=0.06, rely=0.65)
        ctk.CTkButton(self, text="Login", font=("Verdana", 20, "bold"), width=90, height=40, cursor="hand2",
                      command=lambda: employer_log(self)).place(relx=0.67, rely=0.65)

def employee_reg():
    reg_app = ee_App()
    reg_app.mainloop()


def employer_reg():
    reg_app = er_App()
    reg_app.mainloop()




def employee_log(self):
    username = self.employee_name.get().strip().upper()
    password = self.employee_password.get().strip().upper()
    correct_password = retrieve_employees_password(username)

    if correct_password and password == correct_password:
        employee_id = retrieve_employees_id(username) 
        subprocess.Popen(['py', 'employee.py', str(employee_id)])
    # Pass employee_id to the next view
    else:
        messagebox.showerror("Login Failed", "Incorrect username or password. Please try again.")

def employer_log(self):
    company_name = self.employer_name.get().strip().upper()
    password = self.employer_password.get().strip().upper()
    correct_password = retrieve_employers_password(company_name)
    print(company_name )
    print(correct_password)
    if correct_password and password == correct_password:
        employer_id = retrieve_employers_id(company_name)
        subprocess.Popen(['py', 'employer.py', str(employer_id)]) 
    else:
        messagebox.showerror("Login Failed", "Incorrect username or password. Please try again.")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()

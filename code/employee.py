import customtkinter as ctk
from PIL import Image
import os
import sys  # To capture the passed arguments
import subprocess
from database import update_employee, get_employee_details

class Empl(ctk.CTk):
    def __init__(self,user_id):
        super().__init__()

        self.title("Career Castle")
        self.geometry('950x550')
        self.iconbitmap(r"C:\Users\Shema\Desktop\version1.0\code\images\castleicon.ico")
        self.resizable(False, False)

        # Retrieve employee ID passed from subprocess (through sys.argv)
        self.employee_id = user_id 
        print(f"Employee ID: {self.employee_id}")  # You can remove or replace this line with your own logic

        # Side frame
        self.side_bar = SideFrame(self, self.employee_id)  # Pass employee_id to the side frame
        self.side_bar.grid(row=0, column=0, rowspan=2, sticky="ns")

        # Advertisements frame
        self.advert_frame = AdvertFrame(self)
        self.advert_frame.grid(row=0, column=1, columnspan=2, sticky="nsew")

        # Database view
        self.database_view = DatabaseView(self)
        self.database_view.grid(row=1, column=1, columnspan=2, sticky="nsew")


class SideFrame(ctk.CTkFrame):
    def __init__(self, parent, employee_id):
        super().__init__(parent)
        self.configure(fg_color="#72787d", width=200)
        self._corner_radius = 0

        # Store the employee ID
        self.employee_id = employee_id

        # Fetch employee details from the database and store them
        self.employee_details = get_employee_details(self.employee_id)

        # Profile image
        img = Image.open(r"C:\Users\Shema\Desktop\version1.0\code\images\profile.png")
        bg_image = ctk.CTkImage(light_image=img, dark_image=img, size=(100, 100))

        self.label1 = ctk.CTkLabel(self, image=bg_image, text='', width=100, height=100)
        self.label1.place(relx=0.1, rely=0.03)

        self.label2 = ctk.CTkLabel(self, text=f"User: {self.employee_id}", font=("Verdana", 15, "bold"))
        self.label2.place(relx=0.1, rely=0.23)

        # Labels and read-only entries for employee details
        labels = ["Name", "Password", "Email"]
        self.entries = {}
        for i, label in enumerate(labels):
            ctk.CTkLabel(self, text=label, font=("Verdana", 14, "bold")).place(relx=0, rely=0.36 + i * 0.1)
            entry = ctk.CTkEntry(self, width=120, font=("Arial", 14))
            entry.place(relx=0.35, rely=0.35 + i * 0.1)
            entry.insert(0, self.employee_details[i])  # Populate with employee details
            entry.configure(state="readonly")
            self.entries[label] = entry

        # Update button to open a window for editing details
        ctk.CTkButton(self, text="Modify", font=("Verdana", 12, "bold"), command=self.open_update_window).place(relx=0.016, rely=0.835)
        ctk.CTkButton(self, text="Log Out", font=("Verdana", 12, "bold"), command=self.logout).place(relx=0.016, rely=0.935)

    

    def open_update_window(self):
        # Open a new window with editable fields
        update_window = ctk.CTkToplevel(self)
        update_window.title("Update Profile")
        update_window.geometry("400x300")

        # Create editable fields with current employee details
        labels = ["Name", "Password", "Email"]
        fields = {}

        for i, label in enumerate(labels):
            ctk.CTkLabel(update_window, text=label, font=("Verdana", 14, "bold")).grid(row=i, column=0, padx=20, pady=10)
            entry = ctk.CTkEntry(update_window, width=250, font=("Arial", 14))
            entry.grid(row=i, column=1, padx=20, pady=10)
            entry.insert(0, self.employee_details[i])  # Insert current value into the entry field
            fields[label] = entry

        # Submit button to update data
        ctk.CTkButton(update_window, text="Submit", command=lambda: self.submit_update(fields, update_window)).grid(row=3, columnspan=2, pady=20)

    def submit_update(self, fields, update_window):
        # Function to submit updated data to the database
        name = fields["Name"].get().strip()
        password = fields["Password"].get().strip()
        email = fields["Email"].get().strip()
        update_employee(name, password, email, self.employee_id)
        # Update database with new details
            
       
        self.employee_details = (name, password, email)  # Update local details
        update_window.destroy()  # Close the update window

    def logout(self):
        # Function to log out and open the employer program
        subprocess.Popen(['py', 'login.py'])

class AdvertFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="#90a4a3", width=750, height=180)
        self._corner_radius = 0

        self.images = self.load_advertisement_images(range(1, 4))
        self.current_image_index = 0

        if self.images:
            self.display_advertisement(self.current_image_index)
            self.cycle_advertisements()

    def load_advertisement_images(self, img_range):
        images = []
        for i in img_range:
            for ext in ['jpg', 'jpeg']:
                img_path = fr"C:\Users\Shema\Desktop\version1.0\code\images\{i}.{ext}"
                if os.path.exists(img_path):
                    image = Image.open(img_path).resize((400, 300), Image.Resampling.LANCZOS)
                    images.append(image)
                    break
        return images

    def display_advertisement(self, index):
        if 0 <= index < len(self.images):
            ad_image = ctk.CTkImage(light_image=self.images[index], dark_image=self.images[index], size=(400, 300))
            ad_label = ctk.CTkLabel(self, image=ad_image, text='')
            ad_label.place(relx=0.5, rely=0.5, anchor='center')

    def cycle_advertisements(self):
        if self.images:
            self.current_image_index = (self.current_image_index + 1) % len(self.images)
            self.display_advertisement(self.current_image_index)
            self.after(3500, self.cycle_advertisements)


class ScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent, frame_name, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.frame_name = frame_name
        self.refresh_content()

    def refresh_content(self):
        for widget in self.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self, text=f"Table of {self.frame_name}", font=("Verdana", 16, "bold")).pack(pady=10)
        for i in range(10):
            ctk.CTkLabel(self, text=f"Row {i + 1}", font=("Verdana", 14)).pack(pady=5)


class TabView(ctk.CTkTabview):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="black", width=720, height=360)
        self.add("Posted Jobs")
        self.add("Offered Jobs")

        ScrollableFrame(self.tab("Posted Jobs"), "Posted Jobs").pack(fill="both", expand=True)
        ScrollableFrame(self.tab("Offered Jobs"), "Offered Jobs").pack(fill="both", expand=True)


class DatabaseView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="white", width=750, height=370)

        self.jobs = TabView(self)
        self.jobs.place(x=13, y=5)

        ctk.CTkButton(self, text="Refresh", command=self.refresh_view, width=80, height=30).place(x=10, y=10)

    def refresh_view(self):
        self.jobs.refresh_tabs()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_id = sys.argv[1]
        print(f"User ID received: {user_id}")
    else:
        user_id=3
        print("No user ID passed.")
    App = Empl(user_id)
    App.mainloop()

import customtkinter as ctk  
from PIL import Image, ImageTk  
from tkinter import messagebox
import os
import sys
import subprocess
from database import retrieve_employers2,delete_employer_account,retrieve_application,retrieve_employed

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class Empl(ctk.CTk):  
    def __init__(self,user_id):  
        super().__init__()  

        self.title("Career Castle")  
        self.geometry('950x550')  
        self.iconbitmap(r"C:\Users\Shema\Desktop\version1.0\code\images\castleicon.ico") 
        self.resizable(False, False) 
        
        self.employer_id = user_id 
        
        # Sidebar Frame
        self.side_bar = sideframe(self,user_id)
        self.side_bar.pack(side="left", fill='y')

        # Advertisement Frame
        self.advertframe = advert_frame(self)
        self.advertframe.place(relx=0.212, rely=0.0)

        # Database View
        self.databaseview = databaseview(self)
        self.databaseview.place(relx=0.212, rely=0.328)

class sideframe(ctk.CTkFrame):  
    def __init__(self, parent, user_id):  
        super().__init__(parent)  

        self.configure(fg_color="#72787d", width=200)  
        self._corner_radius = 0  
        self.entries = []  # Store entries for later access  
        self.companyid = user_id  # Company ID for loading the image  

        img_path = fr"C:\Users\Shema\Desktop\version1.0\code\images\a{self.companyid}.jpg"  
        if os.path.exists(img_path):  
            self.image = Image.open(img_path).resize((200, 200), Image.Resampling.LANCZOS)  
        else:  
            messagebox.showinfo("Error", "Image path not found")  
            self.image = None  

        if self.image:  
            self.ad_image = ctk.CTkImage(light_image=self.image, dark_image=self.image, size=(100, 100))  
            self.ad_label = ctk.CTkLabel(self, image=self.ad_image, text='')  
            self.ad_label.place(relx=0.1, rely=0.03)  

        self.company_headings = ["NAME", "PASSWORD", "EMAIL"]   
        data = retrieve_employers2(self.companyid)  
        self.values = []  

        if data:  # Ensure that data is not None  
            # Use a list slicing or direct unpacking for cleaner access  
            self.values = list(data)[1:] 
        for i, label in enumerate(self.company_headings):  
            name_label = ctk.CTkLabel(self, text=label, width=50, height=20, font=("Verdana", 16, "bold"), text_color="black")  
            name_label.place(relx=0, rely=0.36 + i * 0.1)  

            # Corrected instantiation of CTkEntry  
            entry = ctk.CTkEntry(self, width=120, height=30, font=("Arial", 14))  
            entry.place(relx=0, rely=0.40 + i * 0.1)  
            entry.insert(0, f"{self.values[i]}")  # Insert the value here  
            entry.configure(state="readonly")  
            self.entries.append(entry)

        # Buttons
        self.modify = ctk.CTkButton(self, text="Delete Account", font=("Verdana", 12, "bold"), command=lambda: self.delete_account(user_id))
        self.modify.place(relx=0.2, rely=0.8)

        

        self.logout = ctk.CTkButton(self, text="Log Out", font=("Verdana", 12, "bold"), command=self.logout)
        self.logout.place(relx=0.15, rely=0.9)
        
    def logout(self):
        # Function to log out and open the employer program
        subprocess.Popen(['py', 'login.py'])    
    
    def delete_account(self,user_id):
        delete_employer_account(user_id)
        subprocess.Popen(['py', 'login.py'])    



class advert_frame(ctk.CTkFrame):  
    def __init__(self, parent):  
        super().__init__(parent)  

        self.configure(fg_color="white", width=750, height=180)  
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
                img_path = fr"C:\Users\Shema\Desktop\version1.0\code\images\a{i}.{ext}"  
                if os.path.exists(img_path):  
                    image = Image.open(img_path).resize((400, 300), Image.Resampling.LANCZOS).convert("RGBA")  
                    images.append(image)  
                    break
        return images  

    def display_advertisement(self, index):  
        if 0 <= index < len(self.images):  
            self.ad_image = ctk.CTkImage(light_image=self.images[index], dark_image=self.images[index], size=(400, 300))  
            self.ad_label = ctk.CTkLabel(self, image=self.ad_image, text='')  
            self.ad_label.place(relx=0.5, rely=0.5, anchor='center')  

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

        label = ctk.CTkLabel(self, text="", font=("Verdana", 16, "bold"))  
        label.pack(pady=10)  

        if self.frame_name == "Submitted Applications":  
            self.content1()  # Call the method using self  
        else:  
            self.content2()  # Call the method using self  

    def content1(self):  
        self.titles = ["employee_name", "education_level", "experience", "employer_name", "job_title", "job_nature", "state"]  

        # Create title labels and pack them  
        title_frame = ctk.CTkFrame(self)  # Create a frame for titles  
        title_frame.pack(pady=10)  # Add some padding at the top  

        for t in self.titles:  
            label = ctk.CTkLabel(title_frame, text=t, font=("Verdana", 10, "bold"))  
            label.pack(side="left", padx=10)  # Pack title labels horizontally with padding  

        # Create a frame for the content rows  
        content_frame = ctk.CTkFrame(self)  # Create a frame for content  
        content_frame.pack(pady=10)  # Add some padding  

        # Retrieve application rows  
        rows = retrieve_application()   

        # Create content labels and pack them  
        for row in rows:  
            row_frame = ctk.CTkFrame(content_frame)  # Create a frame for each row  
            row_frame.pack(pady=5)  # Add vertical spacing between rows  

            for value in row:  
                label = ctk.CTkLabel(row_frame, text=f"{value}", font=("Verdana", 10))  
                label.pack(side="left", padx=10)  # Pack value labels horizontally with padding

    def content2(self):  
        self.titles = ["employee_name","job_title","job_nature"]  

        # Create title labels and pack them  
        title_frame = ctk.CTkFrame(self)  # Create a frame for titles  
        title_frame.pack(pady=10)  # Add some padding at the top  

        for t in self.titles:  
            label = ctk.CTkLabel(title_frame, text=t, font=("Verdana", 10, "bold"))  
            label.pack(side="left", padx=10)  # Pack title labels horizontally with padding  

        # Create a frame for the content rows  
        content_frame = ctk.CTkFrame(self)  # Create a frame for content  
        content_frame.pack(pady=10)  # Add some padding  

        # Retrieve application rows  
        rows = retrieve_employed()

        # Create content labels and pack them  
        for row in rows:  
            row_frame = ctk.CTkFrame(content_frame)  # Create a frame for each row  
            row_frame.pack(pady=5)  # Add vertical spacing between rows  

            for value in row:  
                label = ctk.CTkLabel(row_frame, text=f"{value}", font=("Verdana", 10))  
                label.pack(side="left", padx=10)  # Pack value labels horizontally with padding 
            pass
    
    


class tabview(ctk.CTkTabview):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="black", width=720, height=360)
        self.add("Submitted Applications")
        self.add("Employed")
        self.tab1 = ScrollableFrame(self.tab("Submitted Applications"), "Submitted Applications")
        self.tab1.pack(fill="both", expand=True)
        self.tab2 = ScrollableFrame(self.tab("Employed"), "Employed")
        self.tab2.pack(fill="both", expand=True)


class databaseview(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="white", width=750, height=370)
        self.jobs = tabview(self)
        self.jobs.place(x=13, y=5)
        self.refresh_button = ctk.CTkButton(self, text="Refresh", width=60, height=30)
        self.refresh_button.place(relx=0, rely=0)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_id = sys.argv[1]
        print(f"User ID received: {user_id}")
    else:
        user_id=2
        print("No user ID passed.")
    
    window  = Empl(user_id)

    window.mainloop()

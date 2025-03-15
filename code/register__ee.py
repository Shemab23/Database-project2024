import customtkinter as ctk 
from database import insert_employee

class App(ctk.CTk):  
    def __init__(self):  
        super().__init__()  

        self.title("User Registration")  
        self.geometry("400x300")
        self.resizable(0,0) 
        self.configure(fg_color="light blue") 
        
        # Label names  
        labels = ["NAME", "PASSWORD", "CONFIRM PASSWORD", "EMAIL"]  
        self.entries = []  

        # Create labels and entry fields  
        for i, label in enumerate(labels):  
            # Create and place the label  
            name_label = ctk.CTkLabel(self, text=label, width=50, height=20,  
                                       font=("Verdana", 16, "bold"), text_color="black")  
            name_label.place(x=4.5, y=25 + (i * 30))  # Adjust vertical positioning  

            if label!= "PASSWORD" and label!= "CONFIRM PASSWORD":
                entry = ctk.CTkEntry(self, width=200)  # Adjust width as needed  
                entry.place(x=200, y=25 + (i * 30))  
                self.entries.append(entry)  # Store the entries for later access  
            else:
                entry = ctk.CTkEntry(self, width=200,show='*')  # Adjust width as needed  
                entry.place(x=200, y=25 + (i * 30))  
                self.entries.append(entry)  # Store the entries for later access  
        # Add a submit button  
        submit_button = ctk.CTkButton(self, text="Submit", command=self.submit)  
        submit_button.place(x=150, y=12 + (len(labels) * 30) + 20)  # Position below the entries  
        

    def submit(self):  
        self.value=[]
        for i in range (0,4):
            if i!=2:
                self.value.append(self.entries[i].get().strip().upper())
            else:
                pass
        var1=self.value[0]
        var2=self.value[1]
        var3=self.value[2]
        insert_employee(var1,var2,var3)
        
         
        print("Collected Values:", self.value)
        return self.value 
   

if __name__ == "__main__":  
    app = App()  
    app.mainloop()
    

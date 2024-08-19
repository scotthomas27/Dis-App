import customtkinter as ctk
import os  # Import the os module

ctk.set_appearance_mode("dark")  # Adjust appearance mode as needed
ctk.set_default_color_theme("dark-blue")  # Adjust color theme as needed

class TextApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Disappearing Text App")
        self.window.geometry('1350x750')
        self.window.configure(bg="#333333")  # Darker shade for reduced brightness
        
        # Adjust label colors for better visibility on darker backgrounds
        self.instructions_label = ctk.CTkLabel(self.window, text="Start typing to start the timer. If you stop for 10 seconds, the text will disappear.", text_color='white',
                                               anchor='center', justify='center', font=("Arial", 15))
        self.instructions_label.place(relx=0.05, rely=0.05)
        
        # Adjusted textbox size and placement for better fit and visibility
        self.textbox = ctk.CTkTextbox(self.window, width=1200, height=700, font=("Arial", 18))  # Adjusted size for better fit
        self.textbox.place(relx=0.05, rely=0.09)  # Adjusted placement for centered alignment
        
        self.textbox.focus()
        self.textbox.bind("<Key>", self.reset_timer)
        self.timer = None
        self.remaining_time = 10

    def reset_timer(self, event):
        self.text = self.textbox.get("0.0", "end")
        if self.timer:
            self.window.after_cancel(self.timer)
        self.timer = self.window.after(1000, self.update_timer)
        self.remaining_time = 10
        self.update_color()
    def update_timer(self):
        self.remaining_time -= 1
        if self.remaining_time > 0:
            self.timer = self.window.after(1000, self.update_timer)
        else:
            self.save_text()
            self.clear_text()
        self.update_color()

    def clear_text(self):
        self.textbox.delete("0.0", "end")

    def update_color(self):
        if self.remaining_time >= 7:
            self.textbox.configure(text_color="white")
        elif self.remaining_time >= 4:
            self.textbox.configure(text_color="orange")
        else:
            self.textbox.configure(text_color="red")

    def save_text(self):
        user_text = self.textbox.get("0.0", "end")
        if user_text == "":
            return
        try:
            with open('doc.txt', 'r') as f:
                content = f.read()
        except FileNotFoundError:
            with open('doc.txt', 'w') as f:
                f.write(user_text)
                return
        else:
            if content == "":
                text_to_write = user_text
            else:
                text_to_write = f'\n{user_text}'
            with open('doc.txt', 'a') as f:
                f.write(text_to_write)

    def run(self):
        self.window.mainloop()


app = TextApp()
app.run()

import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class TextApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Disappearing Text App")
        self.window.geometry('1350x750')
        self.window.configure(bg="#333333")
        
        # Corrected placement of the label for the last saved sentence
        self.last_sentence_label = ctk.CTkLabel(self.window, text="", text_color=('white', 'white'), font=("Arial", 18), wraplength=1180)
        self.last_sentence_label.place(relx=0.05, rely=0.025)  # Simplified placement
        
        # Input field for writing
        self.textbox = ctk.CTkTextbox(self.window, width=1200, height=500, font=("Arial", 18))
        self.textbox.place(relx=0.05, rely=0.085)  # Adjusted position below the label
        
        self.textbox.focus()
        self.textbox.bind("<Key>", self.reset_timer)
        self.textbox.bind("<Return>", self.handle_return_key)  # Bind the Return key event
        self.timer = None
        self.remaining_time = 10

        # Ensure the last saved sentence is displayed on launch
        self.update_last_sentence_display()

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
        if user_text == "" or user_text.strip() == "\n":
            return  # Skip saving if the text is empty or just a newline
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
                
        # Update the last sentence label after saving
        self.update_last_sentence_display()

    def update_last_sentence_display(self):
        try:
            with open('doc.txt', 'r') as f:
                lines = f.readlines()
                last_sentence = lines[-1].strip() if lines else ""
                self.last_sentence_label.configure(text=last_sentence)
        except Exception as e:
            print(f"Error reading last sentence: {e}")

    def handle_return_key(self, event):
        # Handle the Return key press here
        self.save_text()
        self.clear_text()
        self.update_last_sentence_display()

    def run(self):
        self.window.mainloop()

app = TextApp()
app.run()

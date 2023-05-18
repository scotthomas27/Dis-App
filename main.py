import customtkinter as ctk

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("dark-blue")


class TextApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Disappearing Text App")
        self.window.geometry('810x600')
        self.label = ctk.CTkLabel(self.window, text="Start typing to start the timer.\nIf you stop for 10 seconds, the text will disappear.", text_color='gray80',
                                  anchor='center', justify='center', font=("Arial", 25))
        self.label.place(relx=0.16, rely=0.02)
        self.label = ctk.CTkLabel(self.window, text="The text will be Green when you have 10 seconds left, Blue when you\nhave 6 seconds left and Red when there are only 3 seconds remaining.", text_color='gray80',
                                  anchor='center', justify="left", font=("Arial", 25))
        self.label.place(relx=0.01, rely=0.2)
        self.label = ctk.CTkLabel(self.window, text="Good Luck!", text_color='gray80',
                                  anchor='center', font=("Arial", 25))
        self.label.place(relx=0.4, rely=0.4)
        self.textbox = ctk.CTkTextbox(self.window, width=500, height=200, font=("Arial", 25))
        self.textbox.place(relx=0.18, rely=0.5)
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
            self.textbox.configure(text_color="green")
        elif self.remaining_time >= 4:
            self.textbox.configure(text_color="blue")
        else:
            self.textbox.configure(text_color="red")

    def save_text(self):
        user_text = self.textbox.get("0.0", "end")
        if user_text == "":
            return
        try:
            f = open('doc.txt', 'r')
        except FileNotFoundError:
            f = open('doc.txt', 'w')
            f.write(user_text)
            return
        else:
            content = f.read()
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
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class TextApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Disappearing Text App")
        self.window.geometry('1350x750')  # Initial geometry for reference
        self.window.configure(bg="#333333")

        # Labels for word counts
        self.session_word_count_label = ctk.CTkLabel(
            self.window, text="Session Words: 0", text_color=("white", "white"), font=("Arial", 18)
        )
        self.session_word_count_label.place(relx=0.05, rely=0.99, anchor="sw")  # Position below the textbox, anchor to bottom left

        self.saved_word_count_label = ctk.CTkLabel(
            self.window, text="Saved Words: 0", text_color=("white", "white"), font=("Arial", 18)
        )
        self.saved_word_count_label.place(relx=0.95, rely=0.99, anchor="se")  # Position below the textbox, anchor to bottom right

        # Corrected placement of the label for the last saved sentence
        self.last_sentence_label = ctk.CTkLabel(
            self.window, text="", text_color=("white", "white"), font=("Arial", 18), wraplength=1180
        )
        self.last_sentence_label.place(relx=0.05, rely=0.025)  # Simplified placement

        # Input field for writing, using relative placement and size calculations
        self.textbox_width = 1200  # Initial width for reference
        self.textbox_height = 500  # Initial height for reference
        self.textbox = ctk.CTkTextbox(
            self.window, width=self.textbox_width, height=self.textbox_height, font=("Arial", 18)
        )
        self.textbox.place(relx=0.05, rely=0.085, relwidth=0.85, relheight=0.65)  # Use relative placement and size

        self.textbox.focus()
        self.textbox.bind("<Key>", self.reset_timer)
        self.textbox.bind("<Return>", self.handle_return_key)  # Bind the Return key event
        self.timer = None
        self.remaining_time = 10

        # Track word counts
        self.initial_word_count = self.get_initial_word_count()
        self.session_word_count = self.initial_word_count

    def get_initial_word_count(self):
        try:
            with open('doc.txt', 'r') as f:
                text = f.read()
                words = text.split()
                return len(words)
        except FileNotFoundError:
            return 0  # If the file doesn't exist, assume initial word count is 0

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
        self.update_session_word_count()  # Update session word count after each save

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

        # Update the last saved sentence label and word counts after saving
        self.update_last_sentence_display()
        self.update_saved_word_count()

    def update_last_sentence_display(self):
        try:
            with open('doc.txt', 'r') as f:
                lines = f.readlines()
                last_sentence = lines[-1].strip() if lines else ""
                self.last_sentence_label.configure(text=last_sentence)
        except Exception as e:
            print(f"Error reading last sentence: {e}")

    def update_session_word_count(self):
        # Get the current total word count from the saved file
        total_word_count = self.get_total_word_count()
        self.session_word_count = total_word_count - self.initial_word_count
        self.session_word_count_label.configure(text=f"Session Words: {self.session_word_count}")

    def get_total_word_count(self):
        try:
            with open('doc.txt', 'r') as f:
                text = f.read()
                return len(text.split())  # Count total words in the saved file
        except FileNotFoundError:
            return 0  # If the file doesn't exist, assume total word count is 0

    def update_saved_word_count(self):
        try:
            with open('doc.txt', 'r') as f:
                text = f.read()
                words = text.split()
                self.saved_word_count = len(words)
                self.saved_word_count_label.configure(text=f"Saved Words: {self.saved_word_count}")
        except FileNotFoundError:
            pass  # File doesn't exist yet, so saved word count is 0

    def handle_return_key(self, event):
        # Handle the Return key press here
        self.save_text()
        self.clear_text()
        self.update_last_sentence_display()

    def run(self):
        self.window.mainloop()

app = TextApp()
app.run()

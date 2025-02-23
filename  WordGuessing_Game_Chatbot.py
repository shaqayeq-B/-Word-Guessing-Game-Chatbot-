import speech_recognition as sr
import random
import tkinter as tk
from tkinter import messagebox

class WordGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Guessing Game")
        
        # تنظیمات اولیه
        self.categories = {
            "Fruits": ["apple", "banana", "orange", "grape", "mango"],
            "Cars": ["audi", "bmw", "ford", "honda", "jeep"],
            "Colors": ["red", "blue", "green", "pink", "cyan"]
        }
        
        self.score = 0
        self.attempts = 3
        self.current_word = ""
        self.current_category = ""
        
        # ایجاد رابط کاربری
        self.create_widgets()
        self.start_new_game()
    
    def create_widgets(self):
        # ایجاد عناصر گرافیکی
        self.score_label = tk.Label(self.root, text=f"Score: {self.score}")
        self.score_label.pack()
        
        self.attempts_label = tk.Label(self.root, text=f"Attempts left: {self.attempts}")
        self.attempts_label.pack()
        
        self.category_label = tk.Label(self.root, text="Select Category:")
        self.category_label.pack()
        
        self.category_frame = tk.Frame(self.root)
        self.category_frame.pack()
        
        self.info_label = tk.Label(self.root, text="")
        self.info_label.pack()
        
        self.listen_btn = tk.Button(self.root, text="Start Listening", command=self.start_listening)
        self.listen_btn.pack(pady=10)
        
        self.restart_btn = tk.Button(self.root, text="New Game", command=self.start_new_game)
        self.restart_btn.pack()
    
    def start_new_game(self):
        # شروع بازی جدید
        self.attempts = 3
        self.current_word = ""
        self.current_category = ""
        self.update_display()
        self.create_category_buttons()
    
    def create_category_buttons(self):
        # ایجاد دکمه‌های دسته‌بندی
        for widget in self.category_frame.winfo_children():
            widget.destroy()
            
        for category in self.categories:
            btn = tk.Button(self.category_frame, text=category, 
                          command=lambda c=category: self.select_category(c))
            btn.pack(side=tk.LEFT, padx=5)
    
    def select_category(self, category):
        # انتخاب دسته‌بندی توسط کاربر
        self.current_category = category
        self.current_word = random.choice(self.categories[category])
        self.info_label.config(text=f"Guess a {len(self.current_word)}-letter word from {category}")
        self.create_category_buttons()
    
    def update_display(self):
        # به روزرسانی وضعیت بازی
        self.score_label.config(text=f"Score: {self.score}")
        self.attempts_label.config(text=f"Attempts left: {self.attempts}")
    
    def recognize_speech(self):
        # تشخیص گفتار
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
        
        try:
            return r.recognize_google(audio, language="en-US").lower()
        except:
            return None
    
    def start_listening(self):
        # شروع فرآیند تشخیص گفتار
        if not self.current_category:
            messagebox.showwarning("Warning", "Please select a category first!")
            return
            
        guess = self.recognize_speech()
        
        if guess:
            self.check_guess(guess)
        else:
            messagebox.showerror("Error", "Could not understand audio")
    
    def check_guess(self, guess):
        # بررسی حدس کاربر
        if guess == self.current_word:
            self.score += 10
            messagebox.showinfo("Correct!", f"Well done! +10 points\nCorrect word: {self.current_word}")
            self.start_new_game()
        else:
            self.attempts -= 1
            if self.attempts > 0:
                messagebox.showwarning("Wrong", f"Try again! Attempts left: {self.attempts}")
                self.update_display()
            else:
                messagebox.showerror("Game Over", f"Out of attempts! Correct word was: {self.current_word}")
                self.start_new_game()

if __name__ == "__main__":
    root = tk.Tk()
    game = WordGame(root)
    root.mainloop()
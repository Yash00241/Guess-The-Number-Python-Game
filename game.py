import random
import json
import os
import tkinter as tk
from tkinter import messagebox

class GuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate Number Guessing Game")
        self.save_path = os.path.join(os.path.expanduser('~/Documents'), 'savegame.json')
        self.create_start_menu()

    def create_start_menu(self):
        self.menu_frame = tk.Frame(self.root, bg="#ffcccb")
        self.menu_frame.pack(fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(self.menu_frame, bg="#ffcccb", width=600, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.title_text = self.canvas.create_text(300, 200, text="Ultimate Number Guessing Game", font=("Helvetica", 36), fill="#ff6347")
        self.start_button = tk.Button(self.menu_frame, text="Start Game", command=self.start_game, font=("Helvetica", 16), bg="#32cd32", fg="white", relief=tk.RAISED)
        self.start_button.pack(pady=10)
        self.quit_button = tk.Button(self.menu_frame, text="Quit", command=self.root.quit, font=("Helvetica", 16), bg="#ff4500", fg="white", relief=tk.RAISED)
        self.quit_button.pack(pady=10)
        self.animate_title()

    def animate_title(self, font_size=36):
        if font_size < 60:
            font_size += 1
            self.canvas.itemconfig(self.title_text, font=("Helvetica", font_size))
            self.root.after(50, self.animate_title, font_size)
        else:
            self.canvas.itemconfig(self.title_text, font=("Helvetica", 36))

    def start_game(self):
        self.menu_frame.destroy()
        self.game_frame = tk.Frame(self.root, bg="#e6e6fa")
        self.game_frame.pack(fill=tk.BOTH, expand=True)
        self.level, self.score = self.load_game()
        self.level_label = tk.Label(self.game_frame, text=f"Level: {self.level}", font=("Helvetica", 18), bg="#e6e6fa", fg="#4b0082")
        self.level_label.pack(pady=10)
        self.range_label = tk.Label(self.game_frame, font=("Helvetica", 18), bg="#e6e6fa", fg="#4b0082")
        self.range_label.pack(pady=10)
        self.attempts_label = tk.Label(self.game_frame, font=("Helvetica", 18), bg="#e6e6fa", fg="#4b0082")
        self.attempts_label.pack(pady=10)
        self.guess_entry = tk.Entry(self.game_frame, font=("Helvetica", 18), width=5, bg="#fffacd", fg="#00008b")
        self.guess_entry.pack(pady=10)
        self.check_button = tk.Button(self.game_frame, text="Submit Guess", command=self.check_guess, font=("Helvetica", 16), bg="#ff69b4", fg="white", relief=tk.RAISED)
        self.check_button.pack(pady=10)
        self.result_label = tk.Label(self.game_frame, font=("Helvetica", 18), bg="#e6e6fa", fg="#ff4500")
        self.result_label.pack(pady=10)
        self.save_button = tk.Button(self.game_frame, text="Save & Exit", command=self.save_and_exit, font=("Helvetica", 16), bg="#00ced1", fg="white", relief=tk.RAISED)
        self.save_button.pack(pady=10)
        self.start_game_logic()

    def start_game_logic(self):
        self.range_start = 1
        self.range_end = self.level * 10
        self.attempts_allowed = max(10 - (self.level // 20), 1)
        self.number_to_guess = random.randint(self.range_start, self.range_end)
        self.attempts_left = self.attempts_allowed
        self.level_label.config(text=f"Level: {self.level}")
        self.range_label.config(text=f"Guess the number between {self.range_start} and {self.range_end}.")
        self.attempts_label.config(text=f"Attempts left: {self.attempts_left}")
        self.result_label.config(text="")
        self.guess_entry.delete(0, tk.END)

    def save_game(self):
        try:
            with open(self.save_path, 'w') as save_file:
                json.dump({'level': self.level, 'score': self.score}, save_file)
            messagebox.showinfo("Save Game", "Game saved successfully!")
        except IOError:
            messagebox.showerror("Save Error", "An error occurred while saving the game.")

    def load_game(self):
        if os.path.exists(self.save_path):
            try:
                with open(self.save_path, 'r') as save_file:
                    data = json.load(save_file)
                messagebox.showinfo("Load Game", f"Loaded game from Level {data['level']} with Score {data['score']}.")
                return data['level'], data['score']
            except IOError:
                messagebox.showerror("Load Error", "An error occurred while loading the game.")
                return 1, 0
        else:
            messagebox.showinfo("Load Game", "No saved game found. Starting a new game.")
            return 1, 0

    def give_hint(self, guess, number_to_guess, range_end):
        difference = abs(number_to_guess - guess)
        if difference == 0:
            return "Correct!"
        elif difference <= range_end * 0.05:
            return "Extremely close!"
        elif difference <= range_end * 0.1:
            return "Very close!"
        elif difference <= range_end * 0.2:
            return "Close!"
        else:
            return "Far off."

    def direction_hint(self, guess, number_to_guess):
        if guess < number_to_guess:
            return "Try a higher number."
        else:
            return "Try a lower number."

    def check_guess(self):
        guess = self.guess_entry.get()
        if not guess.isdigit():
            messagebox.showwarning("Invalid Input", "Please enter a valid number.")
            return
        guess = int(guess)
        if guess < self.range_start or guess > self.range_end:
            messagebox.showwarning("Out of Range", f"Please enter a number between {self.range_start} and {self.range_end}.")
            return
        self.attempts_left -= 1
        self.attempts_label.config(text=f"Attempts left: {self.attempts_left}")
        if guess == self.number_to_guess:
            self.score += (self.attempts_left + 1) * 10
            messagebox.showinfo("Correct!", f"🎉 Correct! You've completed Level {self.level}. Your current score is: {self.score}.")
            self.level += 1
            if self.level > 500:
                messagebox.showinfo("Congratulations!", f"🏆 You've completed all 500 levels! Final Score: {self.score}")
                self.root.quit()
            else:
                self.start_game_logic()
        else:
            proximity_hint = self.give_hint(guess, self.number_to_guess, self.range_end)
            direction_hint_text = self.direction_hint(guess, self.number_to_guess)
            self.result_label.config(text=f"{proximity_hint} {direction_hint_text}")
        if self.attempts_left == 0:
            messagebox.showinfo("Game Over", f"😢 Out of attempts! The correct number was {self.number_to_guess}. Game Over!")
            retry = messagebox.askyesno("Retry", "Do you want to try again from Level 1?")
            if retry:
                self.level, self.score = 1, 0
                self.start_game_logic()
            else:
                self.root.quit()

    def save_and_exit(self):
        self.save_game()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = GuessingGame(root)
    root.mainloop()

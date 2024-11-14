import tkinter as tk
from tkinter import ttk
import random
import pygame
import math
import tkinter.messagebox as messagebox
from collections import Counter
pygame.init()
import sqlite3

# Pygame display setup
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Spinning Wheel")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)
wheel_radius = 250
center = (width // 2, height // 2)
num_segments = 6
angle_per_segment = 360 / num_segments
font = pygame.font.Font(None, 36)
genres = ["Fantasy", "Adventure", "Sci-Fi", "Horror", "Mystery", "Comedy"]
labels = genres
genre_colors = [PURPLE, ORANGE, GREEN, BLUE, YELLOW, PINK]
users_db = {}

class SpinYarnGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Spin a Yarn Game")
        self.root.geometry("800x600")
        self.root.config(bg="#f0f0f0")
        self.main_frame = tk.Frame(self.root, bg="white", bd=5, relief="groove")
        self.main_frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

        self.title_label = tk.Label(self.main_frame, text="Spin a Yarn Game", font=("Helvetica", 32, "bold"), fg="#4B0082", bg="white")
        self.title_label.pack(pady=30)

        self.play_button_friends = ttk.Button(self.main_frame, text="Play with Friends", style="TButton", command=self.ask_number_of_players)
        self.play_button_friends.pack(pady=20)

        self.players = []
        self.current_player_index = 0
        self.selected_genre = None
        self.stories = []
        self.votes = []

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Helvetica", 14), relief="flat", background="#1E3A8A", foreground="blue")
        self.style.map("TButton", background=[("active", "#1D3F87")])

    def show_signup_page(self):
        self.clear_frame()

        self.signup_label = tk.Label(self.main_frame, text="Sign Up", font=("Helvetica", 24), bg="white")
        self.signup_label.pack(pady=20)

        self.username_label = tk.Label(self.main_frame, text="Username:", font=("Helvetica", 14), bg="white")
        self.username_label.pack(pady=5)

        self.username_entry = ttk.Entry(self.main_frame, font=("Helvetica", 14))
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self.main_frame, text="Password:", font=("Helvetica", 14), bg="white")
        self.password_label.pack(pady=5)

        self.password_entry = ttk.Entry(self.main_frame, font=("Helvetica", 14), show="*")
        self.password_entry.pack(pady=5)

        self.confirm_password_label = tk.Label(self.main_frame, text="Confirm Password:", font=("Helvetica", 14), bg="white")
        self.confirm_password_label.pack(pady=5)

        self.confirm_password_entry = ttk.Entry(self.main_frame, font=("Helvetica", 14), show="*")
        self.confirm_password_entry.pack(pady=5)

        self.signup_button = ttk.Button(self.main_frame, text="Sign Up", command=self.handle_signup)
        self.signup_button.pack(pady=20)

        self.back_button = ttk.Button(self.main_frame, text="Back to Login", command=self.show_login_page)
        self.back_button.pack(pady=10)

    def handle_signup(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()

        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "Please fill out all fields.")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        if username in users_db:
            messagebox.showerror("Error", "Username already exists.")
            return

        users_db[username] = password
        messagebox.showinfo("Success", "Account created successfully!")
        self.show_login_page()

    def show_login_page(self):
        self.clear_frame()

        self.login_label = tk.Label(self.main_frame, text="Login", font=("Helvetica", 24), bg="white")
        self.login_label.pack(pady=20)

        self.username_label = tk.Label(self.main_frame, text="Username:", font=("Helvetica", 14), bg="white")
        self.username_label.pack(pady=5)

        self.username_entry = ttk.Entry(self.main_frame, font=("Helvetica", 14))
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self.main_frame, text="Password:", font=("Helvetica", 14), bg="white")
        self.password_label.pack(pady=5)

        self.password_entry = ttk.Entry(self.main_frame, font=("Helvetica", 14), show="*")
        self.password_entry.pack(pady=5)

        self.login_button = ttk.Button(self.main_frame, text="Login", command=self.handle_login)
        self.login_button.pack(pady=20)

        self.signup_button = ttk.Button(self.main_frame, text="Don't have an account? Sign Up", command=self.show_signup_page)
        self.signup_button.pack(pady=10)

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please fill out all fields.")
            return

        if username not in users_db or users_db[username] != password:
            messagebox.showerror("Error", "Invalid username or password.")
            return

        messagebox.showinfo("Success", "Login successful!")
        self.ask_number_of_players()

    def ask_number_of_players(self):
        self.clear_frame()

        self.number_label = tk.Label(self.main_frame, text="Enter number of players:", font=("Helvetica", 18), bg="white")
        self.number_label.pack(pady=20)

        self.number_entry = ttk.Entry(self.main_frame, font=("Helvetica", 14), width=5)
        self.number_entry.pack(pady=10)

        self.submit_number_button = ttk.Button(self.main_frame, text="Submit", command=self.get_player_names)
        self.submit_number_button.pack(pady=20)

    def get_player_names(self):
        try:
            num_players = int(self.number_entry.get())
            if num_players < 2:
                raise ValueError("At least 2 players are required.")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
            return

        self.clear_frame()
        self.players = []
        self.get_names(num_players)

    def get_names(self, num_players):
        self.name_label = tk.Label(self.main_frame, text=f"Enter names for {num_players} players:", font=("Helvetica", 18), bg="white")
        self.name_label.pack(pady=20)

        self.name_entries = []
        for i in range(num_players):
            entry = ttk.Entry(self.main_frame, font=("Helvetica", 14))
            entry.pack(pady=5)
            self.name_entries.append(entry)

        self.start_button = ttk.Button(self.main_frame, text="Start Game", command=self.start_game_from_entries)
        self.start_button.pack(pady=20)

    def start_game_from_entries(self):
        self.players = [entry.get().strip() for entry in self.name_entries]
        self.players = [name for name in self.players if name]  # Remove empty names

        if len(self.players) < 2:
            messagebox.showerror("Error", "Please enter at least two names.")
        else:
            self.start_game()

    def start_game(self):
        self.clear_frame()
        self.stories = []
        self.current_player_index = 0

        self.spin_button = ttk.Button(self.main_frame, text="Spin the Wheel", command=self.spin_wheel)
        self.spin_button.pack(pady=20)

    def spin_wheel(self):
        # Game logic to spin the wheel, determine genre, and prompt players for story submissions
        self.spin_wheel_animation()

    def spin_wheel_animation(self):
        rotation_angle = 0
        rotation_speed = 1
        rotating = True
        result_text = None

        clock = pygame.time.Clock()

        while rotating:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    rotating = False

            rotation_angle += rotation_speed
            rotation_speed *= 0.99  # Gradually slow down

            if rotation_speed < 0.05:
                rotating = False
                result_text = f"Stopped at: {labels[int((rotation_angle % 360) / angle_per_segment)]}"

            screen.fill(WHITE)
            self.draw_wheel(rotation_angle)

            if result_text:
                result_label = font.render(result_text, True, BLACK)
                screen.blit(result_label, (center[0] - result_label.get_width() // 2, height - 50))

            pygame.display.flip()
            clock.tick(60)

        self.selected_genre = labels[int((rotation_angle % 360) / angle_per_segment)]
        pygame.quit()  # Close pygame window after the spinning is done
        messagebox.showinfo("Spin Result", f"The selected genre is: {self.selected_genre}")
        self.ask_story_continuation()

    def draw_wheel(self, rotation_angle=0):
        for i in range(num_segments):
            start_angle = math.radians(i * angle_per_segment + rotation_angle)
            end_angle = math.radians((i + 1) * angle_per_segment + rotation_angle)
            pygame.draw.arc(screen, genre_colors[i], (center[0] - wheel_radius, center[1] - wheel_radius, 2 * wheel_radius, 2 * wheel_radius), start_angle, end_angle, wheel_radius)

            mid_angle = (start_angle + end_angle) / 2
            text_x = center[0] + (wheel_radius - 40) * math.cos(mid_angle)
            text_y = center[1] + (wheel_radius - 40) * math.sin(mid_angle)
            label = font.render(labels[i], True, BLACK)
            screen.blit(label, (text_x - label.get_width() // 2, text_y - label.get_height() // 2))

    def ask_story_continuation(self):
        self.clear_frame()

        current_player = self.players[self.current_player_index]
        prompt_label = tk.Label(self.main_frame,
                                text=f"{current_player}, tell a story based on the '{self.selected_genre}' genre:",
                                font=("Helvetica", 18), bg="white")
        prompt_label.pack(pady=20)

        self.continuation_entry = ttk.Entry(self.main_frame, font=("Helvetica", 14), width=50)
        self.continuation_entry.pack(pady=10)

        submit_button = ttk.Button(self.main_frame, text="Submit Story", command=self.collect_story)
        submit_button.pack(pady=10)

    def collect_story(self):
        player = self.players[self.current_player_index]
        story = self.continuation_entry.get().strip()

        if story:
            self.stories.append((player, story))
            self.continuation_entry.delete(0, tk.END)
            self.current_player_index += 1

            if self.current_player_index < len(self.players):
                self.ask_story_continuation()
            else:
                self.current_player_index = 0
                self.ask_for_voting()
        else:
            messagebox.showerror("Error", "Please enter a story.")

    def ask_for_voting(self):
        self.clear_frame()

        finished_label = tk.Label(self.main_frame, text="All players have submitted their stories! Now, it's time to vote.", font=("Helvetica", 18), bg="white")
        finished_label.pack(pady=20)

        vote_button = ttk.Button(self.main_frame, text="Start Voting", command=self.vote_window)
        vote_button.pack(pady=20)

    def vote_window(self):
        self.current_voter_index = 0
        self.votes = []
        self.ask_for_vote()

    def ask_for_vote(self):
        if self.current_voter_index < len(self.players):
            vote_prompt = tk.Label(self.main_frame, text=f"{self.players[self.current_voter_index]}, vote for your favorite story.", font=("Helvetica", 16), bg="white")
            vote_prompt.pack(pady=20)

            vote_options = [story[0] for story in self.stories]
            for option in vote_options:
                vote_button = ttk.Button(self.main_frame, text=option, command=lambda option=option: self.submit_vote(option))
                vote_button.pack(pady=5)
        else:
            self.calculate_votes()

    def submit_vote(self, vote):
        self.votes.append(vote)
        self.current_voter_index += 1
        self.ask_for_vote()

    def calculate_votes(self):
        vote_counts = Counter(self.votes)
        winner = vote_counts.most_common(1)[0][0]
        vote_count = vote_counts.most_common(1)[0][1]

        # Call display_winner to announce the winner
        self.display_winner(winner, vote_count)

    def display_winner(self, winner_name, vote_count):
        winner_window = tk.Toplevel(self.root)
        winner_window.title("Winner Announcement")
        winner_window.geometry("400x400")

        tk.Label(winner_window, text="🎉🎉 The Winner Is... 🎉🎉", font=("Helvetica", 24), fg="green").pack(pady=20)
        tk.Label(winner_window, text=winner_name, font=("Helvetica", 20), fg="blue").pack(pady=10)
        tk.Label(winner_window, text=f"With {vote_count} votes!", font=("Helvetica", 18)).pack(pady=10)

        close_button = ttk.Button(winner_window, text="Close", command=winner_window.destroy)
        close_button.pack(pady=20)

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

# Running the game
if __name__ == "__main__":
    root = tk.Tk()
    game = SpinYarnGame(root)
    game.show_login_page()  # Start with the login page
    root.mainloop()

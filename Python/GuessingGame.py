import random
import tkinter as tk
from tkinter import messagebox, ttk

# Word lists (same as your original)
easy_words = [
    "apple", "table", "chair", "house", "water", "music", "light", "happy", "green", "beach",
    "smile", "cloud", "tiger", "ocean", "dance", "fruit", "paper", "queen", "river", "sunny",
    "earth", "grape", "horse", "juice", "knife", "lemon", "mango", "night", "olive", "peach",
    "quiet", "radio", "snake", "tulip", "umbra", "vivid", "whale", "xenon", "yacht", "zebra",
    "angel", "baker", "candy", "daisy", "eagle", "flame", "ghost", "honey", "ivory", "jolly",
    "koala", "lucky", "magic", "noble", "opera", "piano", "quilt", "robin", "sugar", "tiger",
    "ultra", "vixen", "wheat", "xerox", "yummy", "zippy", "amber", "bloom", "crisp", "dizzy",
    "elbow", "froze", "globe", "hippo", "inbox", "jumpy", "karma", "lunar", "mirth", "nexus",
    "otter", "pixie", "quirk", "rumba", "scoop", "twist", "unzip", "vocal", "witty", "xylem",
    "youth", "zesty", "acorn", "bliss", "covey", "dwarf", "ember", "fable", "gauze", "haste"
]
medium_words = [
    "banana", "garden", "purple", "summer", "winter", "orange", "planet", "rocket", "silver", "turtle",
    "breeze", "camera", "dragon", "eleven", "floral", "guitar", "harbor", "island", "jacket", "kitten",
    "laptop", "mirror", "noodle", "oxygen", "pepper", "quasar", "rabbit", "sunset", "tomato", "unicorn",
    "velvet", "window", "yellow", "zephyr", "archer", "basket", "candle", "desert", "engine", "frozen",
    "glossy", "helmet", "igloos", "jungle", "kettle", "lizard", "marble", "needle", "orchid", "puzzle",
    "quartz", "ripple", "spirit", "trophy", "upward", "violet", "wizard", "xylose", "yogurt", "zigzag",
    "anchor", "bright", "cobalt", "dancer", "exotic", "fabric", "goblin", "humble", "insect", "jigsaw",
    "knight", "laughs", "mosaic", "nectar", "opaque", "placid", "quirky", "rustic", "shadow", "temple",
    "utopia", "vortex", "waffle", "xenial", "yearly", "zenith", "almond", "blazer", "crimson", "dapper",
    "echoes", "falcon", "glisten", "hazeln", "indigo", "jovial", "kaleid", "lucent", "meadow", "nimbus",
    "onyxes", "photon", "quench", "russet", "sphinx", "tundra", "urchin", "vermin", "willow", "xyloid"
]
hard_words = [
    "airport", "bicycle", "crystal", "diamond", "evening", "freedom", "giraffe", "harmony", "instant", "jasmine",
    "kitchen", "library", "mystery", "natural", "octopus", "penguin", "quality", "rainbow", "sapphire", "traffic",
    "umbrella", "victory", "whisper", "xylophone", "yoghurt", "zeppelin", "aquatic", "brittle", "champion", "dolphin",
    "eclipse", "flamingo", "gallery", "horizon", "inquiry", "jubilee", "kingdom", "lobster", "monarch", "neutral",
    "opulent", "paradox", "quibble", "raccoon", "sincere", "tornado", "unusual", "vibrant", "windsor", "xenopus",
    "yawning", "zipline", "ancient", "beneath", "capture", "dynamic", "eternal", "fortune", "glacier", "habitat",
    "inertia", "jocular", "krypton", "languid", "magnify", "narrate", "oblique", "pancake", "quantum", "radiant",
    "scorpio", "tranquil", "upgrade", "vanilla", "warrant", "xerosis", "yielder", "zodiacs", "alchemy", "biscuit",
    "crimson", "dervish", "emerald", "finesse", "gazelle", "hyacinth", "ironies", "jasmine", "kaleido", "luminous",
    "majesty", "nostril", "obelisk", "pajamas", "quintet", "reptile", "saffron", "triumph", "unicorn", "vulture"
]

class WordGuessingGame:
    def __init__(self):
        # Create the main window with gradient background
        self.root = tk.Tk()
        self.root.title("🌈 Magical Word Guessing Game 🌈")
        self.root.geometry("650x500")
        self.root.configure(bg="#1a1a2e")  # Dark purple background
        self.root.resizable(False, False)
        
        # Color palette
        self.colors = {
            'bg_primary': '#1a1a2e',      # Dark navy
            'bg_secondary': '#16213e',     # Darker navy  
            'accent_1': '#e94560',         # Bright pink/red
            'accent_2': '#f39c12',         # Orange
            'accent_3': '#00d4aa',         # Teal
            'accent_4': '#9b59b6',         # Purple
            'text_light': '#ecf0f1',       # Light text
            'text_dark': '#2c3e50',        # Dark text
            'success': '#2ecc71',          # Green
            'warning': '#e67e22',          # Orange
            'error': '#e74c3c'             # Red
        }
        
        # Initialize game variables
        self.secret_word = ""
        self.attempts = 0
        self.game_started = False
        
        # Setup gradient background
        self.create_gradient_bg()
        
        # Create and setup all GUI elements
        self.setup_gui()
    
    def create_gradient_bg(self):
        """Create a gradient background effect"""
        # Create a canvas for gradient
        self.canvas = tk.Canvas(self.root, width=650, height=500, highlightthickness=0)
        self.canvas.place(x=0, y=0)
        
        # Create gradient effect
        for i in range(500):
            color_ratio = i / 500
            # Interpolate between two colors
            r1, g1, b1 = 26, 26, 46   # #1a1a2e
            r2, g2, b2 = 22, 33, 62   # #16213e
            
            r = int(r1 + (r2 - r1) * color_ratio)
            g = int(g1 + (g2 - g1) * color_ratio)
            b = int(b1 + (b2 - b1) * color_ratio)
            
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.create_line(0, i, 650, i, fill=color, width=1)
    
    def setup_gui(self):
        """Create all the GUI elements with enhanced styling"""
        
        # Main container frame with rounded corners effect
        self.main_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", width=600, height=450)
        
        # Animated title with multiple colors
        self.title_frame = tk.Frame(self.main_frame, bg=self.colors['bg_primary'])
        self.title_frame.pack(pady=20)
        
        title_text = "🎯 WORD MASTER 🎯"
        self.title_label = tk.Label(
            self.title_frame,
            text=title_text,
            font=("Arial Black", 24, "bold"),
            bg=self.colors['bg_primary'],
            fg=self.colors['accent_1']
        )
        self.title_label.pack()
        
        # Subtitle with glow effect
        subtitle = tk.Label(
            self.title_frame,
            text="✨ Guess the Secret Word ✨",
            font=("Arial", 12, "italic"),
            bg=self.colors['bg_primary'],
            fg=self.colors['accent_3']
        )
        subtitle.pack(pady=5)
        
        # Difficulty selection with colorful design
        self.create_difficulty_section()
        
        # Start button with hover effect
        self.create_start_button()
        
        # Game area with enhanced styling
        self.create_game_area()
        
        # Initially hide game elements
        self.hide_game_elements()
    
    def create_difficulty_section(self):
        """Create colorful difficulty selection"""
        diff_container = tk.Frame(self.main_frame, bg=self.colors['bg_primary'])
        diff_container.pack(pady=15)
        
        # Difficulty label with gradient text effect
        diff_label = tk.Label(
            diff_container,
            text="🌟 Choose Your Challenge 🌟",
            font=("Arial", 14, "bold"),
            bg=self.colors['bg_primary'],
            fg=self.colors['text_light']
        )
        diff_label.pack(pady=10)
        
        # Colorful difficulty buttons
        self.difficulty_var = tk.StringVar(value="easy")
        buttons_frame = tk.Frame(diff_container, bg=self.colors['bg_primary'])
        buttons_frame.pack()
        
        difficulty_styles = [
            ("🟢 EASY", "easy", self.colors['success']),
            ("🟡 MEDIUM", "medium", self.colors['warning']),
            ("🔴 HARD", "hard", self.colors['error'])
        ]
        
        self.diff_buttons = []
        for text, value, color in difficulty_styles:
            btn = tk.Radiobutton(
                buttons_frame,
                text=text,
                variable=self.difficulty_var,
                value=value,
                font=("Arial", 11, "bold"),
                bg=self.colors['bg_primary'],
                fg=color,
                selectcolor=self.colors['bg_secondary'],
                activebackground=self.colors['bg_primary'],
                activeforeground=color,
                borderwidth=0,
                highlightthickness=0,
                command=self.on_difficulty_change
            )
            btn.pack(side=tk.LEFT, padx=15)
            self.diff_buttons.append(btn)
    
    def create_start_button(self):
        """Create animated start button"""
        self.start_button = tk.Button(
            self.main_frame,
            text="🚀 START ADVENTURE 🚀",
            command=self.start_game,
            font=("Arial", 14, "bold"),
            bg=self.colors['accent_1'],
            fg=self.colors['text_light'],
            relief="flat",
            borderwidth=0,
            padx=30,
            pady=10,
            cursor="hand2"
        )
        self.start_button.pack(pady=20)
        
        # Bind hover effects
        self.start_button.bind("<Enter>", self.on_start_hover)
        self.start_button.bind("<Leave>", self.on_start_leave)
    
    def create_game_area(self):
        """Create enhanced game area"""
        self.game_frame = tk.Frame(self.main_frame, bg=self.colors['bg_primary'])
        self.game_frame.pack(pady=20, fill=tk.BOTH, expand=True)
        
        # Game info panel
        info_panel = tk.Frame(self.game_frame, bg=self.colors['bg_secondary'], relief="groove", bd=2)
        info_panel.pack(pady=10, padx=20, fill=tk.X)
        
        self.word_length_label = tk.Label(
            info_panel,
            text="",
            font=("Arial", 12, "bold"),
            bg=self.colors['bg_secondary'],
            fg=self.colors['accent_3'],
            pady=8
        )
        self.word_length_label.pack()
        
        # Hint display with letter boxes
        self.hint_frame = tk.Frame(self.game_frame, bg=self.colors['bg_primary'])
        self.hint_frame.pack(pady=15)
        
        self.hint_letters = []  # Will store individual letter labels
        
        # Input section with enhanced styling
        input_section = tk.Frame(self.game_frame, bg=self.colors['bg_primary'])
        input_section.pack(pady=15)
        
        input_label = tk.Label(
            input_section,
            text="💭 Your Guess:",
            font=("Arial", 12, "bold"),
            bg=self.colors['bg_primary'],
            fg=self.colors['text_light']
        )
        input_label.pack()
        
        # Styled entry with border
        entry_frame = tk.Frame(input_section, bg=self.colors['accent_2'], bd=2, relief="solid")
        entry_frame.pack(pady=10)
        
        self.guess_entry = tk.Entry(
            entry_frame,
            font=("Arial", 16, "bold"),
            width=20,
            justify="center",
            bg=self.colors['text_light'],
            fg=self.colors['text_dark'],
            relief="flat",
            borderwidth=5
        )
        self.guess_entry.pack(padx=3, pady=3)
        
        # Colorful guess button
        self.guess_button = tk.Button(
            input_section,
            text="✨ GUESS ✨",
            command=self.make_guess,
            font=("Arial", 12, "bold"),
            bg=self.colors['accent_4'],
            fg=self.colors['text_light'],
            relief="flat",
            borderwidth=0,
            padx=25,
            pady=8,
            cursor="hand2"
        )
        self.guess_button.pack(pady=10)
        
        # Bind Enter key and button hover
        self.guess_entry.bind('<Return>', lambda event: self.make_guess())
        self.guess_button.bind("<Enter>", self.on_guess_hover)
        self.guess_button.bind("<Leave>", self.on_guess_leave)
        
        # Stats display
        stats_frame = tk.Frame(self.game_frame, bg=self.colors['bg_primary'])
        stats_frame.pack(pady=10)
        
        self.attempts_label = tk.Label(
            stats_frame,
            text="",
            font=("Arial", 11, "bold"),
            bg=self.colors['bg_primary'],
            fg=self.colors['accent_2']
        )
        self.attempts_label.pack()
    
    def create_hint_display(self):
        """Create individual letter boxes for hints"""
        # Clear existing hint letters
        for letter_label in self.hint_letters:
            letter_label.destroy()
        self.hint_letters.clear()
        
        # Create new letter boxes
        for i in range(len(self.secret_word)):
            letter_frame = tk.Frame(
                self.hint_frame,
                bg=self.colors['bg_secondary'],
                width=40,
                height=40,
                relief="raised",
                bd=2
            )
            letter_frame.pack(side=tk.LEFT, padx=5, pady=10)
            letter_frame.pack_propagate(False)
            
            letter_label = tk.Label(
                letter_frame,
                text="_",
                font=("Courier New", 18, "bold"),
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_light']
            )
            letter_label.pack(expand=True)
            self.hint_letters.append(letter_label)
    
    def on_difficulty_change(self):
        """Handle difficulty selection change with color feedback"""
        difficulty = self.difficulty_var.get()
        colors = {
            'easy': self.colors['success'],
            'medium': self.colors['warning'], 
            'hard': self.colors['error']
        }
        # Could add visual feedback here
    
    def on_start_hover(self, event):
        """Start button hover effect"""
        self.start_button.configure(bg=self.colors['accent_2'])
    
    def on_start_leave(self, event):
        """Start button leave effect"""
        self.start_button.configure(bg=self.colors['accent_1'])
    
    def on_guess_hover(self, event):
        """Guess button hover effect"""
        self.guess_button.configure(bg=self.colors['accent_1'])
    
    def on_guess_leave(self, event):
        """Guess button leave effect"""
        self.guess_button.configure(bg=self.colors['accent_4'])
    
    def start_game(self):
        """Start a new game with enhanced visual feedback"""
        difficulty = self.difficulty_var.get()
        
        # Choose word based on difficulty
        if difficulty == "easy":
            self.secret_word = random.choice(easy_words)
        elif difficulty == "medium":
            self.secret_word = random.choice(medium_words)
        elif difficulty == "hard":
            self.secret_word = random.choice(hard_words)
        
        # Reset game state
        self.attempts = 0
        self.game_started = True
        
        # Show game elements
        self.show_game_elements()
        
        # Create hint display
        self.create_hint_display()
        
        # Update displays with colors
        self.word_length_label.config(
            text=f"🎯 Word Length: {len(self.secret_word)} letters 🎯"
        )
        self.attempts_label.config(text="💫 Attempts: 0")
        
        # Clear and focus on entry
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus()
        
        # Update start button
        self.start_button.config(text="🔄 NEW GAME 🔄")
        
        # Add welcome message
        messagebox.showinfo(
            "🎉 Game Started!", 
            f"🌟 {difficulty.upper()} level selected!\n🎯 Guess the {len(self.secret_word)}-letter word!\n✨ Good luck!"
        )
    
    def make_guess(self):
        """Handle user's guess with enhanced visual feedback"""
        if not self.game_started:
            messagebox.showwarning("⚠️ Hold On!", "Please start a game first! 🎮")
            return
        
        guess = self.guess_entry.get().lower().strip()
        
        # Validate input
        if not guess:
            messagebox.showwarning("📝 Empty Guess", "Please enter a word! ✏️")
            return
        
        if not guess.isalpha():
            messagebox.showwarning("🔤 Letters Only", "Please enter only letters! 📝")
            return
        
        if len(guess) != len(self.secret_word):
            messagebox.showwarning(
                "📏 Wrong Length", 
                f"Please enter a {len(self.secret_word)}-letter word! 🎯"
            )
            return
        
        self.attempts += 1
        
        # Check if guess is correct
        if guess == self.secret_word:
            self.win_game()
            return
        
        # Update hint display with colors
        self.update_hint_display(guess)
        self.attempts_label.config(text=f"💫 Attempts: {self.attempts}")
        
        # Clear entry for next guess
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus()
        
        # Give encouraging feedback
        if self.attempts % 3 == 0:
            messagebox.showinfo("💪 Keep Going!", "You're doing great! Don't give up! 🌟")
    
    def update_hint_display(self, guess):
        """Update hint display with colorful letter boxes"""
        for i in range(len(self.secret_word)):
            letter_label = self.hint_letters[i]
            if i < len(guess) and guess[i] == self.secret_word[i]:
                # Correct letter in correct position - green
                letter_label.configure(
                    text=guess[i].upper(),
                    bg=self.colors['success'],
                    fg=self.colors['text_light']
                )
            else:
                # Wrong letter or position - keep default
                letter_label.configure(
                    text="_",
                    bg=self.colors['bg_secondary'],
                    fg=self.colors['text_light']
                )
    
    def win_game(self):
        """Handle winning with celebration effects"""
        # Create colorful win message
        if self.attempts == 1:
            title = "🏆 PERFECT! 🏆"
            message = f"🎯 INCREDIBLE! You guessed '{self.secret_word.upper()}' in just ONE try!\n🌟 You're a WORD MASTER! 🌟"
        elif self.attempts <= 3:
            title = "🎉 EXCELLENT! 🎉"
            message = f"🎯 Amazing! You found '{self.secret_word.upper()}' in {self.attempts} attempts!\n⭐ Fantastic word skills! ⭐"
        elif self.attempts <= 6:
            title = "🌟 GREAT JOB! 🌟"
            message = f"🎯 Well done! You discovered '{self.secret_word.upper()}' in {self.attempts} attempts!\n💪 Keep up the good work! 💪"
        else:
            title = "🎊 SUCCESS! 🎊"
            message = f"🎯 Congratulations! You found '{self.secret_word.upper()}' in {self.attempts} attempts!\n🎈 Persistence pays off! 🎈"
        
        # Update all hint letters to show the complete word
        for i, letter_label in enumerate(self.hint_letters):
            letter_label.configure(
                text=self.secret_word[i].upper(),
                bg=self.colors['success'],
                fg=self.colors['text_light']
            )
        
        # Show win dialog
        messagebox.showinfo(title, message)
        
        # Ask if player wants to play again
        play_again = messagebox.askyesno(
            "🎮 Play Again?", 
            "Ready for another word challenge? 🚀"
        )
        if play_again:
            self.start_game()
        else:
            self.hide_game_elements()
            self.game_started = False
            self.start_button.config(text="🚀 START ADVENTURE 🚀")
    
    def show_game_elements(self):
        """Show all game-related GUI elements"""
        self.word_length_label.pack(pady=5)
        self.hint_frame.pack(pady=15)
        self.guess_entry.pack(padx=3, pady=3)
        self.guess_button.pack(pady=10)
        self.attempts_label.pack()
    
    def hide_game_elements(self):
        """Hide all game-related GUI elements"""
        self.word_length_label.pack_forget()
        self.hint_frame.pack_forget()
        # Note: entry and button are in frames that handle visibility
        self.attempts_label.pack_forget()
        
        # Clear hint letters
        for letter_label in self.hint_letters:
            letter_label.destroy()
        self.hint_letters.clear()
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

# Create and run the game
if __name__ == "__main__":
    game = WordGuessingGame()
    game.run()
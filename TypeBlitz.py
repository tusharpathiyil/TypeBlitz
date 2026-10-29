
import tkinter as tk
import random
import time

# ==================== SETTINGS ====================

GAME_DURATION = 60

BG = "#0F172A"
PANEL = "#1E293B"
INPUT_BG = "#F8FAFC"
ACCENT = "#38BDF8"
GREEN = "#34D399"
YELLOW = "#FBBF24"
WHITE = "#F1F5F9"
MUTED = "#94A3B8"
DARK_TEXT = "#0F172A"

PASSAGES = [
    "Python is a popular programming language used to build "
    "applications and solve problems. Practice every day to "
    "improve your typing speed and accuracy.",

    "Technology helps people communicate, learn new skills, "
    "and solve real world problems. Programming teaches us "
    "how to think logically and create useful software.",

    "A computer program is a set of instructions that tells "
    "a computer what to do. Good programs are readable, "
    "reliable, and easy to maintain.",

    "Operating systems manage computer resources and allow "
    "applications to run. They handle memory, files, processes, "
    "and communication between software and hardware.",

    "Learning to code takes patience and consistent practice. "
    "Every error is an opportunity to understand a problem "
    "and develop a better solution."
]


# ==================== APPLICATION ====================

class TypeBlitz:

    def __init__(self, root):
        self.root = root
        self.root.title("TypeBlitz | Typing Speed Test")
        self.root.geometry("850x650")
        self.root.minsize(720, 580)
        self.root.configure(bg=BG)

        self.timer_job = None
        self.running = False

        self.show_home()

    # ==================== HELPERS ====================

    def clear_screen(self):
        if self.timer_job is not None:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

        for widget in self.root.winfo_children():
            widget.destroy()

    def label(self, parent, text, size=12, color=WHITE,
              bold=False, bg=None):
        return tk.Label(
            parent,
            text=text,
            font=("Segoe UI", size,
                  "bold" if bold else "normal"),
            fg=color,
            bg=bg or BG
        )

    def make_button(self, parent, text, command,
                    primary=True):
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 11, "bold"),
            bg=ACCENT if primary else PANEL,
            fg=DARK_TEXT if primary else WHITE,
            activebackground="#7DD3FC",
            activeforeground=DARK_TEXT,
            relief="flat",
            cursor="hand2",
            padx=22,
            pady=10,
            bd=0
        )

    # ==================== HOME SCREEN ====================

    def show_home(self):
        self.running = False
        self.clear_screen()

        self.label(
            self.root, "TYPEBLITZ", 36, ACCENT, True
        ).pack(pady=(100, 5))

        self.label(
            self.root,
            "YOUR SPEED. YOUR FOCUS. YOUR RECORD.",
            11, MUTED, True
        ).pack(pady=5)

        self.label(
            self.root,
            "A simple typing speed and accuracy challenge",
            14, WHITE
        ).pack(pady=(25, 8))

        card = tk.Frame(self.root, bg=PANEL, padx=30, pady=22)
        card.pack(pady=15)

        self.label(
            card, "60 SECONDS", 18, YELLOW, True, PANEL
        ).pack(pady=5)

        self.label(
            card,
            "Type the displayed passage as accurately as possible.",
            11, WHITE, bg=PANEL
        ).pack(pady=5)

        self.label(
            card,
            "Your speed and accuracy update as you type.",
            11, MUTED, bg=PANEL
        ).pack(pady=5)

        self.make_button(
            self.root, "START TYPING  →", self.start_game
        ).pack(pady=22)

        self.label(
            self.root, "Built with Python and Tkinter",
            10, MUTED
        ).pack(side="bottom", pady=20)

    # ==================== GAME SCREEN ====================

    def start_game(self):
        self.clear_screen()

        self.passage = random.choice(PASSAGES)
        self.start_time = time.time()
        self.time_left = GAME_DURATION
        self.running = True
        self.completed_early = False

        self.label(
            self.root, "TYPEBLITZ", 26, ACCENT, True
        ).pack(pady=(18, 2))

        self.label(
            self.root, "TYPE THE PASSAGE BELOW",
            11, MUTED, True
        ).pack(pady=(0, 12))

        # Statistics cards
        stats = tk.Frame(self.root, bg=BG)
        stats.pack(fill="x", padx=30, pady=5)

        self.timer_label = self.create_stat(
            stats, "TIME LEFT", "60s", YELLOW
        )

        self.wpm_label = self.create_stat(
            stats, "SPEED", "0 WPM", GREEN
        )

        self.accuracy_label = self.create_stat(
            stats, "ACCURACY", "100%", ACCENT
        )

        # Passage panel
        passage_panel = tk.Frame(
            self.root, bg=PANEL, padx=15, pady=12
        )
        passage_panel.pack(fill="x", padx=30, pady=12)

        self.label(
            passage_panel, "PASSAGE", 10, MUTED, True, PANEL
        ).pack(anchor="w", pady=(0, 8))

        self.passage_box = tk.Text(
            passage_panel,
            height=4,
            wrap="word",
            font=("Segoe UI", 13),
            bg=PANEL,
            fg=WHITE,
            relief="flat",
            padx=2,
            pady=2,
            cursor="arrow"
        )
        self.passage_box.pack(fill="x")
        self.passage_box.insert("1.0", self.passage)
        self.passage_box.config(
            state="disabled", takefocus=0
        )

        # Typing panel
        typing_panel = tk.Frame(
            self.root, bg=BG
        )
        typing_panel.pack(fill="x", padx=30, pady=4)

        self.label(
            typing_panel, "YOUR TEXT", 10, MUTED, True
        ).pack(anchor="w", pady=(0, 7))

        self.input_box = tk.Text(
            typing_panel,
            height=5,
            wrap="word",
            font=("Consolas", 12),
            bg=INPUT_BG,
            fg=DARK_TEXT,
            insertbackground=DARK_TEXT,
            relief="flat",
            padx=12,
            pady=10,
            undo=True
        )
        self.input_box.pack(fill="x")
        self.input_box.bind("<KeyRelease>", self.update_stats)
        self.input_box.bind("<KeyPress>", self.prevent_overtyping)
        self.input_box.focus_set()

        # Progress bar
        self.label(
            self.root, "PASSAGE PROGRESS", 9, MUTED, True
        ).pack(anchor="w", padx=30, pady=(12, 4))

        self.progress = tk.Canvas(
            self.root,
            height=10,
            bg=PANEL,
            highlightthickness=0
        )
        self.progress.pack(fill="x", padx=30)

        self.progress_bar = self.progress.create_rectangle(
            0, 0, 0, 10, fill=ACCENT, width=0
        )

        self.progress.bind(
            "<Configure>", self.update_progress
        )

        self.label(
            self.root,
            "Tip: Focus on accuracy first. Speed will follow!",
            10, MUTED
        ).pack(pady=12)

        self.timer_tick()

    def create_stat(self, parent, heading, value, color):
        card = tk.Frame(
            parent, bg=PANEL, padx=10, pady=8
        )
        card.pack(side="left", expand=True, fill="x", padx=5)

        self.label(
            card, heading, 9, MUTED, True, PANEL
        ).pack()

        value_label = self.label(
            card, value, 17, color, True, PANEL
        )
        value_label.pack(pady=(3, 0))

        return value_label

    def prevent_overtyping(self, event):
        if not self.running:
            return "break"

        # Keep the text length within the passage length.
        typed = self.input_box.get("1.0", "end-1c")

        if len(typed) >= len(self.passage):
            if event.keysym not in (
                "BackSpace", "Delete", "Left", "Right",
                "Up", "Down", "Home", "End", "Tab",
                "Shift_L", "Shift_R", "Control_L",
                "Control_R"
            ):
                if not (event.state & 0x4):
                    return "break"

    # ==================== LIVE STATISTICS ====================

    def update_stats(self, event=None):
        if not self.running:
            return

        typed = self.input_box.get("1.0", "end-1c")

        elapsed = max(time.time() - self.start_time, 1)
        words = len(typed.split())
        wpm = int(words * 60 / elapsed)

        correct_chars = sum(
            1 for i, char in enumerate(typed)
            if i < len(self.passage)
            and char == self.passage[i]
        )

        accuracy = (
            correct_chars / len(typed) * 100
            if typed else 100
        )

        self.wpm_label.config(text=f"{wpm} WPM")
        self.accuracy_label.config(
            text=f"{accuracy:.1f}%"
        )

        self.update_progress()

        if typed == self.passage:
            self.completed_early = True
            self.finish_game()

    def update_progress(self, event=None):
        if not hasattr(self, "progress"):
            return

        typed = self.input_box.get("1.0", "end-1c")
        fraction = min(len(typed) / len(self.passage), 1)

        width = self.progress.winfo_width()
        self.progress.coords(
            self.progress_bar,
            0, 0, width * fraction, 10
        )

    # ==================== TIMER ====================

    def timer_tick(self):
        if not self.running:
            return

        elapsed = int(time.time() - self.start_time)
        self.time_left = max(GAME_DURATION - elapsed, 0)

        self.timer_label.config(
            text=f"{self.time_left}s"
        )

        if self.time_left <= 10:
            self.timer_label.config(fg="#FB7185")

        if self.time_left == 0:
            self.finish_game()
        else:
            self.timer_job = self.root.after(
                200, self.timer_tick
            )

    # ==================== RESULTS ====================

    def finish_game(self):
        if not self.running:
            return

        self.running = False

        if self.timer_job is not None:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

        typed = self.input_box.get("1.0", "end-1c")
        elapsed = max(time.time() - self.start_time, 1)

        words = len(typed.split())
        wpm = int(words * 60 / elapsed)

        correct_chars = sum(
            1 for i, char in enumerate(typed)
            if i < len(self.passage)
            and char == self.passage[i]
        )

        accuracy = (
            correct_chars / len(typed) * 100
            if typed else 0
        )

        progress = (
            len(typed) / len(self.passage) * 100
        )

        self.clear_screen()

        title = (
            "PASSAGE COMPLETED!"
            if self.completed_early else "TIME'S UP!"
        )

        self.label(
            self.root, title, 27, ACCENT, True
        ).pack(pady=(55, 8))

        self.label(
            self.root, "YOUR RESULTS", 11, MUTED, True
        ).pack(pady=(0, 20))

        results = tk.Frame(self.root, bg=PANEL, padx=30, pady=20)
        results.pack(padx=40, fill="x")

        self.label(
            results, f"{wpm} WPM", 28, GREEN, True, PANEL
        ).pack(pady=7)

        self.label(
            results, "WORDS PER MINUTE", 10, MUTED, True, PANEL
        ).pack()

        self.label(
            results, f"Accuracy: {accuracy:.1f}%",
            16, ACCENT, True, PANEL
        ).pack(pady=(18, 5))

        self.label(
            results, f"Words typed: {words}",
            13, WHITE, bg=PANEL
        ).pack(pady=4)

        self.label(
            results, f"Passage completed: {progress:.1f}%",
            13, WHITE, bg=PANEL
        ).pack(pady=4)

        self.label(
            results, f"Time used: {min(elapsed, GAME_DURATION):.1f}s",
            12, MUTED, bg=PANEL
        ).pack(pady=(4, 8))

        buttons = tk.Frame(self.root, bg=BG)
        buttons.pack(pady=22)

        self.make_button(
            buttons, "PLAY AGAIN", self.start_game
        ).pack(side="left", padx=8)

        self.make_button(
            buttons, "HOME", self.show_home, primary=False
        ).pack(side="left", padx=8)


# ==================== RUN ====================

if __name__ == "__main__":
    root = tk.Tk()
    app = TypeBlitz(root)
    root.mainloop()

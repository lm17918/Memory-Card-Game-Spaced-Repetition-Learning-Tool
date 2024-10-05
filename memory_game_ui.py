import json
import os
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, scrolledtext, ttk

from memory_game import MemoryGame


class MemoryGameUI:
    def __init__(self, root):
        self.root = root
        self.current_card = None
        self.game = None

        self.root.title("Memory Card Game")
        self.root.configure(bg="#f0f0f0")

        main_frame = tk.Frame(root, bg="#ffffff", bd=2, relief=tk.GROOVE)
        main_frame.pack(padx=20, pady=20)

        self.reset_button = tk.Button(
            main_frame,
            text="Reset All Scores",
            command=self.reset_all_scores,
            font=("Helvetica", 14),
            bg="#FF5722",
            fg="white",
            relief=tk.RAISED,
        )
        self.reset_button.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.topic_label = tk.Label(
            main_frame, text="Choose a topic:", font=("Helvetica", 12), bg="#ffffff"
        )
        self.topic_label.grid(row=0, column=1, padx=(10, 10), pady=5)

        self.topic_combobox = ttk.Combobox(main_frame, state="readonly")
        self.topic_combobox.grid(row=1, column=1, columnspan=2, pady=5)
        self.topic_combobox.bind("<<ComboboxSelected>>", self.on_topic_selected)

        self.load_topics()

        self.question_label = tk.Label(
            main_frame,
            text="Press 'Show Question' to start!",
            font=("Helvetica", 16, "bold"),
            bg="#ffffff",
        )
        self.question_label.grid(row=3, column=0, columnspan=2, pady=(10, 20))

        self.answer_entry = tk.Entry(
            main_frame, width=50, font=("Helvetica", 14), bd=2, relief=tk.SUNKEN
        )
        self.answer_entry.grid(row=4, column=0, padx=10, pady=(0, 10))

        self.submit_button = tk.Button(
            main_frame,
            text="Submit Answer",
            command=self.submit_answer,
            font=("Helvetica", 14),
            bg="#4CAF50",
            fg="white",
            relief=tk.RAISED,
        )
        self.submit_button.grid(row=4, column=1, padx=10)

        self.hint_button = tk.Button(
            main_frame,
            text="Hint",
            command=self.give_hint,
            font=("Helvetica", 14),
            bg="#FFC107",
            fg="black",
            relief=tk.RAISED,
        )
        self.hint_button.grid(row=5, column=1, padx=10, pady=10)

        self.show_button = tk.Button(
            main_frame,
            text="Show Question",
            command=self.show_question,
            font=("Helvetica", 14),
            bg="#2196F3",
            fg="white",
            relief=tk.RAISED,
        )
        self.show_button.grid(row=5, column=0, pady=10)

        self.feedback_label = scrolledtext.ScrolledText(
            main_frame,
            width=60,
            height=10,
            font=("Helvetica", 12),
            wrap=tk.WORD,
            bg="#f9f9f9",
        )
        self.feedback_label.grid(row=6, column=0, columnspan=2, pady=10)
        self.feedback_label.config(state=tk.DISABLED)

    def load_topics(self):
        topics_dir = "topics"
        if not os.path.exists(topics_dir):
            os.makedirs(topics_dir)

        json_files = [f for f in os.listdir(topics_dir) if f.endswith(".json")]
        self.topic_combobox["values"] = json_files

    def on_topic_selected(self, event):
        selected_topic = self.topic_combobox.get()
        if selected_topic:
            topic_file = os.path.join("topics", selected_topic)
            self.game = MemoryGame(topic_file)

    def show_question(self):
        if self.game:
            card = self.game.show_question()
            if card:
                self.current_card = card
                self.question_label.config(text=f"Question: {card.question}")
                self.answer_entry.delete(0, tk.END)
                self.feedback_label.config(state=tk.NORMAL)
                self.feedback_label.delete(1.0, tk.END)
                self.feedback_label.config(state=tk.DISABLED)
            else:
                messagebox.showinfo("Info", "No cards available for this topic.")
        else:
            messagebox.showwarning("Warning", "Please select a topic first.")

    def submit_answer(self):
        if self.current_card:
            user_answer = self.answer_entry.get().strip().lower()
            feedback = self.game.check_answer(self.current_card, user_answer)
            self.feedback_label.config(state=tk.NORMAL)
            self.feedback_label.delete(1.0, tk.END)
            self.feedback_label.insert(tk.END, f"Feedback: {feedback}")
            self.feedback_label.config(state=tk.DISABLED)

    def give_hint(self):
        """Provides a hint for the current question."""
        if self.current_card:
            hint = self.game.get_hint(
                self.current_card.question
            )  # Assuming you have a method in MemoryGame to provide a hint
            self.feedback_label.config(state=tk.NORMAL)
            self.feedback_label.delete(1.0, tk.END)
            self.feedback_label.insert(tk.END, f"Hint: {hint}")
            self.feedback_label.config(state=tk.DISABLED)
        else:
            messagebox.showwarning("Warning", "Please show a question first.")

    def reset_all_scores(self):
        """Resets the scores, intervals, and last answered dates in all JSON files."""
        topics_dir = "topics"
        json_files = [f for f in os.listdir(topics_dir) if f.endswith(".json")]

        for json_file in json_files:
            topic_file_path = os.path.join(topics_dir, json_file)
            with open(topic_file_path, "r") as f:
                cards = json.load(f)

            # Reset the fields for each card
            for card in cards:
                card["score"] = 0
                card["interval"] = 1
                card["last_answered"] = datetime.now().isoformat()

            # Save the changes back to the file
            with open(topic_file_path, "w") as f:
                json.dump(cards, f, indent=4)

        messagebox.showinfo(
            "Success", "All scores, intervals, and dates have been reset!"
        )

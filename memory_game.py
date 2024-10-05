import json
import os
import random
from datetime import datetime

from llamabot import SimpleBot

from memory_card import MemoryCard

# Initialize model
model_llm = SimpleBot(
    "We are doing a game of Spaced repetition to learn concepts. The user will try to answer questions and you need to check if the answer is right and explain what is the answer if it is wrong. Start by writing 'score: ' and then a score to the answer between 0 and 10, where 10 is a completely right and detailed answer.",
    session_name="Default",
    model_name="ollama/llama3.2",
)


class MemoryGame:
    def __init__(self, topic_file):
        self.cards = []
        self.topic_file = topic_file
        self.load_cards()
        self.last_card = None  # Track the last shown card

    def load_cards(self):
        if os.path.exists(self.topic_file):
            with open(self.topic_file, "r") as file:
                cards_data = json.load(file)
                for card_data in cards_data:
                    card = MemoryCard(
                        card_data["question"],
                        card_data["interval"],
                        card_data["score"],
                        card_data.get("last_answered", datetime.now().isoformat()),
                    )
                    self.cards.append(card)

    def calculate_priority(self, card):
        now = datetime.now()
        if card.last_answered:
            last_answered_time = datetime.fromisoformat(card.last_answered)
            days_since_answered = (now - last_answered_time).days
        else:
            days_since_answered = float("inf")  # Card never answered before

        # Calculate the recency factor based on the interval
        recency_factor = days_since_answered / card.interval

        # Knowledge penalty: give higher priority to cards with lower scores
        knowledge_penalty = max(
            0, (3 - card.score)
        )  # Example: If score is low, penalty is higher

        # Final priority score
        priority_score = recency_factor + knowledge_penalty
        return priority_score

    def show_question(self):
        if not self.cards:
            return None

        # Calculate the priority score for each card
        scored_cards = [(card, self.calculate_priority(card)) for card in self.cards]

        # Sort by the highest priority score
        scored_cards.sort(key=lambda x: x[1], reverse=True)

        # Select the card with the highest priority score, avoiding the last card if it was answered incorrectly
        top_card = None
        for card, _ in scored_cards:
            if card != self.last_card:
                top_card = card
                break

        if top_card:
            return top_card
        else:
            print("No new questions available.")
            return None

    def save_cards(self):
        cards_data = [
            {
                "question": card.question,
                "interval": card.interval,
                "score": card.score,
                "last_answered": card.last_answered,
            }
            for card in self.cards
        ]
        with open(self.topic_file, "w") as file:
            json.dump(cards_data, file, indent=4)

    def check_answer_with_LLM(self, question, user_answer):
        prompt = f"Question to answer: '{question}'. User answer: '{user_answer}'"
        generated_text = model_llm(prompt).content
        return generated_text

    def check_answer(self, card, user_answer):
        feedback = self.check_answer_with_LLM(card.question, user_answer)
        score = int(feedback.split("Score: ")[1].split()[0])

        # Update card score and interval based on the user's score
        if score > 6:
            card.score += 1
            if card.score >= 3:
                card.interval += 1
        else:
            card.score = max(0, card.score - 1)
            card.interval = max(1, card.interval - 1)

        # Save the last answered card
        self.last_card = card
        card.last_answered = datetime.now().isoformat()
        self.save_cards()
        return feedback

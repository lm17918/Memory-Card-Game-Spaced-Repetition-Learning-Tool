import json
import os
import random
from datetime import datetime
from typing import List, Optional, Tuple

from llamabot import SimpleBot

from memory_card import MemoryCard

model_llm = SimpleBot(
    "We are doing a game of Spaced repetition to learn concepts. The user will try to answer questions and you need to check if the answer is right and explain what is the answer if it is wrong. If you have to provide a hint start you answer with the word 'Hint:' otherwise start by writing 'Score:' and then a score to the answer between 0 and 10, where 10 is a completely right and detailed answer and 6 is a barely acceptable answer.",
    session_name="Default",
    model_name="ollama/llama3.2",
)


class MemoryGame:
    def __init__(self, topic_file: str) -> None:
        self.cards: List[MemoryCard] = []
        self.topic_file: str = topic_file
        self.load_cards()
        self.last_card: Optional[MemoryCard] = None

    def load_cards(self) -> None:
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

    def calculate_priority(self, card: MemoryCard) -> float:
        now = datetime.now()
        if card.last_answered:
            last_answered_time = datetime.fromisoformat(card.last_answered)
            days_since_answered = (now - last_answered_time).days
        else:
            days_since_answered = float("inf")

        recency_factor = days_since_answered / card.interval
        knowledge_penalty = max(0, (3 - card.score))

        priority_score = recency_factor + knowledge_penalty
        return priority_score

    def show_question(self) -> Optional[MemoryCard]:
        if not self.cards:
            return None

        scored_cards: List[Tuple[MemoryCard, float]] = [
            (card, self.calculate_priority(card)) for card in self.cards
        ]
        scored_cards.sort(key=lambda x: x[1], reverse=True)

        top_card: Optional[MemoryCard] = None
        for card, _ in scored_cards:
            if card != self.last_card:
                top_card = card
                break

        if top_card:
            return top_card
        else:
            print("No new questions available.")
            return None

    def save_cards(self) -> None:
        cards_data: List[dict] = [
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

    def check_answer_with_LLM(self, question: str, user_answer: str) -> str:
        prompt: str = f"Question to answer: '{question}'. User answer: '{user_answer}'"
        generated_text: str = model_llm(prompt).content
        return generated_text

    def get_hint(self, question: str) -> str:
        prompt: str = f"Provide a hint for the question: '{question}'"
        hint_text: str = model_llm(prompt).content
        return hint_text

    def check_answer(self, card: MemoryCard, user_answer: str) -> str:
        feedback: str = self.check_answer_with_LLM(card.question, user_answer)
        try:
            score: int = int(feedback.split("Score: ")[1].split()[0])
        except IndexError:
            score = int(feedback.split("score: ")[1].split()[0])

        if score > 6:
            card.score += 1
            if card.score >= 3:
                card.interval += 1
        else:
            card.score = max(0, card.score - 1)
            card.interval = max(1, card.interval - 1)

        self.last_card = card
        card.last_answered = datetime.now().isoformat()
        self.save_cards()
        return feedback

from datetime import datetime

class MemoryCard:
    def __init__(self, question, interval=1, score=0, last_answered=None):
        self.question = question
        self.interval = interval
        self.score = score
        self.last_answered = last_answered or datetime.now().isoformat()

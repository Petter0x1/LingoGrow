import logging
import time
from core.models import Session, Vocab
from core.utils import normalize_arabic, reshape_arabic
from sqlalchemy.sql import func
from datetime import datetime

g = "\033[92m"
r = "\033[91m"
y = "\033[93m"
w = "\033[0m"


def select_timed_quiz():
    try:
        session = Session()
        words = session.query(Vocab).order_by(func.random()).limit(10).all()
        score = 0
        start_time = time.time()

        print(f"{y}Choose answer direction:{w}")
        print("[1] English → Arabic")
        print("[2] Arabic → English")
        mode = input(f"{y}Select mode (1 or 2): {w}").strip()
        if mode not in ("1", "2"):
            print(f"{r}❌ Invalid choice. Defaulting to English → Arabic.{w}")
            mode = "1"

        for word in words:
            if mode == "1":
                print(f"{y}Translate: {word.english}{w}")
                answer = input("→ ").strip()
                answer = normalize_arabic(answer)
                correct = normalize_arabic(word.arabic)
                if answer == correct:
                    print(f"{g}✅ Correct!{w}")
                    score += 1
                    word.correct_count += 1
                else:
                    print(f"{r}❌ Wrong! Correct: {reshape_arabic(word.arabic)}{w}")
                    word.wrong_count += 1
            else:
                print(f"{y}Translate: {reshape_arabic(word.arabic)}{w}")
                answer = input("→ ").strip().lower()
                correct = word.english.strip().lower()
                if answer == correct:
                    print(f"{g}✅ Correct!{w}")
                    score += 1
                    word.correct_count += 1
                else:
                    print(f"{r}❌ Wrong! Correct: {correct}{w}")
                    word.wrong_count += 1
            word.last_seen = datetime.now()

        session.commit()
        session.close()

        end_time = time.time()
        elapsed = int(end_time - start_time)
        print(f"{y}⏱️ Time: {elapsed}s | Score: {score}/{len(words)}{w}")
    except Exception as e:
        logging.error("Error in select_timed_quiz: %s", e, exc_info=True)
        print(f"{r}❌ An error occurred in select_timed_quiz. See log for details.{w}")
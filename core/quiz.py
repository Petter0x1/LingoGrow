import logging
from core.utils import normalize_arabic, reshape_arabic
from core.models import Session, Vocab
from sqlalchemy.sql import func
from datetime import datetime
import random



g = "\033[92m"  # green
y = "\033[93m"  # yellow
b = "\033[94m"  # blue
c = "\033[96m"  # cyan
r = "\033[91m"  # red
w = "\033[0m"   # reset

def start_quiz():
    try:
        session = Session()
        words = session.query(Vocab).order_by(func.random()).limit(10).all()
        score = 0
        for word in words:
            options = [word.arabic]
            while len(options) < 4:
                choice = session.query(Vocab).order_by(func.random()).first()
                if choice and choice.arabic not in options:
                    options.append(choice.arabic)
            random.shuffle(options)

            print(f"{b}Translate: {word.english}{w}")
            for i, option in enumerate(options):
                print(f"[{i+1}] {reshape_arabic(option)}")

            answer = input("Your choice (1-4): ").strip()
            if answer.isdigit() and 1 <= int(answer) <= 4 and options[int(answer)-1] == word.arabic:
                print(f"{g}✅ Correct!{w}")
                score += 1
                word.correct_count += 1
            else:
                print(f"{r}❌ Wrong! Correct answer: {word.arabic}{w}")
                print(f"The answer is: {reshape_arabic(word.arabic)}")
                word.wrong_count += 1
            word.last_seen = datetime.now()

        session.commit()
        session.close()
        print(f"\n{y}🧠 Your Score: {score}/10{w}")
    except Exception as e:
        logging.error("Error in start_quiz: %s", e, exc_info=True)
        print(f"{r}❌ An error occurred in start_quiz. See log for details.{w}")

def review_wrong_words():
    session = Session()
    words = session.query(Vocab).filter(Vocab.wrong_count > Vocab.correct_count).order_by(func.random()).limit(10).all()
    if not words:
        print(f"{g}✅ No wrong words to review!{w}")
        return
    print(f"{c}🔁 Reviewing wrong words:{w}")
    for word in words:
        answer = input(f"Translate: {word.english} → ").strip()
        answer = normalize_arabic(answer)
        correct = normalize_arabic(word.arabic)
        if answer == correct:
            print(f"{g}✅ Correct!{w}")
            word.correct_count += 1
        else:
            print(f"{r}❌ Wrong! Correct: {reshape_arabic(word.arabic)}{w}")
            print(f"The answer is: {reshape_arabic(word.arabic)}")
            word.wrong_count += 1
        word.last_seen = datetime.now()
    session.commit()
    session.close()

def review_spaced_words():
    session = Session()
    words = session.query(Vocab).filter(Vocab.correct_count < 3).order_by(Vocab.last_seen).limit(10).all()
    if not words:
        print(f"{g}✅ All words are well-learned!{w}")
        return
    print(f"{c}🧠 Reviewing spaced words...{w}")
    for word in words:
        answer = input(f"Translate: {word.english} → ").strip()
        answer = normalize_arabic(answer)
        correct = normalize_arabic(word.arabic)
        if answer == correct:
            print(f"{g}✅ Correct!{w}")
            word.correct_count += 1
        else:
            print(f"{r}❌ Wrong! Correct: {reshape_arabic(word.arabic)}{w}")
            print(f"The answer is: {reshape_arabic(word.arabic)}")
            word.wrong_count += 1
        word.last_seen = datetime.now()
    session.commit()
    session.close()

def show_stats():
    session = Session()
    total = session.query(Vocab).count()
    mastered = session.query(Vocab).filter(Vocab.correct_count > 5).count()
    print(f"{y}Total words: {total}, Mastered: {mastered}{w}")
    session.close()

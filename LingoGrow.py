import logging
from core.quiz import start_quiz, review_wrong_words, review_spaced_words, show_stats
from core.quiz_modes import typing_quiz, pronunciation_quiz
from core.batch_loader import load_multiple_srt
from core.db_cleaner import clean_duplicates
from core.timed_quiz import select_timed_quiz
from core.daily_review import review_forgotten_words
from core.daily_goal import check_daily_goal, get_daily_goal, set_daily_goal
from core.achievements import show_achievements
from core.models import Session, Vocab, func
from core.utils import normalize_arabic, reshape_arabic
from datetime import datetime

# Setup logging
logging.basicConfig(
    filename="lingogrow.log",
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(module)s:%(lineno)d %(message)s"
)

# ANSI color variables
g = "\033[92m"  # green
y = "\033[93m"  # yellow
b = "\033[94m"  # blue
c = "\033[96m"  # cyan
r = "\033[91m"  # red
w = "\033[0m"   # reset/white

TRAINED_LIMIT_DAYS = 30

def print_menu():
    print(f"\n{c}🧠 LingoGrow - Main Menu{w}")
    print("[1] (📘) Multiple Choice Quiz")
    print("[2] (⌨️) Typing Quiz")
    print("[3] (🗣️) Pronunciation Quiz")
    print("[4] (🧾) Review Wrong Answers")
    print("[5] (⏰) Spaced Repetition Review")
    print("[6] (📊) Show Stats")
    print("[7] (📂) Load Multiple SRT Files")
    print("[8] (🧹) Clean Duplicate Words")
    print("[9] (🔁) Train on Old Words")
    print("[10] (🎯) Quiz by Difficulty")
    print("[11] (⏳) Timed Survival Quiz")
    print("[12] (🧹) Review Forgotten Words")
    print("[13] (📅) Daily Goal Progress")
    print("[14] (🏅) View Achievements")
    print("[15] (⚙️) Change Daily Goal")
    print("[16] (📋) Show Words To Learn Today")
    print("[0] (🚪) Exit")

def train_old_words():
    try:
        session = Session()
        limit_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        words = session.query(Vocab).filter(Vocab.last_seen <= limit_date).order_by(Vocab.last_seen).limit(10).all()

        if not words:
            print(f"{g}✅ No old words to review today.{w}")
            return

        score = 0
        print(f"\n{y}🔁 Training on older words:{w}")
        for word in words:
            answer = input(f"Translate: {word.english} → ").strip()
            answer = normalize_arabic(answer)
            correct = normalize_arabic(word.arabic)

            if answer == correct:
                print(f"{g}✅ Correct!{w}")
                score += 1
                word.correct_count += 1
            else:
                print(f"{r}❌ Wrong! Correct: {reshape_arabic(word.arabic)}{w}")
                word.wrong_count += 1
            word.last_seen = datetime.now()

            if len(word.english) <= 4:
                word.difficulty = "easy"
            elif len(word.english) <= 7:
                word.difficulty = "medium"
            else:
                word.difficulty = "hard"

        session.commit()
        session.close()
        print(f"\n{b}🧠 Training complete! Score: {score}/{len(words)}{w}")
    except Exception as e:
        logging.error("Error in train_old_words: %s", e, exc_info=True)
        print(f"{r}❌ An error occurred during training old words. See log for details.{w}")

def quiz_by_difficulty():
    try:
        session = Session()
        print(f"\n{c}🎯 Select difficulty level:{w}")
        print("[1] Easy\n[2] Medium\n[3] Hard")
        level_map = {"1": "easy", "2": "medium", "3": "hard"}
        choice = input("Enter choice (1-3): ").strip()
        if choice not in level_map:
            print(f"{r}❌ Invalid difficulty choice.{w}")
            return

        difficulty = level_map[choice]
        words = session.query(Vocab).filter_by(difficulty=difficulty).order_by(func.random()).limit(10).all()
        if not words:
            print(f"{r}⚠️ No words found for difficulty: {difficulty}{w}")
            return

        print(f"\n{b}🧠 Starting quiz for difficulty: {difficulty.upper()}{w}")
        score = 0
        for word in words:
            answer = input(f"Translate: {word.english} → ").strip()
            answer = normalize_arabic(answer)
            correct = normalize_arabic(word.arabic)

            if answer == correct:
                print(f"{g}✅ Correct!{w}")
                score += 1
                word.correct_count += 1
            else:
                print(f"{r}❌ Wrong! Correct: {reshape_arabic(word.arabic)}{w}")
                word.wrong_count += 1
            word.last_seen = datetime.now()
        session.commit()
        session.close()
        print(f"\n{y}🎯 Score: {score}/{len(words)}{w}")
    except Exception as e:
        logging.error("Error in quiz_by_difficulty: %s", e, exc_info=True)
        print(f"{r}❌ An error occurred during quiz by difficulty. See log for details.{w}")

def show_words_to_learn():
    try:
        session = Session()
        today = datetime.now().date()
        daily_goal = get_daily_goal()
        words = session.query(Vocab).filter(
            (Vocab.last_seen < today) | (Vocab.correct_count == 0)
        ).order_by(Vocab.last_seen).limit(daily_goal).all()
        if not words:
            print(f"{g}🎉 You have no pending words to learn for today!{w}")
        else:
            print(f"{c}📋 Words to learn today ({len(words)}/{daily_goal}):{w}")
            for i, word in enumerate(words, 1):
                print(f"{i}. {word.english} → {reshape_arabic(word.arabic)}")
        session.close()
    except Exception as e:
        logging.error("Error in show_words_to_learn: %s", e, exc_info=True)
        print(f"{r}❌ An error occurred while showing words to learn. See log for details.{w}")

if __name__ == '__main__':
    try:
        while True:
            try:
                print_menu()
                choice = input(f"{y}Select an option (0-16):{w} ").strip()

                if choice == '1':
                    start_quiz()
                elif choice == '2':
                    typing_quiz()
                elif choice == '3':
                    pronunciation_quiz()
                elif choice == '4':
                    review_wrong_words()
                elif choice == '5':
                    review_spaced_words()
                elif choice == '6':
                    show_stats()
                elif choice == '7':
                    folder = input("Enter folder path with .srt files: ").strip()
                    load_multiple_srt(folder)
                elif choice == '8':
                    clean_duplicates()
                elif choice == '9':
                    train_old_words()
                elif choice == '10':
                    quiz_by_difficulty()
                elif choice == '11':
                    select_timed_quiz()
                elif choice == '12':
                    review_forgotten_words()
                elif choice == '13':
                    check_daily_goal()
                elif choice == '14':
                    show_achievements()
                elif choice == '15':
                    try:
                        new_goal = int(input("Enter new daily goal (number): ").strip())
                        if new_goal > 0:
                            set_daily_goal(new_goal)
                            print(f"{g}✅ Daily goal updated to {new_goal}.{w}")
                        else:
                            print(f"{r}❌ Please enter a positive number.{w}")
                    except ValueError:
                        print(f"{r}❌ Invalid input. Please enter a number.{w}")
                    except Exception as e:
                        logging.error("Error setting daily goal: %s", e, exc_info=True)
                        print(f"{r}❌ An error occurred while setting daily goal. See log for details.{w}")
                elif choice == '16':
                    show_words_to_learn()
                elif choice == '0':
                    print(f"{b}👋 Goodbye!{w}")
                    break
                else:
                    print(f"{r}❌ Invalid choice. Try again.{w}")
            except Exception as e:
                logging.error("Error in main menu loop: %s", e, exc_info=True)
                print(f"{r}❌ An unexpected error occurred. See log for details.{w}")
    except KeyboardInterrupt:
        print(f"\n{b}👋 Goodbye!{w}")
    except Exception as e:
        logging.error("Fatal error in main: %s", e, exc_info=True)
        print(f"{r}❌ A fatal error occurred. See log for details.{w}")
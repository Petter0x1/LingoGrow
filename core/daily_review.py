from core.models import Session, Vocab
from datetime import datetime, timedelta
from core.utils import normalize_arabic, reshape_arabic

c = "\033[96m"
g = "\033[92m"
r = "\033[91m"
y = "\033[93m"
w = "\033[0m"

def review_forgotten_words():
    session = Session()
    past = datetime.now() - timedelta(days=7)
    words = session.query(Vocab).filter(Vocab.last_seen < past).limit(10).all()
    if not words:
        print(f"{g}✅ No forgotten words to review.{w}")
        return

    print(f"{c}🔁 Reviewing forgotten words:{w}")
    for word in words:
        answer = input(f"Translate: {word.english} → ").strip()
        answer = normalize_arabic(answer)
        correct = normalize_arabic(word.arabic)
        if answer == correct:
            print(f"{g}✅ Correct!{w}")
            word.correct_count += 1
        else:
            print(f"{r}❌ Wrong! Correct: {reshape_arabic(word.arabic)}{w}")
            word.wrong_count += 1
        word.last_seen = datetime.now()
    session.commit()
    session.close()

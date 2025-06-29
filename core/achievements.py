from core.models import Session, Vocab

b = "\033[94m"
g = "\033[92m"
w = "\033[0m"

def show_achievements():
    session = Session()
    total = session.query(Vocab).count()
    mastered = session.query(Vocab).filter(Vocab.correct_count > 5).count()
    daily = session.query(Vocab).order_by(Vocab.date_added.desc()).limit(10).count()

    print(f"{b}🏆 Achievements:{w}")
    print(f"{g}• Total Words Learned: {total}{w}")
    print(f"{g}• Mastered Words (>5 correct): {mastered}{w}")
    print(f"{g}• Words Added Recently: {daily}{w}")
    session.close()

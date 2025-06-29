from core.models import Session, Vocab
from sqlalchemy import func

def clean_duplicates():
    session = Session()
    seen = set()
    duplicates = []
    for word in session.query(Vocab).all():
        if word.english in seen:
            duplicates.append(word)
        else:
            seen.add(word.english)
    for d in duplicates:
        print(f"Deleting duplicate: {d.english}")
        session.delete(d)
    session.commit()
    session.close()
    print("✅ Duplicates removed.")
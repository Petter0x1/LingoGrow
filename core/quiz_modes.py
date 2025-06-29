import logging
from core.models import Session, Vocab
from core.utils import normalize_arabic, reshape_arabic
from sqlalchemy.sql import func
from datetime import datetime
import random
import speech_recognition as sr

g = "\033[92m"
y = "\033[93m"
b = "\033[94m"
c = "\033[96m"
r = "\033[91m"
w = "\033[0m"

def typing_quiz():
    try:
        session = Session()
        words = session.query(Vocab).order_by(func.random()).limit(10).all()
        score = 0
        for word in words:
            answer = input(f"Translate: {word.english} → ").strip()
            answer = normalize_arabic(answer)
            correct = normalize_arabic(word.arabic)
            if answer == correct:
                print(f"{g}✅ Correct!{w}")
                word.correct_count += 1
                score += 1
            else:
                print(f"{r}❌ Wrong! Correct: {reshape_arabic(word.arabic)}{w}")
                word.wrong_count += 1
            word.last_seen = datetime.now()
        session.commit()
        session.close()
        print(f"\n{y}⌨️ Score: {score}/10{w}")
    except Exception as e:
        logging.error("Error in typing_quiz: %s", e, exc_info=True)
        print(f"{r}❌ An error occurred in typing_quiz. See log for details.{w}")

def pronunciation_quiz():
    try:
        session = Session()
        words = session.query(Vocab).order_by(func.random()).limit(5).all()
        recognizer = sr.Recognizer()
        mic = sr.Microphone()
        score = 0

        print(f"\n{b}🗣️ Pronunciation Quiz: Choose which word to pronounce!{w}")
        print("[1] Say the Arabic translation")
        print("[2] Say the English word")
        mode = input(f"{y}Choose mode (1 or 2): {w}").strip()
        if mode not in ("1", "2"):
            print(f"{r}❌ Invalid choice. Defaulting to Arabic.{w}")
            mode = "1"

        for word in words:
            if mode == "1":
                prompt_word = reshape_arabic(word.arabic)
                lang = "ar"
                correct_text = word.arabic
                display_lang = "Arabic"
            else:
                prompt_word = word.english
                lang = "en"
                correct_text = word.english
                display_lang = "English"

            print(f"\n{b}{display_lang} to pronounce: {prompt_word}{w}")
            input(f"Press Enter and say '{prompt_word}'...")

            with mic as source:
                recognizer.adjust_for_ambient_noise(source)
                print(f"{c}Listening...{w}")
                audio = recognizer.listen(source, timeout=5)

            try:
                result = recognizer.recognize_google(audio, language=lang)
                if lang == "ar":
                    print(f"{b}You said: {reshape_arabic(result)}{w}")
                    is_correct = normalize_arabic(result) == normalize_arabic(correct_text)
                else:
                    print(f"{b}You said: {result}{w}")
                    is_correct = result.strip().lower() == correct_text.strip().lower()

                if is_correct:
                    print(f"{g}✅ Correct pronunciation!{w}")
                    word.correct_count += 1
                    score += 1
                else:
                    if lang == "ar":
                        print(f"{r}❌ Incorrect. Correct: {reshape_arabic(correct_text)}{w}")
                    else:
                        print(f"{r}❌ Incorrect. Correct: {correct_text}{w}")
                    word.wrong_count += 1
            except sr.UnknownValueError:
                print(f"{r}❌ Could not understand audio.{w}")
                word.wrong_count += 1
            except sr.RequestError:
                print(f"{r}❌ Speech recognition service error.{w}")
                word.wrong_count += 1

            word.last_seen = datetime.now()

        session.commit()
        session.close()
        print(f"\n{y}🗣️ Score: {score}/5{w}")
    except Exception as e:
        logging.error("Error in pronunciation_quiz: %s", e, exc_info=True)
        print(f"{r}❌ An error occurred in pronunciation_quiz. See log for details.{w}")
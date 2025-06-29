import os
import re
import threading
from queue import Queue
from core.models import Session, Vocab
from core.utils import normalize_arabic, reshape_arabic
from datetime import datetime
from deep_translator import GoogleTranslator
import signal
from tqdm import tqdm

stop_flag = False

def signal_handler(sig, frame):
    global stop_flag
    stop_flag = True
    print("\n🛑 Stopping... please wait.")

signal.signal(signal.SIGINT, signal_handler)

def extract_words_from_srt(srt_content):
    text = re.sub(r"\d+\n", "", srt_content)  # remove subtitle numbers
    text = re.sub(r"\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}", "", text)
    text = re.sub(r"<.*?>", "", text)  # remove tags
    text = re.sub(r"[^a-zA-Z']", " ", text)
    words = text.lower().split()
    return list(set(words))

def worker(queue, results, pbar):
    while not queue.empty() and not stop_flag:
        word = queue.get()
        try:
            arabic = GoogleTranslator(source='en', target='ar').translate(word)
            results.append((word, arabic))
        except Exception as e:
            print(f"Translation failed for {word}: {e}")
        finally:
            queue.task_done()
            pbar.update(1)

def load_multiple_srt(folder_path):
    session = Session()
    all_words = set()

    for filename in os.listdir(folder_path):
        if filename.endswith(".srt"):
            path = os.path.join(folder_path, filename)
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
                words = extract_words_from_srt(content)
                all_words.update(words)

    clean_words = [w.lower().strip() for w in all_words if len(w) >= 2]
    clean_words = list(set(clean_words))

    existing = {v.english for v in session.query(Vocab.english).all()}
    new_words = [w for w in clean_words if w not in existing]

    if not new_words:
        print("No new words to add.")
        return

    queue = Queue()
    for word in new_words:
        queue.put(word)

    results = []
    threads = []
    pbar = tqdm(total=len(new_words), desc="Translating", ncols=70)

    for _ in range(min(50, len(new_words))):  # Max 50 threads
        t = threading.Thread(target=worker, args=(queue, results, pbar))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    pbar.close()

    for word, arabic in results:
        try:
            vocab = Vocab(
                english=word,
                arabic=normalize_arabic(arabic),
                date_added=datetime.now(),
                last_seen=datetime.now(),
                difficulty="easy" if len(word) <= 4 else "medium" if len(word) <= 7 else "hard"
            )
            session.add(vocab)
            print(f"Added: {word} -> {reshape_arabic(arabic)}")
        except Exception as e:
            print(f"Failed to add {word}: {e}")

    session.commit()
    session.close()
    print("✅ All subtitles loaded.")

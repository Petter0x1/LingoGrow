import logging
from core.models import Session, Vocab, get_setting, set_setting
from datetime import datetime
import os

w = "\033[0m"
g = "\033[92m"
y = "\033[93m"

def get_daily_goal():
    try:
        session = Session()
        goal = get_setting(session, "DAILY_GOAL", 20)
        session.close()
        return int(goal)
    except Exception as e:
        logging.error("Error in get_daily_goal: %s", e, exc_info=True)
        print(f"{y}⚠️ Could not fetch daily goal. Defaulting to 20.{w}")
        return 20

def set_daily_goal(new_goal):
    try:
        session = Session()
        set_setting(session, "DAILY_GOAL", new_goal)
        session.close()
    except Exception as e:
        logging.error("Error in set_daily_goal: %s", e, exc_info=True)
        print(f"{y}⚠️ Could not set daily goal.{w}")

def check_daily_goal():
    try:
        session = Session()
        today = datetime.now().date()
        daily_goal = int(get_setting(session, "DAILY_GOAL", 20))
        learned_count = session.query(Vocab).filter(
            Vocab.last_seen >= today,
            Vocab.correct_count > 0
        ).count()
        if learned_count >= daily_goal:
            print(f"{g}🎉 You reached your daily goal! Learned: {learned_count} words today.{w}")
        else:
            print(f"{y}📊 Words learned today: {learned_count}/{daily_goal}{w}")
        session.close()
    except Exception as e:
        logging.error("Error in check_daily_goal: %s", e, exc_info=True)
        print(f"{y}⚠️ Could not check daily goal progress.{w}")

import json
import os

HIGHSCORE_FILE = os.path.join(os.path.dirname(__file__), "highscores.json")


def load_high_score():
    try:
        with open(HIGHSCORE_FILE, "r") as f:
            data = json.load(f)
            return data.get("high_score", 0)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0


def save_high_score(score):
    current_best = load_high_score()
    if score > current_best:
        with open(HIGHSCORE_FILE, "w") as f:
            json.dump({"high_score": score}, f)
        return True
    return False

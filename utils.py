def analyze_quiz(answers: dict) -> dict:
    skin_type = ''
    concerns = []
    preferences = []

    if answers.get('q1') == 'dry':
        skin_type = 'dry'
    elif answers.get('q1') == 'oily':
        skin_type = 'oily'
    elif answers.get('q1') == 'combination':
        skin_type = 'combination'

    if answers.get("q3") == "very_sensitive":
        skin_type = "sensitive"

    if answers.get("q4") == "yes":
        concerns.append("acne")
    if answers.get("q5") == "yes":
        concerns.append("wrinkles")
    if answers.get("q6") == "yes":
        concerns.append("dark_spots")

    preferences = {
        "time": answers.get("q7"),
        "steps": answers.get("q8"),
        "products": answers.get("q9")
    }

    return {
        "skin_type": skin_type,
        "concerns": concerns,
        "preferences": preferences
    }


def csv_to_list(s: str):
    if not s:
        return []
    return [x.strip().lower() for x in s.split(",") if x.strip()]


def list_to_csv(lst: list):
    return ",".join(sorted(set([x.strip().lower() for x in lst if x.strip()])))
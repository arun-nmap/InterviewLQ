def evaluate_answer(answer):
    words = len(answer.split())
    if words < 5:
        return 30
    if words < 20:
        return 60
    return 85

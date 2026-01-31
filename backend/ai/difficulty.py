def adjust_difficulty(confidence):
    if confidence > 75:
        return "hard"
    if confidence > 50:
        return "medium"
    return "easy"

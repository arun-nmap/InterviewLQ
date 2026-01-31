QUESTIONS = []

def load_questions(qs):
    global QUESTIONS
    QUESTIONS = qs

def get_question(index, difficulty):
    for q in QUESTIONS:
        if q["difficulty"] == difficulty:
            return q["question"]
    return QUESTIONS[index]["question"]

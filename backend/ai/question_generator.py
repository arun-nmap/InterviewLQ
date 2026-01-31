def generate_questions(skills):
    questions = []

    for s in skills[:2]:
        questions.append({
            "question": f"Explain your experience with {s}.",
            "difficulty": "medium"
        })

    questions += [
        {"question": "Tell me about yourself.", "difficulty": "easy"},
        {"question": "How do you optimize performance in Python?", "difficulty": "hard"}
    ]

    return questions[:4]

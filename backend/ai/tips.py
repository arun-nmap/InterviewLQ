def generate_tip(confidence, emotion):
    if emotion == "nervous":
        return "Take a breath and slow down."
    if confidence < 50:
        return "Try to give a more structured answer."
    if confidence > 75:
        return "Good confidence. Keep going!"
    return ""

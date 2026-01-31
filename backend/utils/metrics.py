def calculate_metrics(history):
    confidences = [h["confidence"] for h in history]
    emotions = [h["emotion"] for h in history]

    return {
        "avg_confidence": round(sum(confidences) / len(confidences), 2),
        "max_confidence": max(confidences),
        "min_confidence": min(confidences),
        "emotion_distribution": {
            e: emotions.count(e) for e in set(emotions)
        }
    }

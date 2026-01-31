def fuse_confidence(relevance, emotion):
    score = relevance
    if emotion == "confident":
        score += 15
    if emotion == "nervous":
        score -= 10
    return max(0, min(100, score))

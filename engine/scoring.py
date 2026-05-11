BASE_SCORE = 100
DAMAGE_PENALTIES = {
    "crack": 45,
    "scratch_deep": 20,
    "scratch_light": 8,
}


def calculate_freshness_score(detections):
    penalty = 0

    for detection in detections:
        label = detection["label"]
        confidence = detection["confidence"]
        penalty += DAMAGE_PENALTIES.get(label, 0) * confidence

    return max(0, round(BASE_SCORE - penalty))

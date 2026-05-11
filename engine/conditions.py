def classify_condition(freshness_score):
    if freshness_score >= 90:
        return "Fresh-As-New"
    if freshness_score >= 75:
        return "Excellent"
    if freshness_score >= 60:
        return "Good"
    if freshness_score >= 40:
        return "Usable"
    return "Poor"

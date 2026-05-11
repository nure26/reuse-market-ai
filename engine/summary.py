def generate_damage_summary(detections):
    summary = {}

    for detection in detections:
        label = detection["label"]
        summary[label] = summary.get(label, 0) + 1

    return summary

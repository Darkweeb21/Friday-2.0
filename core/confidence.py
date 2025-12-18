# core/confidence.py

CONFIDENCE_THRESHOLD = 0.70


def is_confident(confidence: float) -> bool:
    """
    Returns True if intent confidence is high enough to act.
    """
    return confidence >= CONFIDENCE_THRESHOLD

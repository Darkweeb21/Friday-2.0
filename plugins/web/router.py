# web/router.py

REALTIME_KEYWORDS = {
    # ---- Time / Freshness ----
    "current", "latest", "today", "now", "recent", "updated", "update",
    "this year", "this month", "this week", "as of",

    # ---- Exams / Education ----
    "cutoff", "cut-off", "passing marks", "result", "results",
    "exam date", "exam schedule", "syllabus",
    "admission", "admissions", "fees", "eligibility",
    "rank", "merit list", "counselling",

    # ---- Finance / Money ----
    "price", "prices", "rate", "rates",
    "share", "shares", "stock", "stocks",
    "market", "market cap", "valuation",
    "net worth", "revenue", "profit", "loss",
    "salary", "package", "ctc", "lpa",
    "investment", "crypto", "bitcoin", "ethereum",

    # ---- People / Organizations ----
    "ceo", "founder", "chairman", "owner",
    "company", "organization",
    "networth", "worth",

    # ---- News / Events ----
    "news", "headline", "breaking",
    "announcement", "launched", "launch",
    "policy", "government", "rule", "regulation",

    # ---- Weather / Location ----
    "weather", "temperature", "rain", "rainfall",
    "forecast", "humidity", "climate",

    # ---- Sports ----
    "score", "scores", "live score",
    "match", "matches", "fixture", "points table",
    "ranking", "standings",

    # ---- Jobs / Career ----
    "opening", "openings", "vacancy", "vacancies",
    "hiring", "recruitment", "job", "jobs",
    "internship", "stipend",

    # ---- Dates / Schedules ----
    "date", "dates", "time", "timing",
    "schedule", "deadline", "last date",

    # ---- Health / Public Info ----
    "cases", "outbreak", "alert", "guidelines",

    # ---- Comparison / Dynamic ----
    "vs", "compare", "comparison",
    "best", "top", "ranking",
}

def needs_web_search(query: str, confidence: float) -> bool:
    q = query.lower().strip()

    #  NEVER web-search greetings or casual chat
    casual = {
        "hi", "hello", "hey",
        "hi friday", "hello friday", "hey friday",
        "good morning", "good afternoon", "good evening"
    }
    if q in casual:
        return False

    #  Explicit real-time / factual keywords
    if any(k in q for k in REALTIME_KEYWORDS):
        return True

    #  Numbers usually imply dynamic data
    if any(c.isdigit() for c in q):
        return True

    return False



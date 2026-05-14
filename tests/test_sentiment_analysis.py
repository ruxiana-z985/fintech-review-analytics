from src.sentiment_analysis import score_headline


def test_score_headline_returns_positive_for_positive_text():
    assert score_headline("Stock surges after strong earnings beat") > 0


def test_score_headline_returns_negative_for_negative_text():
    assert score_headline("Shares plunge after weak outlook warning") < 0


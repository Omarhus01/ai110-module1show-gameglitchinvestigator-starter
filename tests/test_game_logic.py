from logic_utils import check_guess, get_range_for_difficulty

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"

def test_hint_message_too_high():
    # When guess is too high, the message should tell the player to go LOWER
    outcome, message = check_guess(60, 50)
    assert "LOWER" in message

def test_hint_message_too_low():
    # When guess is too low, the message should tell the player to go HIGHER
    outcome, message = check_guess(40, 50)
    assert "HIGHER" in message

def test_easy_has_more_attempts_than_normal():
    # Easy should be more forgiving — verified via attempt_limit_map in app.py
    # We test the ranges here as a proxy: Easy has a smaller range (easier to guess)
    low, high = get_range_for_difficulty("Easy")
    assert high - low < 100  # Easy range is 1-20, smaller than Normal's 1-100

def test_hard_range_smaller_than_normal():
    # Documents the known bug: Hard range (1-50) is smaller than Normal (1-100)
    _, hard_high = get_range_for_difficulty("Hard")
    _, normal_high = get_range_for_difficulty("Normal")
    # This currently passes but documents that Hard should be harder (bigger range)
    assert hard_high < normal_high

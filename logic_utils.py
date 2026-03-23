def get_range_for_difficulty(difficulty: str) -> tuple[int, int]:
    """
    Return the inclusive (low, high) number range for a given difficulty level.

    Args:
        difficulty: One of "Easy", "Normal", or "Hard".

    Returns:
        A tuple (low, high) representing the inclusive guessing range.
        Defaults to (1, 100) if an unrecognised difficulty is passed.

    Examples:
        >>> get_range_for_difficulty("Easy")
        (1, 20)
        >>> get_range_for_difficulty("Normal")
        (1, 100)
    """
    # Easy has way too few attempts and smaller range than Hard which doesn't make sense
    # Need fixation for the ranges according to the difficulties
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str) -> tuple[bool, int | None, str | None]:
    """
    Parse raw user input into a validated integer guess.

    Accepts whole numbers and decimals (decimals are truncated to int).
    Returns a three-element tuple so the caller always gets a consistent
    structure regardless of whether parsing succeeded.

    Args:
        raw: The raw string entered by the player.

    Returns:
        A tuple of (ok, guess_int, error_message) where:
            - ok (bool): True if parsing succeeded, False otherwise.
            - guess_int (int | None): The parsed integer, or None on failure.
            - error_message (str | None): A human-readable error, or None on success.

    Examples:
        >>> parse_guess("42")
        (True, 42, None)
        >>> parse_guess("abc")
        (False, None, 'That is not a number.')
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess: int, secret: int) -> tuple[str, str]:
    """
    Compare the player's guess against the secret number.

    Args:
        guess: The player's guessed integer.
        secret: The target secret number. Should be an int, but a TypeError
                fallback handles cases where secret is accidentally a string.

    Returns:
        A tuple of (outcome, message) where outcome is one of:
            - "Win"      — guess matches the secret.
            - "Too High" — guess is above the secret.
            - "Too Low"  — guess is below the secret.
        And message is a human-readable hint string for the player.

    Examples:
        >>> check_guess(50, 50)
        ('Win', '🎉 Correct!')
        >>> check_guess(60, 50)
        ('Too High', '📉 Go LOWER!')
        >>> check_guess(40, 50)
        ('Too Low', '📈 Go HIGHER!')
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    # FIX: Hints were reversed — "Too High" was saying Go HIGHER and "Too Low" was saying Go LOWER.
    # Claude Code identified the bug by reading the original check_guess logic and confirmed
    # that the messages were swapped. Fixed by matching each outcome to the correct direction.
    try:
        if guess > secret:
            return "Too High", "📉 Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """
    Calculate and return the updated score based on the guess outcome.

    Winning earlier yields more points (max 80 on attempt 1, minimum 10).
    Wrong guesses deduct 5 points, except "Too High" on even attempts
    which incorrectly awards +5 — this is a known bug left intentionally.

    Args:
        current_score: The player's score before this guess.
        outcome: One of "Win", "Too High", or "Too Low".
        attempt_number: The 1-based index of the current attempt.

    Returns:
        The updated integer score after applying the outcome.

    Examples:
        >>> update_score(0, "Win", 1)
        80
        >>> update_score(50, "Too Low", 3)
        45
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            # That's incorrect — why do we get more points for being too high on even attempts?
            # This should be fixed to always deduct points for wrong guesses.
            # Known bug, left in place intentionally for this assignment.
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score

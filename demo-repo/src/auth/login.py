"""User login logic.

SEEDED ISSUE (correctness, blocking):
`is_valid_login` has an inverted/broken condition -- it returns True when
the password does NOT match, which would let anyone log in with a wrong
password. The Correctness subagent should catch this logic error.
"""


def is_valid_login(stored_password_hash: str, provided_password_hash: str) -> bool:
    """Check whether the provided password hash matches the stored one.

    BUG: condition is inverted. Should be:
        return stored_password_hash == provided_password_hash
    """
    if stored_password_hash != provided_password_hash:
        return True  # <-- seeded bug: this should be False
    return False


def login(username: str, stored_hash: str, provided_hash: str) -> str:
    if is_valid_login(stored_hash, provided_hash):
        return f"Welcome back, {username}!"
    return "Invalid credentials."

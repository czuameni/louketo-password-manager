import string


class PasswordStrengthMeter:

    def evaluate(self, password):

        score = 0

        # Length
        if len(password) >= 8:
            score += 1
        if len(password) >= 12:
            score += 1
        if len(password) >= 16:
            score += 1

        # Uppercase
        if any(c in string.ascii_uppercase for c in password):
            score += 1

        # Numbers
        if any(c in string.digits for c in password):
            score += 1

        # Symbols
        if any(c in string.punctuation for c in password):
            score += 1

        return score

    # -------------------------

    def get_label(self, score):

        if score <= 2:
            return "Weak"
        elif score <= 4:
            return "Medium"
        elif score <= 6:
            return "Strong"
        else:
            return "Very Strong"

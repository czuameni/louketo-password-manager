import random
import string


class PasswordGenerator:

    def generate(
        self,
        length=12,
        use_uppercase=True,
        use_numbers=True,
        use_symbols=True
    ):

        characters = string.ascii_lowercase

        if use_uppercase:
            characters += string.ascii_uppercase

        if use_numbers:
            characters += string.digits

        if use_symbols:
            characters += string.punctuation

        if not characters:
            raise ValueError("No character sets selected.")

        password = "".join(
            random.choice(characters)
            for _ in range(length)
        )

        return password

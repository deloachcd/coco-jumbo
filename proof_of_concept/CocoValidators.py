allowed_symbols = "-.@_"


def identifier_is_valid(identifier):
    for character in identifier:
        if (not character.isalnum()
                and character not in allowed_symbols):
            return False
    return True

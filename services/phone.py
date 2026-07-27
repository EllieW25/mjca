
def normalize_phone(phone): # covert a phone number to an E.164 format
    digits = ""

    for char in phone:
        if char.isdigit():
            digits += char
    if len(digits) == 10:
        digits = "1" + digits

    return "+" + digits

def validate_phone(phone): #makes sure we are receiving a valid phone number
    cleaned = normalize_phone(phone)
    if len(cleaned) != 12:
        return False
    return True
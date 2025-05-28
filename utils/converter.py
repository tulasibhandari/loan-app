

def convert_to_nepali_digits(text):
    eng_to_nep = str.maketrans('0123456789', '०१२३४५६७८९')
    return str(text).translate(eng_to_nep)
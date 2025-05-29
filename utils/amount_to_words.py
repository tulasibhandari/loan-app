from nepali_number_to_word import convert_to_nepali_words

def convert_number_to_nepali_words(amount: int) ->str:
    try:
        return f"रु. {convert_to_nepali_words(amount)} मात्र"
    except Exception as e:
        print("❌ Error converting to words:", e)
        return ""
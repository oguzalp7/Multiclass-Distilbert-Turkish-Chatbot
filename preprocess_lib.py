import re
from unidecode import unidecode
# 1st step
def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)

# 2nd step
def remove_urls(text):
    return re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)



# 3rd step
def remove_punctuation(text):
    return re.sub(r'[^\w\s]', '', text)

# 4th step
def format_text(text):
    return unidecode(text)




# regex to extract phone numbers.
def contains_phone_number(text):
    pattern = r'\b(\+\d{1,3}\s?)?(0|\d{2})?\s?\d{3}[-.\s]?\d{3}[-.\s]?\d{2}[-.\s]?\d{2}\b'
    
    match = re.search(pattern, text)
    if match:
        return True
    else:
        return False
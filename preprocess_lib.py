import re
from unidecode import unidecode
from zemberek import (
    TurkishSpellChecker,
    TurkishSentenceNormalizer,
    TurkishSentenceExtractor,
    TurkishMorphology,
    TurkishTokenizer
)

# CREATE MORPHOLOGY INSTANCE
morphology = TurkishMorphology.create_with_defaults()

# SENTENCE NORMALIZATION
normalizer = TurkishSentenceNormalizer(morphology)

# SPELL CHECKER (GIVES WORD SUGGESTIONS)
sc = TurkishSpellChecker(morphology)

# SENTENCE EXTRACTOR
extractor = TurkishSentenceExtractor()

# WORD TOKENIZER
tokenizer = TurkishTokenizer.DEFAULT

# 1st step remove any emojis from text.
def remove_emojis(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)

# 2nd step remove urls from text.
def remove_urls(text):
    return re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)

# 3rd step remove punctuations.
def remove_punctuation(text):
    return re.sub(r'[^\w\s]', '', text)

# 4th step unidecode text so we don't have to worry Turkish specific characters (ex: ü,ö,ç,ş)
def format_text(text):
    return unidecode(text)

# 5th step split sentences if multiple sentence contains.
def tokenize_sentences(text):
    return extractor.from_paragraph(text)

# 6th step
def normalize_sentence(text):
    return normalizer.normalize(text)

def disambiguate(text):
    lemmatized_words = []
    stemmed_words = []
    analysis = morphology.analyze_sentence(text)
    after = morphology.disambiguate(text, analysis)
    for analysis in after.best_analysis():
        lemmatized_words.append(analysis.item.normalized_lemma())
        stemmed_words.append(analysis.get_stem())
    return lemmatized_words, stemmed_words


def jaccard_similarity(word1, word2):
    set1 = set(word1)
    set2 = set(word2)
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    jaccard_similarity = len(intersection) / len(union)
    return jaccard_similarity

def spell_suggester(word):
    jaccard_scores = []
    suggestions = list(sc.suggest_for_word(word))
    for suggestion in suggestions:
        jaccard_scores.append(jaccard_similarity(word, suggestion))

    return max(jaccard_scores)

def tokenize_word(text):
    for token in tokenizer.tokenize(text):
        yield token


# regex to extract phone numbers.
def contains_phone_number(text):
    pattern = r'\b(\+\d{1,3}\s?)?(0|\d{2})?\s?\d{3}[-.\s]?\d{3}[-.\s]?\d{2}[-.\s]?\d{2}\b'
    
    match = re.search(pattern, text)
    if match:
        return True
    else:
        return False
    

def preprocess_text(text):
    text = remove_emojis(text)
    text = remove_urls(text)
    sentences = tokenize_sentences(text)
    sentences = [remove_punctuation(sentence) for sentence in sentences]
    sentences = [normalize_sentence(sentence) for sentence in sentences]
    #sentences = [disambiguate(sentence) for sentence in sentences]
    for sentence in sentences:
        lemmas, roots = disambiguate(sentence)
        print(lemmas, roots)

def test():
    text = "Mart ayında düğünüm var. Saç ve makyaj fiyatlarınızı öğrenebilir miyim?"
    sentences = "sac ve mkyaj fiatlarınızı öğrenebilrmiym?"
    preprocess_text(sentences)

def test2():
    sentences = "sac ve mkyaj fiatlarınızı öğrenebilrmiym?"
    tokens = tokenize_word(sentences)
    for token in tokens:
        print('Content = ', token.content)
        print('Type = ', token.type_.name)
test()
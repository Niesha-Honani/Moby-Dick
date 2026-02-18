import nltk
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('stopwords')
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import pos_tag, WordNetLemmatizer, RegexpParser
from nltk.corpus import stopwords
from nltk import Tree
from collections import Counter

import re

START = 0
STOP = 20
WNL = WordNetLemmatizer()
# 1. Open and read the story text
with open('moby-dick.txt') as file_object:
    content = file_object.read()

# 2. (Optional) Remove :any unwanted characters using re.sub
# For example: remove extra whitespace or punctuation symbols
    clean_story = re.sub(r'\s+', ' ', content)
    clean_story = re.sub(r"([!.?])\1+", r"\1", clean_story)
    clean_story = re.sub(r"[^a-zA-Z\s.,'\"-]", '', clean_story)
    clean_story = re.sub(r'\d+', '', clean_story)

    # Keep common sentence characters
# 3. Tokenize the story io sentences
# TODO: Replace the line below with a call to sent_tokenize
    sentences = sent_tokenize(clean_story)

    print("sentences tokenized \n", sentences[0]) 

# 4. Tokenize the story into words
# TODO: Replace the line below with a call to word_tokenize
    words = []
    for sentence in sentences:
        words.append(word_tokenize(sentence))

    total_word_token = sum(len(word) for word in words)

    all_tokens = [token for sentence in words for token in sentence]

#3 Stopwords
# Book List: Sentences each index is a list of Sentence : Words: each index Lists of words)    
    stop_words = set(stopwords.words("english"))
    stop_words_removed = [word for word in all_tokens if word.lower() not in stop_words]
    print(len(stop_words_removed))

# 4 POS tagging
    pos_tokens = pos_tag(stop_words_removed)

# 5 Lemmatization
lemonstolemon = [WNL.lemmatize(word) for word, tag in pos_tokens]

# 6 Chunking
chunk_grammar = r"""
NP: {<DT>?<JJ.*>*<NN.*>+}
VP: {<VB.*><NP|PP|CLAUSE>*}
"""
parser = RegexpParser(chunk_grammar)
chunk = parser.parse(pos_tokens)


def extract_and_count_phrases(chunked_sentences, phrase_label='NP', top_n=10):
    phrases = []
    for tree in chunked_sentences:
        if isinstance(tree, Tree):
            for subtree in tree.subtrees(filter=lambda t: t.label() == phrase_label):
                phrase = " ".join([word for word, tag in subtree.leaves()])
                phrases.append(phrase)
    
    phrase_counts = Counter(phrases)
    return phrase_counts.most_common(top_n)


print('New stuff:\n', lemonstolemon[0:20])
print("POST tagged words:\n", pos_tokens[0])
print("Lemmatize:\n", pos_tokens[0:20])
print("Chunked:\n", chunk[0:20])

print(extract_and_count_phrases(chunk[0:20]))

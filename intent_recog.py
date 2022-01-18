from spacy.matcher import Matcher
from qa_system import nlp

basic_modal_verbs = ["do", "have", "be", "will", "should", "can", "must"]
question_words = ["what", "where", "when", "who", "how"]
# about the word WHY: it should be processed another more complex way

# question types:
# with unknown subj (like what, which, who)
# how + adj (how fast, how long) *
# complex with AND (when and where)
# what + noun (what time, what type) *
# simple yes/no (do, be, have, modal verbs + noun) *
# (when where why how) + (do, be, have, modal verbs) + noun *
# tag questions

# types of questions
# how(many, much, old, long), who, what(time), why, where, whose, whom, have(all forms)
# do(all forms), be(all forms), would, will, can, should, shall
#todo:
# WILL BE, WILL BE ABLE
# WHAT TO DO WITH THEM?


matcher = Matcher(nlp.vocab)
#todo: What AND WHEN did you do? like when we have 2 questions in one
matcher = Matcher(nlp.vocab)
pattern = [  # verb
    {"LOWER": {"IN": question_words}},
    {"_": {"lemma": {"IN": basic_modal_verbs}}},
    {"LEMMA": "not", "OP": "?"},
    {"POS": {"IN": ["NOUN", "PRON"]}}
]
matcher.add("W-QUESTIONS", None, pattern)

pattern = [  # UNKNOWN OBJECT OR VERB
    {"LOWER": {"IN": question_words}},
    {"LEMMA": "not", "OP": "?"},
    {"LOWER": "to"},
    {"POS": "VERB"}
]
matcher.add("OBJorVB", None, pattern)

pattern = [  # SUBJECT
    {"LOWER": {"IN": ["what", "who"]}},
    {"_": {"lemma": {"IN": basic_modal_verbs}}},
    {"LEMMA": "not", "OP": "?"},
    {"POS": {"NOT_IN": ["NOUN", "PRON"]}}
]
matcher.add("SUBJECT", None, pattern)

pattern = [  # yes no
    {"_": {"lemma": {"IN": basic_modal_verbs}}},
    {"LEMMA": "not", "OP": "?"},
    {"LOWER": {"IN": ["the", "a"]}, "OP": "?"},
    {"POS": {"IN": ["NOUN", "PRON", "ADJ", "DET"]}}
]
matcher.add("YesNo", None, pattern)

pattern = [  # additional property
    {"LOWER": {"IN": ["what", "which"]}},
    {"LOWER": "of", "OP": "?"},
    {"LOWER": {"IN": ["the", "a"]}, "OP": "?"},
    {"POS": {"IN": ["NOUN", "PRON"]}},
    {"_": {"lemma": {"IN": basic_modal_verbs}}}  # ,
    # {"DEP": "nsubj"}
]
matcher.add("PROPERTY", None, pattern)

# pattern = [
#            {"LOWER": {"IN": ["what", "who"]}},
#            {"_": {"lemma":{"IN": basicNmodal}}},
#            {"LOWER": "not", "OP":"?"},
#            {"POS": {"NOT_IN": ["NOUN", "PRON"]}}
#          ]
# matcher.add("OBJECT", None, pattern)

pattern = [  # quality
    {"LOWER": "how"},
    {"POS": {"IN": ["ADJ", "ADV"]}},
    {"POS": "ADJ", "OP": "?"},
    {"POS": "NOUN", "OP": "?"},
    {"_": {"lemma": {"IN": basic_modal_verbs}}},
    {"LEMMA": "not", "OP": "?"},
    {"DEP": "nsubj"}
]
matcher.add("QUALITY", None, pattern)



from nltk import word_tokenize, pos_tag


def get_max_value_key(dict):
    m = max(j for j in dict.values())
    for i, j in dict.items():
        if j == m:
            return i


def get_sentence_tense(sentence):
    text = word_tokenize(sentence)
    tagged = pos_tag(text)

    tense = {}
    tense["future"] = len([word for word in tagged if word[1] == "MD"])
    tense["present"] = len(
        [word for word in tagged if word[1] in ["VBP", "VBZ", "VBG"]]
    )
    tense["past"] = len([word for word in tagged if word[1] in ["VBD", "VBN"]])

    return get_max_value_key(tense)


options = {"who": "person", "what": "object", "what do do": "verb", "what have": "result", "why": "reason",
           "have": "result", "do do": "simple", "do": "simple do", "be": "simple be", "would": "probable",
           "might": "probable", "can": "ability", "what be do": "verb",
           "how be": "state", "how many": "quantity", "how": "quality", "how do": "way"}


def get_precise_intent(question):
    # we will consider the first word of a question as an intent

    # tense extraction (will, did, verb(ed), verb
    doc = question
    quest = doc[0]._.lemma
    if (doc[1]._.lemma) in ("do", "have", "be"):
        quest = quest + ' ' + doc[1]._.lemma
        if doc[2]._.lemma == "-PRON-" and doc[3]._.lemma == "do":
            quest = quest + ' ' + doc[3]._.lemma
    return options.get(quest, "not a question")


def get_question_intent(question):
    matches = matcher(question)
    return matches


def intent_to_str(matches):
    q_intent = nlp.vocab[matches[0][0]]
    return q_intent.text


from unittest import TestCase


class IntentTest(TestCase):
    def test(self):
        self.assertEqual(get_question_intent("Has he done it?"), "result")
        self.assertEqual(get_question_intent("What did he do?"), "verb")
        self.assertEqual(get_question_intent("Are you a boy?"), "simple be")
        self.assertEqual(get_question_intent("Can you do it?"), "ability")

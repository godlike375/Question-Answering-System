from qa_system import QASystem
import intent_recog
import spacy
import preprocess
from spacy.matcher import Matcher
from qa_system import nlp
from spacy.tokens import Token
llemma = lambda token: token.lemma_.lower()
# if token.lemma_.lower()!="'s" else  "be"
Token.set_extension("lemma", getter=llemma)
import pyinflect

'''
#from googletrans import Translator
#translator = Translator()
#print(translator.translate('안녕하세요.').text)
'''

#todo:
# there should be the history of text changing
# word.history[0] - the previous state of this lexeme
# for example print(word, word.history[0]) >>> amazing, amazong
# for deleted words: print(word) >>> ''
# Since we know that adding a field in an object is easy, we may add history later and now concentrate on the core functions
# let's assume that we have a clear input now


questions = [
    "How many money will it take?",
    "How fast will it take?",
    "What is the crazy thing you are doing?",
    "What is this?",
    "Who was there",
    "What are you doing?",
    "Where should you go?",
    "What is the purpose?",
    "Which person was trere?",
    "What is going on?",
    "Which one is better?",
    "What time is it?",
    "What will be there?",
    "Are you ready?",
    "What to do?",
    "What is going on?",
    "Can't it make sounds?"
    ]



for q in questions:
    doc = nlp(q)
    for i in doc:
        print(intent_recog.get_precise_intent(doc), end=' ')
        print(intent_recog.intent_to_str(intent_recog.get_question_intent(doc)), end=' ')
        print("{"+i._.lemma, i.dep_, i.pos_, i.tag_+ "}", end=' ')
    print()

qa = QASystem()

import searcher
#print(searcher.compare_secondary(nlp("There will be a celebration in my city tomorrow."), nlp("What will be in my city tomorrow?")))

print(qa.find_answers(["There will be a celebration in my city tomorrow."], ["What will be in my city tomorrow?"]))
print(qa.find_answers(["There will be a celebration in my city tomorrow."], ["When will a celebration in my city be?"]))
print(qa.find_answers(["There will be a celebration in my city tomorrow."], ["Where will be a celebration tomorrow?"]))

#print(qa.ask(["The cat was searching for some food on the street yesterday."], ["Who was searching for something yesterday?"]))
#print(qa.ask(["The cat was searching for some food on the street yesterday."], ["Who was searching for something yesterday?"]))

from unittest import TestCase


class MainTest(TestCase):
    def test(self):
        self.assertEqual(qa.find_answers(["It's a cat. It makes sounds."], ["Does it make sounds?", "Can't it make sounds?"]))
        self.assertEqual(qa.find_answers(["It's a cat. It can't make sounds."], ["Can't it make sounds?", "Can it make sounds?"]))
        self.assertEqual(qa.find_answers(["It's a cat. It can make sounds."], ["Can't it make sounds?"]))
        self.assertEqual(qa.find_answers(["It's, a cat. It can't make sounds."], ["Can it make sounds?"]))


#print(qa.ask(["It's a cat. It makes sounds."], ["Does it make sounds?", "Can't it make sounds?"]))
#print(qa.ask(["It's a cat. It can't make sounds."], ["Can't it make sounds?", "Can it make sounds?"]))
#print(qa.ask(["It's a cat. It can make sounds."], ["Can't it make sounds?"]))
#print(qa.ask(["It's, a cat. It can't make sounds."], ["Can it make sounds?"]))


'''
import nltk
#nltk.download('nps_chat')

import nltk.corpus
from nltk.corpus import nps_chat
from nltk.tokenize import TweetTokenizer
'''

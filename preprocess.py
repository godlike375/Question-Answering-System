# replaces shorting with the full words: ofc => of course and so on
from cleantext import clean
import language_check
import nltk
from qa_system import nlp
from intent_recog import basic_modal_verbs
tool = language_check.LanguageTool('en-US')


#? mark is not necessary for being presented in questions


def clean_replace(text):
    return clean(text,
              fix_unicode=True,  # fix various unicode errors
              to_ascii=True,  # transliterate to closest ASCII representation
              lower=False,  # lowercase text
              no_line_breaks=False,  # fully strip line breaks as opposed to only normalizing them
              no_urls=False,  # replace all URLs with a special token
              no_emails=False,  # replace all email addresses with a special token
              no_phone_numbers=False,  # replace all phone numbers with a special token
              no_numbers=False,  # replace all numbers with a special token
              no_digits=False,  # replace all digits with a special token
              no_currency_symbols=False,  # replace all currency symbols with a special token
              no_punct=False,  # fully remove punctuation
              replace_with_url="<URL>",
              replace_with_email="<EMAIL>",
              replace_with_phone_number="<PHONE>",
              replace_with_number="<NUMBER>",
              replace_with_digit="0",
              replace_with_currency_symbol="<CUR>",
              lang="en"  # set to 'de' for German special handling
                 )

def fix_grammar_mistakes(text):
    solutions = tool.check(text)
    for s in solutions:
        text = text[0:s.fromx]+s.replacements[0]+text[s.tox:]
    #print("debug \n ", text)
    return text

    #todo: some abbriveations may be considered as mistakes but they are not
    # so we should use NER and abbr resolver for misspelling type of mistakes
    # boundary detector should be the first pipe for information, it should process the information and send the sentences to abbr resolver, abbr resolver returns some options for every shorting and sends the sentences with resolved abbriveations next to grammar check, then evolution artificial selection happens for every set of abbreviations and sentence boundaries and the best item is found
def split_sentences(text):
    # we pick our first and only sentence
    # only_sentence = doc.sentences[0]
    sentences = nltk.sent_tokenize(text)
    for i in range(len(sentences)):
        if sentences[i][-1] not in ('.', '?', '!'):
            sentences[i] = sentences[i] + '.'
    return sentences

def simplify(text):
    #todo: Here should be methods to make complex text simpler for further processing
    pass

replacements = {"has to" : "has", "have to" : "have", "can't" : "can not",
                "doesn't":"does not", "don't":"do not", "hasn't": "has not",
                "haven't":"have not"} #, "'s" : " is"}

def replace_nt(word):
    if word== "can't":
        return "can not"
    elif word== "won't":
        return "will not"
    elif word[len(word)-4:len(word)-1] == "n't":
        return word[:len(word)-4] + "not"
    else:
        return word


def normalize(text):
    #todo: replace has/have froms to => has
    words = text.split()
    for i in range(len(words)):
        words[i] = replace_nt(words[i])
    text = ' '.join(words)
    doc = nlp(text)
    words = nltk.word_tokenize(text)

    if len(words)!= len(doc):
        raise ValueError('the length of 2 lists isn\'t the same as expected')
    for i in range(len(words)):
        tup = (words[i], doc[i])
        words[i] = tup

    j = 0
    while j<(len(words)-1):
        i = words[j][1]
        p = words[j-1][1]
        if p._.lemma not in basic_modal_verbs and p._.lemma!= "not":
            if i.tag_ == "VBZ" and i._.lemma not in basic_modal_verbs:
                words[j] = (i._.lemma, nlp(i._.lemma)[0])
                words.insert(j, ("does", nlp("does")[0]))
            elif i.tag_ == "VB" and i._.lemma not in basic_modal_verbs:
                words[j] = (i._.lemma, nlp(i._.lemma)[0])
                words.insert(j, ("do",nlp("do")[0]))
        j = j + 1

    text = ' '.join([i[0] for i in words])
    print(text)
    return text

    #todo: here should be some normalization things like adding do/does after subjects and so on
    pass

def find_abbreviations(text):
    #todo: here should be a vocabulary that contains them and may be extented with time
    #todo: abbriveations should be checked as the most fitable to the current context by using word embendings
    return text

def find_coreferences(text):
    doc = nlp(text)
    print(doc._.coref_clusters)
    #for ent in doc2.ents:
    #    print(ent._.coref_cluster)
    return text
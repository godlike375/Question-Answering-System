from qa_system import nlp
import intent_recog


def get_simple_question_answer(texts, q):
    nsubj = find_word_by_role("nsubj", q)
    root = find_word_by_role("ROOT", q)
    if root._.lemma != "be":  # needs to find a verb
        for doc in texts:
            for s in doc.sents:
                # for i in s:
                nsubj2 = find_word_by_role("nsubj", s)
                if nsubj2._.lemma == nsubj._.lemma:
                    root2 = find_word_by_role("ROOT", s)
                    if root2._.lemma == root._.lemma:
                        if is_negotiated(find_word_by_role("aux", q), q) == is_negotiated(find_word_by_role("aux", s), s):
                            return "yes"
                        else:
                            return "no"
            # if i._.lemma == root._.lemma:
            # for j in s:
            # if j._.lemma == nsubj._.lemma:
            # if negotiated(find("aux", q), q) == negotiated(find("aux", s), s):
            # return "yes"
            # else:
            # return "no"


def compare_secondary_members(text, q):
    matched = []
    for i in text:
        for j in q:
            if i.dep_ == j.dep_:
                matched.append((i, j))

    return matched


def get_complex_question_answer(texts, q, dep):
    # if we find similar words besides nsubj, we start searching for nsubj and return it
    for doc in texts:
        for s in doc.sents:
            nsubj = find_word_by_role(dep, s)
    return nsubj.text


processing_funcs = {"YesNo": get_simple_question_answer, "W-QUESTIONS": get_complex_question_answer}


def find_word_by_role(dep, doc):
    for i in doc:
        if i.dep_ == dep:
            return i
    return False


def is_negotiated(token, doc):
    for i in range(len(doc)):
        t = doc[i]
        if t.text == token.text:
            return doc[i + 1]._.lemma == "not"
    return False


#todo:
# it seems the information for searching there should be labeled like
# every token should have as much as possible information about it
def search_answer(texts, q):
    q_intent = intent_recog.intent_to_str(intent_recog.get_question_intent(q))
    if q_intent == "W-QUESTIONS":
        precise = intent_recog.get_precise_intent(q)
        if precise == "person":
            tag = "nsubj"
            get_complex_question_answer(texts, q, tag)
    # elif precise == "object":

    # print(q_intent.text)
    return processing_funcs[q_intent](texts, q)

#todo:
# if question.intent == "person" or "place":
# use NER with special parameters
#	pass
# some sentences, that we've processed already we don't have to process again, just maybe skip them

'''
# print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])

# find synonims
# from nltk.corpus import wordnet
# wordnet.synsets("application")[0]

# Find named entities, phrases and concepts
def find_entity(doc, intent):
    for entity in doc.ents:
        if entity.label_ == intent:
            return entity
# print(entity.text, entity.label_)

# the simmilarity between the words
# for token1 in tokens:
#    for token2 in tokens:
#        print(token1.text, token2.text, token1.similarity(token2))
'''
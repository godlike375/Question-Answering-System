import spacy
import neuralcoref

from qa_system import nlp

# nlp = spacy.load("en")
# neuralcoref.add_to_pipe(nlp)
doc1 = nlp(
    "Tom and Jane are good friends. They are cool. He knows a lot of things and so does she. His car is red, but her car is blue. It is older than her car. The big cat ate its dinner.")
print(doc1._.coref_clusters)

doc2 = nlp('Angela lives in Boston. She is quite happy in the town.')

for ent in doc2.ents:
    print(ent._.coref_cluster)

    doc = nlp(
        "displaCy uses CSS and JavaScript to show you how computers "
        "understand language"
    )
print("debug````````")
# The easiest way is to find the head of the subtree you want, and then use
# the `.subtree`, `.children`, `.lefts` and `.rights` iterators. `.subtree`
# is the one that does what you're asking for most directly:
for word in doc:
    if word.dep_ in ("xcomp", "ccomp"):
        print("".join(w.text_with_ws for w in word.subtree))
print("debug````````")

text = ("When Sebastian Thrun started working on self-driving cars at "
        "Google in 2007, few people outside of the company took him "
        "seriously. “I can tell you very senior CEOs of major American "
        "car companies would shake my hand and turn away because I wasn’t "
        "worth talking to,” said Thrun, in an interview with Recode earlier "
        "this week.")
doc = nlp(text)

# Analyze syntax
print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

# Find named entities, phrases and concepts
for entity in doc.ents:
    print(entity.text, entity.label_)

tokens = nlp("dog cat banana")

for token1 in tokens:
    for token2 in tokens:
        print(token1.text, token2.text, token1.similarity(token2))

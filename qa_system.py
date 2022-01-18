import spacy
import neuralcoref

nlp = spacy.load("en_core_web_sm")
neuralcoref.add_to_pipe(nlp)
import searcher
import preprocess


class QASystem:
    def __init__(self):
        print("the system is running")

    def run(self):
        texts, questions = self.manual_input()
        self.find_answers(texts, questions)

    def find_answers(self, texts, questions):
        proc_docs = []
        for text in texts:
            proc_docs.append(nlp(
                preprocess.normalize(self.preprocess_text(text))
            ))

        proc_quests = []
        for quest in questions:
            proc_quests.append(nlp(self.preprocess_text(quest)))

        answers = []
        for q in proc_quests:
            answers.append(searcher.search_answer(proc_docs, q))
        return answers

    def preprocess_text(self, text):
        text = preprocess.clean_replace(text)
        sentences = preprocess.split_sentences(text)

        for i in range(len(sentences)):
            sentences[i] = preprocess.fix_grammar_mistakes(sentences[i])
            # add checking if it's a question and use the question mark there

        text = ' '.join(sentences)
        # abbriveations (not necessary now)
        # idioms (not necessary now)
        return text

    def manual_input(self):
        texts = []
        texts.append(input('input a text'))
        questions = []
        question = input('input questions')
        while question != '':
            questions.append(question)
            question = input('input the next question or enter')
        return (texts, questions)

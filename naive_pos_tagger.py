from typing import List

class NaivePOSTagger:

    def __init__(self, p_words_to_tags):

        self.p_words_to_tags = p_words_to_tags

    def tag(self, sentences: List[List[str]]):

        tagged_sentences = []

        for s in sentences:

            tagged_sentence = []

            for word in s:

                # get the most likely tag for the word
                if word in self.p_words_to_tags:

                    max_prob = 0
                    maximizing_tag = None

                    for t, p in self.p_words_to_tags[word].items():

                        if p > max_prob:
                            max_prob = p
                            maximizing_tag = t

                    tagged_sentence.append((word, maximizing_tag))

                else:
                    tagged_sentence.append((word, "?"))

            tagged_sentences.append(tagged_sentence)

        return tagged_sentences

from typing import List

class HMMPosTagger:

    def __init__(self, p_tags_to_words, p_tags_to_tags):

        self.p_tags_to_words = p_tags_to_words
        self.p_tags_to_tags = p_tags_to_tags

        self.tags = sorted(p_tags_to_tags.keys())

        self.tags = list(filter(lambda t: t != "START", self.tags))

    def _tag(self, sentence):

        assert len(sentence) > 0 and not isinstance(sentence[0], tuple), "needs to be unlabeled data"

        P = [[0 for t in self.tags] for _ in range(len(sentence) + 1)]

        for i, t in enumerate(self.tags):
            P[0][i] = self.p_tags_to_tags["START"][t]

        backlinks = dict()

        highest_end_probability = 0
        entry_point = None

        unknown_word_at = set()

        for word_idx in range(1, len(sentence) + 1):

            word = sentence[word_idx-1]

            for tag_idx, tag in enumerate(self.tags):

                for last_tag_idx, last_tag in enumerate(self.tags):

                    tr_prob = P[word_idx - 1][last_tag_idx] * self.p_tags_to_tags[last_tag][tag]

                    if word in self.p_tags_to_words[tag]:
                        emit_prob = self.p_tags_to_words[tag][word]
                    else:
                        unknown_word_at.add(word_idx-1)
                        emit_prob = 1e-3
                    
                    prob = tr_prob * emit_prob

                    if prob >= P[word_idx][tag_idx]:
                        P[word_idx][tag_idx] = prob
                        backlinks[(word_idx, tag_idx)] = (word_idx-1, last_tag_idx)

                        if word_idx == len(sentence) and prob >= highest_end_probability:
                            entry_point = (word_idx, tag_idx)
                            highest_end_probability = prob



        # reconstruct the most likely sequence using the backlinks
        most_likely_sequence_reversed = []

        curr = entry_point

        while curr in backlinks:

            word_idx, tag_idx = curr

            most_likely_sequence_reversed.append(self.tags[tag_idx])

            curr = backlinks[curr]

        most_likely = most_likely_sequence_reversed[::-1]

        for u_idx in unknown_word_at:

            if 0<= u_idx < len(most_likely):
                most_likely[u_idx] = "?"

        return most_likely

    def tag(self, sentences: List[List[str]]):

        res = []

        for s in sentences:

            pred = self._tag(s)

            if len(pred) != len(s):
                res.append(list(zip(s, ["?"] * len(s))))

            else:
                res.append(list(zip(s, pred)))

        return res
from nltk.corpus import treebank
from utils import *
from naive_pos_tagger import NaivePOSTagger
from hmm_pos_tagger import HMMPosTagger
import pickle

# Load the tagged sentences
tagged_sentences = list(treebank.tagged_sents())

train_sentences, test_sentences = random_train_test_split(tagged_sentences, train_ratio=0.8)

p_words_to_tags, p_tags_to_tags, p_tags_to_words, words, tags = get_probs_tables(train_sentences)

print(tags)

naive_tagger = NaivePOSTagger(p_words_to_tags=p_words_to_tags)

hmm_tagger = HMMPosTagger(p_tags_to_words=p_tags_to_words, p_tags_to_tags=p_tags_to_tags)


#with open('hmm_tagger.pkl', 'wb') as file:
#    pickle.dump(hmm_tagger, file)

#with open('naive_tagger.pkl', 'wb') as file:
#    pickle.dump(naive_tagger, file)

#acc_hmm, errors = get_acc_on_test_set(hmm_tagger, test_sentences[:1000])

#acc_naive, errors = get_acc_on_test_set(naive_tagger, test_sentences[:1000])

#print(f"acc HMM: {acc_hmm}, acc NAIVE: {acc_naive}")

#print("Errors Naive Tagger")

#for e in errors[:10]:
#    print(e)

#print("What HMM Tagger says")

res = naive_tagger.tag(split_into_sentences("He sees the homeless"))

print(res)




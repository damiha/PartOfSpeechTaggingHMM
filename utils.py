import random
import numpy as np
import re

def split_into_sentences(text):
    # Split the text into sentences using punctuation symbols as delimiters
    sentences = re.split(r'[.!?]', text)
    
    # Remove empty sentences
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    
    result = []
    
    for sentence in sentences:
        # Split each sentence into words and special symbols
        words_and_symbols = re.findall(r'\b\w+\b|[^\w\s]', sentence)
        
        # Filter out empty items
        words_and_symbols = [item for item in words_and_symbols if item.strip()]
        
        result.append(words_and_symbols)
    
    return result

def random_train_test_split(sentences, train_ratio=0.8):

    n = len(sentences)
    randomly_shuffled = random.sample(sentences, n)

    train_size = int(n * train_ratio)
    test_size = n - train_size

    train_set = randomly_shuffled[:train_size]
    test_set = randomly_shuffled[test_size:]

    return train_set, test_set

def get_probs_tables(sentences, verbose=True):

    # get dimensions
    words = set()
    tags = set()

    for s in sentences:
        for word, tag in s:
            words.add(word)
            tags.add(tag)

    n_words = len(words)
    n_tags = len(tags)

    print(f"There are {n_words} words and {n_tags} categories in the dataset.")

    # for each word, how likely in the different categories
    counts_words_to_tags = { w: { t: 0 for t in tags } for w in words }

    # for each tag, how likely to another tag
    counts_tags_to_tags = { t : { tp: 0 for tp in tags } for t in tags }

    counts_tags_to_tags["START"] = {t: 0 for t in tags}

    counts_tags_to_words = {t : { w: 0 for w in words} for t in tags}

    for s in sentences:

        last_tag = "START"

        for word, tag in s:

            counts_words_to_tags[word][tag] += 1
            counts_tags_to_words[tag][word] += 1

            counts_tags_to_tags[last_tag][tag] += 1

            last_tag = tag

    # normalize WORDS -> TAG
    for word in counts_words_to_tags.keys():

        tags_total = sum(counts_words_to_tags[word].values())

        for tag in counts_words_to_tags[word].keys():

            counts_words_to_tags[word][tag] /= tags_total

    # normalize TAG -> WORD
    for tag in counts_tags_to_words.keys():

        words_total = sum(counts_tags_to_words[tag].values())

        assert len(counts_tags_to_words[tag].keys()) == n_words

        for word in counts_tags_to_words[tag].keys():

            counts_tags_to_words[tag][word] /= words_total

    # normalize TAG -> TAG
    for tag in counts_tags_to_tags.keys():

        next_tags_total = sum(counts_tags_to_tags[tag].values())

        for ntag in counts_tags_to_tags[tag].keys():

            counts_tags_to_tags[tag][ntag] /= next_tags_total

    p_words_to_tags = counts_words_to_tags
    p_tags_to_tags = counts_tags_to_tags
    p_tags_to_words = counts_tags_to_words

    return p_words_to_tags, p_tags_to_tags, p_tags_to_words, words, tags

def get_acc_on_test_set(tagger, test_set, verbose=True):

    unlabeled_test_set = []

    for s in test_set:

        unlabeled_test_set.append(list(map(lambda x: x[0], s)))

    pred_test_set = tagger.tag(unlabeled_test_set)

    # total guesses
    n_total = 0

    # total correct guesses
    c_total = 0

    errors = []

    for idx, s in enumerate(test_set):

        pred_sentence = pred_test_set[idx]

        for i, (w, t) in enumerate(s):

            p = pred_sentence[i][1]
            
            if p == t:
                c_total += 1
            else:
                errors.append({"s_idx": idx, "word": w, "pred": p, "true": t})

            n_total += 1

    acc = c_total / n_total

    return acc, errors

def unlabel(sentences):
    
    unlabeled_sentences = []

    for s in sentences:
        
        unlabeled_sentences.append(list(map(lambda x: x[0], s)))

    return unlabeled_sentences

def show_results(labeled_data, tagger):

    unlabeled_data = unlabel(labeled_data)

    pred = tagger.tag(unlabeled_data)

    for idx, s in enumerate(labeled_data):

        pred_sentence = pred[idx]

        for i, (w, t) in enumerate(s):

            print(f"{w} ==> pred: {pred_sentence[i][1]}, true: {t}")


            


    



    
    
    
    
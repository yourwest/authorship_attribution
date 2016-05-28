__author__ = 'angelinaprisyazhnaya'

import re
import csv
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')

all_files = ['./tweets/dasha_v_kabake_tweets.csv',
             './tweets/feeling_so_real_tweets.csv',
             './tweets/electroeb_tweets.csv']


def text_to_words(text):
    text = re.sub('[1-9a-zA-Z]|0|#|,|\.|\{|:|\(|\)|\}|\]|\[|;|=|&|\||!|\?|"|\'|/|_|»|«|–|-|—|\*|©|•|@|\+|❤|☔', '', text)
    sentences = re.split(r'(?:[.]\s*){3}|[.?!]', text)
    return sentences


def word(sentence):
    return sentence.lower().split()


def collect_tweets(file):
    tweets = []
    f = open(file, 'r', encoding='utf8')
    f = f.read()
    csv_iter = csv.reader(f.split('\n'), delimiter=',')
    for row in csv_iter:
        if not row == []:
            tweets.append(row[2])
    return tweets


def collect_ngrams(*args):
    all_texts = ''
    trigrams = set()
    trigrams_dict = dict()
    for array in args:
        for tweet in array:
            if not tweet == '':
                for sent in text_to_words(tweet):
                    for w in word(sent):
                        all_texts += w
                        all_texts += ' '
                        stripped_word = w.strip('(»),*;&-»/…&”$:--/“«')
                        if len(stripped_word) >= 2:
                            if len(stripped_word) == 2:
                                trigrams.add(stripped_word)
                                if stripped_word not in trigrams_dict:
                                    trigrams_dict[stripped_word] = [w]
                                else:
                                    trigrams_dict[stripped_word].append(w)
                            else:
                                s = 0
                                for i in range(2, len(stripped_word) + 1):
                                    trigrams.add(stripped_word[s:i])
                                    if stripped_word[s:i] not in trigrams_dict:
                                        trigrams_dict[stripped_word[s:i]] = [w]
                                    else:
                                        trigrams_dict[stripped_word[s:i]].append(w)
                                    s += 1
    #for i in trigrams_dict:
        #if len(trigrams_dict[i]) <= 10:
            #print(i + ':' + str(trigrams_dict[i]))

    return trigrams_dict, all_texts


def find_frequent_trigrams(trigrams_dict, texts):
    freqs = []
    final_trigrams = []
    final_trigrams_dict = {}
    final_words = set()
    for trigram in trigrams_dict:
        find = re.findall(trigram, texts, flags=re.DOTALL)
        amount = len(find)
        freq = amount / len(texts.split())
        freqs.append(freq)
        if freq > 0.001:
            final_trigrams.append(trigram)
            final_trigrams_dict[trigram] = trigrams_dict[trigram]
            for i in final_trigrams_dict[trigram]:
                final_words.add(i)
    plt.plot(sorted(freqs))
    plt.xlabel('Число n-грамм')
    plt.ylabel('Частота n-грамм')
    plt.show()
    #for i in trigrams_dict:
        #print(i + str(trigrams_dict[i]))
    return final_trigrams_dict, final_words


def find_frequent_words(texts):
    freqs = dict()
    all_words = texts.split()
    frequent_words = set()
    for w in set(all_words):
        find = re.findall(w, texts, flags=re.DOTALL)
        amount = len(find)
        freq = amount / len(all_words)
        freqs[w] = freq
        if freq > 0.002:
            frequent_words.add(w)
    #plt.plot(sorted(freqs.values()))
    #plt.show()
    return frequent_words


def count_trigrams(tweet, trigrams):
    d = {}
    for trigram in trigrams:
        trigram = re.sub('([)(-*])', '\\' + '\1', trigram)
        finds = re.findall(trigram, tweet, flags=re.DOTALL)
        c = len(finds)
        if trigram not in d:
            d[trigram] = c
        else:
            d[trigram] += c

    for i in d:
        d[i] /= len(tweet.split())

    return d


def collect_data(tweets, author, ngrams, conjs, parenthesis):
    data_train = []
    data_test = []
    l = len(tweets) - 1
    test_numbers = random.sample(range(l), 200)
    print(test_numbers)
    counter = 0
    for tweet in tweets:
        if not tweet == '':
            file_data = [str(author)]

            # Записывает частоты n-грамм
            d = count_trigrams(tweet, ngrams)
            for i in d:
                file_data.append(d[i])

            #Записывает частоты союзов
            conj_freqs = []
            for conj in conjs:
                finds = re.findall(' ' + conj + ' ', tweet, flags=re.DOTALL)
                freq = len(finds) / len(tweet.split())
                conj_freqs.append(freq)
            for i in conj_freqs:
                file_data.append(i)

            #Записывает вводных слов
            parenthesis_freqs = []
            for par in parenthesis:
                finds = re.findall(par, tweet, flags=re.DOTALL)
                freq = len(finds) / len(tweet.split())
                parenthesis_freqs.append(freq)
            #for i in parenthesis_freqs:
                #file_data.append(i)

            #Записывает частоту запятых
            finds = re.findall(',', tweet, flags=re.DOTALL)
            commas_freq = len(finds) / len(tweet.split())
            file_data.append(commas_freq)

            #Записывает частоту восклицательных знаков
            finds = re.findall('!', tweet, flags=re.DOTALL)
            exclamation_freq = len(finds) / len(tweet.split())
            file_data.append(exclamation_freq)

            #Записывает частоту вопросительных знаков
            finds = re.findall('\?', tweet, flags=re.DOTALL)
            question_freq = len(finds) / len(tweet.split())
            file_data.append(question_freq)

            #Записывает среднюю длину предложений (в словах)
            sent = re.split('\.|!|\?|…', tweet, flags=re.DOTALL)
            ls = []
            for i in sent:
                ls.append(len(i.split()))
            file_data.append(np.mean(ls))

            #Записывает количество предложений
            file_data.append(len(sent))

            if counter in test_numbers:
                data_test.append(file_data)
            else:
                data_train.append(file_data)
        counter += 1
    return data_train, data_test


conjunctions = open('conjunctions.txt', 'r', encoding='utf8')
conjs = []
for line in conjunctions:
    conjs.append(line.replace('\n', ''))

prnthss = open('parenthesis.txt', 'r', encoding='utf8')
parenthesis = []
for line in prnthss:
    parenthesis.append(line.replace('\n', ''))

tweets_1 = collect_tweets(all_files[0])
tweets_2 = collect_tweets(all_files[1])
tweets_3 = collect_tweets(all_files[2])

all_trigrams, all_texts = collect_ngrams(tweets_1, tweets_2, tweets_3)
frequent_trigrams, trigrams_words = find_frequent_trigrams(all_trigrams, all_texts)
all_trigrams_list = list(all_trigrams.keys())
frequent_trigrams_list = list(frequent_trigrams.keys())
print(len(all_trigrams_list))
print(len(frequent_trigrams_list))


train_1, test_1 = collect_data(tweets_1, 1, frequent_trigrams_list, conjs, parenthesis)
train_2, test_2 = collect_data(tweets_2, 2, frequent_trigrams_list, conjs, parenthesis)
train_3, test_3 = collect_data(tweets_3, 3, frequent_trigrams_list, conjs, parenthesis)


def write_data():
    data = open('data_tweets.csv', 'w', encoding='utf-8')
    all_data = np.vstack((train_1, train_2, train_3))
    for k in all_data:
        for l in k:
            data.write(str(l) + ';')
        data.write('\r\n')
    data.close()


def write_test_data():
    data_test = open('data_test_tweets.csv', 'w', encoding='utf-8')
    all_data_test = np.vstack((test_1, test_2, test_3))
    for k in all_data_test:
        for l in k:
            data_test.write(str(l) + ';')
        data_test.write('\r\n')
    data_test.close()

write_data()
write_test_data()



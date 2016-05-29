__author__ = 'angelinaprisyazhnaya'

import re
import os
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')

# Два или три потенциальных автора (ID меняются).
all_paths = ['./slon/37648/', './slon/817/'] #, './slon/39477/']


def text_to_words(text):
    text = re.sub('[1-9a-zA-Z]|0|#|,|\.|\{|:|\(|\)|\}|\]|\[|;|=|&|\||!|\?|"|\'|/|\\\|_|»|«|–|-|—|\*|@|\+|%%|…|”|“', '', text)
    sentences = re.split(r'(?:[.]\s*){3}|[.?!]', text)
    return sentences


def word(sentence):
    return sentence.lower().split()


def collect_paths():
    paths = []
    for root, dirs, files in os.walk('.'):
        for fil in files:
            if fil.endswith('txt'):
                paths.append(root + '/' + fil)
    return paths

# Здесь и дальше в названиях функциях и переменных написано "trigrams", но имеются в виду
# и биграммы тоже (если в строках 50, 51 и 59 поменять 3 на 2).
def collect_trigrams(paths):
    all_texts = ''
    trigrams = set()
    trigrams_dict = dict()
    for path in paths:
        files = os.listdir(path=path)
        for file_name in files:
            if file_name.endswith('.txt'):
                f = open(path + file_name, 'r', encoding='utf8')
                f = f.read()
                for sent in text_to_words(f):
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


    return trigrams_dict, all_texts

# Находит частотные n-граммы.
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
        if freq > 0.007: # Пороговое значение.
            final_trigrams.append(trigram)
            final_trigrams_dict[trigram] = trigrams_dict[trigram]
            for i in final_trigrams_dict[trigram]:
                final_words.add(i)
    # График распределения частот.
    plt.plot(sorted(freqs))
    plt.xlabel('Число n-грамм')
    plt.ylabel('Частота n-грамм')
    plt.show()
    return final_trigrams_dict, final_words

# Возвращает список с частотами n-грамм (для одного файла).
def count_trigrams(file_path, trigrams):
    d = {}
    f = open(file_path, 'r', encoding='utf8')
    f = f.read()
    for trigram in trigrams:
        trigram = re.sub('([)(-*])', '\\' + '\1', trigram)
        finds = re.findall(trigram, f, flags=re.DOTALL)
        c = len(finds)
        rev_d = {}
        if trigram not in d:
            d[trigram] = c

        else:
            d[trigram] += c

    for i in d:
        d[i] /= len(f.split())
        #d[i] /= len(f)

    b = list(d.items())
    b.sort(key=lambda item: item[1])
    #print(file_path)
    #for item in b:
        #print(item[0] +' : '+ str(item[1]))

    return d

# Собирает все признаки всех текстов одного автора в таблицу.
def collect_data(files, author, ngrams, conjs, parenthesis):
    data_train = []
    data_test = []
    l = len(files) - 1
    test_numbers = random.sample(range(l), 10) # Случайные номера тестовых текстов.
    print(test_numbers)
    counter = 0
    for file in files:
        if file.endswith('.txt'):
            file_path = './slon/' + str(author) + '/' + file
            f = open(file_path, 'r', encoding='utf8')
            f = f.read()
            ll = len(f.split())

            # Записывает частоты n-грамм
            d = count_trigrams(file_path, ngrams)
            file_data = [str(author)]
            for i in d:
                file_data.append(d[i])

            #Записывает частоты союзов
            conj_freqs = []
            for conj in conjs:
                finds = re.findall(' ' + conj + ' ', f, flags=re.DOTALL)
                freq = len(finds) / ll
                conj_freqs.append(freq)
            for i in conj_freqs:
                file_data.append(i)

            #Записывает частоты вводных слов
            parenthesis_freqs = []
            for par in parenthesis:
                finds = re.findall(par, f, flags=re.DOTALL)
                freq = len(finds) / ll
                parenthesis_freqs.append(freq)
            #for i in parenthesis_freqs:
                #file_data.append(i)

            #Записывает частоту запятых
            finds = re.findall(',', f, flags=re.DOTALL)
            commas_freq = len(finds) / ll
            file_data.append(commas_freq)

            #Записывает частоту восклицательных знаков
            finds = re.findall('!', f, flags=re.DOTALL)
            exclamation_freq = len(finds) / ll
            file_data.append(exclamation_freq)

            #Записывает частоту вопросительных знаков
            finds = re.findall('\?', f, flags=re.DOTALL)
            question_freq = len(finds) / ll
            file_data.append(question_freq)

            #Записывает среднюю длину предложения (в словах)
            sent = re.split('\.|!|\?|…', f, flags=re.DOTALL)
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


all_trigrams, plain_text = collect_trigrams(all_paths)
all_trigrams_list = list(all_trigrams.keys())
frequent_trigrams, trigrams_words = find_frequent_trigrams(all_trigrams, plain_text)
frequent_trigrams_list = list(frequent_trigrams.keys())
print(len(all_trigrams_list))
print(len(frequent_trigrams_list))

conjunctions = open('conjunctions.txt', 'r', encoding='utf8')
conjs = []
for line in conjunctions:
    conjs.append(line.replace('\n', ''))

prnthss = open('parenthesis.txt', 'r', encoding='utf8')
parenthesis = []
for line in prnthss:
    parenthesis.append(line.replace('\n', ''))

# Два или три потенциальных автора (ID меняются).
files_1 = os.listdir(path='./slon/37648/')
files_2 = os.listdir(path='./slon/817/')
#files_3 = os.listdir(path='./slon/39477/')

# Два или три потенциальных автора (ID меняются).
train_1, test_1 = collect_data(files_1, 37648, frequent_trigrams_list, conjs, parenthesis)
train_2, test_2 = collect_data(files_2, 817, frequent_trigrams_list, conjs, parenthesis)
#train_3, test_3 = collect_data(files_3, 39477, frequent_trigrams_list, conjs, parenthesis)


# Записывается обучающий csv файл.
def write_data():
    data = open('data.csv', 'w', encoding='utf-8')
    all_data = np.vstack((train_1, train_2))#, train_3))
    for k in all_data:
        for l in k:
            data.write(str(l) + ';')
        data.write('\r\n')
    data.close()

# Записывается тестовый csv файл.
def write_test_data():
    data_test = open('data_test.csv', 'w', encoding='utf-8')
    all_data_test = np.vstack((test_1, test_2))#, test_3))
    for k in all_data_test:
        for l in k:
            data_test.write(str(l) + ';')
        data_test.write('\r\n')
    data_test.close()

write_data()
write_test_data()

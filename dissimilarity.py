__author__ = 'angelinaprisyazhnaya'

import csv
import numpy as np
from sklearn.preprocessing import label_binarize
import matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot')

# Читаем csv и отдельно записываем данные для каждого автора.
f = open('data.csv', 'r', encoding='utf-8')
f = f.read()
data_1 = []
data_2 = []
# Если три потенциальных автора.
#data_3 = []
csv_iter = csv.reader(f.split('\n'), delimiter=';')
for row in csv_iter:
    if not row == []:
        # ID меняются.
        if row[0] == '37648':
            data_1.append(row[:-1])
        elif row[0] == '817':
            data_2.append(row[:-1])
        # Если три потенциальных автора.    
        #elif row[0] == '39194':
            #data_3.append(row[:-1])


# Читаем csv с данными тестовых текстов.
f_test = open('data_test.csv', 'r', encoding='utf-8')
f_test = f_test.read()
data_test = []
csv_iter = csv.reader(f_test.split('\n'), delimiter=';')
for row in csv_iter:
    if not row == []:
        data_test.append(row[:-1])


# Считаем D.
def count_dissimilarity(profile_1, profile_2):
    length = len(profile_1)
    dissimilarity = 0
    i = 1
    while i < length:
        try:
            d = ((float(profile_1[i]) - float(profile_2[i])) / ((float(profile_1[i]) + float(profile_2[i])) / 2)) ** 2
        except ZeroDivisionError:
            d = 0.0
        dissimilarity += d
        i += 1
    return dissimilarity


# Считаем Dmax.
def find_max_dissimilarity(d_i, data):
    dissimilarities = []
    for profile in data:
        dissimilarity = count_dissimilarity(d_i, profile)
        if dissimilarity != 0:
            dissimilarities.append(dissimilarity)
    max_dissimilarity = max(dissimilarities)
    return max_dissimilarity

# Считаем M и преобразовываем в вероятность (необязательно).
def authorship_verification(test_text, m_dissimilarities, known_texts):
    threshold = 0.95
    c = 0.1
    ratios = []
    counter = 0
    for text in known_texts:
        ratio = count_dissimilarity(test_text, text) / m_dissimilarities[counter]
        ratios.append(ratio)
        counter += 1
    mean_ratio = np.mean(ratios)
    if mean_ratio == threshold:
        probability = 0.5
    elif mean_ratio <= threshold - c:
        probability = 1
    elif mean_ratio >= threshold + c:
        probability = 0
    else:
        probability = (threshold + c - mean_ratio) / (2 * c)
    print(mean_ratio)
    answer = 'Probability of authorship is ' + str(probability)
    return answer, probability, mean_ratio


max_dissimilarities_1 = []
max_dissimilarities_2 = []
# Если три потенциальных автора.
#max_dissimilarities_3 = []
for t in data_1:
    max_dissimilarities_1.append(find_max_dissimilarity(t, data_1))
for t in data_2:
    max_dissimilarities_2.append(find_max_dissimilarity(t, data_2))
# Если три потенциальных автора.
#for t in data_3:
    #max_dissimilarities_3.append(find_max_dissimilarity(t, data_3))


results = []
for i in data_test:
    result_1 = authorship_verification(i, max_dissimilarities_1, data_1)
    results.append(result_1[2])
    # print(result_1[0])
    
    result_2 = authorship_verification(i, max_dissimilarities_2, data_2)
    results.append(result_2[2])
    # print(result_2[0])
    
    #result_3 = authorship_verification(i, max_dissimilarities_3, data_3)
    #results.append(result_3[2])
    # print(result_3[0])

i = 0
TP = 0
TN = 0
FP = 0
FN = 0
print(len(results))
while i < len(results) - 1: #Если три автора, то - 2.
    a = results[i]
    b = results[i + 1]
    # Если три потенциальных автора.
    #c = results[i + 2]
    m = min(a, b)#, c)
    print(m)
    if i < 19: # Если три автора, то 28.
        if m == a:
            TP += 1
            TN += 1
            # 3 автора.
            # TN += 2
        else:
            FP += 1
            FN += 1
            # 3 автора.
            # TN += 1
    if 19 <= i:# < 58:
        if m == b:
            TP += 1
            TN += 2
        else:
            FP += 1
            FN += 1
            TN += 1
    #if 58 <= i:
        #if m == c:
            #TP += 1
            #TN += 2
        #else:
            #FP += 1
            #TN += 1
            #FN += 1
    i += 2

accuracy = TP + TN / (TP + FP + FN + TN)
print(accuracy)


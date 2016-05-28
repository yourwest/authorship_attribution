__author__ = 'angelinaprisyazhnaya'

import csv
import numpy as np
from sklearn import metrics
from sklearn.preprocessing import label_binarize
from sklearn import svm
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')

#Читаем csv.
f = open('data_tweets.csv', 'r', encoding='utf-8')
f = f.read()
X = []
y = []
csv_iter = csv.reader(f.split('\n'), delimiter=';')
for row in csv_iter:
    if not row == []:
        y.append(float(row[0]))
        new_row = []
        for i in row:
            if i != '':
                new_row.append(float(i))
            else:
                new_row.append(0)

        X.append(new_row[1:-1])


#Читаем csv с данными тестовых текстов.
f_test = open('data_test_tweets.csv', 'r', encoding='utf-8')
f_test = f_test.read()
data_test = []
labels_test = []
csv_iter = csv.reader(f_test.split('\n'), delimiter=';')
for row in csv_iter:
    if not row == []:
        labels_test.append(float(row[0]))
        new_row = []
        for i in row:
            if i != '':
                new_row.append(float(i))
            else:
                continue
        data_test.append(new_row[1:])


values = np.array(X)
labels = np.array(y)
data_test = np.array(data_test)
labels_test = np.array(labels_test)

clf = svm.LinearSVC()
clf.fit(values, labels)


print(clf.score(values, labels))
print(clf.score(data_test, labels_test))


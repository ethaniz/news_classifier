# -*- coding:utf8 -*-

print('(1) load texts...')
train_texts = open('datasets/train_contents.txt').read().split('\n')
train_labels = open('datasets/train_labels.txt').read().split('\n')
test_texts = open('datasets/test_contents.txt').read().split('\n')
test_labels = open('datasets/test_labels.txt').read().split('\n')
all_texts = train_texts + test_texts
all_labels = train_labels + test_labels


all_labels = ['__label__' + x for x in all_labels]


lines = []

for i in range(len(all_texts)):
    line = all_texts[i] + ' ' + all_labels[i] + '\n'
    lines.append(line)


MAX_SEQUENCE_LENGTH = 100
EMBEDDING_DIM = 200
VALIDATION_SPLIT = 0.16
TEST_SPLIT = 0.2

print('(3) split data set...')
# split the data into training set, validation set, and test set
# p1 = int(len(lines)*(1-VALIDATION_SPLIT-TEST_SPLIT))
p2 = int(len(lines)*(1-TEST_SPLIT))
x_train = lines[:p2]
x_test = lines[p2:]
print('train docs: '+str(len(x_train)))
print('test docs: '+str(len(x_test)))





train_file = open('datasets/fasttext_train.txt', 'w')
for line in x_train:
    train_file.write(line)
train_file.close()

test_file = open('datasets/fasttext_test.txt', 'w')
for line in x_test:
    test_file.write(line)
test_file.close()

import fasttext

classifier = fasttext.supervised("datasets/fasttext_train.txt", 'fasttext.model', label_prefix='__label__')

result = classifier.test('datasets/fasttext_test.txt')

print(result.precision)



test_lines = all_texts[p2:]
test_labels = all_labels[p2:]
test_labels = [x.split('__')[-1] for x in test_labels]

need_pop = [611, 984, 1060, 1217, 1616, 3017]

for item in need_pop:
    test_lines.pop(item)
    test_labels.pop(item)


preds = []
i = 0
for test_line in test_lines:
    try:
        pred = classifier.predict([test_line])
    except:
        print(i)
        print(test_line)
    preds.append(pred)
    i += 1
# -*- coding:utf8 -*-

import jieba.posseg as pseg

train_contents = open('datasets/train_contents_unsplit.txt')
test_contents = open('datasets/test_contents_unsplit.txt')

train_lines = train_contents.read().split('\n')
test_lines = test_contents.read().split('\n')

train = []
test = []

num = 0

for line in train_lines:
    num += 1
    if num % 100 == 0:
        print(num)
    words = pseg.cut(line)
    line0 = []
    for w in words:
        if 'x' != w.flag:
            line0.append(w.word)
    train.append(' '.join(line0))

for line in test_lines:
    num += 1
    if num%100 == 0:
        print(num)
    words = pseg.cut(line)
    line0 = []
    for w in words:
        if 'x' != w.flag:
            line0.append(w.word)
    test.append(' '.join(line0))

f1 = open('datasets/train_contents.txt','w')
f1.write('\n'.join(train))
f1.close()
f2 = open('datasets/test_contents.txt','w')
f2.write('\n'.join(test))
f2.close()
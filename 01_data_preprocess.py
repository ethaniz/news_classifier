# -*- coding:utf8 -*-

## iconv -c -f gbk -t utf-8 news_sohusite_xml.dat > news_sohusite_xml_utf8.dat

import json

f = open("datasets/news_sohusite_xml_utf8.dat")
lines = f.readlines()
xml = ''
for line in lines:
    xml += line

docs_xml = xml.split('<doc>\n')
print(len(docs_xml))
del docs_xml[0]
docs = []

for doc_xml in docs_xml:
    if (len(doc_xml.split('<url>')) != 2) or (len(doc_xml.split('<docno>')) != 2) or (len(doc_xml.split('<contenttitle>')) != 2) or (len(doc_xml.split('<content>')) != 2):
        continue
    url = doc_xml.split('<url>')[1].split('</url>')[0]
    docno = doc_xml.split('<docno>')[1].split('</docno>')[0]
    title = doc_xml.split('<contenttitle>')[1].split('</contenttitle>')[0]
    content = doc_xml.split('<content>')[1].split('</content>')[0]
    doc = {'url':url, 'docno':docno, 'title':title, 'content':content}
    docs.append(doc)

print(len(docs))
fout = open("datasets/news_sohusite.json",'w')
fout.write(json.dumps(docs,ensure_ascii=False))
fout.close()



docs = json.load(open('news_sohusite.json'))
label_maps = json.load(open('url_to_catagory_to_label.json'))
num_of_docs_of_label = [0]*15
docs_labeled = {}

num = 0
num_labeled = 0
for doc in docs:
    num += 1
    if num%10000 == 0:
        print(num)
    content = doc['title']+' '+doc['content']
    url = doc['url']
    label = None
    for label_map in label_maps:
        if label_map['url'] in url:
            label = label_map['label']
            break
    if label is None:
        continue
    num_labeled += 1
    if str(label) not in docs_labeled:
        docs_labeled[str(label)] = []
        docs_labeled[str(label)].append(content)
    else:
        docs_labeled[str(label)].append(content)

print('all:'+str(len(docs)))
print('labeled:'+str(num_labeled))

for i in range(1,16):
    if str(i) in docs_labeled:
        print('label '+str(i)+':'+str(len(docs_labeled[str(i)])))

fout = open('news_sohusite_labeled.json','w')
fout.write(json.dumps(docs_labeled,ensure_ascii=False,indent=4))
fout.close()



import json
import matplotlib.pyplot as plt
import numpy as np
import random

docs = json.load(open('datasets/news_sohusite_labeled.json'))

min_size = 10
max_size = 100

def length_stac(docs):
    freq = [0]*2100
    X = []
    Y = []
    for label in docs:
        for doc in docs[label]:
            freq[len(doc)] += 1
    for x,y in enumerate(freq):
        if y > 0:
            X.append(x)
            Y.append(y)
    plt.plot(np.asarray(X[:100]),np.asarray(Y[:100]))
    plt.show()
    return


train_docs = []
test_docs = []
label_num = 0

for i in range(1, 16):
    train_num = 0
    test_num = 0
    nums = 0
    if str(i) in docs:
        d = docs[str(i)]
        if len(d) > 1900:     ##取样本数>1900的标签
            label_num += 1
            for doc in d:
                content = doc
                if len(doc) > max_size:    ##字数>100
                    content = doc[:max_size]
                if nums < 1600:
                    train_docs.append({'label':str(label_num), 'content': content})
                    train_num += 1
                else:
                    test_docs.append({'label':str(label_num), 'content': content})
                    test_num += 1
                nums += 1
                if nums == 2000:
                    break
            print('label ' + str(label_num) + ': train ' + str(train_num) + ', test ' + str(test_num))

print('train docs:' + str(len(train_docs)))
print('test docs:' + str(len(test_docs)))

random.shuffle(train_docs)
random.shuffle(test_docs)

train_contents = []
train_labels = []
test_contents = []
test_labels = []

for doc in train_docs:
    train_contents.append(doc['content'])
    train_labels.append(doc['label'])

for doc in test_docs:
    test_contents.append(doc['content'])
    test_labels.append(doc['label'])

f1 = open('datasets/train_contents_unsplit.txt','w')
f2 = open('datasets/train_labels.txt','w')
f3 = open('datasets/test_contents_unsplit.txt','w')
f4 = open('datasets/test_labels.txt','w')
f1.write('\n'.join(train_contents))
f2.write('\n'.join(train_labels))
f3.write('\n'.join(test_contents))
f4.write('\n'.join(test_labels))
f1.close()
f2.close()
f3.close()
f4.close()
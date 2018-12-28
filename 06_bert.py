# -*- coding:utf8 -*-

MAX_SEQUENCE_LENGTH = 100
EMBEDDING_DIM = 200
VALIDATION_SPLIT = 0.16
TEST_SPLIT = 0.2

print('(1) load texts...')
train_texts = open('datasets/train_contents_unsplit.txt').read().split('\n')
train_labels = open('datasets/train_labels.txt').read().split('\n')
test_texts = open('datasets/test_contents_unsplit.txt').read().split('\n')
test_labels = open('datasets/test_labels.txt').read().split('\n')
all_texts = train_texts + test_texts
all_labels = train_labels + test_labels

lines = []

for i in range(len(all_texts)):
    line = all_texts[i] + '\t' + all_labels[i] + '\n'
    lines.append(line)

print('(3) split data set...')
# split the data into training set, validation set, and test set
p1 = int(len(lines)*(1-VALIDATION_SPLIT-TEST_SPLIT))
p2 = int(len(lines)*(1-TEST_SPLIT))
x_train = lines[:p2]
x_test = lines[p2:]

print('train docs: '+str(len(x_train)))
print('test docs: '+str(len(x_test)))

train_file = open('datasets/train.tsv', 'w')
train_file.write('CleanedDescription' + '\t' + 'MainIndustry' + '\n')
for line in x_train:
    train_file.write(line)
train_file.close()

test_file = open('datasets/dev_test.tsv', 'w')
test_file.write('CleanedDescription' + '\t' + 'MainIndustry' + '\n')
for line in x_test:
    test_file.write(line)
test_file.close()





export GLUE_DIR=/path/to/glue

python run_classifier.py \
  --task_name MRPC \
  --do_train \
  --do_eval \
  --do_lower_case \
  --data_dir $GLUE_DIR/ \
  --bert_model /data/tangle/bert/models/bert-base-chinese \
  --max_seq_length 128 \
  --train_batch_size 32 \
  --learning_rate 2e-5 \
  --num_train_epochs 3.0 \
  --output_dir /tmp/mrpc_output/
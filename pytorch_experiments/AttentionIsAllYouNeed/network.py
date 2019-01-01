# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 16:58:57 2018

@author: Shubham
"""

import torch
import torch.nn as nn
import torch.autograd as autograd
import torch.nn.functional as F
import torch.optim as optim

data = [("me gusta comer en la cafeteria".split(), "SPANISH"),
        ("Give it to me".split(), "ENGLISH"),
        ("No creo que sea una buena idea".split(), "SPANISH"),
        ("No it is not a good idea to get lost at sea".split(), "ENGLISH")]

test_data = [("Yo creo que si".split(), "SPANISH"),
             ("it is lost on me".split(), "ENGLISH")]


label_to_ix = {"SPANISH": 0, "ENGLISH": 1}

word_to_ix = {}
for sent, _ in data + test_data:
    for word in sent:
        if word not in word_to_ix:
            word_to_ix[word] = len(word_to_ix)

print(word_to_ix)
    
VOCAB_SIZE = len(word_to_ix)
NUM_LABELS = 2

class BoWClassifier(nn.Module):
    def __init__(self, num_labels, vocab_size):
        super(BoWClassifier, self).__init__()
        self.linear = nn.Linear(vocab_size, num_labels)
    
    def forward(self, bow_vec):
        return F.log_softmax(self.linear(bow_vec), dim=1)
    
    
def make_bow_vector(sentence, word_to_ix):
    vec = torch.zeros(len(word_to_ix))
    for word in sentence:
        vec[word_to_ix[word]] += 1
    return vec.view(1, -1)

def make_target(label, label_to_ix):
    return torch.LongTensor([label_to_ix[label]])

model = BoWClassifier(NUM_LABELS, VOCAB_SIZE)

for param in model.parameters():
    print(param)
    
with torch.no_grad():
    sample = data[0]
    bow_vec = make_bow_vector(sample[0], word_to_ix)
    log_probs = model(bow_vec)
    print(log_probs)
    
print(next(model.parameters())[:, word_to_ix["creo"]])

loss_function = nn.NLLLoss()
optimizer = optim.SGD(model.parameters(), lr=0.1)

for epoch in range(100):
    for instance, label in data:
        model.zero_grad()
        bow_vec = make_bow_vector(instance, word_to_ix)
        target = make_target(label, label_to_ix)
        log_probs = model(bow_vec)
        loss = loss_function(log_probs, target)
        loss = loss.backward()
        optimizer.step()
        
with torch.no_grad():
    for instance, label in test_data:
        bow_vec = make_bow_vector(instance, word_to_ix)
        log_probs = model(bow_vec)
        print(log_probs)
        
print(next(model.parameters())[:, word_to_ix["creo"]])

#! /home/guarelin/mambaforge/envs/py38/bin/python

import pandas as pd

sentences = pd.read_csv('Sentences/snomed_code_sentences_pmbb_id.csv', header=None, index_col=0)
ids = open('genotyped_sample_ids.txt').read().splitlines()

ids = sentences.index.intersection(ids)

geno_sentences = sentences.loc[ids]
training_sentences = sentences[~sentences.index.isin(ids)]

print(geno_sentences)
print(training_sentences)

open('Sentences/non_genotyped_sentence_input.txt', 'w+').write('\n'.join(training_sentences[1]))
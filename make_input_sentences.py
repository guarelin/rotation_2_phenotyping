#! /home/guarelin/mambaforge/envs/py38/bin/python

import pandas as pd

TEST_ROWS = None

full_df = pd.read_table('PMBB_010323_diagnoses_list.rpt', nrows=TEST_ROWS, on_bad_lines='skip')
print(full_df)
full_df = full_df.dropna(subset=['SNOMED'])
print(full_df)
snomed = pd.Series(dtype=str)

for pmbb_id, subDF in full_df.groupby('PMBB_ID'):
    snomed.loc[pmbb_id] = ' '.join(subDF['SNOMED'].drop_duplicates().astype(int).astype(str))
    if len(snomed) % 2000 == 0:
        print(len(snomed), end=' ', flush=True)
print('')

print(snomed)

snomed.to_csv('Sentences/snomed_code_sentences_pmbb_id.csv', header=False)
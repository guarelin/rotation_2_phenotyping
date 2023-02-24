#! /home/guarelin/mambaforge/envs/py38/bin/python

import pandas as pd
from datetime import datetime
import sys

TEST_ROWS = 1E6

full_df = pd.read_table('PMBB_010323_diagnoses_list.rpt', nrows=TEST_ROWS, on_bad_lines='skip', parse_dates=['start_date_shift'])
print(full_df)
full_df = full_df.dropna(subset=['SNOMED'])
print(full_df)
print(full_df.columns)
full_df['date_val'] = full_df['start_date_shift'] - datetime(1970, 1, 1)
print(full_df)
full_df['date_window'] = (full_df['date_val'] // 15).dt.days.astype(int)
full_df['date_window'] = full_df['date_window'] - full_df['date_window'].min()
print(full_df)
person_windows = full_df[['PMBB_ID', 'date_window']].drop_duplicates()
person_windows = person_windows.set_index(['PMBB_ID', 'date_window'])
print(person_windows)
snomed = pd.Series(dtype=str, index=person_windows.index)

i = 0

for (pmbb_id, date_window), subDF in full_df.groupby(['PMBB_ID', 'date_window']):
    snomed.loc[(pmbb_id, date_window)] = ' '.join(subDF['SNOMED'].drop_duplicates().astype(int).astype(str))
    i += 1
    if i % 2000 == 0:
        print(i, end=' ', flush=True)
print('')

print(snomed)

snomed.to_csv('Sentences/snomed_code_window_sentences_pmbb_id.csv', header=False)
import pandas as pd
import numpy as np
from datetime import datetime

date_mtx_head = pd.read_csv('PMBB_date_mtx_codes_gt_20_occurrences.csv', index_col='PMBB_ID', nrows=5)
date_cols = list(date_mtx_head.columns)

input = 'PMBB_date_mtx_codes_gt_20_occurrences.csv'

chunks = []

for chunk in pd.read_csv(input, parse_dates=date_cols, chunksize=2000, nrows=None):
    chunk = chunk.set_index(chunk.columns[0])
    chunk = (chunk - datetime(1970, 1, 1)).applymap(lambda x: x.days)
    chunk = (chunk / 365.25).astype(np.float16)
    chunks.append(chunk)
    print(len(chunks), end=' ', flush=True)

print('')
date_matrix = pd.concat(chunks)
date_matrix.to_csv(input.replace('PMBB_date', 'PMBB_numeric_date'))

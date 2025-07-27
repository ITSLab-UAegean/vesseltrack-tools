import sys
import pandas as pd


def keep_col_values(df, col_keep = []):
    if (col_keep == []):
        return {}
        
    res = df[col_keep].apply(lambda cols: cols.loc[cols.first_valid_index()] 
                             if cols.first_valid_index() is not None else 'None')
    return res.to_dict()


def return_empty_seq_result(h3_col, trip):
    return {
            h3_col + '_seq': None,
            'TIMESTAMP_ENTER': None,
            'TIMESTAMP_LEAVE': None,
            'NO_POSITIONS': None,
            'TRIP': trip,
        }


def create_token_seq_trip(df, col_keep = [], h3_col= 'h3_cell_7', sort=False):
    # Creates a H3 sequence for a df of a single trip.

    if df.empty:
        print('Empty')
        return_empty_seq_result(h3_col, df.name)

    if('TRIP' not in df.columns):
        trip = df.name
    else:
        trip = df.iloc[0]['TRIP']

    if(sort):
        df = df.sort_values(by="TIMESTAMP")

    prev = ''
    prev_t = 0
    cells = []
    starts = []
    ends = []
    pos_counts = []

    for _, row in df.iterrows():
        if(row[h3_col]!=prev):
            cells.append(row[h3_col])
            starts.append(row['TIMESTAMP'])
            if(prev!=''):
                ends.append(prev_t)
                pos_counts.append(counter)
            counter = 1
            prev = row[h3_col]
        else:
            counter += 1
        prev_t = row['TIMESTAMP']
    else:
        ends.append(prev_t)
        pos_counts.append(counter)

    MIN_SEQ_LENGTH = 10
    if(len(cells)<MIN_SEQ_LENGTH):
        res = return_empty_seq_result(h3_col, trip)
    else:
        res = {h3_col+'_seq':cells, 'TIMESTAMP_ENTER':starts, 'TIMESTAMP_LEAVE':ends, 'NO_POSITIONS': pos_counts}
    res.update(keep_col_values(df, col_keep))
    res['TRIP'] = trip
    return res
 
def alex():
    print('yu')


if __name__ == "__main__":
  import json

  config_file = open(sys.argv[1], "r",encoding="utf-8")
  CONFIG = json.load(config_file)
import matplotlib.pyplot as plt
import json
import os
import sys
import pandas as pd
from pprint import pprint
from tqdm import tqdm

data_file = 'distance_data_fine.json'
with open(data_file, 'r') as f:
    distance_data = json.load(f)

df = pd.DataFrame(columns=['origin_id', 'origin_address', 'destination_id', 'destination_address', 'distance_text', 'distance_value', 'duration_text', 'duration_value', 'mode'])
distance_matrices = [(distance_data['distance_matrix_transit'], 'transit'), (distance_data['distance_matrix_transit'], 'driving')]

N_total = 0
for distance_matrix, _ in distance_matrices:
    N_total += len(distance_matrix['rows']) * len(distance_matrix['destination_addresses'])
print(f'Number of rows: {N_total}')

with tqdm(total=N_total) as pbar:
    for distance_matrix, mode in distance_matrices:
        for origin_id, (origin_address, row) in enumerate(zip(distance_matrix['origin_addresses'], distance_matrix['rows'])):
            for destination_id, (destination_address, element) in enumerate(zip(distance_matrix['destination_addresses'], row['elements'])):
                status = element['status']
                if status == 'OK':
                    distance_text = element['distance']['text']
                    distance_value = element['distance']['value']
                    duration_text = element['duration']['text']
                    duration_value = element['duration']['value']
                else:
                    distance_text, distance_value, duration_text, duration_value = None, None, None, None

                df_row = {
                    'origin_id': origin_id,
                    'origin_address': origin_address,
                    'destination_id': destination_id,
                    'destination_address': destination_address,
                    'distance_text': distance_text,
                    'distance_value': distance_value,
                    'duration_text': duration_text,
                    'duration_value': duration_value,
                    'mode': mode,
                    'status': status,
                }
                df = df.append(df_row, ignore_index=True)
            pbar.update(len(row['elements']))
pbar.close()

df_pickle_file = 'distance_data_fine_df.pkl'
df.to_pickle(df_pickle_file)             
        
print('Done!')
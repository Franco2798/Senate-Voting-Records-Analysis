import pandas as pd
import numpy as np
from scipy.spatial.distance import cosine
import random

df = pd.read_csv('senate_votes.csv')
# print(df.head())
print()

# Exercise 1 - Find the senator whose voting record is closest to Rhode Island senator, Lincoln Chafee.
print("Exercise 1:")

row_i = df[(df['Name'] == 'Chafee') & (df['State'] == 'RI')].iloc[:, 3:49].to_numpy().flatten()

distances = []

for i in range(len(df)):
    if not(df.loc[i, 'Name'] == 'Chafee' and df.loc[i, 'State'] == 'RI'):
        evaluated_rows = df.iloc[i, 3:49].to_numpy().flatten()
        dis_to_row_i = cosine(row_i, evaluated_rows)
        distances.append(dis_to_row_i)
    else:
        distances.append(np.inf)

names = df.iloc[:, 0]
states = df.iloc[:, 2]

data_frame_1 = pd.DataFrame({
    'Name': names,
    'Distance': distances,
    'State': states
})

distances_sorted = data_frame_1.sort_values('Distance')

closest_senator = distances_sorted.iloc[0]['Name']
closest_state = distances_sorted.iloc[0]['State']
closest_distance = distances_sorted.iloc[0]['Distance']

print(f"Lincoln Chafee's closest senator is {closest_senator} of the state of {closest_state}, with a distance of {closest_distance:.3f}.")
print()

# Exercise 2 - Find the senator who disagrees most with Pennsylvania senator, Rick Santorum.
print("Exercise 2:")

row_santorum = df[(df['Name'] == 'Santorum') & (df['State'] == 'PA')].iloc[:, 3:49].to_numpy().flatten()

distances_santorum = []

for i in range(len(df)):
    evaluated_rows_santorum = df.iloc[i, 3:49].to_numpy().flatten()
    dis_to_row_santorum = cosine(row_santorum, evaluated_rows_santorum)
    distances_santorum.append(dis_to_row_santorum)
    

data_frame_2 = pd.DataFrame({
    'Name': names,
    'Distance': distances_santorum,
    'State': states
})

distances_sorted_santorum = data_frame_2.sort_values('Distance')

disagree_senator = distances_sorted_santorum.iloc[-1]['Name']
disagree_state = distances_sorted_santorum.iloc[-1]['State']

print(f"The senator who disagrees the most with Rick Santorum is {disagree_senator}, of the state of {disagree_state}.")
print()

# Exercise 3 - Choose 5 Democratic and 5 Republican (or more) senators randomly.
print("Exercise 3:")

democrats = df[df['Party']=='D']
republicans = df[df['Party']=='R']

democrats_random = democrats.sample(5, random_state=42)
republicans_random = republicans.sample(5, random_state=42)

print(democrats_random.iloc[:, 0:3])
print()
print(republicans_random.iloc[:, 0:3])
print()

# Exercise 4 - Compare Jefford's record with each of these 10 senators. Would you classify Jeffords as closer to the Democrats or a Republicans?
print("Exercise 4:")

jeffords = df[df['Name'] == 'Jeffords'].iloc[:, 3:49].to_numpy().flatten()
democrats_jeffords = democrats.iloc[:, 3:49].to_numpy()
republicans_jeffords = republicans.iloc[:, 3:49].to_numpy()

distances_dem_jef = []
distances_rep_jef = []

for i in range(len(democrats_jeffords)):
    distance_dem_jef = cosine(jeffords, democrats_jeffords[i])
    distances_dem_jef.append(distance_dem_jef)

for i in range(len(republicans_jeffords)):
    distance_rep_jef = cosine(jeffords, republicans_jeffords[i])
    distances_rep_jef.append(distance_rep_jef)

data_frame_3 = pd.DataFrame({
    'Name': democrats['Name'],
    'Distance': distances_dem_jef,
    'State': democrats['State']
})

data_frame_4 = pd.DataFrame({
    'Name': republicans['Name'],
    'Distance': distances_rep_jef,
    'State': republicans['State']
})

tot_dist_dem = data_frame_3['Distance'].sum()
tot_dist_rep = data_frame_4['Distance'].sum()

if tot_dist_dem > tot_dist_rep:
    print(f"Comparing with 5 random senators of each party, we could clasify Jefford as closer to the republicans")
else:
    print(f"Comparing with 5 random senators of each party, we could clasify Jefford as closer to the democrats")

print()




import pandas as pd

df = pd.read_csv("/Users/danteamicarella/Documents/GitHub/grad-final/python/results/total/joindf_total.csv")

# Scoring dictionary
scoring = {
    'MVP': 20,
    'SB_MVP': 30,
    'SB_WIN': 25,
    'OPOY': 15,
    'DPOY': 15,
    'OROY': 10,
    'DROY': 10,
    'First_AP': 7,
    'Second_AP': 5,
    'Pro_Bowl': 3
}

# Iterate over each row and calculate the total score
total_scores = []
for index, row in df.iterrows():
    total_score = 0
    for achievement, score in scoring.items():
        value = row[achievement]
        if pd.notna(value):
            total_score += int(value) * score
    total_scores.append(total_score)

# Add the total scores as a new column to the DataFrame
df['Total_Score'] = total_scores

df.sort_values(by=['ID'], inplace=True)
current_round = 1
current_pick_in_round = 1

# List to store the new round pick numbers
new_round_pick_numbers = []

for index, row in df.iterrows():
    if row['Round'] == current_round:
        new_round_pick_numbers.append(current_pick_in_round)
        current_pick_in_round += 1
        if current_pick_in_round > 32:
            current_pick_in_round = 1
            current_round += 1
    else:
        current_round = row['Round']
        current_pick_in_round = 1
        new_round_pick_numbers.append(current_pick_in_round)

df['Round_Pick_No'] = new_round_pick_numbers
# df.to_csv("washPostdataNew.csv", index=False)

# # Display the DataFrame with the new column
# print(df)

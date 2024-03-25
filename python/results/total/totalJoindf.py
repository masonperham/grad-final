import pandas as pd

# Read the CSV file
df = pd.read_csv("/Users/danteamicarella/Documents/GitHub/grad-final/python/results/total/joindf_total.csv")

# Define the scoring dictionary
scoring = {
    'MVP': 20,
    'SB_MVP': 30,
    'SB_WIN': 25,
    'OPOY': 15,
    'DPOY': 15,
    'OROY': 10,
    'DROY': 10,
    'First_AP': 5,
    'Second_AP': 3,
    'Pro_Bowl': 7
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

# Save the updated DataFrame to a new CSV file
df.to_csv("washPostdata.csv", index=False)

# Display the DataFrame with the new column
print(df)

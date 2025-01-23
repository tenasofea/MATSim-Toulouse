import pandas as pd

# Load the CSV file
df = pd.read_csv('agent_positions_motif_filtre_g.csv')

# Filter the DataFrame based on the specified conditions
filtered_df = df[(df['Temps_minute'] >= 540) & 
                 (df['Temps_minute'] <= 600) & 
                 (df['Motif_Orig'] == 'work') & 
                 (df['Motif_Dest'] == 'home')]

# Select the required columns
filtered_df = filtered_df[['AgentId', 'Temps_minute', 'link', 'x', 'y', 'Motif_Orig', 'Motif_Dest']]

# Save the filtered DataFrame to a new CSV file
filtered_df.to_csv('filtered_agent_positions.csv', index=False)

# Display the filtered DataFrame
print(filtered_df)

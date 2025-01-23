import pandas as pd

file_path = 'ordered_daily_trips.csv'  
data = pd.read_csv(file_path)

# filtere les agents
home_to_work = data[(data['Motif_Orig'] == 'home') & (data['Motif_Dest'] == 'work')]
work_to_home = data[(data['Motif_Orig'] == 'work') & (data['Motif_Dest'] == 'home')]

# count the number of trips per agent
home_to_work_counts = home_to_work.groupby('AgentId').size()
work_to_home_counts = work_to_home.groupby('AgentId').size()

# identifier les agents ayant exactement 1 voyage de home to work
home_to_work_1 = set(home_to_work_counts[home_to_work_counts == 1].index)

# Identifier les agents ayant exactement 1 voyage de work to home
work_to_home_1 = set(work_to_home_counts[work_to_home_counts == 1].index)

# trouver agents avec 1 voyage de home to work, mais PAS 1 voyage de work to home
agents_not_in_circle = home_to_work_1 - work_to_home_1 



output_df = pd.DataFrame(list(agents_not_in_circle), columns=['AgentId'])
output_df.to_csv('agents_not_in_circle.csv', index=False)

z = home_to_work_1.intersection(work_to_home_1)
print(len(z), len(home_to_work_1) - len(z))
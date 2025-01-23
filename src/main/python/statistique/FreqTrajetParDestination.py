# import pandas as pd
# import matplotlib.pyplot as plt

# file_path = 'ordered_weekly_trips.csv'  
# data = pd.read_csv(file_path)

# # Filter only for trips where Motif_Dest is 'work'
# # trips = data[(data['Motif_Orig'] == 'home') ]

# # Filter only for trips where Motif_Orig is 'home' & Motif_Dest is 'work'
# trips = data[(data['Motif_Orig'] == 'other') & (data['Motif_Dest'] == 'home')]

# # Count the number of times each agent made a work trip
# trip_frequency = trips.groupby('AgentId').size()

# # Create a frequency distribution for the number of work trips
# frequency_distribution = trip_frequency.value_counts().sort_index()

# # Set fixed ranges for comparison (modify based on your dataset's typical range)
# x_range = range(1, 11)  # Assume max 10 trips
# y_max = 1000  # Assume max 100 agents per frequency

# # plt.figure(figsize=(10, 6))
# # plt.bar(frequency_distribution.index, frequency_distribution.values, width=0.8, edgecolor='black')
# # plt.xlabel('Number of Home-Other Trips During the Week')
# # plt.ylabel('Number of Agents')
# # plt.title('Frequency of Home-Other Trips by Agents Over the Week')
# # plt.xticks(frequency_distribution.index)
# # plt.grid(axis='y', linestyle='--', alpha=0.7)
# # plt.show()

# plt.figure(figsize=(10, 6))
# bars = plt.bar(
#     frequency_distribution.index, 
#     frequency_distribution.values, 
#     width=0.8, 
#     edgecolor='black'
# )

# for bar in bars:
#     height = bar.get_height()
#     plt.text(
#         bar.get_x() + bar.get_width() / 2,  # Center the text on the bar
#         height + 2,  # Place text slightly above the bar
#         f'{int(height)}',  # Display the value as an integer
#         ha='center', 
#         va='bottom',
#         fontsize=10,
#         color='black'
#     )

# # Set fixed scales for comparison
# plt.xlim(min(x_range) - 0.5, max(x_range) + 0.5)  
# plt.ylim(0, y_max)  

# plt.xlabel('Number of Other-to-Home Trips During the Week')
# plt.ylabel('Number of Agents')
# plt.title('Frequency of Other-to-Home by Agents Over the Week')
# plt.xticks(x_range)  
# plt.grid(axis='y', linestyle='--', alpha=0.7)
# plt.show()

# ------------------------------------------------------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt

file_path = 'ordered_weekly_trips.csv'  
data = pd.read_csv(file_path)

# Sort the data by AgentId and trip sequence if there's a timestamp
data = data.sort_values(by=['AgentId']) 

# Create shifted columns to detect consecutive trips
data['Prev_Motif_Orig'] = data['Motif_Orig'].shift(1)
data['Prev_Motif_Dest'] = data['Motif_Dest'].shift(1)
data['Prev_AgentId'] = data['AgentId'].shift(1)

# Detect consecutive trips: home-to-work followed by work-to-home for the same agent
consecutive_trips = data[
    (data['Prev_Motif_Orig'] == 'home') & (data['Prev_Motif_Dest'] == 'other') &  # Previous trip was home->work
    (data['Motif_Orig'] == 'other') & (data['Motif_Dest'] == 'home') &  # Current trip is work->home
    (data['AgentId'] == data['Prev_AgentId'])  # Same agent
]

# Count the number of such consecutive trips per agent
consecutive_trip_counts = consecutive_trips.groupby('AgentId').size()

# Create a frequency distribution for consecutive trips
frequency_distribution = consecutive_trip_counts.value_counts().sort_index()

# Set fixed ranges for comparison (adjust based on typical dataset ranges)
x_range = range(1, 15)  # Assume max 5 consecutive trip patterns
y_max = 700  # Assume max 200 agents per frequency

# Plot the frequency distribution
plt.figure(figsize=(10, 6))
bars = plt.bar(
    frequency_distribution.index, 
    frequency_distribution.values, 
    width=0.8, 
    edgecolor='black'
)

# Annotate each bar with its height value
for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,  # Center the text on the bar
        height + 5,  # Slightly above the bar
        f'{int(height)}',  # Display the value as an integer
        ha='center', 
        va='bottom',
        fontsize=10,
        color='black'
    )

# Set fixed scales for comparison
plt.xlim(min(x_range) - 0.5, max(x_range) + 0.5)  # Fixed X-axis scale
plt.ylim(0, y_max)  # Fixed Y-axis scale

# Add labels and title
plt.xlabel('Number of Consecutive Home-to-Other and Other-to-Home Trip Patterns')
plt.ylabel('Number of Agents')
plt.title('Frequency of Consecutive Home-to-Other and Other-to-Home Trips by Agents')
plt.xticks(x_range)  # Show only integer values on the X-axis
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.show()

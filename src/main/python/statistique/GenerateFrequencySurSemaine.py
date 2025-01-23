import pandas as pd
import matplotlib.pyplot as plt

file_path = 'C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\ordered_weekly_trips.csv'
data = pd.read_csv(file_path)

# calculate trip frequency
trip_frequency = data.groupby(['Motif_Orig', 'Motif_Dest']).size().reset_index(name='Frequency')

# visualize trip frequency
def visualize_trip_frequency(trip_frequency):
    plt.figure(figsize=(12, 6))
    plt.bar(
        trip_frequency['Motif_Orig'] + ' -> ' + trip_frequency['Motif_Dest'],
        trip_frequency['Frequency'],
        color='skyblue'
    )
    plt.xlabel('Trips (Motif_Orig -> Motif_Dest)')
    plt.ylabel('Frequency')
    plt.title('Frequency of Trips')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

# calculer la frequence des agents pour des deplacements particuliers
agent_trip_frequency = data.groupby(['Motif_Orig', 'Motif_Dest', 'AgentId']).size().reset_index(name='AgentFrequency')

# visualize agent frequency
def visualize_agent_frequency(agent_trip_frequency):
    # agregat par Motif_Orig et Motif_Dest
    aggregated_frequency = agent_trip_frequency.groupby(['Motif_Orig', 'Motif_Dest']).size().reset_index(name='AgentCount')

    plt.figure(figsize=(12, 6))
    plt.bar(
        aggregated_frequency['Motif_Orig'] + ' -> ' + aggregated_frequency['Motif_Dest'],
        aggregated_frequency['AgentCount'],
        color='coral'
    )
    plt.xlabel('Trips (Motif_Orig -> Motif_Dest)')
    plt.ylabel('Number of Agents')
    plt.title('Number of Agents Making Each Trip')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

visualize_trip_frequency(trip_frequency)
visualize_agent_frequency(agent_trip_frequency)

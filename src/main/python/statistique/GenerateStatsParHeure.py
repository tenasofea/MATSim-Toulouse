# #-------------------------------------------------------------------------------------------------------------------------
# # Repartition trajet par heure interactive (ca marche)

# import pandas as pd
# import plotly.express as px

# # Define the output path for saving CSVs (adjust as needed)
# output_path = "C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\csv_clean\\"

# # Load the CSV file
# df = pd.read_csv('agent_positions_motif_filtre_g_5000_clean.csv')

# # Convert 'Temps_minute' to hours (assuming it is in minutes)
# df['Temps_hour'] = df['Temps_minute'] // 60

# # Create dictionaries to count distinct agents per hour and motif
# trips_by_motif_per_hour = {}

# # Loop over each row and count distinct trips by agents per hour and motif
# for _, row in df.iterrows():
#     agent_id = row['AgentId']
#     hour = row['Temps_hour']
#     motif_orig = row['Motif_Orig']
#     motif_dest = row['Motif_Dest']
    
#     trip_type = (motif_orig, motif_dest)
    
#     # Initialize the dictionary for this hour if it doesn't exist
#     if hour not in trips_by_motif_per_hour:
#         trips_by_motif_per_hour[hour] = {}
    
#     # Initialize the set for this motif type if it doesn't exist
#     if trip_type not in trips_by_motif_per_hour[hour]:
#         trips_by_motif_per_hour[hour][trip_type] = set()
    
#     # Add the agent to the set for this motif type in this hour
#     trips_by_motif_per_hour[hour][trip_type].add(agent_id)

# # Convert trips by motif per hour to a DataFrame
# motif_data = []
# for hour, motifs in trips_by_motif_per_hour.items():
#     for (motif_orig, motif_dest), agents in motifs.items():
#         motif_data.append([hour, motif_orig, motif_dest, len(agents)])  # Use len(agents) to count distinct agents

# motif_df = pd.DataFrame(motif_data, columns=['Heure', 'Motif_Orig', 'Motif_Dest', 'Nombre_Trajet']).sort_values(by='Heure')

# # Calculate the total number of trips per hour without distinguishing motifs
# trips_per_hour_df = motif_df.groupby('Heure')['Nombre_Trajet'].sum().reset_index()

# # Rename columns appropriately
# trips_per_hour_df.columns = ['Heure', 'Nombre_Trajet']

# # Save the results to CSV files
# motif_df.to_csv(output_path + 'repartition_trajet_par_heure_avec_motif.csv', index=False)
# trips_per_hour_df.to_csv(output_path + 'nombre_trajets_par_heure_sans_motif.csv', index=False)

# # Pivot the data for interactive plotting
# pivot_df = motif_df.pivot(index='Heure', columns=['Motif_Orig', 'Motif_Dest'], values='Nombre_Trajet').fillna(0)

# # Flatten the MultiIndex columns for Plotly compatibility
# pivot_df.columns = [f"{orig} -> {dest}" for orig, dest in pivot_df.columns]

# # Reset index for Plotly
# pivot_df.reset_index(inplace=True)

# # Plotting the interactive stacked bar chart with Plotly
# fig = px.bar(
#     pivot_df, 
#     x='Heure', 
#     y=pivot_df.columns[1:],  # exclude 'Heure' from the y-axis
#     title="Number of Trips by Hour, Origin, and Destination (Distinct Colors for Each Trip)",
#     labels={"value": "Number of Trips", "variable": "Motif (Orig -> Dest)"},
# )

# # Customize layout for clarity
# fig.update_layout(barmode='stack', xaxis_title="Hour", yaxis_title="Number of Trips")

# # Show interactive plot
# fig.show()

#----------------------------------------------------------------------------------------------------------------
# Generate stats evolution traffic & repartition trajet par heure non interactive (ca marche) couleur peut etre different

# import pandas as pd
# import matplotlib.pyplot as plt

# traffic_df = pd.read_csv("C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\csv_clean\\nombre_trajets_par_heure_sans_motif_regroup.csv")
# traffic_df.columns = ['Heure', 'Nombre_Agents']

# motif_df = pd.read_csv("C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\csv_clean\\repartition_trajet_par_heure_avec_motif_regroup.csv")

# motif_df['Heure'] = motif_df['Heure']
# traffic_df['Heure'] = traffic_df['Heure']

# # Calculate the total number of agents per hour across motifs
# total_agents_per_hour = motif_df.groupby('Heure')['Nombre_Trajet'].sum().reset_index()
# total_agents_per_hour.columns = ['Heure', 'Total_Motif_Agents']

# # Merge the traffic data (total active agents) with the motif data (agents per motif)
# merged_df = pd.merge(motif_df, traffic_df, on='Heure')

# # Scale motif counts so that their sum matches the total active agents per hour
# merged_df['Normalized_Trajet'] = merged_df.apply(
#     lambda row: row['Nombre_Trajet'] * row['Nombre_Agents'] / total_agents_per_hour.loc[total_agents_per_hour['Heure'] == row['Heure'], 'Total_Motif_Agents'].values[0],
#     axis=1
# )

# # Pivot the data for stacked bar plotting
# pivot_df = merged_df.pivot(index='Heure', columns=['Motif_Orig', 'Motif_Dest'], values='Normalized_Trajet').fillna(0)

# # Flatten the MultiIndex columns for Plotly compatibility
# pivot_df.columns = [f"{orig} -> {dest}" for orig, dest in pivot_df.columns]

# # Plotting the repartition stacked bar chart with normalized values
# fig, ax = plt.subplots(figsize=(12, 6))
# pivot_df.plot(kind='bar', stacked=True, ax=ax, colormap='tab20')

# ax.set_title("Repartition of Trips by Hour with Total Active Agents")
# ax.set_xlabel("Hour")
# ax.set_ylabel("Number of Trips (Total Active Agents per Hour)")
# ax.legend(title="Motif (Orig -> Dest)", bbox_to_anchor=(1.05, 1), loc='upper left')

# plt.tight_layout()
# plt.show()

# plt.figure(figsize=(10, 6))
# plt.plot(traffic_df['Heure'], traffic_df['Nombre_Agents'], color='blue', linewidth=1)
# plt.title("Évolution du Trafic au Cours de la Simulation")
# plt.xlabel("Hour")
# plt.ylabel("Nombre d'Agents Actifs")
# plt.grid(True)
# plt.tight_layout()
# plt.show()

#----------------------------------------------------------------------------------------------------------------
# Generate stats evolution traffic & repartition trajet par heure avec meme couleurs (ca marche)

# import pandas as pd
# import matplotlib.pyplot as plt

# # Load the data
# traffic_df = pd.read_csv("C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\csv_wednesday\\nombre_trajets_par_heure_sans_motif_regroup.csv")
# traffic_df.columns = ['Heure', 'Nombre_Agents']

# motif_df = pd.read_csv("C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\csv_wednesday\\repartition_trajet_par_heure_avec_motif_regroup.csv")

# motif_df['Heure'] = motif_df['Heure']
# traffic_df['Heure'] = traffic_df['Heure']

# # Calculate the total number of agents per hour across motifs
# total_agents_per_hour = motif_df.groupby('Heure')['Nombre_Trajet'].sum().reset_index()
# total_agents_per_hour.columns = ['Heure', 'Total_Motif_Agents']

# # Merge the traffic data (total active agents) with the motif data (agents per motif)
# merged_df = pd.merge(motif_df, traffic_df, on='Heure')

# # Scale motif counts so that their sum matches the total active agents per hour
# merged_df['Normalized_Trajet'] = merged_df.apply(
#     lambda row: row['Nombre_Trajet'] * row['Nombre_Agents'] / total_agents_per_hour.loc[total_agents_per_hour['Heure'] == row['Heure'], 'Total_Motif_Agents'].values[0],
#     axis=1
# )

# # Pivot the data for stacked bar plotting
# pivot_df = merged_df.pivot(index='Heure', columns=['Motif_Orig', 'Motif_Dest'], values='Normalized_Trajet').fillna(0)

# # Flatten the MultiIndex columns for better handling
# pivot_df.columns = [f"{orig} -> {dest}" for orig, dest in pivot_df.columns]

# # Define a fixed color mapping for each motif
# color_mapping = {
#     "home -> work": "#1f77b4",
#     "home -> education": "#ff7f0e",
#     "home -> leisure": "#2ca02c",
#     "home -> other": "#d62728",
#     "work -> home": "#9467bd",
#     "home -> shop": "#8c564b",
#     "shop -> home": "#e377c2",
#     "divers -> divers": "#7f7f7f",
#     "education -> home": "#bcbd22",
#     "other -> home": "#17becf",
#     "leisure -> home": "#aec7e8"
# }

# # Generate a list of colors for the motifs in the order of the columns
# colors = [color_mapping[col] for col in pivot_df.columns]

# # Plotting the repartition stacked bar chart with normalized values and fixed colors
# fig, ax = plt.subplots(figsize=(12, 6))
# pivot_df.plot(kind='bar', stacked=True, ax=ax, color=colors)

# ax.set_title("Repartition of Trips by Hour with Total Active Agents")
# ax.set_xlabel("Hour")
# ax.set_ylabel("Number of Trips (Total Active Agents per Hour)")
# ax.legend(title="Motif (Orig -> Dest)", bbox_to_anchor=(1.05, 1), loc='upper left')

# plt.tight_layout()
# plt.show()

# # Plotting the traffic evolution
# plt.figure(figsize=(10, 6))
# plt.plot(traffic_df['Heure'], traffic_df['Nombre_Agents'], color='blue', linewidth=1)
# plt.title("Évolution du Trafic au Cours de la Simulation")
# plt.xlabel("Hour")
# plt.ylabel("Nombre d'Agents Actifs")
# plt.grid(True)
# plt.tight_layout()
# plt.show()

#----------------------------------------------------------------------------------------------------------------
# Generate stats evolution traffic & repartition trajet par heure avec meme couleurs et meme echelle (ca marche)

import pandas as pd
import matplotlib.pyplot as plt

# Load the data
traffic_df = pd.read_csv("C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\csv_tuesday\\nombre_trajets_par_heure_sans_motif_regroup.csv")
traffic_df.columns = ['Heure', 'Nombre_Agents']

motif_df = pd.read_csv("C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\csv_tuesday\\repartition_trajet_par_heure_avec_motif_regroup.csv")

motif_df['Heure'] = motif_df['Heure']
traffic_df['Heure'] = traffic_df['Heure']

# Calculate the total number of agents per hour across motifs
total_agents_per_hour = motif_df.groupby('Heure')['Nombre_Trajet'].sum().reset_index()
total_agents_per_hour.columns = ['Heure', 'Total_Motif_Agents']

# Merge the traffic data (total active agents) with the motif data (agents per motif)
merged_df = pd.merge(motif_df, traffic_df, on='Heure')

# Scale motif counts so that their sum matches the total active agents per hour
merged_df['Normalized_Trajet'] = merged_df.apply(
    lambda row: row['Nombre_Trajet'] * row['Nombre_Agents'] / total_agents_per_hour.loc[total_agents_per_hour['Heure'] == row['Heure'], 'Total_Motif_Agents'].values[0],
    axis=1
)

# Pivot the data for stacked bar plotting
pivot_df = merged_df.pivot(index='Heure', columns=['Motif_Orig', 'Motif_Dest'], values='Normalized_Trajet').fillna(0)

# Flatten the MultiIndex columns for better handling
pivot_df.columns = [f"{orig} -> {dest}" for orig, dest in pivot_df.columns]

# Define a fixed color mapping for each motif
color_mapping = {
    "home -> work": "#1f77b4",
    "home -> education": "#ff7f0e",
    "home -> leisure": "#2ca02c",
    "home -> other": "#d62728",
    "work -> home": "#9467bd",
    "home -> shop": "#8c564b",
    "shop -> home": "#e377c2",
    "divers -> divers": "#7f7f7f",
    "education -> home": "#bcbd22",
    "other -> home": "#17becf",
    "leisure -> home": "#aec7e8"
}

# Generate a list of colors for the motifs in the order of the columns
colors = [color_mapping[col] for col in pivot_df.columns]

# Set fixed y-axis scale (adjust these limits based on your expected range)
y_limit = 2000  # Change this value as needed for comparison

# Plotting the repartition stacked bar chart with normalized values and fixed colors
fig, ax = plt.subplots(figsize=(12, 6))
pivot_df.plot(kind='bar', stacked=True, ax=ax, color=colors)

ax.set_title("Repartition of Trips by Hour with Total Active Agents")
ax.set_xlabel("Hour")
ax.set_ylabel("Number of Trips (Total Active Agents per Hour)")
ax.legend(title="Motif (Orig -> Dest)", bbox_to_anchor=(1.05, 1), loc='upper left')
ax.set_ylim(0, y_limit) 

plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(traffic_df['Heure'], traffic_df['Nombre_Agents'], color='blue', linewidth=1)
plt.title("Évolution du Trafic au Cours de la Simulation")
plt.xlabel("Hour")
plt.ylabel("Nombre d'Agents Actifs")
plt.ylim(0, y_limit) 
plt.grid(True)
plt.tight_layout()
plt.show()

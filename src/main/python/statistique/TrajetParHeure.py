
#---------------------------------------------------------------------------------------------------------
# without condition to choose inlcude "other" or not 
# import pandas as pd

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

# # Now, calculate the total number of trips per hour without distinguishing motifs
# trips_per_hour_df = motif_df.groupby('Heure')['Nombre_Trajet'].sum().reset_index()

# # Rename columns appropriately
# trips_per_hour_df.columns = ['Heure', 'Nombre_Trajet']

# # Save the results to CSV files
# motif_df.to_csv(output_path + 'repartition_trajet_par_heure_avec_motif.csv', index=False)
# trips_per_hour_df.to_csv(output_path + 'nombre_trajets_par_heure_sans_motif.csv', index=False)

#-------------------------------------------------------------------------------------------------------------------------
# with the option to include "other" or not

# import pandas as pd

# output_path = "C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\csv_short\\"

# include_other = False  # Set to True to include "other", False to exclude

# df = pd.read_csv('agent_positions_motif_filtre_g_5000_clean_short.csv')

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
    
#     # Check if "other" should be excluded based on the parameter
#     if not include_other and ("other" in [motif_orig, motif_dest]):
#         continue  # Skip this row if "other" should be excluded
    
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
# trips_per_hour_df.columns = ['Heure', 'Nombre_Trajet']

# # motif_df.to_csv(output_path + 'repartition_trajet_par_heure_avec_motif.csv', index=False)
# # trips_per_hour_df.to_csv(output_path + 'nombre_trajets_par_heure_sans_motif.csv', index=False)

# motif_df.to_csv(output_path + 'repartition_trajet_par_heure_avec_motif_sans_other.csv', index=False)
# trips_per_hour_df.to_csv(output_path + 'nombre_trajets_par_heure_sans_motif_sans_other.csv', index=False)

#-------------------------------------------------------------------------------------------------------------------------
# with the option to include "other" or not and to regroup bsaed on motifs

# import pandas as pd


# output_path = "C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\csv_sunday2\\"

# include_other = True  # Set to True to include "other" motifs, False to exclude them
# group_motifs = True   # Set to True to group unspecified motifs into "divers"

# # List of motifs to explicitly keep (if grouping is enabled)
# explicit_motifs = [
#     ("home", "work"), ("home", "leisure"), ("home", "education"),
#     ("home", "other"), ("home", "shop"), ("work", "home"),
#     ("leisure", "home"), ("education", "home"), ("other", "home"),
#     ("shop", "home")
# ]

# df = pd.read_csv('agent_positions_motif_filtre_g_clean_sunday2.csv')

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
    
#     # Exclude "other" motifs if include_other is False
#     if not include_other and ("other" in [motif_orig, motif_dest]):
#         continue  # Skip this row if "other" should be excluded
    
#     # Determine the trip type
#     trip_type = (motif_orig, motif_dest)
    
#     # If grouping is enabled, categorize motifs not in explicit_motifs as "divers"
#     if group_motifs and trip_type not in explicit_motifs:
#         trip_type = ("divers", "divers")
    
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

# motif_df.to_csv(output_path + 'repartition_trajet_par_heure_avec_motif_regroup_nf.csv', index=False)
# trips_per_hour_df.to_csv(output_path + 'nombre_trajets_par_heure_sans_motif_regroup_nf.csv', index=False)



# import pandas as pd

# # Output path for saving CSVs
# output_path = "C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\csv_tuesday_short\\"

# # Parameters to control behavior
# include_other = True  # Set to True to include "other" motifs, False to exclude them
# group_motifs = True  # Set to True to group unspecified motifs into "divers"

# # List of motifs to explicitly keep (if grouping is enabled)
# explicit_motifs = [
#     ("home", "work"), ("home", "leisure"), ("home", "education"),
#     ("home", "other"), ("home", "shop"), ("work", "home"),
#     ("leisure", "home"), ("education", "home"), ("other", "home"),
#     ("shop", "home")
# ]

# # Load the CSV file
# df = pd.read_csv('agent_positions_motif_filtre_g_clean_tuesday_short.csv')

# # Convert 'Temps_minute' to hours (assuming it is in minutes)
# df['Temps_hour'] = df['Temps_minute'] // 60

# # Create dictionaries to count distinct agents per hour and trip type
# trips_by_motif_per_hour = {}

# # Loop over each row and count distinct trips by agents per hour and motif
# for _, row in df.iterrows():
#     agent_id = row['AgentId']
#     hour = row['Temps_hour']
#     motif_orig = row['Motif_Orig']
#     motif_dest = row['Motif_Dest']
    
#     # Exclude "other" motifs if include_other is False
#     if not include_other and ("other" in [motif_orig, motif_dest]):
#         continue  # Skip this row if "other" should be excluded
    
#     # Determine the trip type
#     trip_type = (motif_orig, motif_dest)
    
#     # If grouping is enabled, categorize motifs not in explicit_motifs as "divers"
#     if group_motifs and trip_type not in explicit_motifs:
#         trip_type = ("divers", "divers")
    
#     # Initialize the dictionary for this hour if it doesn't exist
#     if hour not in trips_by_motif_per_hour:
#         trips_by_motif_per_hour[hour] = {}
    
#     # Initialize the set for this trip type if it doesn't exist
#     if trip_type not in trips_by_motif_per_hour[hour]:
#         trips_by_motif_per_hour[hour][trip_type] = set()
    
#     # Add the agent to the set for this trip type in this hour
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
# motif_df.to_csv(output_path + 'repartition_trajet_par_heure_avec_motif_regroup.csv', index=False)
# trips_per_hour_df.to_csv(output_path + 'nombre_trajets_par_heure_sans_motif_regroup.csv', index=False)

import pandas as pd

output_path = "C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\csv_tuesday\\"
include_other = True  # Set to True to include "other" motifs, False to exclude them
group_motifs = True  # Set to True to group unspecified motifs into "divers"

# List of motifs to explicitly keep (if grouping is enabled)
explicit_motifs = [
    ("home", "work"), ("home", "leisure"), ("home", "education"),
    ("home", "other"), ("home", "shop"), ("work", "home"),
    ("leisure", "home"), ("education", "home"), ("other", "home"),
    ("shop", "home")
]

df = pd.read_csv('agent_positions_motif_filtre_g_clean_tuesday.csv')

# Sort by AgentId and Temps_minute to ensure proper ordering of trips
df = df.sort_values(by=['AgentId', 'Temps_minute'])

# Identify trip departures: mark the first row of each trip for each agent
df['Is_Departure'] = (df['Motif_Orig'] != df['Motif_Orig'].shift(-1)) | (df['AgentId'] != df['AgentId'].shift(-1))

# Filter only departure rows and create a copy to avoid SettingWithCopyWarning
departure_df = df[df['Is_Departure']].copy()

# Convert 'Temps_minute' to hours (assuming it is in minutes)
departure_df['Temps_hour'] = departure_df['Temps_minute'] // 60

# Create dictionaries to count distinct trips by agents at departure times
trips_by_motif_per_hour = {}

# Loop over each row and count distinct trips by agents at departure times
for _, row in departure_df.iterrows():
    agent_id = row['AgentId']
    hour = row['Temps_hour']
    motif_orig = row['Motif_Orig']
    motif_dest = row['Motif_Dest']
    
    # Exclude "other" motifs if include_other is False
    if not include_other and ("other" in [motif_orig, motif_dest]):
        continue  # Skip this row if "other" should be excluded
    
    # Determine the trip type
    trip_type = (motif_orig, motif_dest)
    
    # If grouping is enabled, categorize motifs not in explicit_motifs as "divers"
    if group_motifs and trip_type not in explicit_motifs:
        trip_type = ("divers", "divers")
    
    # Initialize the dictionary for this hour if it doesn't exist
    if hour not in trips_by_motif_per_hour:
        trips_by_motif_per_hour[hour] = {}
    
    # Initialize the set for this trip type if it doesn't exist
    if trip_type not in trips_by_motif_per_hour[hour]:
        trips_by_motif_per_hour[hour][trip_type] = set()
    
    # Add the agent to the set for this trip type at this hour
    trips_by_motif_per_hour[hour][trip_type].add(agent_id)

# Convert trips by motif per hour to a DataFrame
motif_data = []
for hour, motifs in trips_by_motif_per_hour.items():
    for (motif_orig, motif_dest), agents in motifs.items():
        motif_data.append([hour, motif_orig, motif_dest, len(agents)])  # Use len(agents) to count distinct agents

motif_df = pd.DataFrame(motif_data, columns=['Heure', 'Motif_Orig', 'Motif_Dest', 'Nombre_Trajet']).sort_values(by='Heure')

# Calculate the total number of trips per hour without distinguishing motifs
trips_per_hour_df = motif_df.groupby('Heure')['Nombre_Trajet'].sum().reset_index()

# Rename columns appropriately
trips_per_hour_df.columns = ['Heure', 'Nombre_Trajet']

motif_df.to_csv(output_path + 'repartition_trajet_par_heure_avec_motif_regroup.csv', index=False)
trips_per_hour_df.to_csv(output_path + 'nombre_trajets_par_heure_sans_motif_regroup.csv', index=False)

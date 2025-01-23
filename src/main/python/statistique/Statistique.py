# -----------------------------------------------------------------------------------------------------------
# Statitique qui calcule l'ensemble trajet tout par exemple si un agent fait 2 fois home to work, il va regrouper (avec fihcier agent_positions_motif_filtre_g.csv)

# import pandas as pd
# import numpy as np

# agents_df = pd.read_csv("agent_positions_motif_filtre_g_5000_short.csv")
# persons_df = pd.read_csv("C:/Users/User/IdeaProjects/matsim-example-project-modified/simulation_output_toulouse_5000/output_persons.csv.gz", sep=';')
# output_path = "C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\csv_short\\"

# agents_df['Heure'] = agents_df['Temps_minute'] // 60 

# # Population car: agents avec des vehicules (identifies avec ':car')
# population_car = agents_df['AgentId'].nunique()

# # Population non car: agents utilisant d'autres modes de transport
# population_autre = persons_df['person'].nunique()

# # Nombre total de trajets
# nombre_total_trajets = agents_df.groupby(['AgentId', 'Motif_Orig', 'Motif_Dest']).ngroups

# # Calculer le nombre de trajets par agent
# # Compter le nombre de combinaisons uniques de Motif_Orig et Motif_Dest par agent
# nombre_trajet_par_agent = agents_df.groupby('AgentId').apply(lambda x: len(x[['Motif_Orig', 'Motif_Dest']].drop_duplicates(subset=['Motif_Orig', 'Motif_Dest']))).reset_index(name='Nombre_Trajets')
# nombre_trajet_par_agent.to_csv(output_path + "nombre_trajet_par_agent.csv", index=False)

# # Calculer la duree pour chaque trajet
# duree_total_par_trajet = agents_df.groupby(['AgentId', 'Motif_Orig', 'Motif_Dest']).agg(
#     Duree_trajet=('Temps_minute', lambda x: x.max() - x.min())
# ).reset_index()
# duree_total_par_trajet.to_csv(output_path + "duree_total_par_trajet.csv", index=False)

# # Calculer le nombre de points (lignes) par trajet pour chaque agent
# nombre_points_par_trajet = agents_df.groupby(['AgentId', 'Motif_Orig', 'Motif_Dest']).size().reset_index(name='Nombre_Points')
# nombre_points_par_trajet.to_csv(output_path + "nombre_points_par_trajet.csv", index=False)

# # Calculer le nombre de trajets par motif
# nombre_trajet_par_motif = agents_df.groupby(['Motif_Orig', 'Motif_Dest'])['AgentId'].nunique().reset_index(name='Nombre_Trajets')
# nombre_trajet_par_motif.to_csv(output_path + "nombre_trajet_par_motif.csv", index=False)

# # Evolution du trafic (nombre d'agents actifs par minute)
# trafic_par_minute = agents_df.groupby('Temps_minute')['AgentId'].nunique().reset_index(name='Agents_Actifs')
# trafic_par_minute.to_csv(output_path + "evolution_trafic.csv", index=False)

# # Calculer la duree moyenne pour chaque trajet
# # On utilise les donnees de duree_total_par_trajet pour calculer la duree moyenne
# duree_moyenne_par_trajet = duree_total_par_trajet.groupby(['Motif_Orig', 'Motif_Dest'])['Duree_trajet'].mean().reset_index(name='Duree_Moyenne')
# duree_moyenne_par_trajet.to_csv(output_path + "duree_moyenne_par_trajet.csv", index=False)

# # Calculer le nombre minimum de points pour chaque type de trajet
# # On se base sur le fichier nombre_points_par_trajet pour calculer le nombre minimum de points
# nombre_min_points_trajet = nombre_points_par_trajet.loc[nombre_points_par_trajet.groupby(['Motif_Orig', 'Motif_Dest'])['Nombre_Points'].idxmin()]
# nombre_min_points_trajet = nombre_min_points_trajet[['Motif_Orig', 'Motif_Dest', 'AgentId', 'Nombre_Points']]
# nombre_min_points_trajet.columns = ['Motif_Orig', 'Motif_Dest', 'AgentId_Min', 'Nombre_Min_Points']
# nombre_min_points_trajet.to_csv(output_path + "nombre_min_points_trajet.csv", index=False)

# # Calculer le nombre maximum de points pour chaque type de trajet
# # On se base sur le fichier nombre_points_par_trajet pour calculer le nombre maximum de points
# nombre_max_points_trajet = nombre_points_par_trajet.loc[nombre_points_par_trajet.groupby(['Motif_Orig', 'Motif_Dest'])['Nombre_Points'].idxmax()]
# nombre_max_points_trajet = nombre_max_points_trajet[['Motif_Orig', 'Motif_Dest', 'AgentId', 'Nombre_Points']]
# nombre_max_points_trajet.columns = ['Motif_Orig', 'Motif_Dest', 'AgentId_Max', 'Nombre_Max_Points']
# nombre_max_points_trajet.to_csv(output_path + "nombre_max_points_trajet.csv", index=False)

# heure_debut_simulation = agents_df['Temps_minute'].min()
# heure_fin_simulation = agents_df['Temps_minute'].max()

# print("\n--- Statistiques sur les trajets dans le fichier agent_positions_motif_filtre_g.csv ---")
# print(f"Population car : {population_car}")
# print(f"Population autre : {population_autre}")
# print(f"Nombre total de trajets : {nombre_total_trajets}")
# print(f"Heure de debut de la simulation : {heure_debut_simulation}")
# print(f"Heure de fin de la simulation : {heure_fin_simulation}")

# -----------------------------------------------------------------------------------------------------------
# Statitique vrai qui prend en compte les different trajet home to work pour un agent (avec fihcier agent_positions_motif_filtre_g.csv)

import pandas as pd

agents_df = pd.read_csv("agent_positions_motif_filtre_g_clean_monday.csv")
persons_df = pd.read_csv("C:/Users/User/IdeaProjects/matsim-example-project-modified/simulation_output_monday/output_persons.csv.gz", sep=';')
output_path = "C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\csv_monday\\"

agents_df['Heure'] = agents_df['Temps_minute'] // 60
# agents_df = agents_df.sort_values(by=['AgentId', 'Motif_Orig', 'Motif_Dest', 'Temps_minute'])
agents_df = agents_df.sort_values(by=['AgentId', 'Temps_minute'])

# Identify a new trip sequence if there's a significant time gap between consecutive rows
agents_df['New_Trip'] = (
    (agents_df['AgentId'] != agents_df['AgentId'].shift()) |  # New agent
    (agents_df['Motif_Orig'] != agents_df['Motif_Orig'].shift()) |  # Change in origin
    (agents_df['Motif_Dest'] != agents_df['Motif_Dest'].shift()) |  # Change in destination
    (agents_df['Temps_minute'].diff() > 5)   # Time gap
    # ((agents_df['Event_Type'] == 'actend') | (agents_df['Event_Type'] == 'departure'))  # Specific events
).astype(int).cumsum()

population_car = agents_df['AgentId'].nunique()
population_autre = persons_df['person'].nunique()

# Total number of distinct trips
nombre_total_trajets = agents_df.groupby(['AgentId', 'Motif_Orig', 'Motif_Dest', 'New_Trip']).ngroups

# Calculate trips per agent
nombre_trajet_par_agent = agents_df.groupby('AgentId')['New_Trip'].nunique().reset_index(name='Nombre_Trajets')
nombre_trajet_par_agent.to_csv(output_path + "nombre_trajet_par_agent.csv", index=False)

# Calculate duration per trip
duree_total_par_trajet = agents_df.groupby(['AgentId', 'New_Trip', 'Motif_Orig', 'Motif_Dest']).agg(
    Duree_trajet=('Temps_minute', lambda x: x.max() - x.min())
).reset_index()

# Sort the DataFrame by AgentId and New_Trip to ensure logical order
duree_total_par_trajet = duree_total_par_trajet.sort_values(by=['AgentId', 'New_Trip'])

# Save the results
duree_total_par_trajet.to_csv(output_path + "duree_total_par_trajet.csv", index=False)

nombre_points_par_trajet = agents_df.groupby(['AgentId', 'Motif_Orig', 'Motif_Dest', 'New_Trip']).size().reset_index(name='Nombre_Points')
nombre_points_par_trajet.to_csv(output_path + "nombre_points_par_trajet.csv", index=False)

nombre_trajet_par_motif = agents_df.groupby(['Motif_Orig', 'Motif_Dest'])['New_Trip'].nunique().reset_index(name='Nombre_Trajets')
nombre_trajet_par_motif.to_csv(output_path + "nombre_trajet_par_motif.csv", index=False)

duree_moyenne_par_trajet = duree_total_par_trajet.groupby(['Motif_Orig', 'Motif_Dest'])['Duree_trajet'].mean().reset_index(name='Duree_Moyenne')
duree_moyenne_par_trajet.to_csv(output_path + "duree_moyenne_par_trajet.csv", index=False)

nombre_min_points_trajet = nombre_points_par_trajet.loc[nombre_points_par_trajet.groupby(['Motif_Orig', 'Motif_Dest'])['Nombre_Points'].idxmin()]
nombre_min_points_trajet = nombre_min_points_trajet[['Motif_Orig', 'Motif_Dest', 'AgentId', 'Nombre_Points']]
nombre_min_points_trajet.columns = ['Motif_Orig', 'Motif_Dest', 'AgentId_Min', 'Nombre_Min_Points']
nombre_min_points_trajet.to_csv(output_path + "nombre_min_points_trajet.csv", index=False)

nombre_max_points_trajet = nombre_points_par_trajet.loc[nombre_points_par_trajet.groupby(['Motif_Orig', 'Motif_Dest'])['Nombre_Points'].idxmax()]
nombre_max_points_trajet = nombre_max_points_trajet[['Motif_Orig', 'Motif_Dest', 'AgentId', 'Nombre_Points']]
nombre_max_points_trajet.columns = ['Motif_Orig', 'Motif_Dest', 'AgentId_Max', 'Nombre_Max_Points']
nombre_max_points_trajet.to_csv(output_path + "nombre_max_points_trajet.csv", index=False)

heure_debut_simulation = agents_df['Temps_minute'].min()
heure_fin_simulation = agents_df['Temps_minute'].max()

print("\n--- Statistiques sur les trajets dans le fichier agent_positions_motif_filtre_g.csv ---")
print(f"Population car : {population_car}")
print(f"Population autre : {population_autre}")
print(f"Nombre total de trajets distincts : {nombre_total_trajets}")
print(f"Heure de debut de la simulation : {heure_debut_simulation}")
print(f"Heure de fin de la simulation : {heure_fin_simulation}")

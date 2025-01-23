#----------------------------------------------------------------------------------------------------------
# Creer un fichier csv qui va etre utilise pour QGIS (AgentID, x_orig,y_orig,x_dest,y_dest)

# import pandas as pd

# # Charger le fichier CSV
# file_path = "C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\agent_positions_motif_filtre_g_5000_clean.csv"
# data = pd.read_csv(file_path)

# # Initialiser une liste pour stocker les trajets filtrés
# filtered_trips = []

# # Variables pour suivre l'état actuel
# current_agent = None
# current_motif = None
# start_row = None

# # Parcourir les données ligne par ligne
# for index, row in data.iterrows():
#     agent_id = row['AgentId']
#     motif_orig = row['Motif_Orig']
#     motif_dest = row['Motif_Dest']
#     x = row['x']
#     y = row['y']
    
#     # Détecter un changement d'agent ou de motif
#     if agent_id != current_agent or motif_orig != current_motif:
#         # Finaliser le trajet précédent si nécessaire
#         if start_row is not None:
#             filtered_trips.append({
#                 'AgentId': current_agent,
#                 'x_orig': start_row['x'],
#                 'y_orig': start_row['y'],
#                 'x_dest': row['x'],
#                 'y_dest': row['y']
#             })
#         # Mettre à jour l'état actuel
#         current_agent = agent_id
#         current_motif = motif_orig
#         start_row = row

# # Ajouter le dernier trajet
# if start_row is not None and current_motif is not None:
#     filtered_trips.append({
#         'AgentId': current_agent,
#         'x_orig': start_row['x'],
#         'y_orig': start_row['y'],
#         'x_dest': row['x'],
#         'y_dest': row['y']
#     })

# # Convertir les trajets filtrés en DataFrame
# filtered_trips_df = pd.DataFrame(filtered_trips)

# # Enregistrer les trajets filtrés dans un fichier CSV
# output_filtered_path = "C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\agent_positions_motif_filtre_g_5000_clean_qgis.csv"
# filtered_trips_df.to_csv(output_filtered_path, index=False)

# print(f"Fichier des trajets filtrés enregistré : {output_filtered_path}")

#----------------------------------------------------------------------------------------------------------
# Creer un fichier csv qui va etre utilise pour QGIS (AgentID, x_orig,y_orig,x_dest,y_dest,Motif_Orig,Motif_Dest)

import pandas as pd

file_path = "C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\agent_positions_motif_filtre_g_5000_clean.csv"
data = pd.read_csv(file_path)

# Initialiser une liste pour stocker les trajets filtrés
filtered_trips = []

# Trier les données par AgentId et Temps (si nécessaire pour garantir l'ordre temporel)
data = data.sort_values(by=['AgentId', 'Temps_minute'])

# Variables pour suivre l'état actuel
current_agent = None
current_motif_orig = None
current_motif_dest = None
start_row = None

# Parcourir les données ligne par ligne
for index, row in data.iterrows():
    agent_id = row['AgentId']
    motif_orig = row['Motif_Orig']
    motif_dest = row['Motif_Dest']
    x = row['x']
    y = row['y']
    
    # Détecter un changement d'agent ou de motifs
    if agent_id != current_agent or motif_orig != current_motif_orig or motif_dest != current_motif_dest:
        # Si un trajet précédent est en cours, enregistrer ses détails
        if start_row is not None:
            filtered_trips.append({
                'AgentId': current_agent,
                'Motif_Orig': current_motif_orig,
                'Motif_Dest': current_motif_dest,
                'x_orig': start_row['x'],
                'y_orig': start_row['y'],
                'x_dest': previous_row['x'],
                'y_dest': previous_row['y']
            })
        # Mettre à jour l'état actuel
        current_agent = agent_id
        current_motif_orig = motif_orig
        current_motif_dest = motif_dest
        start_row = row  # Première ligne du nouveau couple Motif_Orig/Motif_Dest

    # Mémoriser la dernière ligne rencontrée
    previous_row = row

# Ajouter le dernier trajet si nécessaire
if start_row is not None:
    filtered_trips.append({
        'AgentId': current_agent,
        'Motif_Orig': current_motif_orig,
        'Motif_Dest': current_motif_dest,
        'x_orig': start_row['x'],
        'y_orig': start_row['y'],
        'x_dest': previous_row['x'],
        'y_dest': previous_row['y']
    })

filtered_trips_df = pd.DataFrame(filtered_trips)

output_filtered_path = "C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\agent_positions_motif_filtre_g_5000_clean_qgis.csv"
filtered_trips_df.to_csv(output_filtered_path, index=False)

print(f"Fichier des trajets filtrés enregistré : {output_filtered_path}")

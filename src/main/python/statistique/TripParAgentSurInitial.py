import pandas as pd

file_path = "C:/Users/User/IdeaProjects/matsim-example-project-modified/csv_clean/duree_total_par_trajet.csv"
data = pd.read_csv(file_path)

# pour stocker les trajets commandés
ordered_trips = []

# Grouper les données par AgentId
for agent_id, agent_data in data.groupby('AgentId'):
    # Trier les données de l'agent par ordre chronologique des trajets
    agent_data = agent_data.sort_values(by=['New_Trip']).reset_index(drop=True)
    
    # Initialiser le motif courant à l'origine du premier voyage
    current_motif = agent_data.loc[0, 'Motif_Orig']
    
    # Parcourir les trajets de l'agent
    for _, row in agent_data.iterrows():
        if row['Motif_Orig'] == current_motif:
            # Ajouter le trajet à la liste
            ordered_trips.append({
                'AgentId': row['AgentId'],
                'Motif_Orig': row['Motif_Orig'],
                'Motif_Dest': row['Motif_Dest'],
                'New_Trip': row['New_Trip']
            })
            # Mettre à jour le motif courant
            current_motif = row['Motif_Dest']
        else:
            # Ignorer si le motif ne correspond pas
            continue

# Créer un DataFrame à partir des trajets commandés
ordered_trips_df = pd.DataFrame(ordered_trips)

output_file = 'ordered_daily_trips.csv'
ordered_trips_df.to_csv(output_file, index=False)

print(f"Fichier {output_file} généré avec succès.")

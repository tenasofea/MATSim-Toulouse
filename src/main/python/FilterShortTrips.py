import pandas as pd

agents_df = pd.read_csv("C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\agent_positions_motif_filtre_g_clean_monday.csv")

min_duration = 2
max_duration = 90

filtered_trips = []

# trier le DataFrame pour assurer l'ordre chronologique des enregistrements de chaque agent
agents_df = agents_df.sort_values(by=['AgentId', 'Temps_minute']).reset_index(drop=True)

# identifier et traiter chaque sequence de trajets pour chaque agent
for agent_id, group in agents_df.groupby('AgentId'):
    # initialiser les variables pour suivre chaque trajet
    previous_motif_orig = None
    previous_motif_dest = None
    current_trip = []

    for _, row in group.iterrows():
        motif_orig, motif_dest = row['Motif_Orig'], row['Motif_Dest']
        
        # si les motifs changent ou que c'est la premiere ligne, debuter un nouveau trajet
        if (motif_orig != previous_motif_orig or motif_dest != previous_motif_dest) and current_trip:
            # calculer la duree du trajet et l'ajouter s'il est dans les limites
            trip_duration = current_trip[-1]['Temps_minute'] - current_trip[0]['Temps_minute']
            if min_duration <= trip_duration <= max_duration:
                filtered_trips.extend(current_trip)
                
            # reinitialiser les variables pour un nouveau trajet
            current_trip = []
        
        # maj les motifs et ajouter la ligne actuelle au trajet en cours
        previous_motif_orig, previous_motif_dest = motif_orig, motif_dest
        current_trip.append(row)

    # verifier et ajouter le dernier trajet dans le groupe si la duree respecte les limites
    if current_trip:
        trip_duration = current_trip[-1]['Temps_minute'] - current_trip[0]['Temps_minute']
        if min_duration <= trip_duration <= max_duration:
            filtered_trips.extend(current_trip)

filtered_trips_df = pd.DataFrame(filtered_trips)
filtered_trips_df.to_csv("C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\agent_positions_motif_filtre_g_clean_monday_short.csv", index=False)



import pandas as pd

file_paths = {
    'Sunday': "C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\activity_sunday_real_car.csv",
    'Monday': "C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\activity_monday_real_car.csv",
    'Tuesday': "C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\activity_tuesday_real_car.csv",
    'Wednesday': "C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\activity_wednesday_real_car.csv",
    'Thursday': "C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\activity_thursday_real_car.csv",
    'Friday': "C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\activity_friday_real_car.csv",
    'Saturday': "C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\activity_saturday_real_car.csv",
}

all_data = []

# charger chaque fichier, ajouter la colonne Day et ajouter à la liste
for day, path in file_paths.items():
    daily_data = pd.read_csv(path)
    daily_data['Day'] = day  
    all_data.append(daily_data)

# concatener tous les données dans un seul DataFrame
combined_data = pd.concat(all_data, ignore_index=True)

# definir l’ordre des jours pour assurer un tri correct
day_order = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
combined_data['Day'] = pd.Categorical(combined_data['Day'], categories=day_order, ordered=True)

# trier par AgentId, Day et New_Trip pour assurer l’ordre chronologique
combined_data = combined_data.sort_values(by=['AgentId', 'Day', 'New_Trip']).reset_index(drop=True)

# initialiser une liste pour stocker les trajets commandés
ordered_trips = []

# traiter les deplacements de chaque agent séquentiellement
for agent_id, agent_data in combined_data.groupby('AgentId'):
    # trier les données de l’agent par jour et par New_Trip pour maintenir l’ordre des jours
    agent_data = agent_data.sort_values(by=['Day', 'New_Trip']).reset_index(drop=True)
    
    # initialiser le motif courant à l’origine de départ du premier voyage
    current_motif = agent_data.loc[0, 'Motif_Orig']
    
    for i, row in agent_data.iterrows():
        # verifier si le voyage en cours commence à partir de l’origine prevue (motif actuel)
        if row['Motif_Orig'] == current_motif:
            # ajouter la ligne aux trajets commandés
            ordered_trips.append({
                'AgentId': row['AgentId'],
                'Day': row['Day'],
                'Motif_Orig': row['Motif_Orig'],
                'Motif_Dest': row['Motif_Dest']
            })
            # maj le motif actuel pour la destination de ce voyage
            current_motif = row['Motif_Dest']
        else:
            # ignorer cette ligne si elle ne commence pas à partir de l’origine attendue
            continue

# creer un DataFrame à partir des trajets commandes
ordered_trips_df = pd.DataFrame(ordered_trips)

output_file = 'ordered_weekly_trips.csv'
ordered_trips_df.to_csv(output_file, index=False)


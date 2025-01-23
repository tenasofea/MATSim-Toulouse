# import pandas as pd

# # filter consecutive identical links and keep only the last occurrence in each sequence
# def filtrer_liaisons_consecutives(fichier_csv, fichier_sortie):
#     df = pd.read_csv(fichier_csv)
    
#     # trier par AgentId et Temps_minute pour assurer la bonne sequence temporelle
#     df = df.sort_values(by=['AgentId', 'Temps_minute'])

#     # detecter les changements de lien consecutifs par agent
#     df['link_change'] = (df['link'] != df['link'].shift()) | (df['AgentId'] != df['AgentId'].shift())
    
#     # garder uniquement la derniere ligne pour chaque sequence de liens identiques
#     filtered_df = df[(df['link_change'].shift(-1) == True) | (df['link_change'].shift(-1).isnull())]

#     # supprimer la colonne temporaire
#     filtered_df = filtered_df.drop(columns=['link_change'])

#     # Sauvegarder le fichier filtre
#     filtered_df.to_csv(fichier_sortie, index=False)

# fichier_csv = "agent_positions_motif_5000.csv"  
# fichier_sortie = "agent_positions_motif_filtre_5000.csv"  
# filtrer_liaisons_consecutives(fichier_csv, fichier_sortie)

import pandas as pd

# Filter consecutive identical links and keep only the first and last occurrence in each sequence if it exceeds 15 occurrences
def filtrer_liaisons_consecutives(fichier_csv, fichier_sortie):
    df = pd.read_csv(fichier_csv)
    
    # Sort by AgentId and Temps_minute to ensure the correct temporal sequence
    df = df.sort_values(by=['AgentId', 'Temps_minute'])

    # Detect consecutive link changes by agent
    df['link_change'] = (df['link'] != df['link'].shift()) | (df['AgentId'] != df['AgentId'].shift())
    df['sequence_id'] = df['link_change'].cumsum()  # Create a unique identifier for each sequence of identical links
    
    # Group by agent and sequence to check for sequences with more than 15 occurrences
    def filter_sequence(group):
        if len(group) > 15:  # Check if the sequence length exceeds 15
            return pd.concat([group.iloc[[0]], group.iloc[[-1]]])  # Keep only the first and last rows
        return group  # Keep the entire group if sequence length is 15 or less

    # Apply the filtering function to each sequence
    filtered_df = df.groupby(['AgentId', 'sequence_id']).apply(filter_sequence).reset_index(drop=True)
    
    # Drop temporary columns
    filtered_df = filtered_df.drop(columns=['link_change', 'sequence_id'])

    # Save the filtered file
    filtered_df.to_csv(fichier_sortie, index=False)

fichier_csv = "agent_positions_motif_5000_clean.csv"  
fichier_sortie = "agent_positions_motif_filtre_5000_clean_test.csv"  
filtrer_liaisons_consecutives(fichier_csv, fichier_sortie)





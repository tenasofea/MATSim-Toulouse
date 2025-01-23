import pandas as pd
import numpy as np

def ajouter_gaussienne(df, sigma=1.0):
    # ajouter une gaussienne circulaire aux coordonnees x et y pour chaque agent sur le meme lien
    # genere un ensemble de valeurs aleatoires avec une moyenne de 0 et un ecart-type de sigma
    # ~ 68% des valeurs genere par np.random.normal(0, 1, size=len(df)) seront comprises entre -1 et +1.
    df['x'] += np.random.normal(0, sigma, size=len(df)) 
    df['y'] += np.random.normal(0, sigma, size=len(df))  
    return df

fichier_csv = "agent_positions_motif_filtre_clean_monday.csv"
df = pd.read_csv(fichier_csv)

df_avec_gaussienne = ajouter_gaussienne(df, sigma=1.0)  

fichier_sortie_csv = "agent_positions_motif_filtre_g_clean_monday.csv"
df_avec_gaussienne.to_csv(fichier_sortie_csv, index=False)


import pandas as pd
import matplotlib.pyplot as plt

# Fonction pour tracer le trajet d'un agent spécifique
def tracer_trajet_agent(fichier_csv, agent_id):

    df = pd.read_csv(fichier_csv)
    
    # Filtrer les donnees pour l'agent specifie
    df_agent = df[df['AgentId'] == agent_id]
    
    # Verifier si l'agent est present dans le fichier
    if df_agent.empty:
        print(f"Aucun trajet trouve pour l'agent {agent_id}")
        return

    # Tracer le trajet (x, y) pour l'agent
    plt.figure(figsize=(10, 6))
    plt.plot(df_agent['x'], df_agent['y'], marker='o', linestyle='-', color='b', label=f'Trajet de l\'agent {agent_id}')
    
    # Ajouter des labels et un titre
    plt.title(f'Trajet de l\'agent {agent_id}')
    plt.xlabel('Coordinate X')
    plt.ylabel('Coordinate Y')
    
    # Afficher les points de depart et d'arrivee
    plt.scatter(df_agent['x'].iloc[0], df_agent['y'].iloc[0], color='green', label='Depart', zorder=5)
    plt.scatter(df_agent['x'].iloc[-1], df_agent['y'].iloc[-1], color='red', label='Arrivee', zorder=5)
    
    plt.legend()
    plt.grid(True)
    plt.show()

fichier_csv = "agent_positions_motif_filtre_g_5000_clean.csv"
agent_id = "2551898:car" 

tracer_trajet_agent(fichier_csv, agent_id)

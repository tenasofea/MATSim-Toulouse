import pandas as pd
from collections import defaultdict

def detect_home_motif_home(input_file, output_file):
    df = pd.read_csv(input_file)
    
    # Créer un dictionnaire pour suivre les motifs par agent
    agent_motif_counts = defaultdict(set)
    
    # Boucle pour parcourir les lignes et identifier les home-motif-home
    for i in range(len(df) - 1):
        current_row = df.iloc[i]
        next_row = df.iloc[i + 1]
        
        # Vérifier si c'est un trajet de type home -> motif -> home
        if (
            current_row['AgentId'] == next_row['AgentId'] and
            current_row['Motif_Orig'] == 'home' and
            next_row['Motif_Dest'] == 'home' and
            current_row['Motif_Dest'] != 'home'  
        ):
            motif = current_row['Motif_Dest']
            agent_motif_counts[motif].add(current_row['AgentId'])
    
    # Compter le nombre d'agents par motif
    result = {'Motif': [], 'Nombre_Agent': []}
    for motif, agents in agent_motif_counts.items():
        result['Motif'].append(motif)
        result['Nombre_Agent'].append(len(agents))
    
    result_df = pd.DataFrame(result)
    result_df.to_csv(output_file, index=False)

# Fonction pour vérifier les motifs d'un agent spécifique
def check_agent_motifs(input_file, agent_id):
    df = pd.read_csv(input_file)
    motifs = []
    for i in range(len(df) - 1):
        current_row = df.iloc[i]
        next_row = df.iloc[i + 1]
        
        if (
            current_row['AgentId'] == next_row['AgentId'] == agent_id and
            current_row['Motif_Orig'] == 'home' and
            next_row['Motif_Dest'] == 'home' and
            current_row['Motif_Dest'] != 'home'
        ):
            motifs.append(current_row['Motif_Dest'])
    
    if motifs:
        print(f"Agent {agent_id} a motifs : {set(motifs)}")
    else:
        print(f"Aucun motif trouve pour l'agent {agent_id}.")

# Fonction pour afficher les identifiants des agents pour un motif donné
def get_agents_for_motif(input_file, motif):
    df = pd.read_csv(input_file)
    agents = []
    for i in range(len(df) - 1):
        current_row = df.iloc[i]
        next_row = df.iloc[i + 1]
        
        if (
            current_row['Motif_Orig'] == 'home' and
            next_row['Motif_Orig'] == motif and
            next_row['Motif_Dest'] == 'home' and
            current_row['Motif_Dest'] == motif
        ):
            agents.append(current_row['AgentId'])
    
    agents = set(agents)  # Supprimer les doublons
    if agents:
        print(f"Agents '{motif}' :")
        for agent in sorted(agents):
            print(int(agent))  # Conversion explicite en int
    else:
        print(f"Aucun agent n'a effectué le motif '{motif}'.")


input_file = "C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\csv_sunday\\duree_total_par_trajet.csv"
output_file = "C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\csv_sunday\\nombre_agent_par_motif.csv"
detect_home_motif_home(input_file, output_file)

# Vérifier les motifs pour un identifiant d'agent spécifique
# agent_id = 2675231
# check_agent_motifs(input_file, agent_id)


# # Afficher les identifiants des agents pour un motif
# motif = 'education'  # Remplacez par le motif que vous voulez vérifier
# get_agents_for_motif(input_file, motif)

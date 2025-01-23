import pandas as pd
import matplotlib.pyplot as plt

traffic_df = pd.read_csv("C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\csv_semaine\\nombre_trajets_par_jour_sans_motif_regroup.csv")
motif_df = pd.read_csv("C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\csv_semaine\\repartition_trajet_par_jour_avec_motif_regroup.csv")

# renommer colonne
traffic_df.columns = ['Jour', 'Nombre_Agents']

# Define day order for sorting
day_order = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']
traffic_df['Jour'] = pd.Categorical(traffic_df['Jour'], categories=day_order, ordered=True)
motif_df['Jour'] = pd.Categorical(motif_df['Jour'], categories=day_order, ordered=True)

# calculer le nombre total d’agents par jour sur les motifs
total_agents_per_day = motif_df.groupby('Jour')['Nombre_Trajet'].sum().reset_index()
total_agents_per_day.columns = ['Jour', 'Total_Motif_Agents']

# fusionner les datas de trafic (total des agents actifs) avec datas du motif (agents par motif)
merged_df = pd.merge(motif_df, traffic_df, on='Jour')

# compte les motifs de l’echelle pour que leur somme corresponde au total des agents actifs par jour
merged_df['Normalized_Trajet'] = merged_df.apply(
    lambda row: row['Nombre_Trajet'] * row['Nombre_Agents'] / total_agents_per_day.loc[total_agents_per_day['Jour'] == row['Jour'], 'Total_Motif_Agents'].values[0],
    axis=1
)

# faire pivoter les données pour le tracé des barres empilées par jour
pivot_df = merged_df.pivot(index='Jour', columns=['Motif_Orig', 'Motif_Dest'], values='Normalized_Trajet').fillna(0)

# flatten the MultiIndex columns
pivot_df.columns = [f"{orig} -> {dest}" for orig, dest in pivot_df.columns]

# Plotting the repartition stacked bar chart with normalized values
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(12, 6))
pivot_df.plot(kind='bar', stacked=True, ax=ax, colormap='tab20')

ax.set_title("Repartition of Trips by Day with Total Active Agents")
ax.set_xlabel("Day")
ax.set_ylabel("Number of Trips (Total Active Agents per Day)")
ax.legend(title="Motif (Orig -> Dest)", bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.show()

# tracer le graphique à barres empilees de repartition avec des valeurs normalisees
plt.figure(figsize=(10, 6))
plt.plot(traffic_df['Jour'], traffic_df['Nombre_Agents'], color='blue', linewidth=1)
plt.title("Évolution du Trafic au Cours de la Simulation (Par Jour)")
plt.xlabel("Day")
plt.ylabel("Nombre d'Agents Actifs")
plt.grid(True)
plt.tight_layout()
plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

file_path = 'C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\csv_short\\duree_total_par_trajet.csv'
data = pd.read_csv(file_path)

home_work_trips = data[(data['Motif_Orig'] == 'home') & (data['Motif_Dest'] == 'work')]

# --------------------------------------------------------------------------------------------------------------------------
# Display graphique avec matplotlib directcly (ca marche pas)

# plt.figure(figsize=(10, 6))
# plt.hist(home_work_trips['Duree_trajet'], bins=range(0, home_work_trips['Duree_trajet'].max() + 5, 5), edgecolor='black')
# plt.xlabel('Durée du trajet (minutes)')
# plt.ylabel('Nombre de trajets')
# plt.title('Distribution des trajets domicile-travail en fonction de leur durée')
# plt.show()

# ----------------------------------------------------------------------------------------------------------------------------
# Display interactive graph online (ca marche mais attention au nbins)

fig = px.histogram(
    home_work_trips,
    x='Duree_trajet',
    nbins=100,  
    labels={'Duree_trajet': 'Durée du trajet (minutes)'},
    title='Distribution des trajets domicile-travail en fonction de leur durée'
)

fig.update_layout(
    xaxis_title='Durée du trajet (minutes)',
    yaxis_title='Nombre de trajets'
)
fig.show()

#-------------------------------------------------------------------------------------------------------------------------
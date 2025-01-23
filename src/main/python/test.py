# import xml.etree.ElementTree as ET
# import gzip
# from collections import defaultdict

# # lire le fichier reseau et recupere les coordonnees des noeuds et les liens
# def lire_reseau(fichier_network):
#     coordonnees_noeuds = {}  # dict ou chaque cle : un id de noeud, la valeur : un tuple des coordonnees (x, y)
#     liens = {}               # dict ou chaque cle : un id de lien, la valeur : un tuple des noeuds de depart et d'arrivee de ce lien

#     with gzip.open(fichier_network, 'rt', encoding='utf-8') as f:
#         tree = ET.parse(f)
#         root = tree.getroot()

#         # recuperer les noeuds et leurs coordonnees
#         for node in root.findall('.//node'):
#             node_id = node.get('id')
#             x = float(node.get('x'))
#             y = float(node.get('y'))
#             coordonnees_noeuds[node_id] = (x, y)

#         # recuperer les liens et leurs noeuds de depart et d'arrivee
#         for link in root.findall('.//link'):
#             link_id = link.get('id')
#             from_node = link.get('from')
#             to_node = link.get('to')
#             liens[link_id] = (from_node, to_node)

#     return coordonnees_noeuds, liens

# # interpolation des positions entre le temps d'entree et le temps de sortie
# def interpoler_positions(enterTime, leaveTime, coordStart, coordEnd, current_time):
#     interpolated_positions = []
#     duration = leaveTime - enterTime

#     # interpolation à chaque minute entre enterTime et leaveTime
#     for t in range(int(enterTime), int(leaveTime) + 1, 60): 
#         ratio = (t - enterTime) / duration
#         x = coordStart[0] + ratio * (coordEnd[0] - coordStart[0])
#         y = coordStart[1] + ratio * (coordEnd[1] - coordStart[1])
#         interpolated_positions.append((current_time, x, y))  # use current_time starting from actend time
#         current_time += 1
#     return interpolated_positions, current_time

# # lire les events de vehicule, ecrire les positions des agents dans un fichier CSV avec motifs et interpolation
# def ecrire_positions_vehicules(fichier_events, fichier_network, fichier_sortie_csv):
#     coordonnees_noeuds, liens = lire_reseau(fichier_network)
#     positions_par_vehicule = defaultdict(list)  # stocke les positions des vehicules apres interpolation. cle : vehicle_id, valeur : liste de positions interpole
#     motif_orig = None
#     motif_dest = None
#     enter_time = None
#     leave_time = None
#     coord_start = None
#     coord_end = None
#     current_time = 0  # temps_minute starts at the time from output_detaillees
#     offset_time = 0  # to store the actend time and use it for the next trip

#     tree = ET.parse(fichier_events)
#     root = tree.getroot()

#     with open(fichier_sortie_csv, 'a') as f_out:
#         # iterer sur tous les events
#         for event in root.findall('event'):
#             event_type = event.get('type')
#             vehicle_id = event.get('vehicle')

#             # pour capturer le motif d'origine (et ne le prendre en compte que si facility est present)
#             if event_type == 'actend' and event.get('facility') is not None:
#                 motif_orig = event.get('actType')
#                 offset_time = float(event.get('time'))  # store the actend time as the offset
#                 current_time = offset_time  # reset the current_time to this actend time

#             # pour capturer le motif de destination (et ne le prendre en compte que si facility est present)
#             elif event_type == 'actstart' and event.get('facility') is not None:
#                 motif_dest = event.get('actType')

#                 # lorsque l'on a à la fois Motif_Orig et Motif_Dest, on ecrit les positions correspondantes
#                 if motif_orig and motif_dest:
#                     for vehicle, positions in positions_par_vehicule.items():
#                         for (time_minute, x, y, link_id) in positions:
#                             f_out.write(f"{vehicle},{time_minute},{link_id},{x},{y},{motif_orig},{motif_dest}\n")
#                     # effacer les positions pour un nouveau trajet            
#                     positions_par_vehicule.clear()

#             if event_type == 'entered link':
#                 link_id = event.get('link')
#                 enter_time = float(event.get('time'))

#                 # recuper le noeud de depart "from" et d'arrivee "to" du lien
#                 if link_id in liens:
#                     from_node, to_node = liens[link_id]
#                     coord_start = coordonnees_noeuds.get(from_node)
#                     coord_end = coordonnees_noeuds.get(to_node)

#             elif event_type == 'left link':
#                 leave_time = float(event.get('time'))

#                 # si toutes les donnees sont disponibles, effectuer l'interpolation
#                 if enter_time and leave_time and coord_start and coord_end:
#                     interpolated_positions, current_time = interpoler_positions(enter_time, leave_time, coord_start, coord_end, current_time)

#                     # Accumuler les positions interpolées avec le link_id
#                     for time_minute, x, y in interpolated_positions:
#                         positions_par_vehicule[vehicle_id].append((time_minute, x, y, link_id))

#                 # reinitialiser les valeurs pour le prochain lien
#                 enter_time = None
#                 leave_time = None
#                 coord_start = None
#                 coord_end = None

#         # ecrire toutes les positions restantes à la fin de l'iteration
#         if motif_orig and motif_dest:
#             for vehicle, positions in positions_par_vehicule.items():
#                 for (time_minute, x, y, link_id) in positions:
#                     f_out.write(f"{vehicle},{time_minute},{link_id},{x},{y},{motif_orig},{motif_dest}\n")

# # Paths to the files
# fichier_events = "C:/Users/User/IdeaProjects/matsim-example-project-modified/output_detaillees_car.xml"
# fichier_network = "C:/Users/User/IdeaProjects/matsim-example-project-modified/simulation_output_toulouse/output_network.xml.gz"
# fichier_sortie_csv = "agent_positions_motif_test.csv"

# # Initialize the output CSV with headers
# with open(fichier_sortie_csv, 'w') as f_out:
#     f_out.write("AgentId,Temps_minute,link,x,y,Motif_Orig,Motif_Dest\n")

# # Execute the function to extract and write agent positions
# ecrire_positions_vehicules(fichier_events, fichier_network, fichier_sortie_csv)

# import xml.etree.ElementTree as ET
# import gzip
# from collections import defaultdict

# # lire le fichier reseau et recupere les coordonnees des noeuds et les liens
# def lire_reseau(fichier_network):
#     coordonnees_noeuds = {}  # dict ou chaque cle : un id de noeud, la valeur : un tuple des coordonnees (x, y)
#     liens = {}               # dict ou chaque cle : un id de lien, la valeur : un tuple des noeuds de depart et d'arrivee de ce lien

#     with gzip.open(fichier_network, 'rt', encoding='utf-8') as f:
#         tree = ET.parse(f)
#         root = tree.getroot()

#         # recuperer les noeuds et leurs coordonnees
#         for node in root.findall('.//node'):
#             node_id = node.get('id')
#             x = float(node.get('x'))
#             y = float(node.get('y'))
#             coordonnees_noeuds[node_id] = (x, y)

#         # recuperer les liens et leurs noeuds de depart et d'arrivee
#         for link in root.findall('.//link'):
#             link_id = link.get('id')
#             from_node = link.get('from')
#             to_node = link.get('to')
#             liens[link_id] = (from_node, to_node)

#     return coordonnees_noeuds, liens

# def calculer_position(enterTime, leaveTime, coordStart, coordEnd, event_time):
#     # Calculate the ratio of the event time in relation to the link traversal time
#     ratio = (event_time - enterTime) / (leaveTime - enterTime)
#     x = coordStart[0] + ratio * (coordEnd[0] - coordStart[0])
#     y = coordStart[1] + ratio * (coordEnd[1] - coordStart[1])
#     return x, y

# def ecrire_positions_vehicules(fichier_events, fichier_network, fichier_sortie_csv):
#     coordonnees_noeuds, liens = lire_reseau(fichier_network)
#     positions_par_vehicule = defaultdict(list)
#     motif_orig = None
#     motif_dest = None
#     enter_time = None
#     leave_time = None
#     coord_start = None
#     coord_end = None

#     tree = ET.parse(fichier_events)
#     root = tree.getroot()

#     with open(fichier_sortie_csv, 'a') as f_out:
#         for event in root.findall('event'):
#             event_type = event.get('type')
#             vehicle_id = event.get('vehicle')

#             # Capture 'actend' event to store origin motif
#             if event_type == 'actend' and event.get('facility') is not None:
#                 motif_orig = event.get('actType')

#             # Capture 'actstart' event to store destination motif
#             elif event_type == 'actstart' and event.get('facility') is not None:
#                 motif_dest = event.get('actType')

#                 if motif_orig and motif_dest:
#                     for vehicle, positions in positions_par_vehicule.items():
#                         for (event_time, x, y, link_id) in positions:
#                             f_out.write(f"{vehicle},{event_time},{link_id},{x},{y},{motif_orig},{motif_dest}\n")
#                     positions_par_vehicule.clear()  # Clear positions for a new trip

#             # Handle entered link
#             if event_type == 'entered link':
#                 link_id = event.get('link')
#                 enter_time = float(event.get('time'))

#                 if link_id in liens:
#                     from_node, to_node = liens[link_id]
#                     coord_start = coordonnees_noeuds.get(from_node)
#                     coord_end = coordonnees_noeuds.get(to_node)

#             # Handle left link and calculate position only at the leave time
#             elif event_type == 'left link':
#                 leave_time = float(event.get('time'))

#                 if enter_time and leave_time and coord_start and coord_end:
#                     # Calculate positions at both enter_time and leave_time
#                     x_start, y_start = calculer_position(enter_time, leave_time, coord_start, coord_end, enter_time)
#                     x_end, y_end = calculer_position(enter_time, leave_time, coord_start, coord_end, leave_time)

#                     # Append both positions (start and end of the link traversal)
#                     positions_par_vehicule[vehicle_id].append((enter_time, x_start, y_start, link_id))
#                     positions_par_vehicule[vehicle_id].append((leave_time, x_end, y_end, link_id))

#                 # Reset for the next link
#                 enter_time = None
#                 leave_time = None
#                 coord_start = None
#                 coord_end = None

#         # Write remaining positions at the end of iteration
#         if motif_orig and motif_dest:
#             for vehicle, positions in positions_par_vehicule.items():
#                 for (event_time, x, y, link_id) in positions:
#                     f_out.write(f"{vehicle},{event_time},{link_id},{x},{y},{motif_orig},{motif_dest}\n")



# # Paths to the files
# fichier_events = "C:/Users/User/IdeaProjects/matsim-example-project-modified/output_detaillees_car.xml"
# fichier_network = "C:/Users/User/IdeaProjects/matsim-example-project-modified/simulation_output_toulouse/output_network.xml.gz"
# fichier_sortie_csv = "agent_positions_motif_test2.csv"

# # Initialize the output CSV with headers
# with open(fichier_sortie_csv, 'w') as f_out:
#     f_out.write("AgentId,Temps_minute,link,x,y,Motif_Orig,Motif_Dest\n")

# # Execute the function to extract and write agent positions
# ecrire_positions_vehicules(fichier_events, fichier_network, fichier_sortie_csv)

# import xml.etree.ElementTree as ET
# import gzip
# from collections import defaultdict

# def lire_reseau(fichier_network):
#     coordonnees_noeuds = {}  # dict ou chaque cle : un id de noeud, la valeur : un tuple des coordonnees (x, y)
#     liens = {}               # dict ou chaque cle : un id de lien, la valeur : un tuple des noeuds de depart et d'arrivee de ce lien

#     with gzip.open(fichier_network, 'rt', encoding='utf-8') as f:
#         tree = ET.parse(f)
#         root = tree.getroot()

#         # recuperer les noeuds et leurs coordonnees
#         for node in root.findall('.//node'):
#             node_id = node.get('id')
#             x = float(node.get('x'))
#             y = float(node.get('y'))
#             coordonnees_noeuds[node_id] = (x, y)

#         # recuperer les liens et leurs noeuds de depart et d'arrivee
#         for link in root.findall('.//link'):
#             link_id = link.get('id')
#             from_node = link.get('from')
#             to_node = link.get('to')
#             liens[link_id] = (from_node, to_node)

#     return coordonnees_noeuds, liens


# # Fonction d'interpolation pour calculer les positions chaque minute
# def interpoler_positions_par_minute(enterTime, leaveTime, coordStart, coordEnd, offset_time):
#     positions = []
#     duration = leaveTime - enterTime
#     current_time = offset_time  # Début du calcul avec l'offset_time, au début d'un nouveau trajet

#     if duration < 60:  # Si la durée est inférieure à une minute, on prend uniquement la position de fin
#         ratio = 1
#         x = coordStart[0] + ratio * (coordEnd[0] - coordStart[0])
#         y = coordStart[1] + ratio * (coordEnd[1] - coordStart[1])
#         positions.append((current_time, x, y))  # Temps en minutes
#     else:
#         # Générer des positions à chaque minute
#         for t in range(int(enterTime), int(leaveTime), 60):
#             ratio = (t - enterTime) / duration
#             x = coordStart[0] + ratio * (coordEnd[0] - coordStart[0])
#             y = coordStart[1] + ratio * (coordEnd[1] - coordStart[1])
#             positions.append((current_time, x, y))  # Temps en minutes
#             current_time += 1  # Incrémenter le temps à chaque minute
#         # Ajouter également la position exacte au temps de sortie
#         x = coordEnd[0]
#         y = coordEnd[1]
#         positions.append((current_time, x, y))
#     return positions, current_time  # Retourner les positions et le temps courant mis à jour

# # Fonction principale pour écrire les positions des véhicules pendant leur trajet
# def ecrire_positions_vehicules(fichier_events, fichier_network, fichier_sortie_csv):
#     coordonnees_noeuds, liens = lire_reseau(fichier_network)
#     positions_par_vehicule = defaultdict(list)
#     motif_orig = None
#     motif_dest = None
#     enter_time = None
#     leave_time = None
#     coord_start = None
#     coord_end = None
#     offset_time = None  # Stocker le temps de début du trajet
#     en_deplacement = False  # Indicateur si l'agent est en déplacement

#     tree = ET.parse(fichier_events)
#     root = tree.getroot()

#     with open(fichier_sortie_csv, 'a') as f_out:
#         for event in root.findall('event'):
#             event_type = event.get('type')
#             vehicle_id = event.get('vehicle')

#             # Capturer 'actend' pour définir le début d'un trajet
#             if event_type == 'actend' and event.get('facility') is not None:
#                 motif_orig = event.get('actType')
#                 offset_time = float(event.get('time')) // 60  # Le temps de départ du trajet (en minutes)
#                 en_deplacement = True  # L'agent commence un nouveau trajet

#             # Capturer 'actstart' pour définir la fin d'un trajet
#             elif event_type == 'actstart' and event.get('facility') is not None:
#                 motif_dest = event.get('actType')

#                 if motif_orig and motif_dest and en_deplacement:
#                     # Écrire toutes les positions accumulées du trajet entre les deux activités
#                     for vehicle, positions in positions_par_vehicule.items():
#                         for (event_time, x, y, link_id) in positions:
#                             f_out.write(f"{vehicle},{event_time},{link_id},{x},{y},{motif_orig},{motif_dest}\n")
#                     positions_par_vehicule.clear()  # Nettoyer les positions pour un nouveau trajet
#                     en_deplacement = False  # Le trajet est terminé

#             # Gérer les événements 'entered link' pendant le déplacement
#             if en_deplacement and event_type == 'entered link':
#                 link_id = event.get('link')
#                 enter_time = float(event.get('time'))

#                 if link_id in liens:
#                     from_node, to_node = liens[link_id]
#                     coord_start = coordonnees_noeuds.get(from_node)
#                     coord_end = coordonnees_noeuds.get(to_node)

#             # Gérer les événements 'left link' pour calculer les positions minute par minute
#             elif en_deplacement and event_type == 'left link':
#                 leave_time = float(event.get('time'))

#                 if enter_time and leave_time and coord_start and coord_end:
#                     # Interpoler les positions minute par minute pendant la durée du lien
#                     positions_interp, offset_time = interpoler_positions_par_minute(enter_time, leave_time, coord_start, coord_end, offset_time)

#                     # Ajouter les positions interpolées à la liste des positions
#                     for event_time, x, y in positions_interp:
#                         positions_par_vehicule[vehicle_id].append((event_time, x, y, link_id))

#                 # Réinitialiser pour le lien suivant
#                 enter_time = None
#                 leave_time = None
#                 coord_start = None
#                 coord_end = None

#         # Écrire les positions restantes à la fin de l'itération
#         if motif_orig and motif_dest and en_deplacement:
#             for vehicle, positions in positions_par_vehicule.items():
#                 for (event_time, x, y, link_id) in positions:
#                     f_out.write(f"{vehicle},{event_time},{link_id},{x},{y},{motif_orig},{motif_dest}\n")


# def calculer_position(enterTime, leaveTime, coordStart, coordEnd, event_time):
#     # Calcul de la position à un moment précis basé sur l'interpolation
#     ratio = (event_time - enterTime) / (leaveTime - enterTime)
#     x = coordStart[0] + ratio * (coordEnd[0] - coordStart[0])
#     y = coordStart[1] + ratio * (coordEnd[1] - coordStart[1])
#     return x, y

# def ecrire_positions_vehicules(fichier_events, fichier_network, fichier_sortie_csv):
#     coordonnees_noeuds, liens = lire_reseau(fichier_network)
#     positions_par_vehicule = defaultdict(list)
#     motif_orig = None
#     motif_dest = None
#     enter_time = None
#     leave_time = None
#     coord_start = None
#     coord_end = None
#     en_deplacement = False  # Variable pour suivre si l'agent est en déplacement

#     tree = ET.parse(fichier_events)
#     root = tree.getroot()

#     with open(fichier_sortie_csv, 'a') as f_out:
#         for event in root.findall('event'):
#             event_type = event.get('type')
#             vehicle_id = event.get('vehicle')

#             # Capturer 'actend' pour définir le motif d'origine
#             if event_type == 'actend' and event.get('facility') is not None:
#                 motif_orig = event.get('actType')
#                 en_deplacement = True  # Le déplacement commence

#             # Capturer 'actstart' pour définir le motif de destination
#             elif event_type == 'actstart' and event.get('facility') is not None:
#                 motif_dest = event.get('actType')

#                 if motif_orig and motif_dest and en_deplacement:
#                     # Ecrire toutes les positions du trajet entre les deux activités
#                     for vehicle, positions in positions_par_vehicule.items():
#                         for (event_time, x, y, link_id) in positions:
#                             f_out.write(f"{vehicle},{event_time},{link_id},{x},{y},{motif_orig},{motif_dest}\n")
#                     positions_par_vehicule.clear()  # Nettoyer les positions pour un nouveau trajet
#                     en_deplacement = False  # Le déplacement est terminé

#             # Gérer les événements 'entered link' lorsque l'agent est en déplacement
#             if en_deplacement and event_type == 'entered link':
#                 link_id = event.get('link')
#                 enter_time = float(event.get('time'))

#                 if link_id in liens:
#                     from_node, to_node = liens[link_id]
#                     coord_start = coordonnees_noeuds.get(from_node)
#                     coord_end = coordonnees_noeuds.get(to_node)

#             # Gérer les événements 'left link' pour calculer la position seulement au moment de leave_time
#             elif en_deplacement and event_type == 'left link':
#                 leave_time = float(event.get('time'))

#                 if enter_time and leave_time and coord_start and coord_end:
#                     # Calculer les positions à enter_time et leave_time uniquement
#                     x_start, y_start = calculer_position(enter_time, leave_time, coord_start, coord_end, enter_time)
#                     x_end, y_end = calculer_position(enter_time, leave_time, coord_start, coord_end, leave_time)

#                     # Ajouter les positions du début et de la fin du lien dans la liste des positions
#                     positions_par_vehicule[vehicle_id].append((enter_time // 60, x_start, y_start, link_id))
#                     positions_par_vehicule[vehicle_id].append((leave_time // 60, x_end, y_end, link_id))

#                 # Réinitialiser pour le lien suivant
#                 enter_time = None
#                 leave_time = None
#                 coord_start = None
#                 coord_end = None

#         # Écrire les positions restantes à la fin de l'itération
#         if motif_orig and motif_dest and en_deplacement:
#             for vehicle, positions in positions_par_vehicule.items():
#                 for (event_time, x, y, link_id) in positions:
#                     f_out.write(f"{vehicle},{event_time},{link_id},{x},{y},{motif_orig},{motif_dest}\n")

# Chemins vers les fichiers
# fichier_events = "C:/Users/User/IdeaProjects/matsim-example-project-modified/output_detaillees_car.xml"
# fichier_network = "C:/Users/User/IdeaProjects/matsim-example-project-modified/simulation_output_toulouse/output_network.xml.gz"
# fichier_sortie_csv = "agent_positions_motif_test2.csv"

# # Initialiser le fichier CSV de sortie avec des en-têtes
# with open(fichier_sortie_csv, 'w') as f_out:
#     f_out.write("AgentId,Temps_minute,link,x,y,Motif_Orig,Motif_Dest\n")

# # Exécuter la fonction pour extraire et écrire les positions des agents
# ecrire_positions_vehicules(fichier_events, fichier_network, fichier_sortie_csv)



# import xml.etree.ElementTree as ET
# import gzip
# from collections import defaultdict

# def lire_reseau(fichier_network):
#     coordonnees_noeuds = {}  # dict ou chaque cle : un id de noeud, la valeur : un tuple des coordonnees (x, y)
#     liens = {}               # dict ou chaque cle : un id de lien, la valeur : un tuple des noeuds de depart et d'arrivee de ce lien

#     with gzip.open(fichier_network, 'rt', encoding='utf-8') as f:
#         tree = ET.parse(f)
#         root = tree.getroot()

#         # recuperer les noeuds et leurs coordonnees
#         for node in root.findall('.//node'):
#             node_id = node.get('id')
#             x = float(node.get('x'))
#             y = float(node.get('y'))
#             coordonnees_noeuds[node_id] = (x, y)

#         # recuperer les liens et leurs noeuds de depart et d'arrivee
#         for link in root.findall('.//link'):
#             link_id = link.get('id')
#             from_node = link.get('from')
#             to_node = link.get('to')
#             liens[link_id] = (from_node, to_node)

#     return coordonnees_noeuds, liens

# def interpoler_positions_par_minute(enterTime, leaveTime, coordStart, coordEnd):
#     """Interpole les positions entre enterTime et leaveTime pour chaque minute."""
#     interpolated_positions = []
#     duration = leaveTime - enterTime
#     if duration > 0:
#         for t in range(int(enterTime // 60) * 60, int(leaveTime), 60):  # Interpoler chaque minute
#             ratio = (t - enterTime) / duration
#             x = coordStart[0] + ratio * (coordEnd[0] - coordStart[0])
#             y = coordStart[1] + ratio * (coordEnd[1] - coordStart[1])
#             interpolated_positions.append((t // 60, x, y))  # Stocker le temps en minutes
#     return interpolated_positions

# def ecrire_positions_vehicules(fichier_events, fichier_network, fichier_sortie_csv):
#     coordonnees_noeuds, liens = lire_reseau(fichier_network)
#     positions_par_vehicule = defaultdict(list)
#     motif_orig = None
#     motif_dest = None
#     enter_time = None
#     leave_time = None
#     coord_start = None
#     coord_end = None
#     en_deplacement = False

#     tree = ET.parse(fichier_events)
#     root = tree.getroot()

#     with open(fichier_sortie_csv, 'a') as f_out:
#         for event in root.findall('event'):
#             event_type = event.get('type')
#             vehicle_id = event.get('vehicle')

#             # Capturer 'actend' pour démarrer un nouveau trajet
#             if event_type == 'actend' and event.get('facility') is not None:
#                 motif_orig = event.get('actType')
#                 en_deplacement = True

#             # Capturer 'actstart' pour terminer le trajet et écrire les positions
#             elif event_type == 'actstart' and event.get('facility') is not None:
#                 motif_dest = event.get('actType')

#                 if motif_orig and motif_dest and en_deplacement:
#                     for vehicle, positions in positions_par_vehicule.items():
#                         for (time_minute, x, y, link_id) in positions:
#                             f_out.write(f"{vehicle},{time_minute},{link_id},{x},{y},{motif_orig},{motif_dest}\n")
#                     positions_par_vehicule.clear()
#                     en_deplacement = False

#             # Gérer les événements 'entered link' pour récupérer les coordonnées de départ
#             if en_deplacement and event_type == 'entered link':
#                 link_id = event.get('link')
#                 enter_time = float(event.get('time'))

#                 if link_id in liens:
#                     from_node, to_node = liens[link_id]
#                     coord_start = coordonnees_noeuds.get(from_node)
#                     coord_end = coordonnees_noeuds.get(to_node)

#             # Gérer les événements 'left link' pour récupérer les coordonnées d'arrivée
#             elif en_deplacement and event_type == 'left link':
#                 leave_time = float(event.get('time'))

#                 if enter_time and leave_time and coord_start and coord_end:
#                     # Interpoler les positions pour chaque minute pendant le déplacement sur ce lien
#                     interpolated_positions = interpoler_positions_par_minute(enter_time, leave_time, coord_start, coord_end)

#                     # Ajouter les positions à la liste des positions pour ce véhicule
#                     for time_minute, x, y in interpolated_positions:
#                         positions_par_vehicule[vehicle_id].append((time_minute, x, y, link_id))

#                 # Réinitialiser pour le lien suivant
#                 enter_time = None
#                 leave_time = None
#                 coord_start = None
#                 coord_end = None

#         # Écrire les positions restantes à la fin
#         if motif_orig and motif_dest and en_deplacement:
#             for vehicle, positions in positions_par_vehicule.items():
#                 for (time_minute, x, y, link_id) in positions:
#                     f_out.write(f"{vehicle},{time_minute},{link_id},{x},{y},{motif_orig},{motif_dest}\n")

# # Chemins vers les fichiers
# fichier_events = "C:/Users/User/IdeaProjects/matsim-example-project-modified/output_detaillees_car.xml"
# fichier_network = "C:/Users/User/IdeaProjects/matsim-example-project-modified/simulation_output_toulouse/output_network.xml.gz"
# fichier_sortie_csv = "agent_positions_motif_test2.csv"

# # Initialiser le fichier CSV de sortie avec des en-têtes
# with open(fichier_sortie_csv, 'w') as f_out:
#     f_out.write("AgentId,Temps_minute,link,x,y,Motif_Orig,Motif_Dest\n")

# # Exécuter la fonction pour extraire et écrire les positions des agents
# ecrire_positions_vehicules(fichier_events, fichier_network, fichier_sortie_csv)

# import pandas as pd
# from collections import defaultdict

# # Load the CSV file
# df = pd.read_csv('agent_positions_motif_filtre_g.csv')

# # Convert 'Temps_minute' to hours (assuming it is in minutes)
# df['Temps_hour'] = df['Temps_minute'] // 60

# # Create a dictionary to count trips per hour
# trips_per_hour = defaultdict(int)

# # For each unique AgentId, count the number of trips in each hour
# agents = df['AgentId'].unique()

# for agent in agents:
#     agent_df = df[df['AgentId'] == agent]
#     # Identify when a trip starts (Motif_Orig changes) and count trips per hour
#     current_hour = None
#     previous_motif = None
#     for index, row in agent_df.iterrows():
#         hour = row['Temps_hour']
#         motif_orig = row['Motif_Orig']
        
#         if hour != current_hour or motif_orig != previous_motif:
#             trips_per_hour[hour] += 1
#             current_hour = hour
#             previous_motif = motif_orig

# # Convert the results to a DataFrame for easy visualization
# trips_per_hour_df = pd.DataFrame(list(trips_per_hour.items()), columns=['Hour', 'Number_of_Trips'])

# # Sort by the hour to ensure the display is in order
# trips_per_hour_df = trips_per_hour_df.sort_values(by='Hour').reset_index(drop=True)

# # Save the result to a CSV file
# trips_per_hour_df.to_csv('trips_per_hour_sorted.csv', index=False)

# # Display the result in sorted order
# print(trips_per_hour_df)

# import pandas as pd
# import plotly.express as px

# # Define the output path for saving CSVs (adjust as needed)
# output_path = "C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\"

# # Load the CSV file
# df = pd.read_csv('agent_positions_motif_filtre_g_5000_clean.csv')

# # Convert 'Temps_minute' to hours (assuming it is in minutes)
# df['Temps_hour'] = df['Temps_minute'] // 60

# # Create dictionaries to count distinct agents per hour and motif
# trips_by_motif_per_hour = {}

# # Loop over each row and count distinct trips by agents per hour and motif
# for _, row in df.iterrows():
#     agent_id = row['AgentId']
#     hour = row['Temps_hour']
#     motif_orig = row['Motif_Orig']
#     motif_dest = row['Motif_Dest']
    
#     trip_type = (motif_orig, motif_dest)
    
#     # Initialize the dictionary for this hour if it doesn't exist
#     if hour not in trips_by_motif_per_hour:
#         trips_by_motif_per_hour[hour] = {}
    
#     # Initialize the set for this motif type if it doesn't exist
#     if trip_type not in trips_by_motif_per_hour[hour]:
#         trips_by_motif_per_hour[hour][trip_type] = set()
    
#     # Add the agent to the set for this motif type in this hour
#     trips_by_motif_per_hour[hour][trip_type].add(agent_id)

# # Convert trips by motif per hour to a DataFrame
# motif_data = []
# for hour, motifs in trips_by_motif_per_hour.items():
#     for (motif_orig, motif_dest), agents in motifs.items():
#         motif_data.append([hour, motif_orig, motif_dest, len(agents)])  # Use len(agents) to count distinct agents

# motif_df = pd.DataFrame(motif_data, columns=['Heure', 'Motif_Orig', 'Motif_Dest', 'Nombre_Trajet']).sort_values(by='Heure')

# # Calculate the total number of trips per hour without distinguishing motifs
# trips_per_hour_df = motif_df.groupby('Heure')['Nombre_Trajet'].sum().reset_index()

# # Rename columns appropriately
# trips_per_hour_df.columns = ['Heure', 'Nombre_Trajet']

# # Save the results to CSV files
# motif_df.to_csv(output_path + 'repartition_trajet_par_heure_avec_motif.csv', index=False)
# trips_per_hour_df.to_csv(output_path + 'nombre_trajets_par_heure_sans_motif.csv', index=False)

# # Pivot the data for interactive plotting
# pivot_df = motif_df.pivot(index='Heure', columns=['Motif_Orig', 'Motif_Dest'], values='Nombre_Trajet').fillna(0)

# # Flatten the MultiIndex columns for Plotly compatibility
# pivot_df.columns = [f"{orig} -> {dest}" for orig, dest in pivot_df.columns]

# # Reset index for Plotly
# pivot_df.reset_index(inplace=True)

# # Plotting the interactive stacked bar chart with Plotly
# fig = px.bar(
#     pivot_df, 
#     x='Heure', 
#     y=pivot_df.columns[1:],  # exclude 'Heure' from the y-axis
#     title="Number of Trips by Hour, Origin, and Destination (Distinct Colors for Each Trip)",
#     labels={"value": "Number of Trips", "variable": "Motif (Orig -> Dest)"},
# )

# # Customize layout for clarity
# fig.update_layout(barmode='stack', xaxis_title="Hour", yaxis_title="Number of Trips")

# # Show interactive plot
# fig.show()

# import pandas as pd
# import matplotlib.pyplot as plt

# # Load the traffic evolution data
# traffic_df = pd.read_csv("C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\csv_clean\\nombre_trajets_par_heure_sans_motif.csv")
# traffic_df.columns = ['Heure', 'Nombre_Agents']

# # Load the repartition data
# motif_df = pd.read_csv("C:\\Users\\User\\IdeaProjects\\matsim-example-project-modified\\csv_clean\\repartition_trajet_par_heure_avec_motif.csv")

# # Ensure 'Heure' is in hours for both dataframes
# motif_df['Heure'] = motif_df['Heure']
# traffic_df['Heure'] = traffic_df['Heure']

# # Calculate the total number of agents per hour across motifs
# total_agents_per_hour = motif_df.groupby('Heure')['Nombre_Trajet'].sum().reset_index()
# total_agents_per_hour.columns = ['Heure', 'Total_Motif_Agents']

# # Merge the traffic data (total active agents) with the motif data (agents per motif)
# merged_df = pd.merge(motif_df, traffic_df, on='Heure')

# # Scale motif counts so that their sum matches the total active agents per hour
# merged_df['Normalized_Trajet'] = merged_df.apply(
#     lambda row: row['Nombre_Trajet'] * row['Nombre_Agents'] / total_agents_per_hour.loc[total_agents_per_hour['Heure'] == row['Heure'], 'Total_Motif_Agents'].values[0],
#     axis=1
# )

# # Pivot the data for stacked bar plotting
# pivot_df = merged_df.pivot(index='Heure', columns=['Motif_Orig', 'Motif_Dest'], values='Normalized_Trajet').fillna(0)

# # Flatten the MultiIndex columns for Plotly compatibility
# pivot_df.columns = [f"{orig} -> {dest}" for orig, dest in pivot_df.columns]

# # Plotting the repartition stacked bar chart with normalized values
# fig, ax = plt.subplots(figsize=(12, 6))
# pivot_df.plot(kind='bar', stacked=True, ax=ax, colormap='tab20')

# # Customize plot
# ax.set_title("Repartition of Trips by Hour with Total Active Agents")
# ax.set_xlabel("Hour")
# ax.set_ylabel("Number of Trips (Total Active Agents per Hour)")
# ax.legend(title="Motif (Orig -> Dest)", bbox_to_anchor=(1.05, 1), loc='upper left')

# plt.tight_layout()
# plt.show()

# # Plot the evolution traffic chart for comparison
# plt.figure(figsize=(10, 6))
# plt.plot(traffic_df['Heure'], traffic_df['Nombre_Agents'], color='blue', linewidth=1)
# plt.title("Évolution du Trafic au Cours de la Simulation")
# plt.xlabel("Temps (minutes)")
# plt.ylabel("Nombre d'Agents Actifs")
# plt.grid(True)
# plt.tight_layout()
# plt.show()

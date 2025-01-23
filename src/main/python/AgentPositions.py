# Pour extraite des position des agents(par minute) sans la colonne motif - ca marche

# import xml.etree.ElementTree as ET
# import gzip
# from collections import defaultdict

# # Fonction pour lire le fichier réseau et récupérer les coordonnées des nœuds et les liens
# def lire_reseau(fichier_network):
#     coordonnees_noeuds = {}
#     liens = {}
    
#     with gzip.open(fichier_network, 'rt', encoding='utf-8') as f:
#         tree = ET.parse(f)
#         root = tree.getroot()
        
#         # Récupérer les nœuds et leurs coordonnées
#         for node in root.findall('.//node'):
#             node_id = node.get('id')
#             x = float(node.get('x'))
#             y = float(node.get('y'))
#             coordonnees_noeuds[node_id] = (x, y)
        
#         # Récupérer les liens et leurs nœuds de départ et d'arrivée
#         for link in root.findall('.//link'):
#             link_id = link.get('id')
#             from_node = link.get('from')
#             to_node = link.get('to')
#             liens[link_id] = (from_node, to_node)
    
#     return coordonnees_noeuds, liens

# # Fonction pour lire les événements de véhicule et écrire les positions des agents dans un fichier CSV
# def ecrire_positions_vehicules(fichier_events, fichier_network, fichier_sortie_csv):
#     # Lire le réseau pour récupérer les coordonnées des nœuds et les liens
#     coordonnees_noeuds, liens = lire_reseau(fichier_network)
    
#     # Dictionnaire pour stocker les positions des agents à chaque minute
#     positions_par_vehicule = defaultdict(list)
#     dernier_temps_par_vehicule = defaultdict(lambda: -60)  # Dernier temps enregistré pour chaque véhicule (initialisé à -60 pour la première minute)

#     # Ouvrir output_detaillees_car.xml (fichier non gzippé)
#     tree = ET.parse(fichier_events)
#     root = tree.getroot()

#     # Itérer sur tous les éléments "event"
#     for event in root.findall('event'):
#         event_type = event.get('type')
#         vehicle_id = event.get('vehicle')

#         # Se concentrer uniquement sur les événements "entered link" et "left link"
#         if event_type in ['entered link', 'left link']:
#             link_id = event.get('link')
#             time = float(event.get('time'))

#             # Vérifier si ce lien existe dans le réseau
#             if link_id not in liens:
#                 continue  # Si le lien n'existe pas, passer au prochain événement

#             # Récupérer le nœud de départ "from" du lien
#             from_node, _ = liens[link_id]

#             # Récupérer les coordonnées du nœud "from"
#             if from_node in coordonnees_noeuds:
#                 x, y = coordonnees_noeuds[from_node]
#             else:
#                 continue  # Si les coordonnées ne sont pas trouvées, passer au prochain événement

#             # Calculer la prochaine minute à enregistrer
#             if time - dernier_temps_par_vehicule[vehicle_id] >= 60:
#                 # Enregistrer la position pour le véhicule à cette minute
#                 positions_par_vehicule[vehicle_id].append((int(time // 60), x, y))
#                 dernier_temps_par_vehicule[vehicle_id] = time

#     # Écrire le fichier CSV avec les positions des véhicules
#     with open(fichier_sortie_csv, 'w') as f_out:
#         f_out.write("AgentId,Temps_minute,x,y\n")
#         for vehicle_id, positions in positions_par_vehicule.items():
#             # Trier les positions par temps
#             positions_triees = sorted(positions, key=lambda x: x[0])
#             for time_minute, x, y in positions_triees:
#                 f_out.write(f"{vehicle_id},{time_minute},{x},{y}\n")

# # Spécifier les fichiers d'entrée et de sortie
# fichier_events = "C:/Users/User/IdeaProjects/matsim-example-project-modified/output_detaillees_car.xml"
# fichier_network = "C:/Users/User/IdeaProjects/matsim-example-project-modified/simulation_output_toulouse/output_network.xml.gz"
# fichier_sortie_csv = "agent_positions.csv"

# # Appeler la fonction pour écrire les positions des véhicules dans le fichier CSV
# ecrire_positions_vehicules(fichier_events, fichier_network, fichier_sortie_csv)

# -----------------------------------------------------------------------------------------------------------
# Pour extraite des position des agents sans interpolation (par minute) avec Motif_Orig & Motif_Dest

# import xml.etree.ElementTree as ET
# import gzip
# from collections import defaultdict 

# # lire le fichier reseau et recuperer les coordonnees des noeuds et les liens
# def lire_reseau(fichier_network): 
#     coordonnees_noeuds = {}        # dict ou chaque cle : un id de noeud,  la valeur : un tuple des coordonnees (x, y)
#     liens = {}                     # dict ou chaque cle : un id de lien, la valeur : un tuple des noeuds de depart et d'arrivee de ce lien
    
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

# # lire les events vehicule et ecrire les positions des agents dans un fichier CSV avec motifs
# def ecrire_positions_vehicules(fichier_events, fichier_network, fichier_sortie_csv):
#     coordonnees_noeuds, liens = lire_reseau(fichier_network)
    
#     # dict pour stocker les positions des agents à chaque minute : vehicle_id, liste des positions du vehicule (temps,x,y)
#     positions_par_vehicule = defaultdict(list)
#     # dict qui stocke le dernier temps enregistre pour chaque vehicule (initialise à -60 pour 1er minute)
#     dernier_temps_par_vehicule = defaultdict(lambda: -60)  
    
#     motif_orig = None
#     motif_dest = None

#     # ouvrir output_detaillees_car.xml (fichier non gzippe)
#     tree = ET.parse(fichier_events)
#     root = tree.getroot()

#     # iterer sur tous les elements "event"
#     for event in root.findall('event'):
#         event_type = event.get('type')
#         vehicle_id = event.get('vehicle')

#         # gerer les events "actend" pour capturer le motif d'origine
#         if event_type == 'actend':
#             motif_orig = event.get('actType') 
#         # gerer les events "actstart" pour capturer le motif de destination
#         elif event_type == 'actstart':
#             motif_dest = event.get('actType')  

#             # lorsque l'on a à la fois le Motif_Orig et Motif_Dest, on peut ecrire les positions correspondantes
#             for vehicle, positions in positions_par_vehicule.items():
#                 for (time_minute, x, y) in positions:
#                     with open(fichier_sortie_csv, 'a') as f_out:
#                         f_out.write(f"{vehicle},{time_minute},{x},{y},{motif_orig},{motif_dest}\n")
#             positions_par_vehicule.clear()  # on efface les positions pour un nouveau trajet

#         # se concentrer uniquement sur les events "entered link" et "left link"
#         if event_type in ['entered link', 'left link']:
#             link_id = event.get('link')
#             time = float(event.get('time'))

#             # verifier si ce lien existe dans le reseau
#             if link_id not in liens:
#                 continue  # si le lien n'existe pas, passer au prochain events

#             # recuperer le noeud de depart "from" du lien
#             from_node, _ = liens[link_id]

#             # recuperer les coordonnees du noeud "from"
#             if from_node in coordonnees_noeuds:
#                 x, y = coordonnees_noeuds[from_node]
#             else:
#                 continue  # si les coordonnees ne sont pas trouvees, passer au prochain events

#             # calculer la prochaine minute à enregistrer
#             # si une minute s'est scoulse depuis le dernier enregistrement pour ce vehicule, on stocke sa position à ce moment
#             if time - dernier_temps_par_vehicule[vehicle_id] >= 60:
#                 # accumuler la position pour le vehicule à cette minute
#                 positions_par_vehicule[vehicle_id].append((int(time // 60), x, y))
#                 dernier_temps_par_vehicule[vehicle_id] = time

#     # si des positions restent apres la derniere boucle, on les ecrit
#     if motif_orig and motif_dest:
#         for vehicle, positions in positions_par_vehicule.items():
#             for (time_minute, x, y) in positions:
#                 with open(fichier_sortie_csv, 'a') as f_out:
#                     f_out.write(f"{vehicle},{time_minute},{x},{y},{motif_orig},{motif_dest}\n")

# fichier_events = "C:/Users/User/IdeaProjects/matsim-example-project-modified/output_detaillees_car.xml"
# fichier_network = "C:/Users/User/IdeaProjects/matsim-example-project-modified/simulation_output_toulouse/output_network.xml.gz"
# fichier_sortie_csv = "agent_positions_motif.csv"

# with open(fichier_sortie_csv, 'w') as f_out:
#     f_out.write("AgentId,Temps_minute,x,y,Motif_Orig,Motif_Dest\n")

# ecrire_positions_vehicules(fichier_events, fichier_network, fichier_sortie_csv)

# -----------------------------------------------------------------------------------------------------------
# Pour extraite des position exactes avec interpolation des agents (par minute) avec Motif_Orig & Motif_Dest

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
# def interpoler_positions(enterTime, leaveTime, coordStart, coordEnd):
#     interpolated_positions = []
#     duration = leaveTime - enterTime

#     # interpolation à chaque minute entre enterTime et leaveTime
#     for t in range(int(enterTime), int(leaveTime) + 1, 60): 
#         ratio = (t - enterTime) / duration
#         x = coordStart[0] + ratio * (coordEnd[0] - coordStart[0])
#         y = coordStart[1] + ratio * (coordEnd[1] - coordStart[1])
#         interpolated_positions.append((t // 60, x, y))  
#     return interpolated_positions

# # lire les events de vehicule, ecrire les positions des agents dans un fichier CSV avec motifs et interpolation
# def ecrire_positions_vehicules(fichier_events, fichier_network, fichier_sortie_csv):
#     coordonnees_noeuds, liens = lire_reseau(fichier_network)
#     positions_par_vehicule = defaultdict(list)  # stocke les positions des vehicules apres interpolation. cle : vehicle_id, valeur : liste de positions interpole
#     # dernier_temps_par_vehicule = defaultdict(lambda: -60)  # dernier temps enregistre pour chaque vehicule
#     motif_orig = None
#     motif_dest = None
#     enter_time = None
#     leave_time = None
#     coord_start = None
#     coord_end = None

#     tree = ET.parse(fichier_events)
#     root = tree.getroot()

#     # iterer sur tous les events
#     for event in root.findall('event'):
#         event_type = event.get('type')
#         vehicle_id = event.get('vehicle')

#         # pour capturer le motif d'origine
#         if event_type == 'actend':
#             motif_orig = event.get('actType')

#         # pour capturer le motif de destination
#         elif event_type == 'actstart':
#             motif_dest = event.get('actType')

#             # lorsque l'on a à la fois Motif_Orig et Motif_Dest, on ecrire les positions correspondantes
#             if motif_orig and motif_dest:
#                 for vehicle, positions in positions_par_vehicule.items():
#                     for (time_minute, x, y, link_id) in positions:
#                         with open(fichier_sortie_csv, 'a') as f_out:
#                             f_out.write(f"{vehicle},{time_minute},{link_id},{x},{y},{motif_orig},{motif_dest}\n")
#                 # effacer les positions pour un nouveau trajet            
#                 positions_par_vehicule.clear()  

#         if event_type == 'entered link':
#             link_id = event.get('link')
#             enter_time = float(event.get('time'))

#             # recuper le noeud de depart "from" et d'arrivee "to" du lien
#             if link_id in liens:
#                 from_node, to_node = liens[link_id]
#                 coord_start = coordonnees_noeuds.get(from_node)
#                 coord_end = coordonnees_noeuds.get(to_node)

#         elif event_type == 'left link':
#             leave_time = float(event.get('time'))

#             # si toutes les donnees sont disponibles, effectuer l'interpolation
#             if enter_time and leave_time and coord_start and coord_end:
#                 interpolated_positions = interpoler_positions(enter_time, leave_time, coord_start, coord_end)

#                 # # accumuler les positions interpolees
#                 # positions_par_vehicule[vehicle_id].extend(interpolated_positions)

#                 # Accumuler les positions interpolées avec le link_id
#                 for time_minute, x, y in interpolated_positions:
#                     positions_par_vehicule[vehicle_id].append((time_minute, x, y, link_id))

#             # reinitialiser les valeurs pour le prochain lien
#             enter_time = None
#             leave_time = None
#             coord_start = None
#             coord_end = None

#     # si des positions restent apres la derniere boucle, on les ecrit
#     if motif_orig and motif_dest:
#         for vehicle, positions in positions_par_vehicule.items():
#             for (time_minute, x, y) in positions:
#                 with open(fichier_sortie_csv, 'a') as f_out:
#                     f_out.write(f"{vehicle},{time_minute},{link_id},{x},{y},{motif_orig},{motif_dest}\n")

# fichier_events = "C:/Users/User/IdeaProjects/matsim-example-project-modified/output_detaillees_car_5000.xml"
# fichier_network = "C:/Users/User/IdeaProjects/matsim-example-project-modified/simulation_output_toulouse/output_network.xml.gz"
# fichier_sortie_csv = "agent_positions_motif_5000_test.csv"

# with open(fichier_sortie_csv, 'w') as f_out:
#     f_out.write("AgentId,Temps_minute,link,x,y,Motif_Orig,Motif_Dest\n")

# ecrire_positions_vehicules(fichier_events, fichier_network, fichier_sortie_csv)

#-----------------------------------------------------------------------------------------------------------------------------------------------

# import xml.etree.ElementTree as ET
# import gzip
# from collections import defaultdict

# # lire le fichier réseau et récupérer les coordonnées des nœuds et les liens
# def lire_reseau(fichier_network):
#     coordonnees_noeuds = {}  # dict où chaque clé : un id de nœud, la valeur : un tuple des coordonnées (x, y)
#     liens = {}               # dict où chaque clé : un id de lien, la valeur : un tuple des nœuds de départ et d'arrivée de ce lien

#     with gzip.open(fichier_network, 'rt', encoding='utf-8') as f:
#         tree = ET.parse(f)
#         root = tree.getroot()

#         # récupérer les nœuds et leurs coordonnées
#         for node in root.findall('.//node'):
#             node_id = node.get('id')
#             x = float(node.get('x'))
#             y = float(node.get('y'))
#             coordonnees_noeuds[node_id] = (x, y)

#         # récupérer les liens et leurs nœuds de départ et d'arrivée
#         for link in root.findall('.//link'):
#             link_id = link.get('id')
#             from_node = link.get('from')
#             to_node = link.get('to')
#             liens[link_id] = (from_node, to_node)

#     return coordonnees_noeuds, liens

# # interpolation des positions entre le temps d'entrée et le temps de sortie
# def interpoler_positions(enterTime, leaveTime, coordStart, coordEnd):
#     interpolated_positions = []
#     duration = leaveTime - enterTime

#     # interpolation à chaque minute entre enterTime et leaveTime
#     for t in range(int(enterTime), int(leaveTime) + 1, 60): 
#         ratio = (t - enterTime) / duration
#         x = coordStart[0] + ratio * (coordEnd[0] - coordStart[0])
#         y = coordStart[1] + ratio * (coordEnd[1] - coordStart[1])
#         interpolated_positions.append((t // 60, x, y))  
#     return interpolated_positions

# # lire les events de véhicule, écrire les positions des agents dans un fichier CSV avec motifs et interpolation
# def ecrire_positions_vehicules(fichier_events, fichier_network, fichier_sortie_csv, nettoyage_doublons=0):
#     coordonnees_noeuds, liens = lire_reseau(fichier_network)
#     positions_par_vehicule = defaultdict(list)  # stocke les positions des véhicules après interpolation. clé : vehicle_id, valeur : liste de positions interpolées
#     motif_orig = None
#     motif_dest = None
#     enter_time = None
#     leave_time = None
#     coord_start = None
#     coord_end = None

#     tree = ET.parse(fichier_events)
#     root = tree.getroot()

#     # itérer sur tous les events
#     for event in root.findall('event'):
#         event_type = event.get('type')
#         vehicle_id = event.get('vehicle')

#         # pour capturer le motif d'origine
#         if event_type == 'actend':
#             motif_orig = event.get('actType')

#         # pour capturer le motif de destination
#         elif event_type == 'actstart':
#             motif_dest = event.get('actType')

#             # lorsque l'on a à la fois Motif_Orig et Motif_Dest, on écrit les positions correspondantes
#             if motif_orig and motif_dest:
#                 for vehicle, positions in positions_par_vehicule.items():
#                     # Appliquer le filtrage des doublons si nettoyage_doublons est activé
#                     if nettoyage_doublons:
#                         # Utiliser un dictionnaire pour conserver la première occurrence de chaque Temps_minute
#                         unique_positions = {}
#                         for (time_minute, x, y, link_id) in positions:
#                             if time_minute not in unique_positions:
#                                 unique_positions[time_minute] = (x, y, link_id)
#                         # Conversion en liste pour l'écriture dans le fichier
#                         positions_to_write = [(time_minute, *unique_positions[time_minute]) for time_minute in sorted(unique_positions)]
#                     else:
#                         positions_to_write = positions

#                     for (time_minute, x, y, link_id) in positions_to_write:
#                         with open(fichier_sortie_csv, 'a') as f_out:
#                             f_out.write(f"{vehicle},{time_minute},{link_id},{x},{y},{motif_orig},{motif_dest}\n")
#                 # effacer les positions pour un nouveau trajet            
#                 positions_par_vehicule.clear()  

#         if event_type == 'entered link':
#             link_id = event.get('link')
#             enter_time = float(event.get('time'))

#             # récupérer le nœud de départ "from" et d'arrivée "to" du lien
#             if link_id in liens:
#                 from_node, to_node = liens[link_id]
#                 coord_start = coordonnees_noeuds.get(from_node)
#                 coord_end = coordonnees_noeuds.get(to_node)

#         elif event_type == 'left link':
#             leave_time = float(event.get('time'))

#             # si toutes les données sont disponibles, effectuer l'interpolation
#             if enter_time and leave_time and coord_start and coord_end:
#                 interpolated_positions = interpoler_positions(enter_time, leave_time, coord_start, coord_end)

#                 # Accumuler les positions interpolées avec le link_id
#                 for time_minute, x, y in interpolated_positions:
#                     positions_par_vehicule[vehicle_id].append((time_minute, x, y, link_id))

#             # réinitialiser les valeurs pour le prochain lien
#             enter_time = None
#             leave_time = None
#             coord_start = None
#             coord_end = None

#     # si des positions restent après la dernière boucle, on les écrit
#     if motif_orig and motif_dest:
#         for vehicle, positions in positions_par_vehicule.items():
#             if nettoyage_doublons:
#                 unique_positions = {}
#                 for (time_minute, x, y, link_id) in positions:
#                     if time_minute not in unique_positions:
#                         unique_positions[time_minute] = (x, y, link_id)
#                 positions_to_write = [(time_minute, *unique_positions[time_minute]) for time_minute in sorted(unique_positions)]
#             else:
#                 positions_to_write = positions

#             for (time_minute, x, y, link_id) in positions_to_write:
#                 with open(fichier_sortie_csv, 'a') as f_out:
#                     f_out.write(f"{vehicle},{time_minute},{link_id},{x},{y},{motif_orig},{motif_dest}\n")

# fichier_events = "C:/Users/User/IdeaProjects/matsim-example-project-modified/output_detaillees_car_5000.xml"
# fichier_network = "C:/Users/User/IdeaProjects/matsim-example-project-modified/simulation_output_toulouse/output_network.xml.gz"
# fichier_sortie_csv = "agent_positions_motif_5000_test.csv"

# with open(fichier_sortie_csv, 'w') as f_out:
#     f_out.write("AgentId,Temps_minute,link,x,y,Motif_Orig,Motif_Dest\n")

# # Appel de la fonction avec nettoyage_doublons activé (1 pour activer, 0 pour désactiver)
# ecrire_positions_vehicules(fichier_events, fichier_network, fichier_sortie_csv, nettoyage_doublons=1)

#--------------------------------------------------------------------------------------------------------------------

# import xml.etree.ElementTree as ET
# import gzip
# from collections import defaultdict
# import pandas as pd

# # lire le fichier réseau et récupérer les coordonnées des nœuds et les liens
# def lire_reseau(fichier_network):
#     coordonnees_noeuds = {}  
#     liens = {}               

#     with gzip.open(fichier_network, 'rt', encoding='utf-8') as f:
#         tree = ET.parse(f)
#         root = tree.getroot()

#         for node in root.findall('.//node'):
#             node_id = node.get('id')
#             x = float(node.get('x'))
#             y = float(node.get('y'))
#             coordonnees_noeuds[node_id] = (x, y)

#         for link in root.findall('.//link'):
#             link_id = link.get('id')
#             from_node = link.get('from')
#             to_node = link.get('to')
#             liens[link_id] = (from_node, to_node)

#     return coordonnees_noeuds, liens

# def interpoler_positions(enterTime, leaveTime, coordStart, coordEnd):
#     interpolated_positions = []
#     duration = leaveTime - enterTime

#     for t in range(int(enterTime), int(leaveTime) + 1, 60): 
#         ratio = (t - enterTime) / duration
#         x = coordStart[0] + ratio * (coordEnd[0] - coordStart[0])
#         y = coordStart[1] + ratio * (coordEnd[1] - coordStart[1])
#         interpolated_positions.append((t // 60, x, y))  
#     return interpolated_positions

# # fonction pour écrire les positions de véhicule avec motifs et interpolation
# def ecrire_positions_vehicules(fichier_events, fichier_network, fichier_sortie_csv, nettoyage_doublons=0):
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

#     for event in root.findall('event'):
#         event_type = event.get('type')
#         vehicle_id = event.get('vehicle')

#         if event_type == 'actend':
#             motif_orig = event.get('actType')

#         elif event_type == 'actstart':
#             motif_dest = event.get('actType')

#             if motif_orig and motif_dest:
#                 for vehicle, positions in positions_par_vehicule.items():
#                     if nettoyage_doublons:
#                         unique_positions = {}
#                         for (time_minute, x, y, link_id) in positions:
#                             if time_minute not in unique_positions:
#                                 unique_positions[time_minute] = (x, y, link_id)
#                         positions_to_write = [(time_minute, *unique_positions[time_minute]) for time_minute in sorted(unique_positions)]
#                     else:
#                         positions_to_write = positions

#                     for (time_minute, x, y, link_id) in positions_to_write:
#                         with open(fichier_sortie_csv, 'a') as f_out:
#                             f_out.write(f"{vehicle},{time_minute},{link_id},{x},{y},{motif_orig},{motif_dest}\n")
#                 positions_par_vehicule.clear()

#         if event_type == 'entered link':
#             link_id = event.get('link')
#             enter_time = float(event.get('time'))

#             if link_id in liens:
#                 from_node, to_node = liens[link_id]
#                 coord_start = coordonnees_noeuds.get(from_node)
#                 coord_end = coordonnees_noeuds.get(to_node)

#         elif event_type == 'left link':
#             leave_time = float(event.get('time'))

#             if enter_time and leave_time and coord_start and coord_end:
#                 interpolated_positions = interpoler_positions(enter_time, leave_time, coord_start, coord_end)

#                 for time_minute, x, y in interpolated_positions:
#                     positions_par_vehicule[vehicle_id].append((time_minute, x, y, link_id))

#             enter_time = None
#             leave_time = None
#             coord_start = None
#             coord_end = None

#     if motif_orig and motif_dest:
#         for vehicle, positions in positions_par_vehicule.items():
#             if nettoyage_doublons:
#                 unique_positions = {}
#                 for (time_minute, x, y, link_id) in positions:
#                     if time_minute not in unique_positions:
#                         unique_positions[time_minute] = (x, y, link_id)
#                 positions_to_write = [(time_minute, *unique_positions[time_minute]) for time_minute in sorted(unique_positions)]
#             else:
#                 positions_to_write = positions

#             for (time_minute, x, y, link_id) in positions_to_write:
#                 with open(fichier_sortie_csv, 'a') as f_out:
#                     f_out.write(f"{vehicle},{time_minute},{link_id},{x},{y},{motif_orig},{motif_dest}\n")

# def filtrer_liaisons_consecutives(fichier_csv, fichier_sortie):
#     df = pd.read_csv(fichier_csv)
#     df = df.sort_values(by=['AgentId', 'Temps_minute'])

#     # Detect changes in 'link' or 'AgentId' to identify sequences of consecutive identical links
#     df['link_change'] = (df['link'] != df['link'].shift()) | (df['AgentId'] != df['AgentId'].shift())
#     df['sequence_id'] = df['link_change'].cumsum()

#     # Filter sequences that have more than 15 identical links by keeping only the first and last entry
#     filtered_rows = []
#     for _, group in df.groupby(['AgentId', 'sequence_id']):
#         if len(group) > 25:
#             filtered_rows.append(group.iloc[0].to_dict())  # First occurrence as a dictionary
#             filtered_rows.append(group.iloc[-1].to_dict())  # Last occurrence as a dictionary
#         else:
#             filtered_rows.extend(group.to_dict('records'))  # Keep all if <= 25

#     # Create a DataFrame from the filtered rows and save to CSV
#     filtered_df = pd.DataFrame(filtered_rows)
#     filtered_df = filtered_df.drop(columns=['link_change', 'sequence_id'])
#     filtered_df.to_csv(fichier_sortie, index=False)

# # Example usage
# fichier_events = "C:/Users/User/IdeaProjects/matsim-example-project-modified/output_detaillees_car_5000.xml"
# fichier_network = "C:/Users/User/IdeaProjects/matsim-example-project-modified/simulation_output_toulouse/output_network.xml.gz"
# fichier_sortie_csv = "agent_positions_motif_5000.csv"
# fichier_filtre_csv = "agent_positions_motif_filtre_5000.csv"

# with open(fichier_sortie_csv, 'w') as f_out:
#     f_out.write("AgentId,Temps_minute,link,x,y,Motif_Orig,Motif_Dest\n")

# ecrire_positions_vehicules(fichier_events, fichier_network, fichier_sortie_csv, nettoyage_doublons=0)

# # Apply the filtering function to remove consecutive links
# filtrer_liaisons_consecutives(fichier_sortie_csv, fichier_filtre_csv)

#----------------------------------------------------------------------------------------------------------------

# AgentPosition pour tout inclure le FiltrPositionCsv (ca marche)

import xml.etree.ElementTree as ET
import gzip
from collections import defaultdict
import pandas as pd


# lire le fichier réseau et récupérer les coordonnées des nœuds et les liens
def lire_reseau(fichier_network):
    coordonnees_noeuds = {}  
    liens = {}               

    with gzip.open(fichier_network, 'rt', encoding='utf-8') as f:
        tree = ET.parse(f)
        root = tree.getroot()

        for node in root.findall('.//node'):
            node_id = node.get('id')
            x = float(node.get('x'))
            y = float(node.get('y'))
            coordonnees_noeuds[node_id] = (x, y)

        for link in root.findall('.//link'):
            link_id = link.get('id')
            from_node = link.get('from')
            to_node = link.get('to')
            liens[link_id] = (from_node, to_node)

    return coordonnees_noeuds, liens

def interpoler_positions(enterTime, leaveTime, coordStart, coordEnd):
    interpolated_positions = []
    duration = leaveTime - enterTime

    if duration == 0:
        # Handle the case where enterTime equals leaveTime
        interpolated_positions.append((int(enterTime // 60), coordStart[0], coordStart[1]))
        return interpolated_positions

    for t in range(int(enterTime), int(leaveTime) + 1, 60): 
        ratio = (t - enterTime) / duration
        x = coordStart[0] + ratio * (coordEnd[0] - coordStart[0])
        y = coordStart[1] + ratio * (coordEnd[1] - coordStart[1])
        interpolated_positions.append((t // 60, x, y))  
    return interpolated_positions


# fonction pour écrire les positions de véhicule avec motifs et interpolation
def ecrire_positions_vehicules(fichier_events, fichier_network, fichier_sortie_csv, nettoyage_doublons):
    coordonnees_noeuds, liens = lire_reseau(fichier_network)
    positions_par_vehicule = defaultdict(list)  
    motif_orig = None
    motif_dest = None
    enter_time = None
    leave_time = None
    coord_start = None
    coord_end = None

    tree = ET.parse(fichier_events)
    root = tree.getroot()
 
    for event in root.findall('event'):
        event_type = event.get('type')
        vehicle_id = event.get('vehicle')

        if event_type == 'actend':
            motif_orig = event.get('actType')

        elif event_type == 'actstart':
            motif_dest = event.get('actType')

            if motif_orig and motif_dest:
                for vehicle, positions in positions_par_vehicule.items():
                    if nettoyage_doublons:
                        unique_positions = {}
                        for (time_minute, x, y, link_id) in positions:
                            if time_minute not in unique_positions:
                                unique_positions[time_minute] = (x, y, link_id)
                        positions_to_write = [(time_minute, *unique_positions[time_minute]) for time_minute in sorted(unique_positions)]
                    else:
                        positions_to_write = positions

                    for (time_minute, x, y, link_id) in positions_to_write:
                        with open(fichier_sortie_csv, 'a') as f_out:
                            f_out.write(f"{vehicle},{time_minute},{link_id},{x},{y},{motif_orig},{motif_dest}\n")
                positions_par_vehicule.clear()

        if event_type == 'entered link':
            link_id = event.get('link')
            enter_time = float(event.get('time'))

            if link_id in liens:
                from_node, to_node = liens[link_id]
                coord_start = coordonnees_noeuds.get(from_node)
                coord_end = coordonnees_noeuds.get(to_node)

        elif event_type == 'left link':
            leave_time = float(event.get('time'))

            if enter_time and leave_time and coord_start and coord_end:
                interpolated_positions = interpoler_positions(enter_time, leave_time, coord_start, coord_end)

                for time_minute, x, y in interpolated_positions:
                    positions_par_vehicule[vehicle_id].append((time_minute, x, y, link_id))

            enter_time = None
            leave_time = None
            coord_start = None
            coord_end = None

    if motif_orig and motif_dest:
        for vehicle, positions in positions_par_vehicule.items():
            if nettoyage_doublons:
                unique_positions = {}
                for (time_minute, x, y, link_id) in positions:
                    if time_minute not in unique_positions:
                        unique_positions[time_minute] = (x, y, link_id)
                positions_to_write = [(time_minute, *unique_positions[time_minute]) for time_minute in sorted(unique_positions)]
            else:
                positions_to_write = positions

            for (time_minute, x, y, link_id) in positions_to_write:
                with open(fichier_sortie_csv, 'a') as f_out:
                    f_out.write(f"{vehicle},{time_minute},{link_id},{x},{y},{motif_orig},{motif_dest}\n")

# Filter consecutive identical links based on sequence length and motif matching conditions
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
            # Check if the motif of the first and last occurrences in the sequence are different
            if group.iloc[0]['Motif_Orig'] != group.iloc[-1]['Motif_Orig']:
                # Keep only the first and last rows if motifs differ
                return pd.concat([group.iloc[[0]], group.iloc[[-1]]])
        return group  # Keep the entire group if sequence length is 15 or less or motifs match

    # Apply the filtering function to each sequence
    filtered_df = df.groupby(['AgentId', 'sequence_id']).apply(filter_sequence).reset_index(drop=True)
    
    # Drop temporary columns
    filtered_df = filtered_df.drop(columns=['link_change', 'sequence_id'])

    # Save the filtered file
    filtered_df.to_csv(fichier_sortie, index=False)

fichier_events = "C:/Users/User/IdeaProjects/matsim-example-project-modified/output_detaillees_car_monday.xml"
fichier_network = "C:/Users/User/IdeaProjects/matsim-example-project-modified/simulation_output_monday/output_network.xml.gz"
fichier_sortie_csv = "agent_positions_motif_clean_monday.csv"
fichier_filtre_csv = "agent_positions_motif_filtre_clean_monday.csv"

with open(fichier_sortie_csv, 'w') as f_out:
    f_out.write("AgentId,Temps_minute,link,x,y,Motif_Orig,Motif_Dest\n")

ecrire_positions_vehicules(fichier_events, fichier_network, fichier_sortie_csv, nettoyage_doublons=1)

filtrer_liaisons_consecutives(fichier_sortie_csv, fichier_filtre_csv)

#------------------------------------------------------------------------------------------------------------------------

# import xml.etree.ElementTree as ET
# import gzip
# from collections import defaultdict
# import pandas as pd


# # Read the network file and retrieve node coordinates and links
# def lire_reseau(fichier_network):
#     coordonnees_noeuds = {}
#     liens = {}

#     with gzip.open(fichier_network, 'rt', encoding='utf-8') as f:
#         tree = ET.parse(f)
#         root = tree.getroot()

#         for node in root.findall('.//node'):
#             node_id = node.get('id')
#             x = float(node.get('x'))
#             y = float(node.get('y'))
#             coordonnees_noeuds[node_id] = (x, y)

#         for link in root.findall('.//link'):
#             link_id = link.get('id')
#             from_node = link.get('from')
#             to_node = link.get('to')
#             liens[link_id] = (from_node, to_node)

#     return coordonnees_noeuds, liens


# # Interpolation function for positions between enter and leave times
# def interpoler_positions(enterTime, leaveTime, coordStart, coordEnd):
#     interpolated_positions = []
#     duration = leaveTime - enterTime

#     if duration == 0:
#         interpolated_positions.append((int(enterTime // 60), coordStart[0], coordStart[1]))
#         return interpolated_positions

#     for t in range(int(enterTime), int(leaveTime) + 1, 60):
#         ratio = (t - enterTime) / duration
#         x = coordStart[0] + ratio * (coordEnd[0] - coordStart[0])
#         y = coordStart[1] + ratio * (coordEnd[1] - coordStart[1])
#         interpolated_positions.append((t // 60, x, y))
#     return interpolated_positions


# # Write vehicle positions with motifs and interpolation
# def ecrire_positions_vehicules(fichier_events, fichier_network, fichier_sortie_csv, nettoyage_doublons):
#     coordonnees_noeuds, liens = lire_reseau(fichier_network)
#     positions_par_vehicule = defaultdict(list)
#     motif_orig = None
#     motif_dest = None
#     last_motif_dest = None
#     enter_time = None
#     leave_time = None
#     coord_start = None
#     coord_end = None

#     tree = ET.parse(fichier_events)
#     root = tree.getroot()

#     with open(fichier_sortie_csv, 'w') as f_out:
#         f_out.write("AgentId,Temps_minute,link,x,y,Motif_Orig,Motif_Dest\n")

#         for event in root.findall('event'):
#             event_type = event.get('type')
#             vehicle_id = event.get('vehicle')

#             if event_type == 'actend':
#                 motif_orig = event.get('actType')

#             elif event_type == 'actstart':
#                 motif_dest = event.get('actType')

#                 # Record all trips, including repeated motifs (e.g., work-work)
#                 if motif_orig and motif_dest:
#                     if last_motif_dest == motif_orig:
#                         # Handle intermediate trips for repeated motifs
#                         f_out.write(f"{vehicle_id},{enter_time // 60},{link_id},{coord_start[0]},{coord_start[1]},{motif_orig},{motif_orig}\n")

#                     # Record the current trip
#                     for vehicle, positions in positions_par_vehicule.items():
#                         if nettoyage_doublons:
#                             unique_positions = {}
#                             for (time_minute, x, y, link_id) in positions:
#                                 if time_minute not in unique_positions:
#                                     unique_positions[time_minute] = (x, y, link_id)
#                             positions_to_write = [(time_minute, *unique_positions[time_minute]) for time_minute in
#                                                   sorted(unique_positions)]
#                         else:
#                             positions_to_write = positions

#                         for (time_minute, x, y, link_id) in positions_to_write:
#                             f_out.write(f"{vehicle},{time_minute},{link_id},{x},{y},{motif_orig},{motif_dest}\n")
#                     positions_par_vehicule.clear()

#                 last_motif_dest = motif_dest

#             if event_type == 'entered link':
#                 link_id = event.get('link')
#                 enter_time = float(event.get('time'))

#                 if link_id in liens:
#                     from_node, to_node = liens[link_id]
#                     coord_start = coordonnees_noeuds.get(from_node)
#                     coord_end = coordonnees_noeuds.get(to_node)

#             elif event_type == 'left link':
#                 leave_time = float(event.get('time'))

#                 if enter_time and leave_time and coord_start and coord_end:
#                     interpolated_positions = interpoler_positions(enter_time, leave_time, coord_start, coord_end)

#                     for time_minute, x, y in interpolated_positions:
#                         positions_par_vehicule[vehicle_id].append((time_minute, x, y, link_id))

#                 enter_time = None
#                 leave_time = None
#                 coord_start = None
#                 coord_end = None


# # Filter consecutive identical links based on sequence length
# def filtrer_liaisons_consecutives(fichier_csv, fichier_sortie):
#     df = pd.read_csv(fichier_csv)

#     # Sort by AgentId and Temps_minute to ensure the correct temporal sequence
#     df = df.sort_values(by=['AgentId', 'Temps_minute'])

#     # Detect consecutive link changes by agent
#     df['link_change'] = (df['link'] != df['link'].shift()) | (df['AgentId'] != df['AgentId'].shift())
#     df['sequence_id'] = df['link_change'].cumsum()  # Create a unique identifier for each sequence of identical links

#     # Group by agent and sequence to check for sequences with more than 15 occurrences
#     def filter_sequence(group):
#         if len(group) > 15:  # Check if the sequence length exceeds 15
#             # Keep only the first and last rows if sequence length > 15
#             return pd.concat([group.iloc[[0]], group.iloc[[-1]]])
#         return group  # Keep the entire group if sequence length is 15 or less

#     # Apply the filtering function to each sequence
#     filtered_df = df.groupby(['AgentId', 'sequence_id']).apply(filter_sequence).reset_index(drop=True)

#     # Drop temporary columns
#     filtered_df = filtered_df.drop(columns=['link_change', 'sequence_id'])

#     # Save the filtered file
#     filtered_df.to_csv(fichier_sortie, index=False)




# fichier_events = "C:/Users/User/IdeaProjects/matsim-example-project-modified/output_detaillees_car_sunday.xml"
# fichier_network = "C:/Users/User/IdeaProjects/matsim-example-project-modified/simulation_output_sunday2/output_network.xml.gz"
# fichier_sortie_csv = "agent_positions_motif_clean_sunday.csv"
# fichier_filtre_csv = "agent_positions_motif_filtre_clean_sunday.csv"

# with open(fichier_sortie_csv, 'w') as f_out:
#     f_out.write("AgentId,Temps_minute,link,x,y,Motif_Orig,Motif_Dest\n")

# ecrire_positions_vehicules(fichier_events, fichier_network, fichier_sortie_csv, nettoyage_doublons=1)

# # filtrer_liaisons_consecutives(fichier_sortie_csv, fichier_filtre_csv)


# -*- coding: utf-8 -*-
import csv
import argparse
import folium

def chargement_fichier(chemin,i):
    """Ouvre et enregistre le fichier dans un dictionnaire.
    Suppression de la première ligne (labels)
    Key : le champs i
    Data : ensemble des champs"""
    fichier = open(chemin, "rb")
    liste = list(csv.reader(fichier,delimiter=";"))
    liste.pop(0) #suppression 1ere ligne
    fichier.close()
    dictionnaire = {}
    for definitions in liste :
        key_dico = definitions[i]   # n°STATION
        data_dico = definitions[0:] # Toutes les colonnes
        dictionnaire[key_dico] = data_dico
    return dictionnaire

def conversion(coord_DMS) :
    """Converti les coordonnées DMS en DD"""
    if coord_DMS[3] == "N" or coord_DMS[3] == "E":
        coord_DD = coord_DMS[0] + (coord_DMS[1] * 1/60) + (coord_DMS[2] * 1/3600)
    if coord_DMS[3] == "S" or coord_DMS[3] == "W":
        coord_DD = (coord_DMS[0] + (coord_DMS[1] * 1/60) + (coord_DMS[2] * 1/3600)
                   )*(-1)
    return coord_DD

def liste_unique(chemin,techno):
    """Extrait les émetteurs et retourne une liste unique des stations
    appartenant à la techno spécifiée"""
    fichier = open(chemin, "rb")
    liste = list(csv.reader(fichier,delimiter=";"))
    liste.pop(0) #suppression 1ere ligne
    fichier.close()
    liste_emetteur = []
    liste_unique = []
    for ligne in liste :
        if ligne[1] == techno:
            liste_emetteur.append(ligne[2])
    #liste sans doublons :
    liste_unique = list(set(liste_emetteur))
    return liste_unique, liste_emetteur

def mix_support_insee(d_insee,dico_support):
    """Ajoute des DATA Nom commune et n°département du dictionnaire insee
    au dictionnaire Support selon le code insee indiqué dans le champs 18
    des DATA du Support"""
    for key, support in dico_support.items() :
        commune = d_insee.get(support[18]) # code insee
        if commune == None:
            commune = ["","",""]
        support.append(commune[2])         # nom commune
        support.append(commune[1])         # département
    return dico_support

############################### PARSER #########################################
parser = argparse.ArgumentParser()
parser.add_argument('type', action='store',
                    help="Technologie de l'emetteur", type=str)
parser.add_argument('-c', action='store_true', dest='cluster',
                    help='Fonction altitude')
results = parser.parse_args()
if results.type == "GSMR":      # Raccourci GSMR
    techno = "GSM R"
elif results.type == "POCSAG":  # Raccourci POCSAG
    techno = "RMU-POCSAG"
else:
    techno = results.type

################### Chargement des fichiers ####################################
liste_unique, liste_emetteur = liste_unique("csv/SUP_EMETTEUR.txt",techno)
d_station=chargement_fichier("csv/SUP_STATION.txt", 0)
d_insee=chargement_fichier("csv/code-insee.csv", 0)
dico_support=chargement_fichier("csv/SUP_SUPPORT.txt", 1)
d_support=mix_support_insee(d_insee,dico_support)
d_nature=chargement_fichier("csv/SUP_NATURE.txt", 0)
d_proprietaire =chargement_fichier("csv/SUP_PROPRIETAIRE.txt", 0)

############# Intersection GSMR / STATION et GSMR / SUPPORT ####################
keys_station_unique = set(liste_unique).intersection(set(d_station.keys()))
d_station_unique = {k:d_station[k] for k in keys_station_unique}
keys_support_unique = set(liste_unique).intersection(set(d_support.keys()))
d_support_unique = {k:d_support[k] for k in keys_support_unique}

########################### MISE EN FORME ######################################
map_osm = folium.Map(location=[48.8589, 2.3469], zoom_start=12,
                   tiles='Stamen Toner')
if results.cluster: # Si option -c PARSER
    marker_cluster = folium.MarkerCluster().add_to(map_osm)
else:
    marker_cluster = map_osm
for key, data in d_support_unique.items():
    l_coord_dms_LAT = float(data[3]), float(data[4]), float(data[5]), data[6]
    l_coord_dms_LON = float(data[7]), float(data[8]), float(data[9]), data[10]
    datastation = d_station_unique.get(key)
    datemes = str(datastation[5])
    dateimplan = str(datastation[3])
    datanature = d_nature.get(data[2])
    nature = str(datanature[1])
    latnature = nature.decode('latin-1')
    if data[12] :
        proprio = d_proprietaire.get(data[12])
        latproprio = proprio[1].decode('latin-1')
    else :
        latproprio = ""
    html="Station : " + key + "<br>" + data[19] + " ("+data[20] + ")" \
    + "<br>Implantation : " + dateimplan + "<br>En service : " + datemes \
    + "<br>Antennes : " + str(liste_emetteur.count(key)) \
    + "<br>Support : " + data[0] + "<br>" + latnature \
    + " (" + str(data[11]) + "m)<br>" +  latproprio
    iframe = folium.element.IFrame(html=html, width=275, height=175)
    popup = folium.Popup(iframe, max_width=2650)
    folium.Marker([conversion(l_coord_dms_LAT), conversion(l_coord_dms_LON)],\
    popup=popup).add_to(marker_cluster)

map_osm.save("RadioMap_"+techno+".html")

# -*- coding: utf-8 -*-
from __future__ import unicode_literals #str utf-8
import folium
import json
import argparse

class Support(object):
    def __init__(self, support):
        self.id = support['id']
        #self.nature_id = support['nature_id']
        self.nature = support['nature']
        self.code_postal = support['code_postal']
        self.ville = support['ville']
        self.departement = support['departement']
        self.lat = support['lat']
        self.lon = support['lon']
        self.hauteur = support['hauteur']
        #self.proprio_id = support['proprietaire_id']
        self.proprietaire = support['proprietaire']
        self.antennes = []
    def get_systeme(self):
        liste = []
        for antenne in self.antennes:
            for station in antenne.stations:
                for emetteur in station.emetteurs:
                    liste.append(emetteur.systeme)
        return set(liste)
    def print_support(self):
        data_str = '{0} {1} ({2})\n'.format(self.id,self.proprietaire,self.departement)
        data_str += "{0} ({1}m)\n".format(self.nature, self.hauteur)
        liste = sorted(self.antennes, key=lambda x: float(x.altitude.replace(',', '.')), reverse=True)
        for antenne in liste:
            ant = [antenne.altitude, antenne.azimut]
            tec = ""
            compteur = 0
            for station in antenne.stations :
                exp = station.exploitant
                for emetteur in station.emetteurs:
                    tec += ' ' + emetteur.systeme
                if compteur == 0 :
                    data_str += '{0:5}m ({1:5}°) - {2:20} -{3}\n'.format(ant[0], ant[1], exp, tec)
                else :
                    data_str += '|____________>> - {0:20} -{1:3}\n'.format(exp, tec)
                compteur += 1
        return data_str
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

class Antenne(object):
    def __init__(self, antenne):
        #self.id = antenne['id']
        #self.type_id antenne['type_id']
        self.type = antenne['type']
        self.dimension, self.rayon = antenne['dimension'], antenne['rayon']
        self.azimut, self.altitude = antenne['azimut'], antenne['altitude']
        self.stations = []

class Station(object):
    def __init__(self, station):
        self.id = station['id']
    #    self.exploitant_id = station['exploitant_id']
        self.exploitant = station['exploitant']
        self.dateImplan = station['dateImplan']
        self.dateModif = station['dateModif']
        self.dateService = station['dateService']
        self.emetteurs = []

class Emetteur():
    def __init__(self, emetteur):
        #self.id = emetteur[0]
        self.systeme=emetteur['systeme']
        self.bandes = []

class Bande():
    def __init__(self, bande):
        self.debut = bande['debut']
        self.fin = bande['fin']
        self.unite = bande['unite']
###############################################################################
def lecture_json(fichier):
    with open(fichier, 'r') as f:
        data = json.load(f)
    dictionnaire = {}
    for support in data['supports']:
        o_sup = Support(support)
        for antenne in support['antennes']:
            o_ant = Antenne(antenne)
            o_sup.antennes.append(o_ant)
            for station in antenne['stations']:
                o_sta = Station(station)
                o_ant.stations.append(o_sta)
                for emetteur in station['emetteurs']:
                    o_eme = Emetteur(emetteur)
                    o_sta.emetteurs.append(o_eme)
                    for bande in emetteur['bandes']:
                        o_ban = Bande(bande)
                        o_eme.bandes.append(o_ban)
        dictionnaire[o_sup.id]=o_sup
    return dictionnaire

def liste_supports_systeme(dictionnaire, systeme):
    liste_supports_systeme = []
    for support in dictionnaire.values():
        if systeme in support.get_systeme():
            liste_supports_systeme.append(support.id)
    return liste_supports_systeme

def affichage_support(liste, couleur):
    for support in liste:
        data_sup = dictionnaire[support].print_support().replace('\n','<br>')
        geo=(dictionnaire[support].lat,dictionnaire[support].lon)
        html=folium.IFrame(html=data_sup,width=700, height=300)
        popup = folium.Popup(html, max_width=800)
        folium.Marker(geo,\
        popup=popup, icon = folium.Icon(color=couleur)).add_to(marker_cluster)
    return True

############################### PARSER #########################################
parser = argparse.ArgumentParser()
parser.add_argument('type', action='store',
                    help="Technologie de l'emetteur", type=str)
parser.add_argument('-c', action='store_true', dest='cluster',
                    help='Affichage Cluster')
results = parser.parse_args()
if results.type == "GSMR":      # Raccourci GSMR
    techno = "GSM R"
elif results.type == "POCSAG":  # Raccourci POCSAG
    techno = "RMU-POCSAG"
else:
    techno = results.type
###############################################################################
dictionnaire = lecture_json('json/dataradio.json')

liste_supports = liste_supports_systeme(dictionnaire, techno)

### CREATION DE LA CARTE ###
map_osm = folium.Map(location=[48.8589, 2.3469], zoom_start=12,
                   tiles='Stamen Toner')
if results.cluster: # Si option -c PARSER
    marker_cluster = folium.MarkerCluster().add_to(map_osm)
else:
    marker_cluster = map_osm
affichage_support(liste_supports, 'red')
map_osm.save("dataradio-map.html")

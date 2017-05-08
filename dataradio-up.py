# -*- coding: utf-8 -*-
from __future__ import unicode_literals #str utf-8
import re
import urllib
import zipfile
import os
import csv
import json

############################# CONSTANTES ######################################
dir_path = os.path.dirname(os.path.realpath(__file__))
dir_zip = "/zip/"
dir_csv = "/csv/"
dir_json = '/json/'
dir_insee = '/insee/'
anfr_data = "https://www.data.gouv.fr/fr/datasets/donnees-sur-les-installations-radioelectriques-de-plus-de-5-watts-1/"
insee_link = "https://public.opendatasoft.com/explore/dataset/correspondance-code-insee-code-postal/download/?format=csv&timezone=Europe/Paris&use_labels_for_header=true"
insee_file = "code-insee.csv"

############################ CLASSES JSON #####################################
class Support(object):
    def __init__(self, support):
        self.id = support[0]
        #self.station = support[1]
        #self.nature_id = support[2]
        self.nature = d_nature[support[2]][1].decode('latin-1')
        self.lat = conversion_coord(support[3:7])
        self.lon = conversion_coord(support[7:11])
        self.hauteur = support[11]
        #self.proprio_id = support[12]
        self.adresse_lieu = support[13].decode('latin-1')
        self.adresse_1 = support[14].decode('latin-1')
        self.adresse_2 = support[15].decode('latin-1')
        self.adresse_3 = support[16].decode('latin-1')
        self.code_postal = support[17]
        self.ville, self.departement = code_insee2postal(support[18])
        try:
            self.proprietaire = d_proprio[support[12]][1].decode('latin-1')
        except:
            self.proprietaire = ""
        self.antennes = []

class Antenne(object):
    def __init__(self, antenne):
        #self.id = antenne[1]
        #self.type_id = antenne[2]
        self.type = d_type_antenne[antenne[2]][1].decode('latin-1')
        self.dimension, self.rayon = antenne[3], antenne[4]
        self.azimut, self.altitude = antenne[5], antenne[6]
        self.stations = []

class Station(object):
    def __init__(self, station):
        self.id = station[0]
        #self.exploitant_id = station[1]
        id_exploitant, trash = station[1].split(',')
        self.exploitant = d_exploitant[id_exploitant][1].decode('latin-1')
        self.dateImplan = station[3]
        self.dateModif = station[4]
        self.dateService = station[5]
        self.emetteurs = []

class Emetteur(object):
    def __init__(self, emetteur):
        #self.id = emetteur[0]
        self.systeme = emetteur[1]
        self.bandes = []

class Bande(object):
    def __init__(self, bande):
        self.debut = bande[3]
        self.fin = bande[4]
        self.unite = bande[5]

########################### FONCTIONS JSON ####################################
def code_insee2postal(n_insee):
    """Retourne une liste au format [Nom commune,n°département]
        récupérée dans le dictionnaire d_insee
        selon le 'n_insee' indiqué"""
    commune = d_insee.get(n_insee) # code insee
    if commune == None: # Pour gerer les erreurs Insee
        commune = ["","","","","","","","","","","","","","","","","","","",""]
    resultat = [commune[2],\
                commune[15]]
    return resultat

def conversion_coord(coord_DMS) :
    """Converti les coordonnées géographiques DMS en DD"""
    if coord_DMS[3] == "N" or coord_DMS[3] == "E":
        coord_DD = float(coord_DMS[0]) + (float(coord_DMS[1]) * 1/60) + (float(coord_DMS[2]) * 1/3600)
    if coord_DMS[3] == "S" or coord_DMS[3] == "W":
        coord_DD = (float(coord_DMS[0]) + (float(coord_DMS[1]) * 1/60) + (float(coord_DMS[2]) * 1/3600)
                   )*(-1)
    return coord_DD

def chargement_fichier_complexe(chemin,i, j):
    """Retourne un dictionnaire au format i:[j]"""
    fichier = open(chemin, "rb")
    liste = list(csv.reader(fichier,delimiter=b';'))
    liste.pop(0) #suppression 1ere ligne
    fichier.close()
    dictionnaire = {}
    for ligne in liste :
        key_dico = ligne[i]
        data_dico = ligne[j]
        if dictionnaire.has_key(key_dico) : # si key_dico existe déjà
            dictionnaire[key_dico].append(data_dico)
        else :
            dictionnaire[key_dico] = [data_dico]
    return dictionnaire

def chargement_fichier_simple(chemin,i):
    """Retourne un dictionnaire au format i:[0:]"""
    fichier = open(chemin, "rb")
    liste = list(csv.reader(fichier,delimiter=b';'))
    liste.pop(0) #suppression 1ere ligne
    fichier.close()
    dictionnaire = {}
    for ligne in liste :
        key_dico = ligne[i]
        data_dico = ligne[0:]
        dictionnaire[key_dico] = data_dico
    return dictionnaire

def extraction_fichiers():
    """Retourne un dictionnaire au format :
        Key : N° Support
        Values : Objets support, antennes, stations, emetteurs, bandes
    """
    dictionnaire = {}
    for antenne in d_antenne.values(): #parcours du fichier antenne
        try:
            supports = d_station2support[antenne[0]] #recherche supports
            data_sta = d_station[antenne[0]]
            emetteurs = d_antenne2emetteur[antenne[1]] # recherche emetteurs
        except:
            pass #antenne sans support, sans station ou sans emetteur
        else:
            for support in supports:   # parcours des supports, cas de plusieurs supports...
                o_ant = Antenne(antenne)            # creation de l'objet antenne
                o_sta = Station(data_sta)           # creation de l'objet station
                for emetteur in emetteurs:
                    data_emetteur = d_emetteur[emetteur]
                    o_eme = Emetteur(data_emetteur) # creation de l'objet emetteur
                    try:
                        bandes = d_emetteur2bande[data_emetteur[0]] # recherche bandes
                        for bande in bandes:
                            data_bande = d_bande[bande]
                            o_bande = Bande(data_bande) # creation de l'objet bande
                            o_eme.bandes.append(o_bande)
                        o_sta.emetteurs.append(o_eme)
                    except:
                        pass #emetteur sans bande...

                if dictionnaire.has_key(support):   # Si le dictionnaire existe deja ?
                    o_sup = dictionnaire[support]   # recupération de l'objet support existant
                    mutu = 0
                    for ant in o_sup.antennes :     # parcours des antennes du support, cas du mutualisation d'antennes...
                        if ant.azimut == o_ant.azimut and ant.altitude == o_ant.altitude : # Mutualisation détectée
                            for sta in ant.stations :
                                if sta.id != o_sta.id: # Protection contre duplication d'antenne sur les stations sur plusieurs supports.
                                    ant.stations.append(o_sta)
                                    mutu = 1
                                    break
                    if mutu == 0:
                        o_ant.stations.append(o_sta)
                        o_sup.antennes.append(o_ant) # ajout de l'objet antenne à l'objet support
                else :
                    o_sup = Support(d_support[support]) #creation de l'objt support
                    o_ant.stations.append(o_sta)
                    o_sup.antennes.append(o_ant) # ajout de l'objet antenne à l'objet support
                    dictionnaire[support]=o_sup
    return dictionnaire

def sauvegarde_fichier(dossier, nom_fichier, fichier):
    """ Sauvegarde du 'fichier' à l'emplacement 'dossier'/'nom_fichier'  """
    supprimer_repertoire(dir_csv)
    try:
        ls_dir_zip = os.listdir(dir_path + dossier)
    except:
        print "Création du dossier {0}".format(dossier)
        os.mkdir(dir_path+dir_json)
    print "Sauvegarde du fichier {0}".format(nom_fichier)
    f = open(dossier[1:] + nom_fichier, 'w')
    print >> f, fichier
    f.close()
    return True

def mise_en_json(dictionnaire):
    """ Mise en forme du dictionnaire au format json """
    print "Mise en forme des données..."
    d_final = {}
    ### METADONNEES
    d_final['dataset'] = 'anfr:donnees-sur-les-installations-radioelectriques-de-plus-de-5-watts'
    d_final['date'] = '{0}-{1}-{2}'.format(datazip[0:4],datazip[4:6],datazip[6:8])
    ### DONNEES
    d_final['supports'] = []
    for station in dictionnaire.values():
        d_final["supports"].append(station)
    j = json.dumps(d_final, default=lambda o: o.__dict__,
                    sort_keys=True, indent=4)
    return j

########################### FONCTIONS UP ######################################
def verifier_site(anfr_data):
    """Avec une expression régulière sur la page web du jeu de données,
    récupère les noms des fichiers DATA et Tables_de_reference les plus récents,
    ainsi que leur URL"""
    page=urllib.urlopen(anfr_data)
    strpage=page.read()
    redatalink = r'https?://(?:[a-z0-9\-]+\.)+[a-z]{2,6}(?:/[^/#?]+)+\DATA.zip'
    redatafile = r'[0-9]+_DATA.zip'
    rereflink = r'https?://(?:[a-z0-9\-]+\.)+[a-z]{2,6}(?:/[^/#?]+)+\_Tables_de_reference.zip'
    rereffile = r'[0-9]+_Tables_de_reference.zip'
    datalinkre = re.compile(redatalink,re.IGNORECASE)
    datalink = datalinkre.findall(strpage)
    datazipre = re.compile(redatafile,re.IGNORECASE)
    datazip = datazipre.findall(strpage)
    reflinkre = re.compile(rereflink,re.IGNORECASE)
    reflink = reflinkre.findall(strpage)
    refzipre = re.compile(rereffile,re.IGNORECASE)
    refzip = refzipre.findall(strpage)
    print "Fichier disponible sur internet :", datazip[0]
    print "Fichier disponible sur internet :", refzip[0]
    return datalink[0], datazip[0], reflink[0], refzip[0]

def telechargement_data(data_link, data_file, ref_link, ref_file):
    """Telechargement des fichiers de données"""
    try:    # Verification de l'existance du dossier Zip
        ls_dir_zip = os.listdir(dir_path+dir_zip)
    except: # Sinon, le créé
        print "Création du dossier {0}".format(dir_zip)
        os.mkdir(dir_path+dir_zip)
    print "Le téléchargement du fichier va débuter"
    urllib.urlretrieve(data_link, dir_path + dir_zip + data_file)
    urllib.urlretrieve(ref_link, dir_path + dir_zip + ref_file)
    print "Téléchargement fini."
    return True

def unzip(source_file):
    """Extraction du fichier zip"""
    with zipfile.ZipFile(dir_path + dir_zip + source_file) as zf:
        print "Extraction du fichier {0} en cours...".format(source_file)
        zf.extractall(dir_path + dir_csv)
        print "Extraction finie"
    return True

def telechargement_insee():
    """Vérifie la présence du jeu de données INSEE, sinon le télécharge"""
    try:    # Vérification de la présence du dossier
        ls_dir_insee = os.listdir(dir_path+dir_insee)
    except: # Sinon, le créé
        print "Création du dossier {0}".format(dir_insee)
        os.mkdir(dir_path+dir_insee)
    if os.path.isfile(dir_path + dir_insee + insee_file): # Présence du fichier ?
        print "Fichier INSEE présent dans le répertoire {0}".format(dir_insee)
    else : # Sinon, le télécharge
        print "Fichier INSEE absent dans le répertoire {0}\nTéléchargement...".format(dir_insee)
        urllib.urlretrieve(insee_link, dir_path + dir_insee + insee_file)
        print "Téléchargement fini."
    return True

def supprimer_repertoire(repertoire):
    """ Supprime le répertoire 'repertoire'"""
    #SUPRESSION DES FICHIERS DU REPERTOIRE
    print "Suppression du répertoire {0}...".format(repertoire)
    for root, dirs, files in os.walk(dir_path + repertoire, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    #SUPRESSION DU REPERTOIRE
    os.removedirs(dir_path + repertoire)
    return True

######################### EXECUTION DU PROGRAMME ###############################

# Téléchargement des données
datalink, datazip, reflink, refzip = verifier_site(anfr_data)
telechargement_data(datalink, datazip, reflink, refzip)
unzip(datazip)
unzip(refzip)
supprimer_repertoire(dir_zip)
telechargement_insee()

# Chargement des fichiers
print "Chargement des fichiers..."
d_station2support=chargement_fichier_complexe("csv/SUP_SUPPORT.txt", 1, 0)
d_antenne2station=chargement_fichier_complexe("csv/SUP_ANTENNE.txt", 1, 0)
d_antenne2emetteur=chargement_fichier_complexe("csv/SUP_EMETTEUR.txt", 3, 0)
d_emetteur2bande=chargement_fichier_complexe("csv/SUP_BANDE.txt", 2, 1)

d_antenne=chargement_fichier_simple("csv/SUP_ANTENNE.txt", 1)
d_support=chargement_fichier_simple("csv/SUP_SUPPORT.txt", 0)
d_station=chargement_fichier_simple("csv/SUP_STATION.txt", 0)
d_emetteur=chargement_fichier_simple("csv/SUP_EMETTEUR.txt", 0)
d_bande=chargement_fichier_simple("csv/SUP_BANDE.txt", 1)

d_exploitant=chargement_fichier_simple("csv/SUP_EXPLOITANT.txt", 0)
d_nature=chargement_fichier_simple("csv/SUP_NATURE.txt", 0)
d_proprio=chargement_fichier_simple("csv/SUP_PROPRIETAIRE.txt", 0)
d_type_antenne=chargement_fichier_simple("csv/SUP_TYPE_ANTENNE.txt", 0)
d_insee=chargement_fichier_simple("insee/code-insee.csv", 0)

print "Extraction des données..."
d_extraction = extraction_fichiers()

### Création du JSON
json = mise_en_json(d_extraction)
sauvegarde_fichier(dir_json, 'dataradio.json', json)

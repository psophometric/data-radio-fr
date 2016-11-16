# -*- coding: utf-8 -*-
from datetime import datetime
import csv
import argparse

def chargement_fichier(chemin,i):
    """ Charge un fichier CSV et renvoi un dictionnaire
    Key : champs à spécifier en paramètre "i"
    Data : tous les champs du fichier """
    fichier = open(chemin, "rb")
    liste = list(csv.reader(fichier,delimiter=";"))
    liste.pop(0) #suppression 1ere ligne
    fichier.close()
    dictionnaire = {}
    for definitions in liste :
        key_dico = definitions[i]
        data_dico = definitions[0:]
        dictionnaire[key_dico] = data_dico
    return dictionnaire

def tri_date_stations(dico, ecart):
    """ tri dictionnaire "STATION" selon les dates d'Implantation (3)
    et date de Mise en service (5). Renvoi une liste.
    Le format de la date est vérifié. """
    liste = []
    for keys, data in dico.items():
        if data[5] is not "":
            try :
                data1 = datetime.strptime(data[5], '%d/%m/%Y')
                data0 = datetime.strptime(data[3], '%d/%m/%Y')
            except :
                print "\033[1;31mERREUR FORMAT (Date Implant.  Date EnServ)",\
                data[3], data[5], "STATION : ", keys, "\033[1;m"
            if data1 < data0:
                duree = data0 - data1
                if duree.days >= ecart:
                    data.append(duree.days)
                    liste.append(data)
    return liste

def conversion_float(fichier_virgule, i):
    """
    Remplace dans un champs "i" de dictinnaire les virgules par des points
    """
    for keys, data in fichier_virgule.items():
        if data[i]:
            data[i] = float(data[i].replace(',','.'))
    return True

def traduction_txt(fichier_txt, i, fichier_traduction,j):
    """
    Dans un dictionnaire, remplace le champs i par sa correspondance dans un
    second dictionnaire situé en champs j
    """
    for keys, data in fichier_txt.items():
        if data[i]:
            data_trad = fichier_traduction.get(data[i])
            data[i] = data_trad[j]
    return True

def action_date(duree_ecart):
    """ OPTION -d ecart_jour """
    fichier_station = chargement_fichier("csv/SUP_STATION.txt",0)
    resultat_tri_stations = tri_date_stations(fichier_station,duree_ecart)
    print "Il y a %s stations dont la date de MES est antérieure de plus de %s jours à celle d'implantation."\
    % (len(resultat_tri_stations), duree_ecart)
    for site in resultat_tri_stations :
        print "Date", site[3], site[5], "Station", site[0], "Ecart jours", site[6]

def action_altitude():
    """ OPTION -a """
    fichier_support = chargement_fichier("csv/SUP_SUPPORT.txt",1)
    fichier_antenne = chargement_fichier("csv/SUP_ANTENNE.txt",1)
    fichier_nature = chargement_fichier("csv/SUP_NATURE.txt",0)

    conversion_float(fichier_antenne,6)
    conversion_float(fichier_support,11)
    traduction_txt(fichier_support,2,fichier_nature,1)

    compteur_diff, compteur_tout_vide = 0, 0
    compteur_support_vide, compteur_antenne_vide = 0, 0

    for keys, data in fichier_antenne.items():
        data_sup = fichier_support.get(data[0])
        if data[6] > data_sup[11] and data[6] != "":
            compteur_diff += 1
            print "Station ", data[0], "Antenne altitude ", data[6], "Support ", \
                 data_sup[0]," hauteur", data_sup[11], data_sup[2].decode('latin-1')
        elif data[6] == "" and data_sup[11] == "":
            compteur_tout_vide += 1
            print "Station ", data[0], "Antenne altitude ", data[6], "Support ", \
                 data_sup[0]," hauteur", data_sup[11], data_sup[2].decode('latin-1')
        elif data[6] != "" and data_sup[11] == "":
            compteur_support_vide += 1
            print "Station ", data[0], "Antenne altitude ", data[6], "Support ", \
                 data_sup[0]," hauteur", data_sup[11], data_sup[2].decode('latin-1')
        elif data[6] == "" and data_sup[11] != "":
            compteur_antenne_vide += 1
            print "Station ", data[0], "Antenne altitude ", data[6], "Support ", \
                 data_sup[0]," hauteur", data_sup[11], data_sup[2].decode('latin-1')
    print "\033[1;31mRésultats"
    print compteur_antenne_vide, \
        "sites avec l'altitude de l'antenne non renseignée uniquement"
    print compteur_support_vide, \
        "sites avec l'altitude du support non renseignée uniquement"
    print compteur_tout_vide, \
        "sites avec l'altitudes de l'antenne et du support non renseignées"
    print compteur_diff, \
    "sites avec l'altitude de l'antenne plus haute que celle du support\033[1;m"
    return True

parser = argparse.ArgumentParser()
parser.add_argument('-d', action='store', dest='ecart_jour',
                    help='Ecart en jours', type=int)
parser.add_argument('-a', action='store_true', dest='altitude',
                    help='Fonction altitude')
results = parser.parse_args()
if results.ecart_jour:
    action_date(results.ecart_jour)
if results.altitude:
    action_altitude()

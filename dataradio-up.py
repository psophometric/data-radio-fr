# -*- coding: utf-8 -*-
import re
import urllib
import zipfile
import os

############################# CONSTANTES ######################################
dir_path = os.path.dirname(os.path.realpath(__file__))
dir_zip = "/zip/"
dir_csv = "/csv/"
anfr_data = "https://www.data.gouv.fr/fr/datasets/donnees-sur-les-installations-radioelectriques-de-plus-de-5-watts-1/"
insee_link = "http://public.opendatasoft.com/explore/dataset/correspondance-code-insee-code-postal/download/?format=csv&timezone=Europe/Paris&use_labels_for_header=true"
insee_file = "code-insee.csv"

def verifier_site(anfr_data):
    """Avec une expression régulière sur la page web du jeu de données,
    récupère le nom du fichier (DATA et Tables_de_reference) le plus récent,
    ainsi que son URL"""
    page=urllib.urlopen(anfr_data)
    strpage=page.read()
    redatalink = r'https://.+DATA.zip'
    redatafile = r'[0-9]+_DATA.zip'
    rereflink = r'https://.+reference.zip'
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
    return datalink[0], datazip[0], reflink[0], refzip[0]

def verifier_date(local_name, data_link, data_file, ref_link, ref_file):
    """Compare le fichier DATA du répertoire et le fichier DATA du site web,
    et télécharge si nécessaire"""
    if data_file > local_name:
        print "Le téléchargement va débuter"
        urllib.urlretrieve(data_link, dir_path + dir_zip + data_file)
        urllib.urlretrieve(ref_link, dir_path + dir_zip + ref_file)
        print "Téléchargement fini."
        return True
    else:
        print "Déjà à jour"
        return False

def unzip(source_file):
    """Extraction du fichier zip"""
    with zipfile.ZipFile(dir_path + dir_zip + source_file) as zf:
        print "Extraction du fichier %s en cours..." % source_file
        zf.extractall(dir_path + dir_csv)
        print "Extraction finie"

def trouver_dernier_fichier():
    """Recherche le nom du premier fichier (tri décroissant) du répertoire zip,
    si le répertoire n'existe pas, le créé"""
    try:
        ls_dir_zip = os.listdir(dir_path+dir_zip)
        regex = r'[0-9]{8}_DATA.zip'
        for fichier in sorted(ls_dir_zip, reverse = True):
            if re.match(regex, fichier):
                print "Fichier présent localement :", fichier
                return fichier
    except:
        print "Création du dossier ./zip/"
        os.mkdir(dir_path+dir_zip)

def insee():
    """Vérifie la présence du jeu de données INSEE, sinon le télécharge"""
    if os.path.isfile(dir_path + dir_csv + insee_file):
        print "Fichier INSEE présent dans le répertoire csv/"
    else :
        print "Fichier INSEE absent dans le répertoire csv/\nTéléchargement..."
        urllib.urlretrieve(insee_link, dir_path + dir_csv + insee_file)
        print "Téléchargement fini."
######################### EXECUTION DU PROGRAMME ###############################
datalink, datazip, reflink, refzip = verifier_site(anfr_data)
fichier = trouver_dernier_fichier()
update = verifier_date(fichier, datalink, datazip, reflink, refzip)
if update:
    unzip(datazip)
    unzip(refzip)
insee()

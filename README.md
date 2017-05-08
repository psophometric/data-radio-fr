# data-radio-fr

## Description
Programmes [Python](https://www.python.org/) qui permettent de travailler avec le jeu de données de l'Anfr [Les installations radioélectriques de plus de 5 watts](https://www.data.gouv.fr/fr/datasets/donnees-sur-les-installations-radioelectriques-de-plus-de-5-watts-1/)

- **dataradio-up**
Télécharge, met en forme et sauvegarde le jeu de données au format JSON.
- **dataradio-map**
Produit un fichier *html* permettant l'affichage sur une carte OpenStreetMap des émetteurs d'une technologie radio.

## Dépendance
- [Folium](https://github.com/python-visualization/folium)

## Installation (Linux Debian / Ubuntu)
Pré-requis (Pip, Git)
```
sudo apt-get install python-pip
sudo apt-get install git
```
Dépendance<br>
`pip install folium`<p>
Récupérer le dépôt <br>
`git clone https://github.com/psophometric/data-radio-fr.git`<p>
Initialisation de la base
```
cd data-radio-fr/
python dataradio-up.py
```

## Installation (Windows)
[Voir le Readme dédié](https://github.com/psophometric/data-radio-fr/blob/master/README-win10.md)

## Usage
`python dataradio-up.py` Télécharge, met en forme et sauvegarde le jeu de données au format JSON. **A exécuter en premier, après l'installation pour initialiser les bases.**<p>
`python dataradio-map.py GSMR` Produit un fichier html, affichant les émetteurs GSMR sur une carte OpenStreetMap. <br>
`python dataradio-map.py GSMR -c` Idem, mais avec l'option d'affichage *cluster* activée. <p>
> La carte se trouve dans le répertoire /home/Nom_Utilisateur/data-radio-fr/ au format html à ouvrir dans un naviateur web <p>

Liste exhaustive des technologies utilisables avec `data-radio-map` :
'BLR 3 GHz', 'COM MAR', 'COM MAR/COM TER', 'COM TER', 'DME', 'EM', 'EM/REC',
'ER HF', 'FH', 'FH ABI', 'FH/EM/REC', 'FM', 'GALILEO', 'GONIO', 'GPS', 'GPS D',
'GSM 1800', 'GSM 1800/GSM 900', 'GSM 900', 'GSM 900/GSM 1800',
'GSM 900/UMTS 2100', 'GSM R', 'LTE 1800', 'LTE 2600', 'LTE 700', 'LTE 800',
'PMR', 'RADIOASTRO', 'RDF AM', 'RDF DVB-T', 'RDF T-DAB', 'RDF TV-AN', 'RDR',
'RDR COT', 'RDR MTO', 'RDR PFL', 'REC', 'REC/GONIO', 'RMU-POCSAG', 'RS',
'RS/TELEM', 'SAT', 'SAT GEO', 'SAT NGEO', 'TELECD', 'TELECD/TELEM', 'TELEM',
'TELEM/TELECD', 'TETRA', 'TETRAPOL',
'UMTS 2100', 'UMTS 2100/UMTS 900', 'UMTS 900', 'VOR-C'<p>
Liste des raccourcis : 'GSMR'->'GSM R' 'POCSAG'->'RMU-POCSAG'

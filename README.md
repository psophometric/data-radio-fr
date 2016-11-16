# data-radio-fr

## Description
Trois programmes [Python](https://www.python.org/) qui permettent de travailler avec le jeu de données de l'Anfr [Les installations radioélectriques de plus de 5 watts](https://www.data.gouv.fr/fr/datasets/donnees-sur-les-installations-radioelectriques-de-plus-de-5-watts-1/)

- **dataradio-up**
Equivalent à un update/upgrade sur le jeu de données.
- **dataradio-tri**
Recherche d'incohérences des données sur les dates (format et écarts Implatantion/EnService) et sur les hauteurs de support / altitudes d'antennes.
- **dataradio-map**
Produit un fichier *html* permettant l'affichage sur une carte OpenStreetMap des émetteurs d'une technologie.

## Dépendances
- [Folium](https://github.com/python-visualization/folium)

## Usage
`dataradio-up`
Vérifie que la version du jeu de données dans le répertoire est bien à jour. Si nécessaire : télécharge et décompresse le jeu de données. **A exécuter en premier, après l'installation pour initialiser les bases.**<br><br>
`dataradio-tri -d 500` Affiche les stations ayant une date EnService antérieure de 500 jours à la date d'Implantation. *Affiche également si des données sont manquantes ou avec des erreurs de mise en forme*<br>
`dataradio-tri -a` Affiche les antennes ayant une altitude supérieure à la hauteur du support. *Affiche également si des données sont manquantes*<br><br>
`dataradio-map GSMR` Produit un fichier html, affichant les émetteurs GSMR sur une carte OpenStreetMap. <br>
`dataradio-map GSMR -c` Idem, mais avec l'option d'affichage *cluster* activée. <br>

Liste exhaustive des technologies utilisables avec `data-radio-map` :
'BLR 3 GHz', 'COM MAR', 'COM MAR/COM TER', 'COM TER', 'DME', 'EM', 'EM/REC',
'ER HF', 'FH', 'FH ABI', 'FH/EM/REC', 'FM', 'GALILEO', 'GONIO', 'GPS', 'GPS D',
'GSM 1800', 'GSM 1800/GSM 900', 'GSM 900', 'GSM 900/GSM 1800',
'GSM 900/UMTS 2100', 'GSM R', 'LTE 1800', 'LTE 2600', 'LTE 700', 'LTE 800',
'PMR', 'RADIOASTRO', 'RDF AM', 'RDF DVB-T', 'RDF T-DAB', 'RDF TV-AN', 'RDR',
'RDR COT', 'RDR MTO', 'RDR PFL', 'REC', 'REC/GONIO', 'RMU-POCSAG', 'RS',
'RS/TELEM', 'SAT', 'SAT GEO', 'SAT NGEO', 'TELECD', 'TELECD/TELEM', 'TELEM',
'TELEM/TELECD', 'TETRA', 'TETRAPOL',
'UMTS 2100', 'UMTS 2100/UMTS 900', 'UMTS 900', 'VOR-C'<br>
Liste des raccourcis : 'GSMR'->'GSM R' 'POCSAG'->'RMU-POCSAG'
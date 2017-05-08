# Pour les utilisateurs de Windows

## Installation de Python
Allez sur la page [Download Python 2.7.12](https://www.python.org/downloads/release/python-2712/).<br>
Cliquez sur *Windows x86-64 MSI installer* (ou *Windows x86 MSI installer* pour la version 32 bits).<p>
Lancez le fichier téléchargé.<br>
Laissez les choix par défaut sur les deux premières pages.<br>
Sur la troisième page, intitulée "Customize", sélectionnez l'option "Add python.exe to Path".<p>

## Installation de Git
Allez sur la page [git-for-windows.github.io/](https://git-for-windows.github.io/)<br>
Cliquez sur *Download*<br>
Lancez le fichier téléchargé et laissez les choix par défaut.<p>
Lancez l'invité de commandes (Clic-droit sur le "Bouton Démarrer" > Invite de commandes).<br>
`git clone https://github.com/psophometric/data-radio-fr.git`<p>

## Installation de la dépendance Folium
Lancez l'invité de commandes (Clic-droit sur le "Bouton Démarrer" > Invite de commandes).<br>
`pip install folium`<p>

## Initialisation de la base
Lancez l'invité de commandes (Clic-droit sur le "Bouton Démarrer" > Invite de commandes).
```
cd data-radio-fr
python dataradio-up.py
```
Cela provoque un message d'erreur. Plus d'information sur [cette page](https://www.python.org/dev/peps/pep-0476/).<br>
Pour cette raison, il est nécessaire d'ajouter au fichier `dataradio-up.py` (clic droit sur le fichier / Edit with IDLE) les lignes suivantes juste après les lignes *import* existantes :
```
import ssl

# This restores the same behavior as before.
context = ssl._create_unverified_context()
urllib.urlopen("https://www.data.gouv.fr/fr/datasets/donnees-sur-les-installations-radioelectriques-de-plus-de-5-watts-1/", context=context)
```
> Le fichier se trouve dans le répertoire : C:\Users\Nom_Utilisateur\data-radio-fr

## Usage
Lancez l'invité de commandes (Clic-droit sur le "Bouton Démarrer" > Invite de commandes).<br>
Se rendre dans le répertoire du programme :<br>
`cd data-radio-fr`<br>
Puis :<br>
`python dataradio-up.py`Télécharge, met en forme et sauvegarde le jeu de données au format JSON. **A exécuter en premier, après l'installation pour initialiser les bases.**<p>

`python dataradio-map.py GSMR` Produit un fichier html, affichant les émetteurs GSMR sur une carte OpenStreetMap. <br>
`python dataradio-map.py GSMR -c` Idem, mais avec l'option d'affichage *cluster* activée. <p>
> La carte se trouve dans le répertoire C:\Users\Nom_Utilisateur\data-radio-fr au format html à ouvrir dans un naviateur web 

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

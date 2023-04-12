import pandas as pd  #manipulation des donnees
import numpy as np   #calcul mathematiques
import matplotlib.pyplot as plt  #visualisation
import scipy as scipy   # faire des statistques, probabilités et optimisation
import seaborn as sns   #visualiser les données
import random
from datetime import timedelta, datetime

def caster_date(data, liste_date):
    """
    La fonction convertit des colonnes de dates dans un dataframe Pandas en utilisant « .to_datetime()». 
    Args:
        data
        liste_date (list):liste de noms de colonnes 
    Returns:
        L'ensemble de données Pandas mis à jour avec les colonnes de dates converties.
    """
    for col in liste_date:
        data[col] = pd.to_datetime(data[col])
    return data
def caster_Time(data, liste_time):
    """
   Elle convertit chaque élément de chaque colonne en un objet datetime en utilisant « .to_datetime() »
   et la méthode « .dt.time » de Pandas pour extraire la composante temps de chaque objet datetime converti.
    Args:
        data
        liste_time (list): Liste de noms de colonnes à convertir.
    Returns:
        L'ensemble de données Pandas mis à jour avec les colonnes de temps converties.
    """
    for col in liste_time:
        data[col] = pd.to_datetime(data[col], format='%H:%M:%S').dt.time
    return data
def caster_quali(data, liste_quali):
    """ 
    Elle utilise la méthode astype() de Pandas pour convertir chaque élément de chaque colonne en un objet de type 'object'.
    
    Args:
        data
        liste_quali (list): Liste de noms de colonnes de valeurs qualitatives à convertir.
    Returns:
        L'ensemble de données Pandas mis à jour avec les colonnes de valeurs qualitatives converties.
    """
    for col in liste_quali:
        data[col] = data[col].astype('object')
    return data
def caster_quanti(data, liste_quanti):
    """ 
    Elle utilise une fonction lambda pour remplacer les virgules par des points et convertir 
    chaque élément de chaque colonne en un nombre flottant.
    Args:
        data
        liste_quanti (list): Liste de noms de colonnes de valeurs quantitatives à convertir.
    Returns:
        L'ensemble de données Pandas mis à jour avec les colonnes de valeurs quantitatives converties.
    """
    for col in liste_quanti:
        data[col] = data[col].apply(lambda x: float(x.replace(",", ".")))
    return data


class DataAugmenter:
    """
    Classe pour augmenter les données d'un ensemble de données Pandas en générant des données synthétiques.

    Args:
        data (pandas.DataFrame): Ensemble de données à augmenter.
        liste_quanti (list): Liste de noms de colonnes quantitatives à augmenter.
        liste_quali (list): Liste de noms de colonnes qualitatives à augmenter.
        liste_date (list): Liste de noms de colonnes de dates à augmenter.

    Methods:
        aug_var_quali():
            Génère et renvoie un ensemble de données Pandas contenant des données synthétiques pour les variables qualitatives.
        aug_var_quanti():
            Génère et renvoie un ensemble de données Pandas contenant des données synthétiques pour les variables quantitatives.
        aug_var_date():
            Génère et renvoie un ensemble de données Pandas contenant des données synthétiques pour les variables de dates.
        aug_pipeline():
            Exécute le pipeline complet pour générer des données synthétiques pour toutes les variables spécifiées et les renvoie
            sous forme d'un ensemble de données Pandas.

    """
    def __init__(self, data, liste_quanti, liste_quali,liste_date):
        self.data = data
        self.liste_quanti = liste_quanti
        self.liste_quali = liste_quali
        self.liste_date = liste_date
    
    def aug_var_quali(self):
        """
        La fonction crée une liste vide et itère 1000 fois pour ajouter des lignes 
        de données augmentées. Pour chaque ligne, elle choisit aléatoirement des valeurs 
        pour chaque colonne qualitative et les ajoute à un dictionnaire. Le dictionnaire
        est ensuite ajouté à la liste « donnees_augment »
        """
        donnees_augment = []
        for i in range(1000):
            ligne_augmentee = {}
            for col in self.liste_quali:
                col_augment = random.choice(self.data[col])
                ligne_augmentee[col] = col_augment
            donnees_augment.append(ligne_augmentee)
        return pd.DataFrame(donnees_augment)
    
    def aug_var_quanti(self):
        """
       Initialise une liste vide 'donnees_augmentees' et Itère 1000 fois pour créer 1000 lignes de données
        Pour chaque colonne quantitative dans la liste 'liste_quanti', 
        génère une valeur aléatoire à partir d’une distribution uniforme et l’ajoute au dictionnaire 'ligne_augmentee'.
        Les données augmentées sont stockées dans l’ensemble de données « donnees_augmentees », 
        """
        donnees_augmentees = []
        for i in range(1000):
            ligne_augmentee = {}
            for col in self.liste_quanti:
                min_col, max_col = self.data[col].min(), self.data[col].max()
                col_augmente = np.random.uniform(min_col, max_col)
                ligne_augmentee[col] = col_augmente
            donnees_augmentees.append(ligne_augmentee)
        return pd.DataFrame(donnees_augmentees)
    
    def aug_var_date(self):
        """
        Elle itère sur chaque colonne de date pour trouver la date minimale et maximale, 
        calculer le nombre de jours entre elles et générer une nouvelle date aléatoire 
        en ajoutant un nombre de jours aléatoire compris entre 0 et le nombre de jours calculé. 
        Les nouvelles dates sont stockées dans une liste de dictionnaires 'donnees_augmentees' qui 
        est retournée sous forme d’un objet DataFrame.
        """
        donnees_augmentees = []
        for i in range(1000):
            ligne_augmentee = {}
            for col in self.liste_date:
                min_col, max_col = self.data[col].min(), self.data[col].max()
                days = (max_col - min_col).days
                random_days = random.randint(0, days)
                col_augmente = min_col + timedelta(days=random_days)
                ligne_augmentee[col] = col_augmente
            donnees_augmentees.append(ligne_augmentee)
        return pd.DataFrame(donnees_augmentees)
    
    def aug_pipeline(self):
        """
        crée un pipeline complet pour la génération de données augmentées en appelant 
        les fonctions 'aug_var_quanti', 'aug_var_quali' et 'aug_var_date'.
        Elle fusionne ensuite les données numériques et qualitatives augmentées en utilisant 
        '.merge' avant de fusionner les données avec les valeurs de date augmentées.
        """
        donnees_quanti = self.aug_var_quanti()
        donnees_quali = self.aug_var_quali()
        donnees_date = self.aug_var_date()

        donnees_quanti_quali = pd.merge(donnees_quanti, donnees_quali, left_index=True, right_index=True)
        donnees_augmentees = pd.merge(donnees_quanti_quali, donnees_date, left_index=True, right_index=True)

        return donnees_augmentees
    
    

def aug_var_quanti(data, liste):
    donnees_augmentees = []
    for i in range(1000):
        ligne_augmentee = {}
        for col in liste:
            min_col, max_col = data[col].min(), data[col].max()
            col_augmente = np.random.uniform(min_col, max_col)
            ligne_augmentee[col] = col_augmente
        donnees_augmentees.append(ligne_augmentee)
    return pd.DataFrame(donnees_augmentees)

def aug_var_quali(data, liste):
    donnees_augment = []
    for i in range(1000):
        ligne_augmentee = {}
        for col in liste:
            col_augment = random.choice(data[col])
            ligne_augmentee[col] = col_augment
        donnees_augment.append(ligne_augmentee)
    return pd.DataFrame(donnees_augment)

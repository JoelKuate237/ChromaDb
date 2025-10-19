# ============================================================================
# IMPORTATION DES BIBLIOTHÈQUES NÉCESSAIRES
# ============================================================================

# ChromaDB pour la base de données vectorielle
import chromadb
# Module CSV pour lire les fichiers de données
import csv

# ============================================================================
# ÉTAPE 1: INITIALISATION DU CLIENT CHROMADB
# ============================================================================

# Créer un client persistant (les données sont sauvegardées sur le disque)
# Par défaut, les données sont stockées dans le dossier ./chroma
client = chromadb.PersistentClient()

# ============================================================================
# ÉTAPE 2: CRÉATION OU RÉCUPÉRATION DE LA COLLECTION
# ============================================================================

# Créer ou récupérer une collection nommée "diamonds"
# Si la collection existe déjà, elle sera récupérée
# Sinon, une nouvelle collection sera créée
col = client.get_or_create_collection(name="diamonds")

# ============================================================================
# ÉTAPE 3: DÉFINITION DU CHEMIN DU FICHIER CSV
# ============================================================================

# Chemin vers le fichier CSV contenant les données de population
csv_file_path = "population.csv"

# ============================================================================
# ÉTAPE 4: PRÉPARATION DES LISTES POUR STOCKER LES DONNÉES
# ============================================================================

# Liste pour stocker les documents textuels formatés
documents = []
# Liste pour stocker les identifiants uniques de chaque document
ids = []

# ============================================================================
# ÉTAPE 5: LECTURE ET TRAITEMENT DU FICHIER CSV
# ============================================================================

# Ouvrir le fichier CSV en mode lecture avec encodage ISO-8859-1
# (pour gérer les caractères spéciaux comme les accents)
with open(csv_file_path, mode="r", encoding="ISO-8859-1") as file:
    # Créer un lecteur CSV qui interprète chaque ligne comme un dictionnaire
    # Les clés sont les noms de colonnes, les valeurs sont les données
    csv_reader = csv.DictReader(file, delimiter=",")
    
    # Afficher les noms des colonnes du fichier CSV
    print("CSV columns: ", csv_reader.fieldnames)

    # Parcourir chaque ligne du fichier CSV avec son index
    for idx, row in enumerate(csv_reader):
        # Exemple d'ancien format pour les diamants (commenté):
        # document = f"Carat: {row['carat']}, Cut: {row['cut']}, Color: {row['color']}, Clarity: {row['clarity']}, Depth: {row['depth']}, Table: {row['table']}, Price: {row['price']}, Dimensions: ({row['x']} x {row['y']} x {row['z']})"
        
        # Formater les données de la ligne en une chaîne de texte descriptive
        # Extrait le pays et sa population depuis le CSV
        document = f"Country: {row['Country']}, Population: {row['Population']}"
        
        # Ajouter le document formaté à la liste
        documents.append(document)
        
        # Générer un ID unique pour chaque document (id_0, id_1, id_2, etc.)
        ids.append(f"id_{idx}")

# ============================================================================
# ÉTAPE 6: INSERTION DES DONNÉES DANS LA COLLECTION
# ============================================================================

# Utiliser upsert pour insérer ou mettre à jour les documents
# upsert = "update" + "insert" (ajoute si nouveau, met à jour si existant)
col.upsert(
    documents=documents,  # Liste des documents textuels
    ids=ids               # Liste des identifiants correspondants
)

# ============================================================================
# ÉTAPE 7: EFFECTUER UNE RECHERCHE SÉMANTIQUE
# ============================================================================

# Effectuer une requête de recherche par similarité sémantique
# ChromaDB va trouver les documents les plus similaires à la question posée
results = col.query(
    query_texts=["Donne-moi la population de la Chine."],  # Question en langage naturel
    n_results=2  # Nombre de résultats à retourner (top 2 documents les plus pertinents)
)

# ============================================================================
# ÉTAPE 8: AFFICHAGE DU RÉSULTAT
# ============================================================================

# Afficher le premier document du premier résultat
# results['documents'] est une liste de listes
# [0][0] = première requête, premier résultat
print(results['documents'][0][0])
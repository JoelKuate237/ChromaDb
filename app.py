# Importer la bibliothèque ChromaDB
import chromadb

# Créer un client ChromaDB
chromadb_client = chromadb.Client()

# Créer une collection nommée "personne"
collection = chromadb_client.create_collection(name ="personne")

# Ajouter des documents à la collection
collection.add (
    # Liste des documents textuels
    documents=[
        "bonjour je suis heureux de vous lire",
        " j'aime travailler avec vous"
    ],
    # Identifiants uniques pour chaque document
    ids=["1", "2"]
)

# Effectuer une recherche par similarité sémantique
result = collection.query (
    query_texts=["Bonjour"],  # Texte de recherche
    n_results=2  # Nombre de résultats à retourner
)

# Afficher les résultats de la recherche
print(result)



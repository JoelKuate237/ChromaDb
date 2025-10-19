# ============================================================================
# EXEMPLE 1: UTILISATION BASIQUE DE CHROMADB (CLIENT EN MÉMOIRE)
# ============================================================================

import chromadb

# Créer un client ChromaDB en mémoire (données perdues à la fermeture)
chromadb_client = chromadb.Client()

# Créer une nouvelle collection nommée "Personne"
collection = chromadb_client.create_collection(name="Personne")

# Ajouter des documents à la collection
collection.add(
    documents=[
        "Salut, les amis de la Data !",
        "J'aime la Data Science."
    ],
    ids=["id1", "id2"]
)

# Effectuer une recherche sémantique sur le mot "Data"
results = collection.query(
    query_texts=["voiture"],
    n_results=3
)

# Afficher les résultats complets
print(results)
# Afficher uniquement le premier document trouvé
print(results['documents'][0][0])

# Afficher les informations sur la collection
print(collection.name)
print(collection.count())
# Récupérer un document spécifique par son ID
print(collection.get(ids=["id2"]))


# ============================================================================
# NOTES IMPORTANTES:
# ============================================================================
# 
# 1. Client() : Stockage en mémoire - données perdues à la fermeture
# 2. PersistentClient() : Stockage sur disque - données conservées
# 3. HttpClient() : Connexion à un serveur ChromaDB distant
# 
# 4. create_collection() : Crée une nouvelle collection (erreur si existe)
# 5. get_or_create_collection() : Crée ou récupère une collection
# 
# 6. add() : Ajoute de nouveaux documents (erreur si ID existe)
# 7. upsert() : Ajoute ou met à jour des documents
# 
# 8. query() : Recherche par similarité sémantique
# 9. get() : Récupère des documents par ID
# 
# 10. count() : Nombre de documents dans la collection
# 11. name : Nom de la collection
# ============================================================================



# ============================================================================
# EXEMPLE 3: CLIENT PERSISTANT - RECHERCHE DE VOITURES
# ============================================================================

import chromadb

# Créer un client persistant (données sauvegardées sur disque)
client = chromadb.PersistentClient()

# Créer ou récupérer une collection de voitures
coll = client.get_or_create_collection(name="voitures")

# Demander à l'utilisateur ce qu'il cherche
text_user = input("Que voulez-vous ?")

# Ajouter des marques de voitures
coll.upsert(
    documents=[
        "DavRos",
        "BMW",
        "VX",
        "RAV4"
    ],
    ids=["id1", "id2", "id3", "id4"]
)

# Rechercher la voiture correspondant à la requête
results = coll.query(
    query_texts=text_user,
    n_results=1
)

# Afficher la voiture trouvée
print(results["documents"][0][0])

# ============================================================================
# EXEMPLE 4: CLIENT HTTP (SERVEUR CHROMADB DISTANT)
# ============================================================================

import chromadb

# Se connecter à un serveur ChromaDB distant via HTTP
# Nécessite un serveur ChromaDB en cours d'exécution sur localhost:8000
client_db = chromadb.HttpClient(host='localhost', port=8000)


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

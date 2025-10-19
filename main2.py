# ============================================================================
# EXEMPLE 2: SYSTÈME DE RECHERCHE DE LIVRES AVEC REQUÊTE UTILISATEUR
# ============================================================================

import chromadb

# Créer un client ChromaDB
client_chroma = chromadb.Client()

# Créer ou récupérer une collection de livres
col = client_chroma.get_or_create_collection(name="books")

# Ajouter des livres avec leurs prix
col.upsert(
    documents=[
        "Livre Python à 50 €",
        "Livre R à 15 €",
        "Livre Java 49 €",
        "Livre JavaScript à 18 €"
    ],
    ids=["id1", "id2", "id3", "id4"]
)

# Demander à l'utilisateur de saisir sa recherche
text = input("Tapez votre requête en langage naturel: ")

# Rechercher le livre correspondant à la requête
results = col.query(
    query_texts=text,
    n_results=1
)

# Afficher le livre trouvé
print(results['documents'][0][0])
# Afficher le nombre total de livres
print(col.count())
# Afficher le nom de la collection
print(col.name)







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

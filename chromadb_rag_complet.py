# ============================================================================
# GUIDE COMPLET CHROMADB POUR RAG (Retrieval Augmented Generation)
# ============================================================================

import chromadb
from chromadb.config import Settings

# ============================================================================
# 1. CRÉATION DU CLIENT CHROMADB
# ============================================================================

# Client en mémoire (les données sont perdues après l'arrêt du programme)
client_memoire = chromadb.Client()

# Client avec persistance (les données sont sauvegardées sur le disque)
client_persistant = chromadb.PersistentClient(path="./chromadb_data")

# Client avec configuration personnalisée
client_config = chromadb.Client(Settings(
    anonymized_telemetry=False,  # Désactiver la télémétrie
))

# ============================================================================
# 2. GESTION DES COLLECTIONS
# ============================================================================

# Créer une nouvelle collection
collection = client_persistant.create_collection(
    name="ma_collection_rag",
    metadata={"description": "Collection pour système RAG"}
)

# Récupérer une collection existante
collection_existante = client_persistant.get_collection(name="ma_collection_rag")

# Créer ou récupérer une collection (si elle existe déjà, la récupère)
collection = client_persistant.get_or_create_collection(
    name="ma_collection_rag",
    metadata={"description": "Collection pour système RAG"}
)

# Lister toutes les collections
toutes_collections = client_persistant.list_collections()
print(f"# Collections disponibles: {len(toutes_collections)}")

# Supprimer une collection
# client_persistant.delete_collection(name="ma_collection_rag")

# ============================================================================
# 3. AJOUT DE DOCUMENTS (ADD)
# ============================================================================

# Ajouter des documents simples avec IDs
collection.add(
    documents=[
        "Python est un langage de programmation populaire",
        "JavaScript est utilisé pour le développement web",
        "Java est un langage orienté objet"
    ],
    ids=["doc1", "doc2", "doc3"]
)

# Ajouter des documents avec métadonnées
collection.add(
    documents=[
        "L'intelligence artificielle transforme le monde",
        "Le machine learning est une branche de l'IA"
    ],
    metadatas=[
        {"categorie": "IA", "annee": 2024, "source": "article1"},
        {"categorie": "ML", "annee": 2024, "source": "article2"}
    ],
    ids=["doc4", "doc5"]
)

# Ajouter des documents avec embeddings personnalisés
# (utile si vous générez vos propres vecteurs)
collection.add(
    documents=["Document avec embedding personnalisé"],
    embeddings=[[0.1, 0.2, 0.3, 0.4]],  # Vecteur d'embedding
    metadatas=[{"type": "custom"}],
    ids=["doc6"]
)

# ============================================================================
# 4. REQUÊTES ET RECHERCHE (QUERY)
# ============================================================================

# Recherche simple par similarité sémantique
resultats = collection.query(
    query_texts=["langage de programmation"],
    n_results=3  # Nombre de résultats à retourner
)

print("\n# Résultats de la recherche simple:")
print(f"Documents: {resultats['documents']}")
print(f"IDs: {resultats['ids']}")
print(f"Distances: {resultats['distances']}")

# Recherche avec filtre sur les métadonnées
resultats_filtres = collection.query(
    query_texts=["intelligence artificielle"],
    n_results=2,
    where={"categorie": "IA     "}  # Filtre sur les métadonnées
)

print("\n# Résultats avec filtre:")
print(f"Documents: {resultats_filtres['documents']}")

# Recherche avec filtre sur le contenu des documents
resultats_where_document = collection.query(
    query_texts=["programmation"],
    n_results=3,
    where_document={"$contains": "langage"}  # Filtre sur le contenu
)

# Recherche avec embedding personnalisé
resultats_embedding = collection.query(
    query_embeddings=[[0.1, 0.2, 0.3, 0.4]],
    n_results=2
)

# ============================================================================
# 5. RÉCUPÉRATION DE DOCUMENTS (GET)
# ============================================================================

# Récupérer tous les documents
tous_documents = collection.get()
print(f"\n# Total de documents: {len(tous_documents['ids'])}")

# Récupérer des documents spécifiques par IDs
documents_specifiques = collection.get(
    ids=["doc1", "doc2"],
    include=["documents", "metadatas", "embeddings"]
)

# Récupérer avec filtre sur métadonnées
documents_filtres = collection.get(
    where={"categorie": "IA"},
    include=["documents", "metadatas"]
)

# Récupérer avec limite
premiers_documents = collection.get(
    limit=5,
    include=["documents", "metadatas"]
)

# Récupérer avec offset (pagination)
documents_pagines = collection.get(
    limit=10,
    offset=5,  # Sauter les 5 premiers
    include=["documents", "metadatas"]
)

# ============================================================================
# 6. MISE À JOUR DE DOCUMENTS (UPDATE)
# ============================================================================

# Mettre à jour le contenu d'un document
collection.update(
    ids=["doc1"],
    documents=["Python est un langage de programmation très populaire et puissant"]
    
)

# Mettre à jour les métadonnées
collection.update(
    ids=["doc1"],
    metadatas=[{"categorie": "Programmation", "mise_a_jour": "2024-10-19"}]
)

# Mettre à jour document et métadonnées
collection.update(
    ids=["doc2"],
    documents=["JavaScript est le langage le plus utilisé pour le web"],
    metadatas=[{"categorie": "Web", "popularite": "haute"}]
)

# Mettre à jour avec embedding personnalisé
collection.update(
    ids=["doc3"],
    embeddings=[[0.5, 0.6, 0.7, 0.8]]
)

# ============================================================================
# 7. UPSERT (Ajouter ou Mettre à jour)
# ============================================================================

# Upsert : ajoute si l'ID n'existe pas, met à jour sinon
collection.upsert(
    ids=["doc7", "doc1"],  # doc7 sera ajouté, doc1 sera mis à jour
    documents=[
        "C++ est utilisé pour les applications haute performance",
        "Python 3.12 apporte de nouvelles fonctionnalités"
    ],
    metadatas=[
        {"categorie": "Programmation", "performance": "haute"},
        {"categorie": "Python", "version": "3.12"}
    ]
)

# ============================================================================
# 8. SUPPRESSION DE DOCUMENTS (DELETE)
# ============================================================================

# Supprimer des documents par IDs
collection.delete(ids=["doc6"])

# Supprimer avec filtre sur métadonnées
collection.delete(
    where={"categorie": "test"}  # Supprime tous les docs de catégorie "test"
)

# Supprimer avec filtre sur le contenu
collection.delete(
    where_document={"$contains": "obsolète"}
)

# ============================================================================
# 9. INFORMATIONS SUR LA COLLECTION
# ============================================================================

# Obtenir le nom de la collection
nom_collection = collection.name
print(f"\n# Nom de la collection: {nom_collection}")

# Obtenir les métadonnées de la collection
metadata_collection = collection.metadata
print(f"# Métadonnées de la collection: {metadata_collection}")

# Compter le nombre de documents
nombre_documents = collection.count()
print(f"# Nombre de documents dans la collection: {nombre_documents}")

# Modifier les métadonnées de la collection
collection.modify(metadata={"description": "Collection RAG mise à jour", "version": "2.0"})

# ============================================================================
# 10. GESTION DES EMBEDDINGS
# ============================================================================

# ChromaDB utilise par défaut le modèle "all-MiniLM-L6-v2"
# Vous pouvez spécifier une fonction d'embedding personnalisée

from chromadb.utils import embedding_functions

# Utiliser un modèle Sentence Transformers
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Créer une collection avec fonction d'embedding personnalisée
collection_custom = client_persistant.get_or_create_collection(
    name="collection_custom_embedding",
    embedding_function=sentence_transformer_ef
)

# Utiliser OpenAI pour les embeddings (nécessite une clé API)
# openai_ef = embedding_functions.OpenAIEmbeddingFunction(
#     api_key="votre_cle_api",
#     model_name="text-embedding-ada-002"
# )

# Utiliser Cohere pour les embeddings
# cohere_ef = embedding_functions.CohereEmbeddingFunction(
#     api_key="votre_cle_api",
#     model_name="embed-english-v2.0"
# )

# ============================================================================
# 11. EXEMPLE COMPLET DE SYSTÈME RAG
# ============================================================================

def systeme_rag_complet():
    """
    Exemple d'un système RAG complet avec ChromaDB
    """
    # Étape 1: Initialiser le client avec persistance
    client = chromadb.PersistentClient(path="./rag_database")
    
    # Étape 2: Créer ou récupérer la collection
    collection = client.get_or_create_collection(
        name="base_connaissances",
        metadata={"type": "RAG", "domaine": "informatique"}
    )
    
    # Étape 3: Charger les documents dans la base de connaissances
    documents_base = [
        "RAG combine la recherche et la génération pour créer des réponses précises",
        "ChromaDB est une base de données vectorielle open-source",
        "Les embeddings transforment le texte en vecteurs numériques",
        "La recherche sémantique permet de trouver des documents similaires par le sens",
        "L'IA générative utilise des modèles de langage pour créer du contenu"
    ]
    
    collection.upsert(
        documents=documents_base,
        metadatas=[
            {"topic": "RAG", "importance": "haute"},
            {"topic": "Database", "importance": "haute"},
            {"topic": "NLP", "importance": "moyenne"},
            {"topic": "Search", "importance": "haute"},
            {"topic": "AI", "importance": "moyenne"}
        ],
        ids=[f"kb_{i}" for i in range(len(documents_base))]
    )
    
    # Étape 4: Fonction de recherche RAG
    def rechercher_contexte(question, n_results=3):
        """
        Recherche les documents les plus pertinents pour la question
        """
        resultats = collection.query(
            query_texts=[question],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )
        return resultats
    
    # Étape 5: Utiliser le système RAG
    question_utilisateur = "Qu'est-ce qu'une base de données vectorielle?"
    
    contexte = rechercher_contexte(question_utilisateur, n_results=2)
    
    print("\n# ======= SYSTÈME RAG EN ACTION =======")
    print(f"# Question: {question_utilisateur}")
    print(f"\n# Contexte récupéré:")
    for i, doc in enumerate(contexte['documents'][0]):
        print(f"  {i+1}. {doc}")
        print(f"     Métadonnées: {contexte['metadatas'][0][i]}")
        print(f"     Distance: {contexte['distances'][0][i]:.4f}")
    
    # Étape 6: Le contexte serait ensuite envoyé à un LLM pour générer la réponse
    print(f"\n# Le contexte ci-dessus serait maintenant envoyé à un LLM")
    print(f"# (comme GPT-4, Claude, etc.) pour générer une réponse complète")
    
    return collection

# Exécuter l'exemple de système RAG
if __name__ == "__main__":
    print("# ======= DÉMONSTRATION CHROMADB POUR RAG =======\n")
    systeme_rag_complet()
    print("\n# ======= FIN DE LA DÉMONSTRATION =======")

# ============================================================================
# 12. BONNES PRATIQUES POUR UN SYSTÈME RAG
# ============================================================================

"""
BONNES PRATIQUES:

1. PERSISTANCE:
   - Toujours utiliser PersistentClient en production
   - Faire des sauvegardes régulières du dossier de données

2. GESTION DES COLLECTIONS:
   - Utiliser get_or_create_collection pour éviter les erreurs
   - Organiser les documents par collections thématiques
   - Ajouter des métadonnées descriptives

3. MÉTADONNÉES:
   - Inclure: source, date, auteur, catégorie
   - Utiliser pour filtrer et affiner les recherches
   - Permet de tracer l'origine des informations

4. EMBEDDINGS:
   - Choisir le modèle adapté à votre langue/domaine
   - all-MiniLM-L6-v2: bon compromis vitesse/qualité
   - OpenAI: meilleure qualité mais coût
   - Garder le même modèle pour toute la collection

5. CHUNKING (découpage):
   - Découper les longs documents en morceaux de 200-500 mots
   - Garder le contexte dans les métadonnées
   - Éviter les chunks trop petits ou trop grands

6. RECHERCHE:
   - Ajuster n_results selon le besoin (3-5 généralement)
   - Utiliser where pour filtrer par métadonnées
   - Vérifier les distances pour évaluer la pertinence

7. MISE À JOUR:
   - Utiliser upsert pour les flux de données dynamiques
   - Mettre à jour régulièrement les documents obsolètes
   - Versionner vos données avec métadonnées

8. PERFORMANCE:
   - Limiter la taille des collections (< 1M documents)
   - Indexer par thématique si nécessaire
   - Utiliser offset/limit pour la pagination

9. SÉCURITÉ:
   - Ne jamais stocker d'informations sensibles non chiffrées
   - Valider les entrées utilisateur
   - Contrôler l'accès aux collections

10. MONITORING:
    - Logger les requêtes et performances
    - Surveiller la pertinence des résultats
    - Ajuster les paramètres selon les retours
"""

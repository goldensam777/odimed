# Historique des Agents (Agents Activity Log)

Ce fichier retrace les grandes étapes de développement et de refactoring réalisées par les agents sur le projet Odimed.

## Phase 1 : Nettoyage, Sécurité et Abstraction de Stockage

### 1. Refactoring du Stockage (Storage Layer)
- Création d'une couche d'abstraction de stockage dans `app/core/storage.py` (`save_file`, `delete_file`).
- Migration de toutes les opérations de fichiers (assets des médecins, templates) pour utiliser cette abstraction.
- Mise en place d'une structure hiérarchique stricte (`medecins/{id}/...`) pour anticiper une future migration vers un stockage objet (S3, Cloudflare R2) sans avoir à toucher au code métier.

### 2. Développement des Routes API Core
- Développement et sécurisation des routes pour :
  - **Médecins** : Gestion du profil et des assets (cachets, signatures).
  - **Templates** : Upload et gestion de modèles de documents.
  - **Patients** : Ajout de la fonctionnalité de création de patients "fantômes" (ghost patients) par les médecins.
  - **Ordonnances** : Création et gestion des ordonnances.

### 3. Sécurité et Contrôle d'Accès (RBAC)
- Création de la dépendance `CurrentMedecinDep` dans `app/api/deps.py`.
- Verrouillage des routes sensibles (comme la liste des patients ou la création d'ordonnances) pour qu'elles ne soient accessibles qu'aux utilisateurs ayant un profil médecin valide. Cela empêche les fuites de données de santé (ex: un utilisateur classique ne peut plus lister les patients).

### 4. Nettoyage du Template Initial
- Suppression complète du modèle `Item` par défaut du template FastAPI (CRUD, tests, routes API).
- Création d'une migration Alembic (`bbe578841664_remove_item_table.py`) pour supprimer proprement la table `item` de la base de données PostgreSQL.

### 5. Corrections de Bugs
- Résolution d'une erreur de syntaxe de compatibilité Python 2/3 (`except InvalidTokenError, ValidationError:`) dans `deps.py` qui empêchait le serveur de démarrer.

### 6. Tests et Qualité
- Couverture de test atteinte à **100%** sur les modules métiers principaux (52/52 tests passant avec succès via `uv run pytest`).

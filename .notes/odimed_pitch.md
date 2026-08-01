# Odimed — Pitch & Vision

## En une phrase

Odimed est une plateforme web qui permet aux médecins de générer des ordonnances numériques à partir de leur propre modèle personnalisé (Word), avec signature et cachet intégrés — et qui, à terme, connecte médecins, patients et pharmacies dans un même écosystème.

## Le problème

- Les ordonnances manuscrites sont souvent illisibles, source d'erreurs de dispensation en pharmacie
- Aucun historique centralisé et sécurisé des prescriptions d'un patient
- Les médecins n'ont pas d'outil simple pour digitaliser leur propre format d'ordonnance sans perdre leur identité professionnelle (en-tête, cachet, mise en page)
- Les patients cherchent des médecins sans repère fiable sur leurs compétences ou spécialités
- Les pharmacies n'ont aucune visibilité anticipée sur les prescriptions à venir

## Le concept central

Chaque médecin importe son propre template Word d'ordonnance, dans lequel il place des tokens (`$nom_patient$`, `$posologie$`, `$signature:img$`, `$cachet:img$`, etc.). Odimed détecte ces tokens et génère automatiquement l'ordonnance finale — en Word et en PDF — remplie avec les données de la consultation, signée et cachetée numériquement.

## Avantages par acteur

### Médecins
- Gain de temps réel sur la rédaction — plus besoin de retaper une ordonnance similaire à chaque fois
- Historique et traçabilité complets des ordonnances émises par patient
- Rendu visuel professionnel et cohérent à chaque prescription
- Mobilité : prescrire depuis n'importe où (visite à domicile, garde, déplacement)
- Un profil vérifié avec historique de prescriptions et publications peut servir de CV vivant pour des cliniques, ONG ou programmes de recrutement médical

### Patients
- Lisibilité garantie, fin des erreurs liées à une écriture illisible
- Accès à leur propre historique de prescriptions (second avis, changement de médecin, renouvellement)
- Orientation facilitée vers le bon type de consultation grâce à un futur assistant IA de pré-qualification
- Visibilité sur les pharmacies proches ayant les médicaments prescrits en stock

### Pharmaciens / pharmacies
- Réception anticipée de l'ordonnance numérique, préparation en amont de l'arrivée du patient
- Vérification automatique de l'authenticité (contre la falsification), l'ordonnance provenant d'un compte médecin vérifié
- Historique de dispensation lié au patient, utile pour repérer interactions médicamenteuses ou sur-prescriptions
- Meilleure gestion des stocks grâce à la visibilité sur la demande à venir

### Écosystème de santé
- Standardisation du format d'ordonnance à l'échelle d'un pays, voire au-delà
- Réduction de la fraude et de la falsification de documents médicaux
- Données agrégées et anonymisées exploitables comme signal de santé publique (médicaments les plus prescrits, par région, par diagnostic)
- Mise en réseau de tous les médecins d'un pays (et potentiellement du monde) sur une même plateforme

## Fonctionnalités prévues (roadmap)

**MVP**
- Upload de template Word personnalisé + détection automatique des tokens
- Génération d'ordonnance (Word + PDF) à partir des données saisies
- Upload de signature/cachet avec suppression automatique de l'arrière-plan
- Stockage des signatures/cachets récents, réutilisables sans re-upload
- Comptes médecins gérés par email

**Post-MVP**
- Créateur de cachets intégré (éditeur canvas)
- Base de données médicaments/molécules/diagnostics (autocomplétion à la saisie)
- Enregistrement audio de consultation avec récapitulatif généré par IA
- Profils patients et mise en relation directe avec des médecins
- Messagerie intégrée type WhatsApp
- Intégration pharmacies (réception anticipée d'ordonnance, disponibilité stock)
- Assistant IA d'orientation/pré-qualification pour les patients

## Stack technique (état actuel)

- Backend : template FastAPI full-stack (Sebastián Ramírez), géré avec `uv`
- Frontend : web (React envisagé)
- Base de données : PostgreSQL, architecture multi-tenant par médecin
- Repo : `odimed`

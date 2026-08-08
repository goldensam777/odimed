#!/bin/bash

# S'assure qu'on est à la racine du projet
cd "$(dirname "$0")"

echo "🚀 Lancement de l'écosystème Odimed (Mode Universel)..."

# Utilise 'npx concurrently' pour lancer les deux processus dans le même terminal
# avec des couleurs différentes pour bien distinguer les logs.
npx concurrently \
    -c "blue.bold,green.bold" \
    -n "BACKEND,FRONTEND" \
    "cd backend && uv run fastapi dev" \
    "cd frontend && npm run dev"

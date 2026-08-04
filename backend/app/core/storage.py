import os
from pathlib import Path

# Répertoire de base pour le stockage local (MVP)
BASE_STORAGE_DIR = Path("uploads")


def save_file(relative_path: str, content: bytes) -> str:
    """
    Sauvegarde un fichier binaire selon une clé/chemin relatif déterministe
    (ex: medecins/{medecin_id}/assets/signature/xyz.png).
    
    En local : écrit le fichier dans BASE_STORAGE_DIR / relative_path.
    En prod (Cloudflare R2) : enverra le fichier vers le bucket R2 sans toucher au code des routes !
    """
    full_path = BASE_STORAGE_DIR / relative_path
    full_path.parent.mkdir(parents=True, exist_ok=True)

    with open(full_path, "wb") as f:
        f.write(content)

    return relative_path


def delete_file(relative_path: str) -> bool:
    """
    Supprime un fichier stocké.
    """
    full_path = BASE_STORAGE_DIR / relative_path
    if full_path.exists():
        try:
            os.remove(full_path)
            return True
        except OSError:
            return False
    return False


def get_file_path(relative_path: str) -> str:
    """
    Retourne le chemin absolu/local du fichier pour lecture ou envoi HTTP.
    """
    full_path = BASE_STORAGE_DIR / relative_path
    return str(full_path.resolve())

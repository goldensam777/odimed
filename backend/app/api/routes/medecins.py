import os
import uuid
from typing import Annotated, Any

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from sqlmodel import select

from app.api.deps import CurrentUser, SessionDep
from app.models import (
    AssetMedecin,
    AssetMedecinPublic,
    ProfilMedecin,
    ProfilMedecinCreate,
    ProfilMedecinPublic,
    ProfilMedecinUpdate,
    TypeAsset,
)

router = APIRouter(prefix="/medecins", tags=["medecins"])

# Dossier d'upload pour les signatures et cachets
UPLOAD_DIR_ASSETS = "uploads/assets"


@router.get("/me", response_model=ProfilMedecinPublic)
def read_my_profil(session: SessionDep, current_user: CurrentUser) -> Any:
    """
    Récupérer le profil médecin de l'utilisateur connecté.
    """
    statement = select(ProfilMedecin).where(ProfilMedecin.user_id == current_user.id)
    profil = session.exec(statement).first()
    if not profil:
        raise HTTPException(
            status_code=404, detail="Profil médecin introuvable pour cet utilisateur."
        )
    return profil


@router.post("/me", response_model=ProfilMedecinPublic)
def create_my_profil(
    *, session: SessionDep, current_user: CurrentUser, profil_in: ProfilMedecinCreate
) -> Any:
    """
    Créer le profil médecin pour l'utilisateur connecté.
    """
    statement = select(ProfilMedecin).where(ProfilMedecin.user_id == current_user.id)
    existing_profil = session.exec(statement).first()
    if existing_profil:
        raise HTTPException(
            status_code=400, detail="Un profil médecin existe déjà pour cet utilisateur."
        )

    # Vérifier l'unicité du numéro d'ordre
    statement_ordre = select(ProfilMedecin).where(
        ProfilMedecin.numero_ordre == profil_in.numero_ordre
    )
    if session.exec(statement_ordre).first():
        raise HTTPException(
            status_code=400, detail="Ce numéro d'ordre est déjà utilisé."
        )

    profil = ProfilMedecin(
        user_id=current_user.id,
        numero_ordre=profil_in.numero_ordre,
        specialite=profil_in.specialite,
        pays_exercice=profil_in.pays_exercice,
        bio=profil_in.bio,
    )
    session.add(profil)
    session.commit()
    session.refresh(profil)
    return profil


@router.patch("/me", response_model=ProfilMedecinPublic)
def update_my_profil(
    *, session: SessionDep, current_user: CurrentUser, profil_in: ProfilMedecinUpdate
) -> Any:
    """
    Mettre à jour le profil médecin de l'utilisateur connecté.
    """
    statement = select(ProfilMedecin).where(ProfilMedecin.user_id == current_user.id)
    profil = session.exec(statement).first()
    if not profil:
        raise HTTPException(
            status_code=404, detail="Profil médecin introuvable."
        )

    update_data = profil_in.model_dump(exclude_unset=True)
    profil.sqlmodel_update(update_data)
    session.add(profil)
    session.commit()
    session.refresh(profil)
    return profil


@router.post("/me/assets", response_model=AssetMedecinPublic)
def upload_asset(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    type_asset: Annotated[TypeAsset, Form(...)],
    file: Annotated[UploadFile, File(...)],
    est_par_defaut: Annotated[bool, Form()] = False,
) -> Any:
    """
    Uploader une image de signature ou de cachet pour le médecin connecté.
    """
    statement = select(ProfilMedecin).where(ProfilMedecin.user_id == current_user.id)
    profil = session.exec(statement).first()
    if not profil:
        raise HTTPException(
            status_code=400,
            detail="Vous devez créer un profil médecin avant d'uploader une signature ou un cachet.",
        )

    file_ext = os.path.splitext(file.filename or "")[1] or ".png"
    filename = f"{uuid.uuid4().hex[:8]}{file_ext}"
    relative_path = f"medecins/{profil.id}/assets/{type_asset.value}/{filename}"

    from app.core import storage
    saved_path = storage.save_file(relative_path, file.file.read())

    # Si c'est l'asset par défaut, décocher les précédents de même type
    if est_par_defaut:
        existing_assets = session.exec(
            select(AssetMedecin).where(
                AssetMedecin.medecin_id == profil.id,
                AssetMedecin.type_asset == type_asset,
            )
        ).all()
        for ass in existing_assets:
            ass.est_par_defaut = False
            session.add(ass)

    asset = AssetMedecin(
        medecin_id=profil.id,
        type_asset=type_asset,
        chemin_fichier=saved_path,
        est_par_defaut=est_par_defaut,
    )
    session.add(asset)
    session.commit()
    session.refresh(asset)
    return asset



@router.get("/me/assets", response_model=list[AssetMedecinPublic])
def list_my_assets(
    session: SessionDep,
    current_user: CurrentUser,
    type_asset: TypeAsset | None = None,
) -> Any:
    """
    Lister les signatures et cachets récents uploadés par le médecin connecté.
    """
    statement = select(ProfilMedecin).where(ProfilMedecin.user_id == current_user.id)
    profil = session.exec(statement).first()
    if not profil:
        return []

    statement_asset = select(AssetMedecin).where(AssetMedecin.medecin_id == profil.id)
    if type_asset:
        statement_asset = statement_asset.where(AssetMedecin.type_asset == type_asset)
    statement_asset = statement_asset.order_by(AssetMedecin.created_at.desc())
    assets = session.exec(statement_asset).all()
    return assets


from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.api.deps import CurrentMedecinDep, CurrentUser, SessionDep
from app.models import (
    ProfilPatient,
    ProfilPatientCreate,
    ProfilPatientPublic,
)

router = APIRouter(prefix="/patients", tags=["patients"])


@router.get("/me", response_model=ProfilPatientPublic)
def read_my_patient_profil(session: SessionDep, current_user: CurrentUser) -> Any:
    """
    Récupérer le profil patient de l'utilisateur connecté.
    """
    statement = select(ProfilPatient).where(ProfilPatient.user_id == current_user.id)
    profil = session.exec(statement).first()
    if not profil:
        raise HTTPException(
            status_code=404, detail="Profil patient introuvable pour cet utilisateur."
        )
    return profil


@router.post("/me", response_model=ProfilPatientPublic)
def create_my_patient_profil(
    *, session: SessionDep, current_user: CurrentUser, profil_in: ProfilPatientCreate
) -> Any:
    """
    Créer le profil patient pour l'utilisateur connecté.
    """
    statement = select(ProfilPatient).where(ProfilPatient.user_id == current_user.id)
    existing_profil = session.exec(statement).first()
    if existing_profil:
        raise HTTPException(
            status_code=400, detail="Un profil patient existe déjà pour cet utilisateur."
        )

    profil = ProfilPatient(
        user_id=current_user.id,
        date_naissance=profil_in.date_naissance,
        antecedents=profil_in.antecedents,
    )
    session.add(profil)
    session.commit()
    session.refresh(profil)
    return profil


@router.post("/fantome", response_model=ProfilPatientPublic)
def create_ghost_patient_profil(
    *,
    session: SessionDep,
    current_medecin: CurrentMedecinDep,
    profil_in: ProfilPatientCreate,
) -> Any:
    """
    Créer un profil patient 'fantôme' (non encore inscrit) par un médecin pour une consultation.
    """
    profil = ProfilPatient(
        user_id=None,  # Profil non réclamé
        date_naissance=profil_in.date_naissance,
        antecedents=profil_in.antecedents,
    )
    session.add(profil)
    session.commit()
    session.refresh(profil)
    return profil


@router.get("/", response_model=list[ProfilPatientPublic])
def search_patients(
    session: SessionDep,
    current_medecin: CurrentMedecinDep,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Lister ou rechercher des patients (réservé exclusivement aux médecins authentifiés).
    """
    statement = select(ProfilPatient).offset(skip).limit(limit)
    patients = session.exec(statement).all()
    return patients



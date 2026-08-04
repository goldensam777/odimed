import secrets
import string
import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import col, func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import (
    Ordonnance,
    OrdonnanceCreate,
    OrdonnancePublic,
    OrdonnancesPublic,
    ProfilMedecin,
)

router = APIRouter(prefix="/ordonnances", tags=["ordonnances"])


def generate_lien_token(length: int = 8) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


@router.get("/", response_model=OrdonnancesPublic)
def read_ordonnances(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Récupérer les ordonnances du médecin connecté (ou toutes si superuser).
    """
    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Ordonnance)
        count = session.exec(count_statement).one()
        statement = (
            select(Ordonnance)
            .order_by(col(Ordonnance.date_emission).desc())
            .offset(skip)
            .limit(limit)
        )
        ordonnances = session.exec(statement).all()
    else:
        # Trouver le profil médecin associé à l'utilisateur
        statement_medecin = select(ProfilMedecin).where(ProfilMedecin.user_id == current_user.id)
        profil_medecin = session.exec(statement_medecin).first()
        if not profil_medecin:
            return OrdonnancesPublic(data=[], count=0)

        count_statement = (
            select(func.count())
            .select_from(Ordonnance)
            .where(Ordonnance.medecin_id == profil_medecin.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Ordonnance)
            .where(Ordonnance.medecin_id == profil_medecin.id)
            .order_by(col(Ordonnance.date_emission).desc())
            .offset(skip)
            .limit(limit)
        )
        ordonnances = session.exec(statement).all()

    ordonnances_public = [OrdonnancePublic.model_validate(ord_obj) for ord_obj in ordonnances]
    return OrdonnancesPublic(data=ordonnances_public, count=count)


@router.get("/{id}", response_model=OrdonnancePublic)
def read_ordonnance(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Récupérer une ordonnance par son ID.
    """
    ordonnance = session.get(Ordonnance, id)
    if not ordonnance:
        raise HTTPException(status_code=404, detail="Ordonnance introuvable")

    if not current_user.is_superuser:
        statement_medecin = select(ProfilMedecin).where(ProfilMedecin.user_id == current_user.id)
        profil_medecin = session.exec(statement_medecin).first()
        if not profil_medecin or ordonnance.medecin_id != profil_medecin.id:
            raise HTTPException(status_code=403, detail="Permissions insuffisantes")

    return ordonnance


@router.post("/", response_model=OrdonnancePublic)
def create_ordonnance(
    *, session: SessionDep, current_user: CurrentUser, ordonnance_in: OrdonnanceCreate
) -> Any:
    """
    Créer une nouvelle ordonnance.
    """
    statement_medecin = select(ProfilMedecin).where(ProfilMedecin.user_id == current_user.id)
    profil_medecin = session.exec(statement_medecin).first()
    if not profil_medecin:
        raise HTTPException(
            status_code=400,
            detail="Un profil médecin actif est obligatoire pour émettre une ordonnance.",
        )

    ordonnance = Ordonnance(
        medecin_id=profil_medecin.id,
        patient_id=ordonnance_in.patient_id,
        template_id=ordonnance_in.template_id,
        lien_token=generate_lien_token(),
    )
    session.add(ordonnance)
    session.commit()
    session.refresh(ordonnance)
    return ordonnance


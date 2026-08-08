import secrets
import string
import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import SQLModel, col, func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import (
    Ordonnance,
    OrdonnanceCreate,
    OrdonnancePublic,
    OrdonnancesPublic,
    ProfilMedecin,
    StatutOrdonnance,
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


@router.get("/{id}/pdf")
def get_ordonnance_pdf(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Télécharger le fichier PDF de l'ordonnance.
    """
    from fastapi.responses import FileResponse

    from app.core.storage import get_file_path

    ordonnance = session.get(Ordonnance, id)
    if not ordonnance:
        raise HTTPException(status_code=404, detail="Ordonnance introuvable")

    # Permissions check (superuser or the doctor who created it)
    if not current_user.is_superuser:
        statement_medecin = select(ProfilMedecin).where(ProfilMedecin.user_id == current_user.id)
        profil_medecin = session.exec(statement_medecin).first()
        if not profil_medecin or ordonnance.medecin_id != profil_medecin.id:
            raise HTTPException(status_code=403, detail="Permissions insuffisantes")

    if not ordonnance.pdf_name:
        raise HTTPException(status_code=404, detail="Le PDF de cette ordonnance n'a pas encore été généré")

    pdf_path = f"medecins/{ordonnance.medecin_id}/ordonnances/{ordonnance.pdf_name}"
    abs_path = get_file_path(pdf_path)

    import os
    if not os.path.exists(abs_path):
        raise HTTPException(status_code=404, detail="Fichier PDF introuvable sur le disque")

    return FileResponse(abs_path, media_type="application/pdf", filename=ordonnance.pdf_name)


class OrdonnanceGenerateRequest(SQLModel):
    html_content: str
    patient_id: uuid.UUID | None = None
    template_id: uuid.UUID | None = None
    paper_size: str = "A4"


@router.post("/generate", response_model=OrdonnancePublic)
def generate_ordonnance(
    *, session: SessionDep, current_user: CurrentUser, req: OrdonnanceGenerateRequest
) -> Any:
    """
    Génère un PDF à partir de contenu HTML, remplace les tokens, le sauvegarde et crée l'ordonnance.
    """
    from datetime import datetime

    from app.core.pdf import generate_pdf_from_html
    from app.core.storage import save_file
    from app.models import OrdonnanceTemplate, ProfilPatient, User

    # 1. Vérifier le médecin
    statement_medecin = select(ProfilMedecin).where(ProfilMedecin.user_id == current_user.id)
    profil_medecin = session.exec(statement_medecin).first()
    if not profil_medecin:
        raise HTTPException(
            status_code=400,
            detail="Un profil médecin actif est obligatoire pour émettre une ordonnance.",
        )

    # 2. Récupérer les données pour remplacer les tokens
    # Fallback pour le MVP si patient ou template non sélectionné
    patient_id = req.patient_id
    if not patient_id:
        first_patient = session.exec(select(ProfilPatient)).first()
        if not first_patient:
            # Créer un patient fantôme de test
            first_patient = ProfilPatient()
            session.add(first_patient)
            session.commit()
            session.refresh(first_patient)
        patient_id = first_patient.id

    template_id = req.template_id
    if not template_id:
        first_template = session.exec(select(OrdonnanceTemplate)).first()
        if not first_template:
            # Créer un template par défaut
            first_template = OrdonnanceTemplate(
                medecin_id=profil_medecin.id,
                nom_modele="Modèle par défaut",
                contenu_html=""
            )
            session.add(first_template)
            session.commit()
            session.refresh(first_template)
        template_id = first_template.id

    patient = session.get(ProfilPatient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient introuvable")

    patient_name = "Patient Inconnu"
    if patient.user_id:
        patient_user = session.get(User, patient.user_id)
        if patient_user and patient_user.full_name:
            patient_name = patient_user.full_name

    # 3. Moteur de remplacement de tokens extensible
    import base64
    import re

    from app.core.storage import get_file_path

    # Dictionnaire des valeurs textuelles disponibles
    text_context = {
        "medecin_nom": current_user.full_name or "",
        "medecin_specialite": profil_medecin.specialite or "",
        "medecin_ordre": profil_medecin.numero_ordre or "",
        "patient_nom": patient_name,
        "date_jour": datetime.now().strftime("%d/%m/%Y"),
    }

    # Dictionnaire des assets (images) du médecin (clé = type_asset, valeur = chemin_absolu)
    image_context = {}
    for asset in profil_medecin.assets:
        # En cas de doublons (plusieurs signatures), on pourrait filtrer sur 'est_par_defaut'
        # Pour l'instant, on prend le dernier itéré
        try:
            image_context[asset.type_asset.value] = get_file_path(asset.chemin_fichier)
        except Exception:
            pass

    def token_replacer(match):
        key = match.group(1)
        modifier = match.group(2) # peut être ":img" ou None

        if modifier == ":img":
            # C'est une demande d'image (ex: $signature:img$)
            img_path = image_context.get(key)
            if img_path:
                try:
                    with open(img_path, "rb") as img_file:
                        b64_str = base64.b64encode(img_file.read()).decode("utf-8")
                        return f'<img src="data:image/png;base64,{b64_str}" style="max-height: 120px; object-fit: contain;" />'
                except Exception:
                    return "" # Fichier illisible
            return "" # Asset non trouvé
        else:
            # C'est une demande de texte (ex: $patient_nom$)
            return text_context.get(key, match.group(0)) # Retourne le texte ou le token d'origine si inconnu

    # Pattern: $clef$ ou $clef:img$
    # match.group(1) -> clef
    # match.group(2) -> :img (optionnel)
    html_content = req.html_content
    pattern = re.compile(r"\$([a-zA-Z0-9_]+)(:img)?\$")
    html_content = pattern.sub(token_replacer, html_content)

    # 4. Créer l'Ordonnance en base (pour avoir un ID)
    ordonnance = Ordonnance(
        medecin_id=profil_medecin.id,
        patient_id=patient_id,
        template_id=template_id,
        lien_token=generate_lien_token(),
        statut=StatutOrdonnance.signee,
        date_signature=datetime.now(),
    )
    session.add(ordonnance)
    session.commit()
    session.refresh(ordonnance)

    # 5. Générer le PDF
    pdf_bytes = generate_pdf_from_html(html_content, paper_size=req.paper_size)

    # 6. Sauvegarder le PDF
    pdf_path = f"medecins/{profil_medecin.id}/ordonnances/{ordonnance.id}.pdf"
    save_file(pdf_path, pdf_bytes)

    # 7. Mettre à jour l'ordonnance avec le nom du fichier
    ordonnance.pdf_name = f"{ordonnance.id}.pdf"
    session.add(ordonnance)
    session.commit()
    session.refresh(ordonnance)

    return ordonnance


import uuid
from datetime import UTC, date, datetime
from enum import Enum

from pydantic import EmailStr
from sqlalchemy import DateTime
from sqlmodel import Field, Relationship, SQLModel


def get_datetime_utc() -> datetime:
    return datetime.now(UTC)


# ============================================================
# Enums
# ============================================================

class TypeUtilisateur(str, Enum):
    medecin = "medecin"
    patient = "patient"
    pharmacien = "pharmacien"


class TypeAsset(str, Enum):
    signature = "signature"
    cachet = "cachet"


class StatutOrdonnance(str, Enum):
    brouillon = "brouillon"
    signee = "signee"
    preparee = "preparee"
    dispensee = "dispensee"
    annulee = "annulee"


# ============================================================
# User (du template, étendu avec le rôle odimed)
# ============================================================

# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False  # -> gère l'accès admin (ex: base médicaments/diagnostics)
    full_name: str | None = Field(default=None, max_length=255)
    type_utilisateur: TypeUtilisateur | None = Field(default=None, index=True)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(default=None, max_length=255)
    type_utilisateur: TypeUtilisateur | None = Field(default=None)


# Properties to receive via API on update, all are optional
class UserUpdate(SQLModel):
    email: EmailStr | None = Field(default=None, max_length=255)
    is_active: bool | None = None
    is_superuser: bool | None = None
    full_name: str | None = Field(default=None, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=128)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    items: list[Item] = Relationship(back_populates="owner", cascade_delete=True)
    profil_medecin: ProfilMedecin = Relationship(back_populates="user", cascade_delete=True)
    profil_patient: ProfilPatient = Relationship(back_populates="user", cascade_delete=True)
    profil_pharmacien: ProfilPharmacien = Relationship(back_populates="user", cascade_delete=True)


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID
    created_at: datetime | None = None


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# ============================================================
# Item (démo du template, à retirer plus tard si inutile)
# ============================================================

class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


class ItemCreate(ItemBase):
    pass


class ItemUpdate(SQLModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")


class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    created_at: datetime | None = None


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# ============================================================
# ProfilMedecin
# ============================================================

class ProfilMedecinBase(SQLModel):
    numero_ordre: str = Field(unique=True, index=True, max_length=64)
    specialite: str = Field(max_length=255)
    pays_exercice: str = Field(max_length=100)
    bio: str | None = Field(default=None, max_length=2000)
    est_verifie: bool = False


class ProfilMedecinCreate(ProfilMedecinBase):
    pass


class ProfilMedecinUpdate(SQLModel):
    specialite: str | None = Field(default=None, max_length=255)
    bio: str | None = Field(default=None, max_length=2000)
    est_verifie: bool | None = None


class ProfilMedecin(ProfilMedecinBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, unique=True, ondelete="CASCADE")

    user: User | None = Relationship(back_populates="profil_medecin")
    assets: list[AssetMedecin] = Relationship(back_populates="medecin", cascade_delete=True)
    templates: list[OrdonnanceTemplate] = Relationship(back_populates="medecin", cascade_delete=True)
    ordonnances: list[Ordonnance] = Relationship(back_populates="medecin")


class ProfilMedecinPublic(ProfilMedecinBase):
    id: uuid.UUID
    user_id: uuid.UUID


# ============================================================
# ProfilPatient (peut être "fantôme", non rattaché à un User)
# ============================================================

class ProfilPatientBase(SQLModel):
    date_naissance: date | None = None
    antecedents: str | None = Field(default=None, max_length=2000)


class ProfilPatientCreate(ProfilPatientBase):
    pass


class ProfilPatientUpdate(SQLModel):
    date_naissance: date | None = None
    antecedents: str | None = Field(default=None, max_length=2000)


class ProfilPatient(ProfilPatientBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    # nullable: profil "fantôme" créé quand un médecin saisit un patient non inscrit
    user_id: uuid.UUID | None = Field(
        default=None, foreign_key="user.id", unique=True, ondelete="CASCADE"
    )

    user: User | None = Relationship(back_populates="profil_patient")
    ordonnances: list[Ordonnance] = Relationship(back_populates="patient")


class ProfilPatientPublic(ProfilPatientBase):
    id: uuid.UUID
    user_id: uuid.UUID | None


# ============================================================
# Officine + garde
# ============================================================

class OfficineBase(SQLModel):
    nom_officine: str = Field(max_length=255)
    adresse: str = Field(max_length=500)
    latitude: float | None = None
    longitude: float | None = None


class OfficineCreate(OfficineBase):
    pass


class OfficineUpdate(SQLModel):
    nom_officine: str | None = Field(default=None, max_length=255)
    adresse: str | None = Field(default=None, max_length=500)
    latitude: float | None = None
    longitude: float | None = None


class Officine(OfficineBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    pharmaciens: list[ProfilPharmacien] = Relationship(back_populates="officine")
    gardes: list[GardeOfficine] = Relationship(back_populates="officine", cascade_delete=True)


class OfficinePublic(OfficineBase):
    id: uuid.UUID


class GardeOfficineBase(SQLModel):
    debut_garde: datetime = Field(sa_type=DateTime(timezone=True))  # type: ignore
    fin_garde: datetime = Field(sa_type=DateTime(timezone=True))  # type: ignore


class GardeOfficineCreate(GardeOfficineBase):
    officine_id: uuid.UUID


class GardeOfficine(GardeOfficineBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    officine_id: uuid.UUID = Field(foreign_key="officine.id", nullable=False, ondelete="CASCADE")

    officine: Officine | None = Relationship(back_populates="gardes")


class GardeOfficinePublic(GardeOfficineBase):
    id: uuid.UUID
    officine_id: uuid.UUID


# ============================================================
# ProfilPharmacien
# ============================================================

class ProfilPharmacienBase(SQLModel):
    numero_licence: str = Field(unique=True, index=True, max_length=64)
    est_verifie: bool = False


class ProfilPharmacienCreate(ProfilPharmacienBase):
    officine_id: uuid.UUID | None = None


class ProfilPharmacienUpdate(SQLModel):
    officine_id: uuid.UUID | None = None
    est_verifie: bool | None = None


class ProfilPharmacien(ProfilPharmacienBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, unique=True, ondelete="CASCADE")
    officine_id: uuid.UUID | None = Field(default=None, foreign_key="officine.id")

    user: User | None = Relationship(back_populates="profil_pharmacien")
    officine: Officine | None = Relationship(back_populates="pharmaciens")


class ProfilPharmacienPublic(ProfilPharmacienBase):
    id: uuid.UUID
    user_id: uuid.UUID
    officine_id: uuid.UUID | None


# ============================================================
# AssetMedecin (signature / cachet)
# ============================================================

class AssetMedecinBase(SQLModel):
    type_asset: TypeAsset
    chemin_fichier: str = Field(max_length=500)
    est_par_defaut: bool = False


class AssetMedecinCreate(AssetMedecinBase):
    pass


class AssetMedecin(AssetMedecinBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    medecin_id: uuid.UUID = Field(foreign_key="profilmedecin.id", nullable=False, ondelete="CASCADE")
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )

    medecin: ProfilMedecin | None = Relationship(back_populates="assets")


class AssetMedecinPublic(AssetMedecinBase):
    id: uuid.UUID
    medecin_id: uuid.UUID
    created_at: datetime | None = None


# ============================================================
# OrdonnanceTemplate
# ============================================================

class OrdonnanceTemplateBase(SQLModel):
    nom_template: str = Field(max_length=255)
    chemin_fichier_docx: str = Field(max_length=500)


class OrdonnanceTemplateCreate(OrdonnanceTemplateBase):
    pass


class OrdonnanceTemplate(OrdonnanceTemplateBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    medecin_id: uuid.UUID = Field(foreign_key="profilmedecin.id", nullable=False, ondelete="CASCADE")
    date_upload: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )

    medecin: ProfilMedecin | None = Relationship(back_populates="templates")
    ordonnances: list[Ordonnance] = Relationship(back_populates="template")


class OrdonnanceTemplatePublic(OrdonnanceTemplateBase):
    id: uuid.UUID
    medecin_id: uuid.UUID
    date_upload: datetime | None = None


# ============================================================
# Ordonnance
# ============================================================

class OrdonnanceBase(SQLModel):
    pdf_name: str | None = Field(default=None, max_length=255)
    docx_name: str | None = Field(default=None, max_length=255)
    statut: StatutOrdonnance = StatutOrdonnance.brouillon


class OrdonnanceCreate(SQLModel):
    patient_id: uuid.UUID
    template_id: uuid.UUID


class OrdonnanceUpdate(SQLModel):
    statut: StatutOrdonnance | None = None
    date_signature: datetime | None = None


class Ordonnance(OrdonnanceBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    medecin_id: uuid.UUID = Field(foreign_key="profilmedecin.id", nullable=False, ondelete="CASCADE")
    patient_id: uuid.UUID = Field(foreign_key="profilpatient.id", nullable=False)
    template_id: uuid.UUID = Field(foreign_key="ordonnancetemplate.id", nullable=False)
    date_emission: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    date_signature: datetime | None = Field(default=None, sa_type=DateTime(timezone=True))  # type: ignore
    # identifiant court unique pour le lien de partage sans compte (ex: odi.med/X5R9)
    lien_token: str = Field(unique=True, index=True, max_length=16)

    medecin: ProfilMedecin | None = Relationship(back_populates="ordonnances")
    patient: ProfilPatient | None = Relationship(back_populates="ordonnances")
    template: OrdonnanceTemplate | None = Relationship(back_populates="ordonnances")
    lignes: list[OrdonnanceLigne] = Relationship(back_populates="ordonnance", cascade_delete=True)


class OrdonnancePublic(OrdonnanceBase):
    id: uuid.UUID
    medecin_id: uuid.UUID
    patient_id: uuid.UUID
    template_id: uuid.UUID
    date_emission: datetime | None = None
    date_signature: datetime | None = None
    lien_token: str


class OrdonnancesPublic(SQLModel):
    data: list[OrdonnancePublic]
    count: int



# ============================================================
# Référentiel médicaments / diagnostics
# ============================================================

class MoleculeBase(SQLModel):
    nom_molecule: str = Field(unique=True, index=True, max_length=255)


class Molecule(MoleculeBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    medicaments: list[Medicament] = Relationship(back_populates="molecule")


class MoleculePublic(MoleculeBase):
    id: uuid.UUID


class MedicamentDiagnostic(SQLModel, table=True):
    # table de jonction many-to-many (doit être définie avant Medicament/Diagnostic
    # qui la référencent toutes les deux via link_model)
    medicament_id: uuid.UUID = Field(foreign_key="medicament.id", primary_key=True, ondelete="CASCADE")
    diagnostic_id: uuid.UUID = Field(foreign_key="diagnostic.id", primary_key=True, ondelete="CASCADE")


class MedicamentBase(SQLModel):
    nom_officiel: str = Field(max_length=255, index=True)
    forme: str | None = Field(default=None, max_length=100)
    dosage: str | None = Field(default=None, max_length=100)


class MedicamentCreate(MedicamentBase):
    molecule_id: uuid.UUID | None = None
    diagnostic_ids: list[uuid.UUID] = []


class Medicament(MedicamentBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    molecule_id: uuid.UUID | None = Field(default=None, foreign_key="molecule.id")

    molecule: Molecule | None = Relationship(back_populates="medicaments")
    diagnostics: list[Diagnostic] = Relationship(
        back_populates="medicaments", link_model=MedicamentDiagnostic
    )
    lignes_ordonnance: list[OrdonnanceLigne] = Relationship(back_populates="medicament")


class MedicamentPublic(MedicamentBase):
    id: uuid.UUID
    molecule_id: uuid.UUID | None


class DiagnosticBase(SQLModel):
    description: str = Field(max_length=500)
    code_cim10: str | None = Field(default=None, max_length=16, index=True)


class Diagnostic(DiagnosticBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    medicaments: list[Medicament] = Relationship(
        back_populates="diagnostics", link_model=MedicamentDiagnostic
    )


class DiagnosticPublic(DiagnosticBase):
    id: uuid.UUID


# ============================================================
# OrdonnanceLigne
# ============================================================

class OrdonnanceLigneBase(SQLModel):
    posologie: str = Field(max_length=500)
    duree_traitement: str | None = Field(default=None, max_length=100)


class OrdonnanceLigneCreate(OrdonnanceLigneBase):
    medicament_id: uuid.UUID


class OrdonnanceLigne(OrdonnanceLigneBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    ordonnance_id: uuid.UUID = Field(foreign_key="ordonnance.id", nullable=False, ondelete="CASCADE")
    medicament_id: uuid.UUID = Field(foreign_key="medicament.id", nullable=False)

    ordonnance: Ordonnance | None = Relationship(back_populates="lignes")
    medicament: Medicament | None = Relationship(back_populates="lignes_ordonnance")


class OrdonnanceLignePublic(OrdonnanceLigneBase):
    id: uuid.UUID
    ordonnance_id: uuid.UUID
    medicament_id: uuid.UUID


# ============================================================
# Generic / Auth (du template, inchangé)
# ============================================================

class Message(SQLModel):
    message: str


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)

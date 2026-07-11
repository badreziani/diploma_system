import os
import base64
import io
import pandas as pd
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.database import get_db
from app.db.models import (
    DiplomaBatch,
    Student,
    AcademicRecord,
    DiplomaType,
    Diplome,
    Departement,
    Filiere,
    Parcours,
)
from app.services.data_processor import process_excel_files

router = APIRouter()


# --- SCHÉMAS DE DONNÉES POUR LA SAISIE MANUELLE (PYDANTIC) ---
class DepartementSchema(BaseModel):
    id: Optional[int] = None
    intitule_fr: str
    intitule_ar: str


class FiliereSchema(BaseModel):
    id: Optional[int] = None
    code: str
    intitule_fr: str
    intitule_ar: str
    departement_id: int
    diplome_id: int


class ParcoursSchema(BaseModel):
    id: Optional[int] = None
    code: str
    intitule_fr: str
    intitule_ar: str
    filiere_id: int
    diplome_id: int


# =========================================================================
# 1. ROUTES CRUD : LECTURE ET SAISIE DES COMPOSANTES DE LA STRUCTURE
# =========================================================================


@router.get("/structure/")
def get_full_academic_structure(db: Session = Depends(get_db)):
    """Récupère l'ensemble des données de structure pour alimenter le Dashboard."""
    diplomes = db.query(Diplome).all()
    departements = db.query(Departement).all()
    filieres = db.query(Filiere).all()
    parcours = db.query(Parcours).all()

    return {
        "diplomes": [
            {"id": d.id, "intitule_fr": d.intitule_fr, "intitule_ar": d.intitule_ar}
            for d in diplomes
        ],
        "departements": [
            {"id": d.id, "intitule_fr": d.intitule_fr, "intitule_ar": d.intitule_ar}
            for d in departements
        ],
        "filieres": [
            {
                "id": f.id,
                "code": f.code,
                "intitule_fr": f.intitule_fr,
                "intitule_ar": f.intitule_ar,
                "departement_id": f.departement_id,
                "diplome_id": f.diplome_id,
            }
            for f in filieres
        ],
        "parcours": [
            {
                "id": p.id,
                "code": p.code,
                "intitule_fr": p.intitule_fr,
                "intitule_ar": p.intitule_ar,
                "filiere_id": p.filiere_id,
                "diplome_id": p.diplome_id,
            }
            for p in parcours
        ],
    }


@router.post("/manage-departement/")
def save_or_update_departement(
    payload: DepartementSchema, db: Session = Depends(get_db)
):
    if payload.id:  # Modification
        dept = db.query(Departement).filter(Departement.id == payload.id).first()
        if not dept:
            raise HTTPException(status_code=404, detail="Département introuvable")
        dept.intitule_fr = payload.intitule_fr
        dept.intitule_ar = payload.intitule_ar
    else:  # Création
        dept = Departement(
            intitule_fr=payload.intitule_fr, intitule_ar=payload.intitule_ar
        )
        db.add(dept)
    db.commit()
    return {"status": "success", "message": "Département enregistré avec succès"}


@router.post("/manage-filiere/")
def save_or_update_filiere(payload: FiliereSchema, db: Session = Depends(get_db)):
    try:
        if payload.id:  # Modification
            filiere = db.query(Filiere).filter(Filiere.id == payload.id).first()
            if not filiere:
                raise HTTPException(status_code=404, detail="Filière introuvable")
            filiere.code = payload.code
            filiere.intitule_fr = payload.intitule_fr
            filiere.intitule_ar = payload.intitule_ar
            filiere.departement_id = payload.departement_id
            filiere.diplome_id = payload.diplome_id
        else:  # Création
            filiere = Filiere(
                code=payload.code,
                intitule_fr=payload.intitule_fr,
                intitule_ar=payload.intitule_ar,
                departement_id=payload.departement_id,
                diplome_id=payload.diplome_id,
            )
            db.add(filiere)
        db.commit()
        return {"status": "success", "message": "Filière enregistrée avec succès"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Ce code de filière existe déjà.")


@router.post("/manage-parcours/")
def save_or_update_parcours(payload: ParcoursSchema, db: Session = Depends(get_db)):
    try:
        if payload.id:  # Modification
            parc = db.query(Parcours).filter(Parcours.id == payload.id).first()
            if not parc:
                raise HTTPException(status_code=404, detail="Parcours introuvable")
            parc.code = payload.code
            parc.intitule_fr = payload.intitule_fr
            parc.intitule_ar = payload.intitule_ar
            parc.filiere_id = payload.filiere_id
            parc.diplome_id = payload.diplome_id
        else:  # Création
            parc = Parcours(
                code=payload.code,
                intitule_fr=payload.intitule_fr,
                intitule_ar=payload.intitule_ar,
                filiere_id=payload.filiere_id,
                diplome_id=payload.diplome_id,
            )
            db.add(parc)
        db.commit()
        return {"status": "success", "message": "Parcours enregistré avec succès"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Ce code de parcours existe déjà.")


# =========================================================================
# 2. ANCIENNES ROUTES : IMPORT ARCHITECTURE EXCEL ET RECHERCHE DASHBOARD
# =========================================================================

# ... [Laissez ici vos routes existantes : /upload-filieres/, /upload-data/ et /search/] ...
# (Elles restent 100% compatibles et fonctionnelles)

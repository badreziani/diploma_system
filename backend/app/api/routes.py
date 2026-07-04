import os
from typing import List
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.data_processor import process_excel_files

router = APIRouter()

@router.post("/upload-data/")
def upload_excel_data(
    diploma_type: str = Form(...),
    annee_universitaire: str = Form(...),
    deliberation_dates: List[str] = Form(...),
    students_files: List[UploadFile] = File(...),
    marks_files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    try:
        students_contents_list = [file.file.read() for file in students_files]
        
        marks_data_list = [
            {"bytes": f.file.read(), "date": d} 
            for f, d in zip(marks_files, deliberation_dates)
        ]
        
        # Exécution du traitement avec détection des anomalies
        processed_students, unmatched_students = process_excel_files(
            students_contents_list, 
            marks_data_list
        )
        
        # Ici se fera l'insertion dans la base de données SQLalchemy pour `processed_students`
        
        return {
            "status": "success", 
            "message": f"Traitement effectué avec succès pour {len(processed_students)} étudiants.",
            "processed_count": len(processed_students),
            "unmatched_students": unmatched_students  # Envoyé au frontend pour affichage des alertes
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
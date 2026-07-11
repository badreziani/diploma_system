import enum
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

# ==========================================
# 0. ÉNUMÉRATIONS ET LOTS
# ==========================================
class DiplomaType(str, enum.Enum):
    DEUG = "DEUG"
    LICENCE = "Licence"
    LICENCE_FONDAMENTALE = "Licence Fondamentale"
    LICENCE_EXCELLENCE = "Licence d'Excellence"
    MASTER = "Master"
    MASTER_SPECIALISE = "Master Spécialisé"
    MASTER_EXCELLENCE = "Master Excellence"

class DiplomaBatch(Base):
    __tablename__ = "diploma_batches"
    
    id = Column(Integer, primary_key=True, index=True)
    diploma_type = Column(SQLEnum(DiplomaType), index=True)
    annee_universitaire = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    records = relationship("AcademicRecord", back_populates="batch", cascade="all, delete-orphan")


# ==========================================
# 1. TABLE DES DIPLÔMES (Cycles)
# ==========================================
class Diplome(Base):
    __tablename__ = "diplomes"

    id = Column(Integer, primary_key=True, index=True)
    intitule_fr = Column(String, unique=True, index=True) # ex: "LICENCE D'ETUDES FONDAMENTALES", "MASTER"
    intitule_ar = Column(String, nullable=True)           # ex: "الإجازة الأساسية", "الماستر"
    
    filieres = relationship("Filiere", back_populates="diplome")
    parcours = relationship("Parcours", back_populates="diplome")


# ==========================================
# 2. TABLE DES DÉPARTEMENTS (Parents)
# ==========================================
class Departement(Base):
    __tablename__ = "departements"

    id = Column(Integer, primary_key=True, index=True)
    intitule_fr = Column(String, unique=True, index=True) # ex: "ECONOMIE ET GESTION"
    intitule_ar = Column(String, nullable=True)           # ex: "الاقتصاد والتدبير"
    
    filieres = relationship("Filiere", back_populates="departement", cascade="all, delete-orphan")


# ==========================================
# 3. TABLE DES FILIÈRES
# ==========================================
class Filiere(Base):
    __tablename__ = "filieres"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)        # ex: 'SEG'
    intitule_fr = Column(String, nullable=False)          # ex: 'SCIENCES ECONOMIQUES ET GESTION'
    intitule_ar = Column(String, nullable=True)           
    
    departement_id = Column(Integer, ForeignKey("departements.id"))
    diplome_id = Column(Integer, ForeignKey("diplomes.id"), nullable=True)
    
    departement = relationship("Departement", back_populates="filieres")
    diplome = relationship("Diplome", back_populates="filieres")
    
    parcours = relationship("Parcours", back_populates="filiere", cascade="all, delete-orphan")
    academic_records = relationship("AcademicRecord", back_populates="filiere")


# ==========================================
# 4. TABLE DES PARCOURS (Options)
# ==========================================
class Parcours(Base):
    __tablename__ = "parcours"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)        # ex: 'GES', 'ECO'
    intitule_fr = Column(String, nullable=False)          # ex: 'GESTION'
    intitule_ar = Column(String, nullable=True)           
    
    filiere_id = Column(Integer, ForeignKey("filieres.id"), nullable=True)
    diplome_id = Column(Integer, ForeignKey("diplomes.id"), nullable=True)
    
    filiere = relationship("Filiere", back_populates="parcours")
    diplome = relationship("Diplome", back_populates="parcours")
    academic_records = relationship("AcademicRecord", back_populates="parcours")


# ==========================================
# 5. TABLE DES ÉTUDIANTS (Profil Civil)
# ==========================================
class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    cne = Column(String, unique=True, index=True) 
    cin = Column(String, index=True)
    student_name_fr = Column(String)
    student_name_ar = Column(String)
    birth_date = Column(String)
    birth_date_ar = Column(String)
    birth_place_fr = Column(String)
    birth_place_ar = Column(String)
    
    diplomas = relationship("AcademicRecord", back_populates="student")


# ==========================================
# 6. TABLE DES DOSSIERS ACADÉMIQUES
# ==========================================
class AcademicRecord(Base):
    __tablename__ = "academic_records"
    
    id = Column(Integer, primary_key=True, index=True)
    
    student_id = Column(Integer, ForeignKey("students.id"))
    batch_id = Column(Integer, ForeignKey("diploma_batches.id"))
    
    # L'étudiant peut être inscrit dans une filière globale ou un parcours précis
    filiere_id = Column(Integer, ForeignKey("filieres.id"), nullable=True)
    parcours_id = Column(Integer, ForeignKey("parcours.id"), nullable=True)
    filiere_code_excel = Column(String) # Trace du CODFIL lu dans l'Excel
    
    # Notes semestrielles
    s1 = Column(String); s2 = Column(String); s3 = Column(String); s4 = Column(String); s5 = Column(String); s6 = Column(String)
    s7 = Column(String); s8 = Column(String); s9 = Column(String); s10 = Column(String)
    
    moyenne_generale = Column(String)
    mention_fr = Column(String)
    mention_ar = Column(String)
    deliberation_date = Column(String)
    doc_number = Column(String, unique=True, index=True)
    is_printed = Column(Boolean, default=False)
    
    # Relations
    student = relationship("Student", back_populates="diplomas")
    batch = relationship("DiplomaBatch", back_populates="records")
    filiere = relationship("Filiere", back_populates="academic_records")
    parcours = relationship("Parcours", back_populates="academic_records")




from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base


class DiplomaBatch(Base):
    __tablename__ = "diploma_batches"

    id = Column(Integer, primary_key=True, index=True)
    diploma_type = Column(String, index=True)
    annee_universitaire = Column(String)
    issue_date = Column(String)

    # Relationship to link to the students
    students = relationship(
        "StudentDiploma", back_populates="batch", cascade="all, delete-orphan"
    )


class StudentDiploma(Base):
    __tablename__ = "student_diplomas"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("diploma_batches.id"))

    # Grouping Data
    filiere_code = Column(String, index=True)

    # Personal Data
    student_name_fr = Column(String)
    student_name_ar = Column(String)
    birth_date = Column(String)
    birth_date_ar = Column(String)
    birth_place_fr = Column(String)
    birth_place_ar = Column(String)

    # Identifiers
    cne = Column(String, index=True)
    cin = Column(String, index=True)

    # Academic Data
    filiere_fr = Column(String)
    filiere_ar = Column(String)
    mention_fr = Column(String)
    mention_ar = Column(String)
    deliberation_date = Column(String)

    # Document Tracking
    doc_number = Column(String, unique=True, index=True)
    is_printed = Column(
        Boolean, default=False
    )  # Useful for tracking what has been generated!

    # Relationship back to the batch
    batch = relationship("DiplomaBatch", back_populates="students")

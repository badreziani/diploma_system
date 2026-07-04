import pandas as pd
import io

def format_arabic_date(date_str):
    """Convertit '2026-06-20' en '20 يونيو 2026'"""
    if not date_str:
        return ""
    try:
        parts = date_str.split('-')
        if len(parts) != 3: return date_str
        year, month, day = parts[0], parts[1], parts[2]
        
        months_ar = {
            "01": "يناير", "02": "فبراير", "03": "مارس", "04": "أبريل",
            "05": "ماي", "06": "يونيو", "07": "يوليوز", "08": "غشت",
            "09": "شتنبر", "10": "أكتوبر", "11": "نونبر", "12": "دجنبر"
        }
        day_num = str(int(day))
        return f"{day_num} {months_ar.get(month, month)} {year}"
    except:
        return date_str

def get_arabic_mention(mention_fr):
    mention_fr = str(mention_fr).strip().upper()
    if "TRÈS BIEN" in mention_fr or "TRES BIEN" in mention_fr: return "حسن جدا"
    elif "ASSEZ BIEN" in mention_fr: return "مستحسن"
    elif "BIEN" in mention_fr: return "حسن"
    elif "PASSABLE" in mention_fr: return "مقبول"
    else: return "" 

def process_excel_files(students_files_bytes: list, marks_data_list: list):
    # 1. Charger et concaténer les fichiers Étudiants
    df_students_list = [pd.read_excel(io.BytesIO(f)) for f in students_files_bytes]
    df_students = pd.concat(df_students_list, ignore_index=True)
    df_students.columns = df_students.columns.str.strip()
    
    # Nettoyage et conversion des CNE en chaînes de caractères épurées
    df_students["CNE"] = df_students["CNE"].astype(str).str.strip()

    # 2. Charger et concaténer les fichiers de Notes
    df_marks_list = []
    for mark_data in marks_data_list:
        df = pd.read_excel(io.BytesIO(mark_data["bytes"]))
        df.columns = df.columns.str.strip()
        df["CODE ATTALIB"] = df["CODE ATTALIB"].astype(str).str.strip()
        
        # Attacher la date de délibération saisie à ce fichier de notes
        df["deliberation_date_ar"] = format_arabic_date(mark_data["date"])
        df_marks_list.append(df)
        
    df_marks = pd.concat(df_marks_list, ignore_index=True)

    # --- AJOUT CRITIQUE : VÉRIFICATION DES ÉTUDIANTS EXISTANTS ---
    cne_base_etudiants = set(df_students["CNE"].unique())
    cne_fichiers_notes = set(df_marks["CODE ATTALIB"].unique())
    
    # Détecter les CNE présents dans les notes mais introuvables dans le fichier étudiants
    cnes_manquants = cne_fichiers_notes - cne_base_etudiants
    unmatched_students = []
    
    if cnes_manquants:
        # On extrait ces lignes pour récupérer les noms saisis dans le fichier de notes pour le rapport
        df_manquants = df_marks[df_marks["CODE ATTALIB"].isin(cnes_manquants)].drop_duplicates(subset=["CODE ATTALIB"])
        for _, row in df_manquants.iterrows():
            unmatched_students.append({
                "cne": row.get("CODE ATTALIB", ""),
                "nom_complet": row.get("NOM ET PRENOM", "Nom inconnu dans le fichier de notes")
            })

    # 3. Fusion des données (Inner join : élimine automatiquement les manquants du flux de traitement)
    df_merged = pd.merge(df_students, df_marks, left_on="CNE", right_on="CODE ATTALIB", how="inner")
    df_merged = df_merged.fillna("")

    students_list = []
    
    # 4. Construction du dictionnaire pour l'insertion future en BDD / Impression
    for index, row in df_merged.iterrows():
        mention_fr_val = str(row.get("MENTION", "Passable")).title()
        
        student_data = {
            "filiere_code": str(row.get("CODFIL", "Economie_Gestion")), 
            "student_name_fr": row.get("NOM COMPLET (FR)", ""),
            "student_name_ar": row.get("NOM COMPLET (AR)", ""),
            "cne": row.get("CNE", ""),
            "cin": row.get("CIN", ""),
            "filiere_fr": "Economie et Gestion",
            "filiere_ar": "الاقتصاد والتدبير",
            "mention_fr": mention_fr_val,
            "mention_ar": get_arabic_mention(mention_fr_val),
            "deliberation_date": row.get("deliberation_date_ar", ""),
            "doc_number": str(row.get("NUM_DIP", f"{index + 1}/2026"))
        }
        students_list.append(student_data)

    # On retourne les étudiants valides ET la liste des étudiants manquants détectés
    return students_list, unmatched_students
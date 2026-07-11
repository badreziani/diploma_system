import pandas as pd
import io

def format_arabic_date(date_str):
    if not date_str: return ""
    try:
        parts = str(date_str).split("-")
        if len(parts) != 3: return date_str
        year, month, day = parts[0], parts[1], parts[2][:2]
        months_ar = {
            "01": "يناير", "02": "فبراير", "03": "مارس", "04": "أبريل", "05": "ماي", "06": "يونيو",
            "07": "يوليوز", "08": "غشت", "09": "شتنبر", "10": "أكتوبر", "11": "نونبر", "12": "دجنبر"
        }
        return f"{str(int(day))} {months_ar.get(month, month)} {year}"
    except:
        return str(date_str)

def get_arabic_mention(mention_fr):
    mention_fr = str(mention_fr).strip().upper()
    if "TRÈS BIEN" in mention_fr or "TRES BIEN" in mention_fr: return "حسن جدا"
    elif "ASSEZ BIEN" in mention_fr: return "مستحسن"
    elif "BIEN" in mention_fr: return "حسن"
    elif "PASSABLE" in mention_fr: return "مقبول"
    return ""

def process_excel_files(students_files_bytes: list, marks_data_list: list):
    df_students_list = [pd.read_excel(io.BytesIO(f)) for f in students_files_bytes]
    df_students = pd.concat(df_students_list, ignore_index=True)
    df_students.columns = df_students.columns.str.strip()
    df_students["CNE"] = df_students["CNE"].astype(str).str.strip()

    df_marks_list = []
    for mark_data in marks_data_list:
        df = pd.read_excel(io.BytesIO(mark_data["bytes"]))
        df.columns = df.columns.str.strip()
        df["CODE ATTALIB"] = df["CODE ATTALIB"].astype(str).str.strip()
        df["deliberation_date_ar"] = format_arabic_date(mark_data["date"])
        df_marks_list.append(df)
    
    df_marks = pd.concat(df_marks_list, ignore_index=True)

    cne_base_etudiants = set(df_students["CNE"].unique())
    cne_fichiers_notes = set(df_marks["CODE ATTALIB"].unique())
    cnes_manquants = cne_fichiers_notes - cne_base_etudiants
    unmatched_students = []

    if cnes_manquants:
        df_manquants = df_marks[df_marks["CODE ATTALIB"].isin(cnes_manquants)].drop_duplicates(subset=["CODE ATTALIB"])
        for _, row in df_manquants.iterrows():
            unmatched_students.append({
                "cne": row.get("CODE ATTALIB", ""),
                "nom_complet": row.get("NOM ET PRENOM", "Nom inconnu dans le fichier de notes")
            })

    df_merged = pd.merge(df_students, df_marks, left_on="CNE", right_on="CODE ATTALIB", how="inner")
    df_merged = df_merged.fillna("")

    students_list = []
    for index, row in df_merged.iterrows():
        mention_fr_val = str(row.get("MENTION", "Passable")).title()
        
        datnais = row.get("DATNAIS", "")
        if isinstance(datnais, pd.Timestamp):
            birth_date_str = datnais.strftime("%d/%m/%Y")
            birth_date_ar_str = datnais.strftime("%Y/%m/%d")
        else:
            birth_date_str = str(datnais)
            birth_date_ar_str = str(datnais)
            
        student_data = {
            "filiere_code": str(row.get("CODFIL", "Economie_Gestion")), 
            "student_name_fr": row.get("NOM COMPLET (FR)", ""),
            "student_name_ar": row.get("NOM COMPLET (AR)", ""),
            "cne": row.get("CNE", ""),
            "cin": row.get("CIN", ""),
            "birth_date": birth_date_str,
            "birth_date_ar": birth_date_ar_str,
            "birth_place_fr": row.get("LIEU DE NAISSANCE (FR)", ""),
            "birth_place_ar": row.get("LIEU DE NAISSANCE (AR)", ""),
            "s1": str(row.get("S1", "")), "s2": str(row.get("S2", "")), "s3": str(row.get("S3", "")),
            "s4": str(row.get("S4", "")), "s5": str(row.get("S5", "")), "s6": str(row.get("S6", "")),
            "s7": str(row.get("S7", "")), "s8": str(row.get("S8", "")), "s9": str(row.get("S9", "")), "s10": str(row.get("S10", "")),
            "moyenne_generale": str(row.get("MOYENNE", "")),
            "mention_fr": mention_fr_val,
            "mention_ar": get_arabic_mention(mention_fr_val),
            "deliberation_date": row.get("deliberation_date_ar", ""),
            "doc_number": str(row.get("NUM_DIP", f"{index + 1}/2026"))
        }
        students_list.append(student_data)

    return students_list, unmatched_students
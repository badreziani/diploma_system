import pandas as pd

# 1. Chargement des deux fichiers (remplacez par les vrais noms de vos fichiers)
file_filieres = "./Table Filières.xlsx"
file_mentions = "./Table mentions (partagé).xlsx"

print("⏳ Lecture et homogénéisation des fichiers...")

try:
    # Lecture des fichiers Excel
    df_filieres = pd.read_excel(file_filieres)
    df_mentions = pd.read_excel(file_mentions)
    
    # Nettoyage automatique des espaces dans les noms de colonnes
    df_filieres.columns = df_filieres.columns.str.strip()
    df_mentions.columns = df_mentions.columns.str.strip()
    
    # Élimination des lignes vides ou des doublons sur la clé unique (ex: CODE ou MENTION)
    if "CODE" in df_filieres.columns:
        df_filieres = df_filieres.dropna(subset=["CODE"]).drop_duplicates(subset=["CODE"])
    
    # Remplacer les valeurs manquantes par du texte vide
    df_filieres = df_filieres.fillna("")
    df_mentions = df_mentions.fillna("")
    
    # 2. Construction du fichier homogène
    # Si les deux fichiers partagent une colonne commune (par exemple 'CODE' ou 'FILIERE'), on les fusionne :
    # Ici, nous faisons l'hypothèse d'une fusion sur une colonne commune. 
    # Si ce sont deux tables de référence distinctes, nous les écrivons dans deux feuilles d'un même fichier Excel.
    
    output_file = "Referentiel_Universitaire_Homogene.xlsx"
    
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Sauvegarde de la table des filières épurée (4 colonnes sélectionnées)
        colonnes_utiles_filieres = [col for col in ["CODE", "FILIERE", "FILIERE (AR)", "DIPLOME"] if col in df_filieres.columns]
        df_filieres_clean = df_filieres[colonnes_utiles_filieres]
        df_filieres_clean.to_excel(writer, sheet_name="Filieres_Parcours", index=False)
        
        # Sauvegarde de la table des mentions épurée
        df_mentions.to_excel(writer, sheet_name="Mentions_Configuration", index=False)
        
    print(f"✅ Succès ! Le fichier homogène a été créé : '{output_file}'")
    print("En-têtes conservés pour les Filières :", list(df_filieres_clean.columns))
    print("En-têtes conservés pour les Mentions :", list(df_mentions.columns))

except Exception as e:
    print(f"❌ Une erreur est survenue : {str(e)}")
    print("Veuillez vérifier que les noms des fichiers et des colonnes sont corrects.")
*Repérage des pages dupliquées"

- 'check_txt.py' détecte les pages dupliquées dans les documents :
-- prend un dossier en argument (par défaut : dossier_exemple_txt/)
-- parcourt tous les fichiers txt
-- isole les pages supectes et les place dans "suspect_files/"
-- fait des visualisations html et les place dans "html_vizu/"

- 'grap_suspect_pdf_files.py' isole les PDF impliqués
-- prend un dossier (ou une liste en intension) de PDF
-- isole les PDF trouvés et les copie dans "suspected_pdf/"
-- donne en sortie la liste des PDF non trouvés

from scipy import spatial 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import DistanceMetric
import glob
import json
import os
import re
from tools import *

def get_pathout_name(liste_path, matrix_dir):
  """
  Génère le nom du fichier de sortie et vérifie que le dossier existe
  """
  os.makedirs(matrix_dir, exist_ok=True)
  filename = re.sub("/", "__", liste_path[0])
  NB_files = len(liste_path)#Si on avait pas le même nombre de pages
  path_out = f"{matrix_dir}/{filename}_{NB_files}.json"
  return path_out

def get_similarites(liste_path, path_out):
  """
  Calcule la similarité entre les fichiers de 'liste_path" (des pages a priori)
  Enregistre la matrice résultant dans 'path_out'
  """
  pages = []
  for path in liste_path:
    with open(path, "r", encoding = "utf-8") as f:
      pages.append(f.read())
  V = CountVectorizer(analyzer="char", ngram_range=(4,5))
  X = V.fit_transform(pages).toarray()
  
  dist = DistanceMetric.get_metric("braycurtis")
  similarites = dist.pairwise(X).tolist()

  with open(path_out, "w") as w:
    w.write(json.dumps(similarites))
  return similarites

def  get_suspect(ordered_sim, path_out, matrix_dir, seuil_dist=0.1):
  """
  Etant donné une liste de triplets de la forme suivante:
    sim(doc1, doc2), path_doc1, path_doc2
  Récupère tous les triplets avec sim < seuil_dist
  Stocke les triplets résultants dans un dossier "suspect_files"
  Le nom de fichier reste le même que celui qu'il avit dans "path_out"
  """
  suspect_dir = "suspect_files"
  os.makedirs(suspect_dir, exist_ok=True)
  path_suspect = re.sub(matrix_dir, suspect_dir, path_out)
  ordered_sim = sorted(ordered_sim)
  if ordered_sim[0][0]<0.1:
    suspect = [x for x in ordered_sim if x[0]<seuil_dist]
    if len(suspect)>1:
      with open(path_suspect, "w") as w:
        w.write(json.dumps(suspect))
      is_suspect = visual_suspects(path_suspect)
      if is_suspect>0:
        print(f"{is_suspect} paires : {path_suspect}")
        w = open("pdf_suspects.csv", "a")
        pages = [re.findall("-[0-9]{1,3}.png", x[1]+x[2])[:2] for x in suspect]
        pages = [re.sub("-|.png","", ":".join(x)) for x in pages]
        pdf_name = get_pdf_name(path_suspect)
        w.write("\t".join([pdf_name]+pages)+"\n")
        w.close()
      else:
        os.system(f"rm {path_suspect}")

def compare_txt(liste_path):
  """
  Fonction principale qui déclenche lesprocessus suivants :
  - étant donné une liste de chemins de fichiers
  - calcule la similarité entre eux
  - stocke cette matrice
  - en tire une liste de fichiers soupçonnés de similarités
  """
  liste_path = sorted(liste_path)
  matrix_dir = "sim_matrix"
  path_out = get_pathout_name(liste_path, matrix_dir)

  if os.path.exists(path_out):
    with open(path_out) as f:
      similarites = json.load(f)
  else:
    similarites = get_similarites(liste_path, path_out)

  ordered_sim = []
  for i in range(len(liste_path)):
    for j in range(i+1, len(liste_path)):
      if i ==j:#On ne compare pas une page par rapport à elle même
        continue
      ordered_sim.append([similarites[i][j], liste_path[i],liste_path[j]])
  get_suspect(ordered_sim, path_out, matrix_dir)

import sys

if len(sys.argv)>1:
  provided_path = sys.argv[1]
  print(f"Using provided path : {provided_path}")
else:
  provided_path = "dossier_exemple_txt"
  print(f"Using default path : {provided_path}")

liste_path_pdf = glob.glob(f"{provided_path}/*")
print("\n-->processing %i pdf path\n"%len(liste_path_pdf))

import tqdm

path_out_csv = "pdf_suspects.csv"
path_suspect = "suspect_files/"
path_vizu = "html_vizu/"

w = open(path_out_csv, "w")
w.close()
for path_pdf in tqdm.tqdm(liste_path_pdf):
    txt_files = glob.glob(f"{path_pdf}/*.txt")
  #try:
    if len(txt_files)==0:
      txt_files = glob.glob(f"{path_pdf}/*/*.txt")
    if len(txt_files)>0:
      compare_txt(txt_files)
    else:
      print(f"Error searching files in '{path_pdf}'")
print(f"Output :\n - Global:{path_out_csv}\n - Individual files:{path_suspect} - Vizu html : {path_vizu}")
print("")
print("Lancer 'grap_suspect_pdf_files.py' avec en argument la liste des PDF dispos pour permettre d'isoler les PDF problématiques")

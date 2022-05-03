import glob
import sys
import re
import os
from tools import *
import sys

path_out = "suspected_pdf"
os.makedirs(path_out, exist_ok=True)

print("Argument: dossier ou liste de fichiers")
if len(sys.argv)>2:
  all_pdf_names = sys.argv[1:]
  print("Liste en intention comprenant %i fichiers"%len(all_pdf_names))
else:
  if len(sys.argv)==2:
    path_pdf = sys.argv[1]
    print(f"Using given : {path_pdf}")
  else:
    path_pdf = "dossier_exemple_pdf/"
    print(f"Using default path : {path_pdf}")
  all_pdf_names = glob.glob(f"{path_pdf}/*")
  print("Liste de PDF issues du dossier : %i"%len(all_pdf_names))

#pdf_source = sys.argv[1]

dic= {"found":set(), "not-found":set()}
for suspect in glob.glob("suspect_files/*.json"):
  pdf_name = get_pdf_name(suspect)  
  l_pdf_path = [x for x in all_pdf_names if pdf_name in x]
  if len(l_pdf_path)==0:
    dic["not-found"].add(pdf_name)
  else:
    dic["found"].add(pdf_name)
    pdf_path = l_pdf_path[0]
    os.system(f"cp {pdf_path} {path_out}/")

print("-"*20)
for cle, set_pdf in dic.items():
  print(cle, len(set_pdf), sorted(list(set_pdf)[:10]))
print("-"*20)

NB_suspects = len(dic["found"])
print(f"{NB_suspects} Suspects placed in : {path_out}")

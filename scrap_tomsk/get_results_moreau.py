import os
import re
import time
import random
# si pas dans la base, on tombe directement sur le catalogue
# ex Moreau1

with open("missing_pdf_titles.txt") as f:
  lignes = f.readlines()

cpt = 0
for l in lignes:
  elems = re.split("\t| ", l)
  MOREAU = elems[0]
  if "Moreau" not in MOREAU or "suppl" in MOREAU or "nan" in MOREAU or "SANS" in MOREAU:
    continue
  url = f"https://vital.lib.tsu.ru/vital/access/manager/Repository?query=%22{MOREAU}%22&queryType=vitalDismax&x=0&y=0"
  path_html = f"SEARCH_RES/{MOREAU}.html"
  if os.path.exists(path_html)==True:
    with open(path_html) as f:
      chaine = f.read()
    link = re.findall('<a href="(.*?)" title=', chaine)
    print(path_html)
    print(len(link))
    continue
  print(url)
  cpt+=1
  time.sleep(random.randint(1, 9)/7)
  os.system(f"wget '{url}' -O '{path_html}'")
  if cpt==200:
    break

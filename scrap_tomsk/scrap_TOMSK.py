from bs4 import BeautifulSoup
import glob
import re
import json
import sys
import tqdm
import os
import time
import random

DOSSIER= sys.argv[1]
liste_fichiers = glob.glob(f"{DOSSIER}/Moreau*.html")
dic_stats = {"html":len(liste_fichiers), "with_result":len(liste_fichiers), "with_PDF":0, "to_check":0}
print("Processing %i fichiers"%len(liste_fichiers))

path_log = "tomsk.log"
w_log = open(path_log, "w")

dic_tomsk = {}
for path_html in liste_fichiers:#tqdm.tqdm(liste_fichiers):
  w_log.write(path_html)
  ID = re.split("/", re.sub("\.html", "", path_html))[-1]
  with open(path_html) as f:
    chaine = f.read()
  soup = BeautifulSoup(chaine, 'html.parser')
  #elems_results = soup.find_all("div", {"class":"searchResult"})
  liste_dt = soup.find_all("dt")
  liste_dd = soup.find_all("dd")
  dic = {}
  for i, elem in enumerate(liste_dt):
#    print(elem.text)
    dic[elem.text] = liste_dd[i].text
#  print(json.dumps(dic, indent=2, ensure_ascii=False))
  link = re.findall('<td><a href="(.*?)">Télécharger</a></td>', chaine)
  link = re.findall('<td><a href="(.*?)">Download</a></td>', chaine)
  links =re.findall('<a href="(.*?)" title="Download', chaine)
  link+=links
  if len(link)==0:
    if "No items were found" not in chaine:
      os.system(f"cp {path_html} MISSING_TO_CHECK/")
      dic_stats["to_check"]+=1
    w_log.write(f"Nothing : {ID}")
    dic_stats["with_result"]-=1
    continue
  link_str = "https://vital.lib.tsu.ru/"+link[0]
  path_out_pdf = f"PDFS/{ID}.pdf"
  dic["url"] = link_str
  dic_tomsk[ID] = dic 
  if os .path.exists(path_out_pdf)==True:
    dic_stats["with_PDF"]+=1
    continue
  time.sleep(random.randint(1, 9)/7)
  cmd = f"wget {link_str} -O {path_out_pdf}"
  os.system(cmd)
  dic_stats["with_PDF"]+=1

w_log.close()
print(f"LOG : {path_log}")
print(json.dumps(dic_stats, indent=2))

with open("dic_tomsk.json", "w") as w:
  w.write(json.dumps(dic_tomsk, indent=2, ensure_ascii=False))

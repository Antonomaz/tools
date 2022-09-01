# -*- coding: utf-8 -*-
import pandas

path_xls = "data/ListeMazarinades.xlsx"

xls = pandas.ExcelFile(path_xls)
df = pandas.read_excel(xls, 'Documents_all')

#Génrérer le JSOn (garder trace de la version ?)
dic = {}

for line in df.iterrows():
  id_base = line[1][0]
  #if "*" in str(id_base) or "-" in str(id_base) or "_" in str(id_base):
  #  ID = str(id_base)
  #else:
  #  ID = str(int(id_base))
  ID = str(id_base)
  value = list(line[1].values[1:])
  nom_infos = ["Titre", "Année", "Date Précise", "Lieu", "Nb. Pages", "Notice", "Note"]
  try:
    value[1] = int(value[1])
  except:
    pass
  try:
    value[4] = int(value[4])
  except:
    pass
  value = {nom_infos[i]:value[i] for i in range(len(value))}
  if ID in dic:
    print("ID déjà présente", ID)
    1/0
  dic[ID] = value
as_list = [[cle, val["Titre"]] for cle, val in dic.items()]

import json
for nom, struct in [["liste", as_list], ["dico", dic]]:
  path_out = f"data/{nom}_titres_ID.json"
  print(path_out)
  w = open(path_out, "w")
  w.write(json.dumps(struct, indent =2, ensure_ascii=False))
  w.close()

# Générer le HTML (externaliser le script)

#from antono_tools import *
import re


with open("visualisation_tools/head.html", encoding="utf-8") as f:
    header = f.read()

with open("data/dico_titres_ID.json") as f:
    dic_titres = json.load(f)

out = ""
table_header = []
cpt = 0
test = []
for ID, infos in dic_titres.items():
#  if int(ID)>10:
#    break
  if len(table_header) == 0:
    table_header = infos.keys()
    out+="  <tr><th>ID</th><th>%s</th></tr>\n"%"</th><th>".join(table_header)
#  infos["Notice"] = re.escape(infos["Notice"])
  elems = [infos[cle] for cle in table_header]
  test.append([len(str(infos["Date Précise"])),infos["Date Précise"]])
  elems = [str(x) if str(x)!="null" and str(x)!="None" and str(x)!="nan" else "" for x in elems]
  link = f"id=\"{ID}\""
  link= ""
  this_info = "</td><td>".join(elems)
  l = f"  <tr {link}><td>{ID}</td><td>{this_info}</td></tr>\n"
  out +=l
out_html = re.sub("{{content_table}}", out, header)
with open("test.html", "w", encoding="utf-8") as w:
    w.write(out_html)


print(sorted(test)[-10:])



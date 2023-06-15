import json
import glob
import re
import os

with open("dic_tomsk.json") as f:
  dic = json.load(f)

cpt_OK =0
liste_fic = glob.glob("PDFS/*/*.pdf")
L = []
dd = {}
for pdf in liste_fic:
   moreau = re.split("/|_", pdf)[1]
   if moreau not in dic.keys():
     #os.system(f"evince {pdf} &")
     pass
   else:
     if "Moreau" in moreau:
       num = int(re.findall("[0-9][0-9]*", moreau)[0])
       L.append([num, moreau, dic[moreau]["url"]])
       if dic[moreau]["url"] in dd:
         print(moreau)
         print(dd[dic[moreau]["url"]])
       dd[dic[moreau]["url"]] = moreau
##   if len(dic[moreau]) <2:
##     print(moreau)
##     #os.system(f"evince {pdf} &")
##   else:
##     cpt_OK+=1
print(len(liste_fic))
print(cpt_OK)
print(len([x for x,y in dic.items() if len(y)>1]))

for a, b, c in sorted(L):
  print(b,c)

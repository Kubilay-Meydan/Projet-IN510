``````````````````````````````````````````````````````````````````````````````````````````````
`````````````````````````````,,```````````````````````````````````````````````````````````````
`7MM"""Mq.```````````````````db```````````mm````````7MMF'`7MN.````7MF'````````````````````````
``MM````MM.```````````````````````````````MM`````````MM````MMN.````M```````````__,````````````
``MM```,M9``7Mb,od8`,pW"Wq.`7MM``.gP"Ya`mmMMmm```````MM````M`YMb```M``M******``7MM``,pP""Yq.``
``MMmmdM9````MM'`"'6W'````Wb`MM`,M'```Yb``MM`````````MM````M```MN.`M`.M`````````MM`6W'`````Wb`
``MM`````````MM````8M`````M8`MM`8MTMTTMM``MM`````````MM````M````MM.M`|bMMAg.````MM`8M``````M8`
``MM`````````MM````YA.```,A9`MM`YM.````,``MM`````````MM````M`````YMM```````Mb```MM`YA.````,A9`
.JMML.`````.JMML.````Ybmd9'``MM```Mbmmd'```Mbmo````.JMML..JML.````YM```````jM`.JMML.`Ybmmd9'``
``````````````````````````QO`MP``````````````````````````````````````(O)``,M9`````````````````
```````````````````````````bmP````````````````````````````````````````6mmm9```````````````````
``````````````````````````````````````````````````````````````````````````````````````````````                         
MEYDAN Kubilay - CARRE Nathan


I) Quelques infos utiles :


Notre script fonctionne avec des fichiers MT en format .txt. 
La syntaxe s'agit de la même que celle du site https://turingmachinesimulator.com (à peu de choses près).
Le fichier doit commencer par "name: (Lorem ipsum)" ou par "init: (Lorem ipsum)". 
Le nom de la machine importe peu et peut être ignoré.
Ensuite, pour définir un état accept, on écrit "accept: (Lorem ipsum)".
Puis, nous pouvons définir des appels (ou links) avec cette syntaxe:
"link: q1,_,machine2.txt,q2"
Plusieurs appels peuvent êtres définis.
Les commentaires sont autorisés, tant qu'ils commencent par un // et ne contiennent pas de  ' (peut causer des bugs parfois donc à eviter).
Pour le reste, la structure des transitions est la même.

Nous avons inclus un fichier exemple_syth.txt comme exemple de fichier respectant la syntaxe. 


II) Prise en main


Pour exécuter le script, il suffit d'organiser la commande du terminal comme suit:

python main.py [fonction] [Machine1] [Mot] --Machine2 [Machine2]

[fonction]: Correspond au fonction du script 
valeurs possibles: charge_transitions, premiere_etape, run_machine, linker, dead

[Machine1]: Correspond à la machine sur lequel la fonction s'exécute.
valeurs possibles: chemin du fichier ou nom du fichier si le terminal est dans le bon répertoire (en .txt)

[Mot]: Mot donné en entrée.
valeurs possibles: tous les mots formes par l'alphabet {0,1}

[Machine2]: (optionnel) Utile seulement si la fonction choisie est linker.
valeurs possibles: chemin du fichier ou nom du fichier si le terminal est dans le bon répertoire (en .txt)


II) Organisation générale :


Notre script python se décompose en 6 étapes principales :
  1)         -MT-         La définition de la classe MT
  2)    -lirefichier-     L'initialisation de d'une MT à partir de son code (.txt) ainsi que d'un mot d'entre.
  3) -charge_transitions- L'ajout des transitions sous forme de dictionnaire des états, et des transitions spéciales (links) dans la classe MT (cette fonction appelle au préalable la précédente)
  4)   -premiere_etape-   L'exécution, étant donné un mot et une machine de Turing, d'une étape de calcul (fait appel aux fonctions précédentes pour simplifier l'utilisation)
  5)     -run_machine-    L'exécution étape par étape de la machine jusqu'à un état accept ou reject.
  6)       -linker-       Produit le code d'une machine de Turing équivalant à machine1, ou machine1 fait des appels à machine2, sans les appels.
 10)        -Dead-        Le Bonus dead_code_remover crée un fichier no_dead----.txt où toutes les transtions des états inatteignables (dead code) sont effacés du code de la MT.


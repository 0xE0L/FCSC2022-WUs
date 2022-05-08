# Énoncé 

Connectez-vous au service en ligne donné ci-dessous, et pour chaque chaîne de caractères reçue, vous devez renvoyer la chaîne de caractères contenant les caractères dans l'ordre inverse.

Par exemple, pour la chaîne ANSSI, vous devez renvoyer ISSNA (note : le respect de la casse est important).

`nc challenges.france-cybersecurity-challenge.fr 2000`


# Approche

Je ne ferai pas de write-up détaillé, on comprend qu'ici la difficulté technique est juste d'automatiser l'envoi de toutes nos strings inversées !

Cela peut se faire en quelques lignes de Python via la librairie pwntools, voir le script de résolution `solve.py`.
# Énoncé 

On vous demande d'exploiter le binaire fourni pour lire le fichier flag qui se trouve sur le serveur distant.
SHA256(pwn) = b44030df647475507f65e910f71810b8d1633985cecef9d0862a702bcd308335
`nc challenges.france-cybersecurity-challenge.fr 2050`

# Approche

Un dépassement de tampon nous permet de réécrire le pointeur de retour (le `saved RIP`) stocké sur la pile. On peut donc rediriger le flux d'exécution du programme sur ce que l'on veut !

En l'occurrence, une fonction shell() située à l'adresse 0x4011A2 est présente dans ce programme. On va donc faire en sorte de le réécrire au bon endroit sur la stack pour exécuter cette fonction qui va nous octroyer le shell distant que l'on recherche.

Voir script `solve.py`.
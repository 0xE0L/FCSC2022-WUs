# Énoncé

On vous demande d'exploiter le binaire fourni pour lire le fichier flag qui se trouve sur le serveur distant.

`SHA256(microroptor) = e19b38ec152eb2600b79ed9088d79d53eae588fd49a721d1ce3a3cfaba247339`

nc challenges.france-cybersecurity-challenge.fr 2052

Note : le binaire à exploiter n'a pas accès à Internet


# Solution

En reversant le programme dans IDA ou Ghidra, on voit dans main() qu'un read() nous permet d'écrire 512 octets sur la stack, dans un buffer qui n'en fait en réalité que 32 !
Donc autant dire que l'on a largement de quoi exploiter un buffer overflow.

Un checksec sur le binaire nous montre qu'il a toutes les protections (PIE compris), à part le canari stack dont on n'aura pas à se soucier.
Heureusement, un leak sur une adresse de .data (dont on voit dans IDA qu'elle correspond à l'offset 0x4010 pour une adresse de base à 0x0) est volontairement effectué par le programme !

On se sert donc ce leak (baseAddress= leak - 0x4010) pour récupérer l'adresse de base du binaire et bypasser le PIE.
Un outil comme ropper nous apprend que nous avons tous les gadgets au sein du binaire nécessaires pour 1) effectuer un write-what-where de '/bin/sh\0' dans .data et 2) de faire un execve('/bin/sh\0', 0, 0), donc on effectue une ROP chain tout à fait classique pour exploiter le binaire distant.
Bref, vraiment le challenge de ROP le plus classique que l'on peut retrouver en pwn !

Ceci est implémenté dans le script solve.py.
On exploite correctement le binaire et on capable de faire un "cat flag" sur la machine distante.

Finalement, le flag est: FCSC{e3752da07f2c9e3a0f9ad69679792e5a8d53ba717a2652e29fb975fcf36f9258}
# Énoncé 

Connaissez-vous le principe d'un shellcode ?

SHA256(execut0r) = 3980b324c99371125949ed18fffde9320f17c0c11da1e3aa6c7cb8580429cdbf.

`nc challenges.france-cybersecurity-challenge.fr 2051`


# Solution

En reversant succinctement le programme dans IDA ou Ghidra et au vu de ce que nous indique l'énoncé, on se doute qu'il suffit d'envoyer un shellcode à ce binaire qui se chargera de l'exécuter.

Mais qu'est-ce qu'un shellcode ? C'est un bout de code machine (la représentation "CPU" d'un code assembleur) que l'on va généralement injecter dans un programme vulnérable, au vu d'effectuer une action comme nous octroyer un shell. Ici, le programme est bien gentil puisqu'il nous autorise explicitement à exécuter un shellcode qu'on lui envoie (d'habitude il faut trouver une vulnérabilité non volontaire dans le programme pour y parvenir).

Étant donné qu'il s'agit d'un binaire Linux ELF 64-bits (on le voit via `file execut0r`), on cherche donc un shellcode :
* Pour Linux, chargé de nous ouvrir un shell '/bin/sh' bien souvent
* Un shellcode 64-bits (pas un 32-bits où c'est différent !)

On peut trouver de tels shellcodes en ligne, comme celui-ci que j'ai utilisé : https://shell-storm.org/shellcode/files/shellcode-77.php

Il ne reste plus qu'à l'envoyer au programme distant via un script Python utilisant pwntools et à profiter de notre shell ! Voir le script solve.py.

Flag : FCSC{9f8a2eb6fbb26644dab670f1a948c449ba36102417efc3e40c3bd4774bfb4f7a}
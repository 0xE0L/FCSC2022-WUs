# Énoncé

On vous demande de lire le fichier flag.txt sur le serveur distant.

SHA256(xoraas) = 2bd5a583195adf5c978bb5c7b657ccefe1372bea643a31f208723ec6ec58eab5.

`nc challenges.france-cybersecurity-challenge.fr 2053`

Note : le binaire à exploiter n'a pas accès à Internet.


# Solution

En reversant le programme, on voit :
- Qu'une première string de 128 chars est lue via un fread()
- Qu'une seconde string  de 145 chars est lue via un fread() elle aussi

Les deux strings sont ensuite XORées ensembles... Et ensuite le programme reçoit une SEGFAULT ?!

Pourquoi ? Tout simplement parce-que la stack est complètement corrompue :

- Dans la fonction main(), on remarque déjà le "add rsp, 0xFFFFFFFFFFFFFF80 qui est peu conventionnel...
  0xFFFFFFFFFFFFFF80 correspond à un nombre 64-bits signé dont la valeur est "-128"...
  Bref, on a un "add rsp, -128", donc en fait l'équivalent d'un "sub rsp, 128" ! Je ne savais même pas qu'on pouvait faire ça, c'est assez marrant.
- main() fait donc l'équivalent d'un "sub rsp, 128" détaillé ci-dessus pour réserver de la mémoire sur la stack...
  Par contre à la fin de la fonction il ne supprime pas ses variables locales par un "add rsp, 128", ça serait pourtant la moindre des choses. :)
- xor() réserve de la mémoire via un "sub rsp, 160" et oublie lui aussi de supprimer l'espace réservé avant de return via un "add rsp, 160"...
  On remarquera d'ailleurs qu'il y a 2 NOPs avant le "leave + ret", ça correspond fort probablement à un patching manuel d'une instruction par le challmaker !
  J'aurais logiquement misé sur un patching du "add rsp, 160", mais cette instruction fait 7 octets donc oublions... Je ne sais pas ce que le challmaker a pu patcher, bref ce n'est pas grave.

En tout cas tout ceci fait que la stack est corrompue et qu'à la fin de la fonction main(), on constate dans un débugger que l'instruction "ret" va "popper" une certaine valeur située au sommet de la stack ("ret" = +/- "pop rip" pour rappel)...
Et il se trouve que cette valeur se situe parfois dans les 2 strings XORées que l'on contrôle !
On pourrait donc se débrouiller pour popper une adresse que l'on veut dans RIP afin d'exécuter du code arbitrairement !

Ce qui va nous intéresser, c'est jumper sur 0x401146 car ça va nous permettre d'ouvrir un shell !
En effet, voici les instructions qui seront exécutées à cette adresse :
```
.text:0000000000401146    mov     edx, 0
.text:000000000040114B    mov     esi, 0
.text:0000000000401150    lea     rdi, path
.text:0000000000401157    call    _execve
```

Pour info, ces instructions sont contenues dans la fonction shell() en 0x404012, on ne va pas jumper au tout début de cette fonction car ça nous ferait exécuter le function prologue `push rbp; mov rbp, rsp`...
Au vu de ce que j'ai expliqué avant, on va éviter de manipuler inutilement la stack...

Pour former la payload, voyons comment on pourrait faire. Voici avec quels caractères imprimables on pourrait générer notre adresse "0x401146" :
```
0x46 = "a" XOR "'"
0x11 = "a" XOR "p"
0x40 = "a" XOR "!"
```

Pour générer les 0x0 qui suivent, il suffit de XORer n'importe quel caractère avec lui-même ('A' XOR 'A', 'B' XOR 'B', etc)

On a dit qu'on souhaitait écrire 0x0000000000401146, mais il faut l'écrire en little-endian...
Donc en xorant ces deux strings :
str1: aaaaaaaa
str2: 'p!aaaaa
On obtient bien (à l'envers) 0x4611400000000000 !

Bien sûr, il suffit ensuite de padder tout le reste avec n'importe quoi, des 'AAAA' comme d'habitude par exemple.

En testant mes exploits dans différents debuggers (GDB et R2), je constate qu'il y a des variations aléatoires sur la stack, probablement dues à l'ASLR.
Donc malheureusement, à la fin de main(), le "ret" ne poppe pas toujours la valeur 0x0000000000401146 que je voudrais dans RIP ! :( 

Mais je me rends compte que même quand ça fail, ma valeur "0x0000000000401146" n'est pas située bien loin de la valeur junk poppée sur la stack...
Et surtout je me rends compte que l'espace / la différence entre la valeur junk poppée sur la stack et ma payload varie ! Par exemple des fois ma valeur est à 56 octets de celle poppée sur la stack, parfois que 11... Bref, ça change !

Je me dis donc qu'en testant plusieurs fois et en faisant continuellement "slider" mon exploit, je finirais peut-être par arriver à faire popper cette fichue valeur dans le RIP ! On va donc faire un peu de bruteforce !

D'ailleurs, au lieu de "déplacer/slider" mon adresse 0x401146 (via les strings "aaaaaaaa" et "'p!aaaaa" comme indiqué), pourquoi ne pas tout simplement la sprayer (= la répéter plusieurs fois) ?
Eh bien j'ai remarqué qu'en la sprayant (notamment en testant dans un débugger), bizarrement, ça se passait moins bien...
Et en faisant le bruteforcing en sprayant, ça semble effectivement appuyer cette théorie et ne pas marcher du tout. Je ne saurais pas expliquer pourquoi.

Dans tous les cas, cette méthode de juste déplacer/slider l'adresse semble fonctionner en bruteforce avec un peu de patience !
Je mets donc tout ceci en place dans mon script solve.py

Je l'ai testé en local, et même en montant moi-même moi binaire sur un socket via socat !
En quelques dizaines de secondes, j'arrive bien à faire réussir l'exploit.

Je teste ensuite sur le challenge en ligne, où je crains que cela soit plus délicat. Après 3-4 minutes de bruteforce, miracle, l'exploit fini par marcher !

```
[+] Opening connection to challenges.france-cybersecurity-challenge.fr on port 2053: Done
Trying to slide address by: 67
Bad luck :(
[+] Opening connection to challenges.france-cybersecurity-challenge.fr on port 2053: Done
Trying to slide address by: 68
Bad luck :(
[+] Opening connection to challenges.france-cybersecurity-challenge.fr on port 2053: Done
Trying to slide address by: 69
Bad luck :(
[+] Opening connection to challenges.france-cybersecurity-challenge.fr on port 2053: Done
Trying to slide address by: 70
Bad luck :(
[+] Opening connection to challenges.france-cybersecurity-challenge.fr on port 2053: Done
Trying to slide address by: 71
Bad luck :(
[+] Opening connection to challenges.france-cybersecurity-challenge.fr on port 2053: Done
Trying to slide address by: 72
Bad luck :(
[+] Opening connection to challenges.france-cybersecurity-challenge.fr on port 2053: Done
Trying to slide address by: 73
[*] Switching to interactive mode
$ 
$ ls
flag.txt
$ cat flag.txt
FCSC{0d6c81576d1465a876422910769e79af287c9e73254112572737383039194f5d}
```

Intuitivement, je n'ai pas l'impression que ma méthode de résolution soit la meilleure et la plus fiable, peut-être ai-je loupé certaines choses... En tout cas ça ne m'a pas empêché de le résoudre ! Je serais bien curieux d'avoir des retours et méthodes d'autres challengers, peut-être plus fiables. :)

Flag: FCSC{0d6c81576d1465a876422910769e79af287c9e73254112572737383039194f5d}!
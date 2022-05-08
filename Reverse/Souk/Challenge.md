# Énoncé

Sur l'étal d'un marché ambulant, un ordinateur est en vente. Après l'avoir acheté, le binaire contenu à l'intérieur semble renfermer quelques secrets.

`SHA256(souk) = 48da39c81fd3e4c95e2b9b1e851545f75de3c2dfa97d2164dcc4e41c97497425.`


# Solution

Note : j'ai résolu le challenge en utilisant principalement une méthode d'analyse dynamique (debugger).

Dans le main() du binaire, on commence par voir un premier tableau de DWORDs, que j'appellerai LocDword1 par la suite.

On voit ensuite qu'une entrée utilisateur de 71 caractères est lue, puis que chaque DWORD situé à un indice "i" de LocDword1 est additionné avec le char pris dans userEntry[i].
Dans le cadre de mon analyse dynamique, je souhaite éviter un maximum de modifier tous les dwords originaux présents dans LocDword1 ! Ayant rapidement regardé en statique la fonction qui agit sur LocDword1, je me doute quelle "mélange" les DWORDs et je voudrais donc voir, en dynamique, comment les DWORDS ont été mélangés. Pour me simplifier la tâche, je vais donc au maximum éviter de les modifier avec mon entrée utilisateur.

Donc quand le programme me demande le flag, je ne saisis aucun caractère et tape directement un "Entrée".

--> Cela veut dire que seul le 1er dword sera additionné avec la valeur 10 correspondant à un "\n" (dû au fait que j'ai appuyé sur Entrée), mais les 70 autres DWORDs ne seront pas modifiés.
Tous les autres caractères de mon entrée utilisateur étant set à '\0', LocDword1 n'en sera pas affecté.

Voici donc le LocDword1 original (sauf en prenant compte que le premier a été additionné avec 10, mais on s'en fiche pour le moment) :

```
b9 d1 02 00 d2 20 07 00 6f 7a f5 ff d4 1a fc ff
a2 6a 0e 00 c5 34 0a 00 2d d9 04 00 32 fa f4 ff
53 07 03 00 c5 c3 f2 ff 76 aa 07 00 30 79 ff ff
43 d8 0d 00 42 1f 0b 00 87 71 03 00 2d 0c 00 00
7c ff 0d 00 52 b7 08 00 09 2b 07 00 d0 dd 09 00
c7 df 09 00 91 a9 0d 00 26 a6 fd ff 12 34 0b 00
74 30 f4 ff 2b f5 07 00 56 ac fc ff d0 03 ff ff
2f e9 f6 ff 82 4c ff ff 2d f6 0a 00 17 13 f1 ff
79 91 f3 ff 6c 43 03 00 6f 2b fc ff 6d 14 fb ff
cd 9c 01 00 fb a0 01 00 43 b5 fa ff 99 c8 f8 ff
26 c8 f3 ff 70 1b 07 00 38 5c fc ff 40 52 fb ff
60 1b f8 ff c4 b6 f9 ff 08 9b f3 ff 77 53 03 00
f5 71 05 00 91 be 07 00 13 ee f7 ff 63 dc 05 00
06 d4 f2 ff 65 7f fd ff 97 ad 07 00 ad 11 f7 ff
bd a9 04 00 00 8b fc ff 88 f5 fb ff 38 53 09 00
34 3e f3 ff 22 1f 03 00 2d 9d 02 00 9e cf fd ff
a2 38 0e 00 eb 97 07 00 04 1b f1 ff ac 3a f3 ff
ea 19 f8 ff 91 a4 f6 ff 07 31 02 00 (00 00 00 00)
```
(RAPPEL : on est en little-endian, le premier dword du tableau ci-dessus est donc égal à 0x02d1b9 par exemple)

Voici maintenant LocDword1 après l'appel à "sub_1316((__int64)LocDword2_4160, n, 1u);" :
```
17 13 f1 ff 04 1b f1 ff c5 c3 f2 ff 06 d4 f2 ff
ac 3a f3 ff 34 3e f3 ff 79 91 f3 ff 08 9b f3 ff
26 c8 f3 ff 74 30 f4 ff 32 fa f4 ff 6f 7a f5 ff
91 a4 f6 ff 2f e9 f6 ff ad 11 f7 ff 13 ee f7 ff
ea 19 f8 ff 60 1b f8 ff 99 c8 f8 ff c4 b6 f9 ff
43 b5 fa ff 6d 14 fb ff 40 52 fb ff 88 f5 fb ff
d4 1a fc ff 6f 2b fc ff 38 5c fc ff 00 8b fc ff
56 ac fc ff 65 7f fd ff 26 a6 fd ff 9e cf fd ff
d0 03 ff ff 82 4c ff ff 30 79 ff ff 2d 0c 00 00
cd 9c 01 00 fb a0 01 00 07 31 02 00 2d 9d 02 00
b9 d1 02 00 53 07 03 00 22 1f 03 00 6c 43 03 00
77 53 03 00 87 71 03 00 bd a9 04 00 2d d9 04 00
f5 71 05 00 63 dc 05 00 70 1b 07 00 d2 20 07 00
09 2b 07 00 eb 97 07 00 76 aa 07 00 97 ad 07 00
91 be 07 00 2b f5 07 00 52 b7 08 00 38 53 09 00
d0 dd 09 00 c7 df 09 00 c5 34 0a 00 2d f6 0a 00
42 1f 0b 00 12 34 0b 00 91 a9 0d 00 43 d8 0d 00
7c ff 0d 00 a2 38 0e 00 a2 6a 0e 00 (00 00 00 00)
```

Comme on le constate chaque DWORD est juste permuté, mais sa valeur n'est pas touchée (on peut s'en assurer via des petits CTRL+F) ! Très intéressant !

---

Maintenant, concentrons-nous sur l'autre tableau contenant des DWORDs, que j'appellerai LocDword2.

Voici LocDword2 avant l'appel à "sub_1316((__int64)LocDword2_4160, n, 1u);" :

```
d7 aa 07 00 a8 d8 0d 00 72 1f 0b 00 30 9d 01 00
e5 11 f7 ff 5f f6 0a 00 c2 7a f5 ff 0e a5 f6 ff
1e aa 04 00 1d 6b 0e 00 fb c8 f8 ff 8e f5 07 00
00 e0 09 00 4b 13 f1 ff 9a 3e f3 ff 5a 1f 03 00
dc 91 f3 ff a7 b5 fa ff 63 d9 04 00 00 d0 fd ff
63 79 ff ff b9 71 03 00 b3 b7 08 00 08 de 09 00
1b 98 07 00 c1 f5 fb ff 78 ee f7 ff b3 ff 0d 00
99 53 09 00 3d 9b f3 ff a7 2b fc ff 17 1b fc ff
96 7f fd ff 8f ac fc ff 31 8b fc ff a5 1b 07 00
71 52 fb ff a4 43 03 00 97 1b f8 ff 36 d4 f2 ff
36 04 ff ff 93 9d 02 00 39 1b f1 ff 2d 72 05 00
41 2b 07 00 fb 34 0a 00 f5 be 07 00 d7 30 f4 ff
f9 ad 07 00 d2 38 0e 00 5c c8 f3 ff 4a 34 0b 00
94 dc 05 00 67 fa f4 ff 64 0c 00 00 65 e9 f6 ff
f5 d1 02 00 07 31 02 00 2b c4 f2 ff c3 a9 0d 00
fc b6 f9 ff 1f 1a f8 ff 15 21 07 00 5b a6 fd ff
d3 14 fb ff ac 53 03 00 6c 5c fc ff 34 a1 01 00
e7 4c ff ff e3 3a f3 ff b6 07 03 00 (00 00 00 00)
```

Ce même LocDword2 après que cette fonction ait fait son travail :

```
1d 6b 0e 00 d2 38 0e 00 b3 ff 0d 00 a8 d8 0d 00
c3 a9 0d 00 4a 34 0b 00 72 1f 0b 00 5f f6 0a 00
fb 34 0a 00 00 e0 09 00 08 de 09 00 99 53 09 00
b3 b7 08 00 8e f5 07 00 f5 be 07 00 f9 ad 07 00
d7 aa 07 00 1b 98 07 00 41 2b 07 00 15 21 07 00
a5 1b 07 00 94 dc 05 00 2d 72 05 00 63 d9 04 00
1e aa 04 00 b9 71 03 00 ac 53 03 00 a4 43 03 00
5a 1f 03 00 b6 07 03 00 f5 d1 02 00 93 9d 02 00
07 31 02 00 34 a1 01 00 30 9d 01 00 64 0c 00 00
63 79 ff ff e7 4c ff ff 36 04 ff ff 00 d0 fd ff
5b a6 fd ff 96 7f fd ff 8f ac fc ff 31 8b fc ff
6c 5c fc ff a7 2b fc ff 17 1b fc ff c1 f5 fb ff
71 52 fb ff d3 14 fb ff a7 b5 fa ff fc b6 f9 ff
fb c8 f8 ff 97 1b f8 ff 1f 1a f8 ff 78 ee f7 ff
e5 11 f7 ff 65 e9 f6 ff 0e a5 f6 ff c2 7a f5 ff
67 fa f4 ff d7 30 f4 ff 5c c8 f3 ff 3d 9b f3 ff
dc 91 f3 ff 9a 3e f3 ff e3 3a f3 ff 36 d4 f2 ff
2b c4 f2 ff 39 1b f1 ff 4b 13 f1 ff (00 00 00 00)
```

Même constatation : on a juste eu une permutation des dwords, mais c'est tout.

A la fin de main(), on voit qu'une comparaison est faite entre :
- Les DWORDs de LocDword1, qui sont parcourus dans l'ordre.
- Les DWORDs de LocDword2, qui sont parcourus dans l'ordre inverse !

Formulé autrement, pour que le programme nous affiche qu'on a trouvé le bon flag, il faut que le premier DWORD de LocDword1 soit égal au dernier DWORD de LocDword2 ; que le second DWORD de LocDword1 soit égal à l'avant-dernier de LocDword2 ; etc.

Maintenant, chose très intéressante : on constate effectivement que le LocDword2 post call à sub_1316(), si on lit les DWORD dans le sens inverse, est très similaire au LocDword1 post-sub_1316() (si on le lit dans l'ordre).

Pour donner un exemple, le dernier dword de LocDword2 (post appel à la fonction) est 0xfff1134b, il est très proche du premier dword de LocDword1 (post appel à la fonction) qui est 0xfff11378
Si on avait trouvé le bon caractère, le 1er dword de LocDword1 aurait dû être égal au dernier de LocDword2 en fait (soit 0xfff1134b).

==> Justement, on va maintenant s'attacher à trouver les bons caractères :)

Pour ça, il suffit de prendre le dword de LocDword2 post-call (le dernier par exemple) et de le soustraire au dword correspondant dans LocDword1 post-call (le premier par exemple).
Ainsi, ça nous donne la "valeur à additionner" au dword de LocDword1 pour qu'il corresponde à la cible (le dword de LocDword2, en l'occurrence 0xfff1134b)
Ceci étant fait on obtiendra la valeur d'un char !

Si on reprend l'exemple que j'ai donné (dernier dword de LocDword2 postcall - premier dword de LocDword1 postcall) on a :
0xfff1134b - 0xfff11317 ==> 52, qui correspond au caractère '4' du flag !

Cool, on a retrouvé un char, c'est bien ! Mais comment on fait pour savoir à quel indice du flag il est, vu que tout semble mélangé ?
Eh bien c'est simple, on prend le dword dans LocDword1 POST call (= 0xfff1134b) qu'on a utilisé pour trouver le char, et on regarde à quel indice du LocDword1 AVANT le call il était situé !
En l'occurrence, dans le LocDword1 original, on voit que "0xfff1134b" est situé en 31ème position !
'4' est donc le 31ème caractère du flag (en partant de 0 pour compter) ! On a pu le remettre dans l'ordre.

Maintenant, j'automatise ce que je viens d'expliquer ici pour le faire sur tous les caractères, dans mon script `solve.py`.
Le script me renvoie finalement : <CSC{665cfa3e0277a889258cc9f6e24c88fc9db654178558de101b8a19af8fb00575}

Le 1er caractère est mauvais, un '<' au lieu d'un 'F', tout simplement à cause de ce que j'ai expliqué au début : le tout premier DWORD a juste été additionné par la valeur 10 ('\n') alors qu'il n'aurait pas fallu qu'il le soit.
Si on fait, dans Python, "chr(ord('<') + 10)" --> on obtient en effet 'F' !

Bref, le flag est donc : FCSC{665cfa3e0277a889258cc9f6e24c88fc9db654178558de101b8a19af8fb00575} !
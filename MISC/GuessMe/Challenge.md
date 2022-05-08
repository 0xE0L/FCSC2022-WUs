# Énoncé 

Devine le secret !
`nc challenges.france-cybersecurity-challenge.fr 2001`
Note : Soyez rapides, la connexion est coupée au bout de cinq minutes.


# Solution

L'idée derrière ce challenge est probablement de nous faire utiliser la méthode mathématique de dichotomie, qui est - à ma connaissance - la plus optimisée pour déterminer algorithmiquement une valeur inconnue en un nombre de "requêtes" le plus limité possible.

Si vous vous souvenez de vos cours de maths de collège/lycée, cette méthode vous rappelle peut-être quelque-chose !
Cette vidéo l'explique super bien et dynamiquement : https://www.youtube.com/watch?v=RVXa_TS31OY
(Si vous n'aimez pas les maths ne prenez pas peur, ici on n'y aura quasiment pas recours, c'est juste pour vous familiariser au principe)

La dichotomie peut servir concrètement dans certains challenges cybers ou dans la vraie vie, par exemple je sais qu'elle peut servir dans certains cas d'injections SQL (notamment "blind"). Cas typique : un mot de passe (ou hash de mot de passe) est présent dans une base de données, mais l'injection ne vous permet pas de l'afficher directement.

La méthode "de base" consiste à "bruteforcer" le 1er caractère du mot de passe en disant que s'il est égal à 'a', il faut sleep() 2 secondes --> si la réponse du serveur tarde, on sait qu'on a bruteforcé le bon caractère, sinon on passe au caractère suivant 'b', puis 'c' etc, jusqu'à trouver le bon caractère.

Eh bien plutôt que d'utiliser cette méthode bruteforce en testant caractère par caractère ('a', 'b', 'c' etc), on peut utiliser la méthode de dichotomie qui permet de l'accélérer grandement !
Si l'on sait que le mot de passe à deviner ne contient que des lettres en minuscules, on peut faire une requête du genre "si le caractère est situé entre 'a' et 'm', sleep 2 secondes" --> si ça sleep() on réduit progressivement le scope jusqu'à tomber sur le bon caractère, si ça ne sleep pas on sait que le caractère sera compris entre 'n' et 'z' et on réduit le scope dans ce champ-là via d'autres requêtes, etc.
Si mes calculs approximatifs sont bons, ça permet de déterminer le bon caractère en 5 essais maximum, alors qu'en méthode de bruteforce char par char de base, il vous faudrait potentiellement jusqu'à 26 essais ! Donc si on doit bruteforcer un mot de passe de 120 caractères, ça fait tout de même gagner un temps conséquent.

Bref, j'imagine que le principe de ce challenge est de nous familiariser avec cette méthode utile. :)

Comme on dispose d'un nombre d'essais limité pour deviner le bon nombre, on est obligés d'utiliser cette méthode. Tester valeur par valeur (1, 2, 3, etc) mettrait un temps fou, sachant que la valeur à deviner peut être située entre 0 et 2^64 (= 1.84E+19... donc bon courage, ça mettrait juste des milliers d'années), et le challenge ne nous laisse pas assez d'essais pour faire ça de toute façon.

Tout ceci est implémenté dans solve.py.
Après quelques dizaines de secondes à dialoguer avec le serveur, on finit par récupérer le flag : FCSC{7b20416c4f019ea4486e1e5c13d2d1667eebac732268b46268a9b64035ab294d}
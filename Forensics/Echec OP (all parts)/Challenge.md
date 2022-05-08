# Note

Le fichier fourni pour le challenge (`fcsc.raw`) faisant 10Go, je ne suis malheureusement pas en mesure de vous le fournir ici. :(

# Énoncé

## [Intro] Étape 0/3

Quel est l'identifiant unique (UUID) de la table de partition de ce disque ? Une fois que vous l'aurez trouvé, encadrez le dans FCSC{} pour obtenir le flag. Par exemple FCSC{1111-2222-3333-4444}.

 * SHA256(fcsc.7z) = fe23478be033fb87db95313650619d95a3756d90d272e82887d70936c7700f5c (5.4GB).
 * SHA256(fcsc.raw) = 18b33658c9fc8e81666f04999bd38cb6709c6a7399d8a43a72028caa278067bf (10GB).

Note : le fichier fcsc.7z est le même pour tous les challenges Echec OP.

## [Forensics] Étape 1/3

L'administrateur de ce serveur a chiffré son disque, le mot de passe est `fcsc2022`.
Quelle est la date de la création du système de fichiers en UTC ?
Le flag est au format ISO 8601, tel que dans l'exemple suivant : FCSC{2022-04-22T06:59:59Z}.

 * SHA256(fcsc.7z) = fe23478be033fb87db95313650619d95a3756d90d272e82887d70936c7700f5c (5.4GB).
 * SHA256(fcsc.raw) = 18b33658c9fc8e81666f04999bd38cb6709c6a7399d8a43a72028caa278067bf (10GB).

Note : le fichier fcsc.7z est le même pour tous les challenges Echec OP.

## [Forensics] Étape 2/3

Retrouvez le mot de passe de l'utilisateur principal de ce serveur. La force ne résout pas tout... Le mot de passe correspond au flag, entouré de FCSC{}, par exemple : FCSC{password}. Aussi, l'administrateur de ce serveur a chiffré son disque et le mot de passe est `fcsc2022`.

 * SHA256(fcsc.7z) = fe23478be033fb87db95313650619d95a3756d90d272e82887d70936c7700f5c (5.4GB).
 * SHA256(fcsc.raw) = 18b33658c9fc8e81666f04999bd38cb6709c6a7399d8a43a72028caa278067bf (10GB).

Note : le fichier fcsc.7z est le même pour tous les challenges Echec OP.

## [Forensics] Étape 3/3

L'administrateur semble avoir essayé de dissimuler l'une de ses adresses IP avec laquelle il a administré ce serveur. Aidez nous à retrouver cette adresse. Une fois l'IP trouvée, encadrez-la dans FCSC{} pour avoir le flag (par exemple : FCSC{1.2.3.4}).

Attention : vous n'avez que 5 essais.

 * SHA256(fcsc.7z) = fe23478be033fb87db95313650619d95a3756d90d272e82887d70936c7700f5c (5.4GB).
 * SHA256(fcsc.raw) = 18b33658c9fc8e81666f04999bd38cb6709c6a7399d8a43a72028caa278067bf (10GB).

```
Note :
Le fichier fcsc.7z est le même pour tous les challenges Echec OP.
Le disque est chiffré, le mot de passe est fcsc2022.
```
# Énoncé

Pour votre première analyse, on vous confie le téléphone du PDG de GoodCorp.
Ce dernier est certain que les précieuses photos stockées sur son téléphone sont récupérées par un acteur malveillant.
Vous décidez de mettre en place une capture réseau sur le téléphone, afin de voir ce qu'il en est...

`SHA256(capture.cap) = 7b63c22567098f829dfdc190b6f531bbdf23a23e222508752a0a5e5dfa28259c (61Mo).`

Note : les épreuves C-3PO, R2-D2 et R5-D4 sont indépendantes

# Solution

En inspectant la capture réseau, j'observe ceci :
- IP victime:   10.0.2.16
- IP attaquant: 172.18.0.1 (port 1337)

L'échange malveillant débute au paquet 48294, il semble s'agir d'un meterpreter... Possible que l'attaquant extraie des données en utilisant ce canal. Mais jusque-là rien de bien intelligible.

Par contre, à partir de paquet 52809, le graal.
Cette fois, dans les échanges, on trouve du base64... En le décodant en ligne, je vois via son header qu'il semble s'agir d'un PNG.
Je décide donc de décoder l'image encodée en base64 [ici](https://codebeautify.org/base64-to-image-converter) ; je la récupère bien ensuite :

![Image récupérée dans la capture](./img/flag.png)

Et dedans est contenu le flag !
FCSC{2d47d546d4f919e2d50621829a8bd696d3cd1938}
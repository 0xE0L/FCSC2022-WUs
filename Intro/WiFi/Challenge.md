# Énoncé 

Saurez-vous déchiffrer cette capture Wi-Fi ?

Le mot de passe du réseau est `FCSC p0w3r is the answer`.

`SHA256(intro-wifi.pcap.xz) = ef484cf1bde9f6f57fe606ed4e259a585f5b5c023acbdf567d712c31a2396f7c.`


# Solution

On va devoir déchiffrer la capture, dont on voit qu'il s'agit de 802.11.
On commence donc par lire la doc de Wireshark à propos de ce protocole : https://wiki.wireshark.org/HowToDecrypt802.11

Je pars à ce moment-là du principe qu'il s'agit probablement d'une authentification via wpa-pwd.
On sait que le mot de passe est : `FCSC p0w3r is the answer`.

Pour paramétrer le déchiffrement dans Wireshark, il suffit de faire clic droit sur un paquet 802.11 --> Préférences du Protocole --> IEEE 802.11 wireless LAN --> Decryption keys.
On ajoute ensuite une clé "wpa-pwd", et un couple "psw:ssid" soit `FCSC p0w3r is the answer:FCSC-WiFi`.

Ensuite les paquets sont effectivement déchiffrés et une capture HTTP en clair apparaît.
En suivant le flux TCP/HTTP on voit le flag s'afficher !

Flag : FCSC{60d67d7de8aadb7d1241de9a6fdf9148982d2363eab88e862bb98402ac835c8f}
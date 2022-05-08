# Énoncé 

J'ai développé un gestionnaire de mots de passe super sécurisé, seulement il est complètement bogué et je n'ai plus accès ni au code ni au binaire :(((

En effet, il ouvre bien mon fichier de mots de passe, mais ensuite il refuse de m'afficher son contenu !!!

Heureusement, avant de me faire déconnecter du serveur j'ai réussi à lancer GDB, peut-être que vous pourrez m'aider ?

`nc challenges.france-cybersecurity-challenge.fr 2200`

# Solution

En faisant un `disas main` dans gdb, on voit ceci :

```
Dump of assembler code for function main:
   0x0000000000001165 <+0>:     push   rbp
   0x0000000000001166 <+1>:     mov    rbp,rsp
   0x0000000000001169 <+4>:     sub    rsp,0x4b0
   0x0000000000001170 <+11>:    movabs rax,0x491e1e4f4f194b1f
   0x000000000000117a <+21>:    movabs rdx,0x4e481c1d4e191c1d
   0x0000000000001184 <+31>:    mov    QWORD PTR [rbp-0x460],rax
   0x000000000000118b <+38>:    mov    QWORD PTR [rbp-0x458],rdx
   0x0000000000001192 <+45>:    movabs rax,0x4e12484f1818181a
   0x000000000000119c <+55>:    movabs rdx,0x4b1f491f1c181348
   0x00000000000011a6 <+65>:    mov    QWORD PTR [rbp-0x450],rax
   0x00000000000011ad <+72>:    mov    QWORD PTR [rbp-0x448],rdx
   0x00000000000011b4 <+79>:    movabs rax,0x184c18131f1a1b1a
   0x00000000000011be <+89>:    movabs rdx,0x1b1b194b4b1e4e1e
   0x00000000000011c8 <+99>:    mov    QWORD PTR [rbp-0x440],rax
   0x00000000000011cf <+106>:   mov    QWORD PTR [rbp-0x438],rdx
   0x00000000000011d6 <+113>:   movabs rax,0x4c1f49181d4b1f48
   0x00000000000011e0 <+123>:   movabs rdx,0x131f4819131c4e1f
   0x00000000000011ea <+133>:   mov    QWORD PTR [rbp-0x430],rax
   0x00000000000011f1 <+140>:   mov    QWORD PTR [rbp-0x428],rdx
   0x00000000000011f8 <+147>:   mov    DWORD PTR [rbp-0x420],0x5e525e04
   0x0000000000001202 <+157>:   mov    QWORD PTR [rbp-0x4b0],0x0
   0x000000000000120d <+168>:   mov    QWORD PTR [rbp-0x4a8],0x0
   0x0000000000001218 <+179>:   mov    QWORD PTR [rbp-0x4a0],0x0
   0x0000000000001223 <+190>:   mov    QWORD PTR [rbp-0x498],0x0
   0x000000000000122e <+201>:   mov    QWORD PTR [rbp-0x490],0x0
   0x0000000000001239 <+212>:   mov    QWORD PTR [rbp-0x488],0x0
   0x0000000000001244 <+223>:   mov    QWORD PTR [rbp-0x480],0x0
   0x000000000000124f <+234>:   mov    QWORD PTR [rbp-0x478],0x0
   0x000000000000125a <+245>:   mov    DWORD PTR [rbp-0x470],0x0
   0x0000000000001264 <+255>:   mov    BYTE PTR [rbp-0x46c],0x0
   0x000000000000126b <+262>:   lea    rdi,[rip+0xd96]        # 0x2008
   0x0000000000001272 <+269>:   call   0x1030 <puts@plt>
   0x0000000000001277 <+274>:   mov    rax,QWORD PTR [rip+0x2dca]        # 0x4048 <stdout@GLIBC_2.2.5>
   0x000000000000127e <+281>:   mov    rdi,rax
   0x0000000000001281 <+284>:   call   0x1050 <fflush@plt>
   0x0000000000001286 <+289>:   mov    DWORD PTR [rbp-0x4],0x0
   0x000000000000128d <+296>:   jmp    0x12b1 <main+332>
   0x000000000000128f <+298>:   mov    eax,DWORD PTR [rbp-0x4]
   0x0000000000001292 <+301>:   cdqe
   0x0000000000001294 <+303>:   movzx  eax,BYTE PTR [rbp+rax*1-0x460]
   0x000000000000129c <+311>:   xor    eax,0x2a
   0x000000000000129f <+314>:   mov    edx,eax
   0x00000000000012a1 <+316>:   mov    eax,DWORD PTR [rbp-0x4]
   0x00000000000012a4 <+319>:   cdqe
   0x00000000000012a6 <+321>:   mov    BYTE PTR [rbp+rax*1-0x4b0],dl
   0x00000000000012ad <+328>:   add    DWORD PTR [rbp-0x4],0x1
   0x00000000000012b1 <+332>:   cmp    DWORD PTR [rbp-0x4],0x43
   0x00000000000012b5 <+336>:   jle    0x128f <main+298>
   0x00000000000012b7 <+338>:   lea    rax,[rbp-0x4b0]
   0x00000000000012be <+345>:   mov    esi,0x0
   0x00000000000012c3 <+350>:   mov    rdi,rax
   0x00000000000012c6 <+353>:   mov    eax,0x0
   0x00000000000012cb <+358>:   call   0x1060 <open@plt>
   0x00000000000012d0 <+363>:   mov    DWORD PTR [rbp-0x8],eax
   0x00000000000012d3 <+366>:   cmp    DWORD PTR [rbp-0x8],0x0
   0x00000000000012d7 <+370>:   jns    0x12e5 <main+384>
   0x00000000000012d9 <+372>:   lea    rdi,[rip+0xd58]        # 0x2038
   0x00000000000012e0 <+379>:   call   0x1030 <puts@plt>
   0x00000000000012e5 <+384>:   lea    rcx,[rbp-0x410]
   0x00000000000012ec <+391>:   mov    eax,DWORD PTR [rbp-0x8]
   0x00000000000012ef <+394>:   mov    edx,0x80
   0x00000000000012f4 <+399>:   mov    rsi,rcx
   0x00000000000012f7 <+402>:   mov    edi,eax
   0x00000000000012f9 <+404>:   call   0x1040 <read@plt>
   0x00000000000012fe <+409>:   mov    DWORD PTR [rbp-0xc],eax
   0x0000000000001301 <+412>:   mov    eax,DWORD PTR [rbp-0xc]
   0x0000000000001304 <+415>:   cdqe
   0x0000000000001306 <+417>:   mov    QWORD PTR [rbp+rax*8-0x410],0x0
   0x0000000000001312 <+429>:   mov    eax,0x0
   0x0000000000001317 <+434>:   leave
   0x0000000000001318 <+435>:   ret
```

Je finis par comprendre ceci : le programme arrive bien à ouvrir le fichier (open) et lire son contenu pour le copier dans un buffer (read), mais ne print tout simplement pas ce buffer !
On va donc devoir l'afficher nous-même.

Pour cela, je mets un breakpoint sur l'appel à read() à main+404 : `break *main+404`, puis je lance le programme pour atteindre ce breakpoint via `run`.
Ce qui m'intéresse, c'est de récupérer l'adresse du buffer où il va copier le contenu (le flag) du fichier lu.
Comme nous sommes en x64 et que read() prend l'adresse du buffer où copier le contenu en second argument, je sais que l'adresse de ce buffer est dans RSI.

Je fais donc un `info reg`, et voit en l'occurrence que l'adresse du buffer contenue dans RSI est 0x7ffe2f986270.
Je souhaite maintenant exécuter le call à read() sur lequel je viens de breakpointer, donc je tape la commande GDB `ni` (comme "next instruction").

L'appel à read() ayant été effectué, notre buffer doit maintenant contenir le flag.
Je fais un `x /s 0x7ffe2f986270` pour afficher le contenu qui se trouve à l'adresse du buffer sous forme de string.

Output, le flag! :
```
"0x7ffe2f986270: "FCSC{da8ae129af8512620bc6c9a711392395fba426edc6713819c1baffe004024ff2}\n""
```
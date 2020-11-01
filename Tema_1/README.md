# Tema 1 Securitatea Informatiei

Trei scripturi in python care comunica intre ele prin `UDP` pentru a trimite un mesaj criptat prin ECB sau OFB de la un nod la celalalt. A fost folosit `UDP` si nu `TCP` intrucat pentru functionalitati similare de scala redusa care sunt rulate pe aceeasi masina nu ar trebuii sa existe o diferenta.

## Testarea pe o masina virtuala de Linux online, oferita de [Repl.it](https://repl.it/) 
 * **RECOMANDAT**
 * codul a suferit putine modificari, acestea fiind necesare pentru a rula cele 3 noduri in procese diferite intrucat masina virtuala nu pune la dispozitie mai multe console pentru a rula separat cele 3 noduri; functionalitatile principale raman aceleasi
 * Pagina de testare: [aici](https://uaicfiisi.ancestormithril.repl.run/)
   * pe pagina de mai sus poate fi urmarita executia algoritmului dupa terminarea instalarii dependintelor
 * Pentru vizualizarea codului si executii personalizate, se acceseaza urmatorul [link](https://repl.it/@ancestormithril/UAICFIISI#Tema_1/main.py)
   * se poate rula apasand `Run` sau: 
     * instalarea din `packages` a modulului `pycrypto` si rularea
     * `python Tema_1/main.py`
   * nu pot fi introdusi parametrii de la linia de comanda dar poate fi deschis fisierul `Tema_1/main.py` si la linia `12` poate fi modificat modul de operare din `OFB` in `ECB`, in fisierul `text.txt` poate fi modificat textul ce va fi transmis iar in `keys.txt` pot fi modificate cheile de criptare
   * doar pentru prima rulare se configureaza masina virtuala si este instalata biblioteca necesara automat odata cu apasarea butonului `Run`, iar apoi in aceeasi sesiune de lucru pot fi rulate teste multiple


## Pregatirea mediului de lucru local
  * Conditii necesare:
    * Windows sau o arhitectura de Linux pe 64 de biti
    * Un environment de python3.6.9 sau orice versiune ulterioara
    * Existenta in environmentul de python curent a bibliotecii `pycrypto` si inexistenta bibliotecii `pycryptodome`
  * In cazul in care nu sunt satisfacute conditiile anterioare
    * Se descarca [lubuntu Alternate 64-bit](http://cdimage.ubuntu.com/lubuntu/releases/18.04/release/lubuntu-18.04-alternate-amd64.iso)
    * Dupa instalarea si pornirea masinii virtuale de la linkul de mai sus, se face actualizarea systemului
    * Se verifica daca exista python3.6.9 sau orice versiune ulterioara (testarea personala a confirmat ca este fara a fi nevoie de o actiune ulterioara)
    * Se verifica existenta pachetelor de python `pycrypto` si inexistenta bibliotecii `pycryptodome` prin deschiderea unui terminal cu environmentul curent de python si rularea
      ```
      python3
      >>>from Crypto.Cipher import AES
      ```
      * pe masina virtuala de mai sus, `pycrypto` exista default la probare
    * In caz de eroare se instaleaza bibliotecile prin urmatoarele comenzi:
      ```
      pip uninstall pycryptodome
      pip install pycrypto
      ```
      * sau daca nu exista `pip`
      ```
      sudo apt-get install build-essential python3-dev
      pip uninstall pycryptodome
      pip install pycrypto
      ```

## Rulare
In directorul curent, urmatoarea ordine:
  * terminalul 1:
    ```
    <your-path-to-python> server_km.py
    ```
    * va porni serverul `KeyManager`, server UDP, care poate fi lasat pornit pe tot parcursul testarii comunicarii intre A si B
    * `KM` va asculta in permanenta pentru mesaje de tipul `ECB` sau `OFB` si de fiecare data va trimite inapoi `cheia 1` sau `cheia 2` criptata cu `cheia 3` 
    * Pentru oprire se foloseste `KeyboardInterrupt`
  * terminalul 2:
    ```
    <your-path-to-python> client_b.py
    ```
    * porneste nodul `B`, in mod server, va astepta mesaje de la nodul `A` pentru inceperea comunicarii, dupa care va solicita de la `KM` o cheie, ulterior va anunta nodul `A` de posibilitatea inceperii comunicarii si in cele din urma va astepta mesajul de la nodul `A`, il va decripta si afisa pe `stdout`
  * terminalul 3:
    ```
    <your-path-to-python> client_a.py <operation-mode> <file-to-be-sent>
    ```
    * `<operation-mode>` poate fi doar `ECB` sau `OFB`
    * `<file-to-be-sent>` este un fisier text cu mesajul care se vrea criptat
    * exemplu:
    ```
    <your-path-to-python> client_a.py ECB text.txt
    <your-path-to-python> client_a.py OFB text.txt
    ```
    * Va porni nodul `A`, care va anunta nodul `B` de protocolul de comunicare si va cere de la `KM` cheia pe care o va folosi in inciptarea mesajului ce va fi trimis la nodul `B` de indata ce nodul `A` primeste confirmarea de la `B` ca este disponibil pentru primirea mesajului
  * Nodurile `B` si `A` trebuie pornite in aceasta ordine de fiecare data cand se doreste testarea scripturilor.
  * `<your-path-to-python>` poate fi de obicei `python3` sau `python.exe` sau doar `python`, iar in alte cazuri calea completa catre interpretatorul de `Python`
  
## Comunicare
![Diagrama Comunicare](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggVERcbiAgQVtBXSAtLT58T0ZCL0VDQnwgQltCXVxuICBCMVtCXSAtLT4gfENlcmUgY2hlaWEgcGVudHJ1IE9GQi9FQ0J8QzFbS01dXG4gIEExW0FdIC0tPiB8Q2VyZSBjaGVpYSBwZW50cnUgT0ZCL0VDQnxDMltLTV1cbiAgQzJbS01dIC0tPiB8VHJpbWl0ZSBjaGVpYSBwZW50cnUgT0ZCL0VDQnxBMVtBXVxuICBDMVtLTV0gLS0-IHxUcmltaXRlIGNoZWlhIHBlbnRydSBPRkIvRUNCfEIxW0JdXG4gIEIyW0JdIC0tPiB8QW51bnRhIGNhIGUgZGlzcG9uaWJpbHxBMltBXVxuICBBMltBXSAtLT4gfFRyaW1pdGUgbWVzYWp1bCBpbmNyaXB0YXR8QjJbQl1cblx0XHQiLCJtZXJtYWlkIjp7InRoZW1lIjoiZGVmYXVsdCIsInRoZW1lVmFyaWFibGVzIjp7ImJhY2tncm91bmQiOiJ3aGl0ZSIsInByaW1hcnlDb2xvciI6IiNFQ0VDRkYiLCJzZWNvbmRhcnlDb2xvciI6IiNmZmZmZGUiLCJ0ZXJ0aWFyeUNvbG9yIjoiaHNsKDgwLCAxMDAlLCA5Ni4yNzQ1MDk4MDM5JSkiLCJwcmltYXJ5Qm9yZGVyQ29sb3IiOiJoc2woMjQwLCA2MCUsIDg2LjI3NDUwOTgwMzklKSIsInNlY29uZGFyeUJvcmRlckNvbG9yIjoiaHNsKDYwLCA2MCUsIDgzLjUyOTQxMTc2NDclKSIsInRlcnRpYXJ5Qm9yZGVyQ29sb3IiOiJoc2woODAsIDYwJSwgODYuMjc0NTA5ODAzOSUpIiwicHJpbWFyeVRleHRDb2xvciI6IiMxMzEzMDAiLCJzZWNvbmRhcnlUZXh0Q29sb3IiOiIjMDAwMDIxIiwidGVydGlhcnlUZXh0Q29sb3IiOiJyZ2IoOS41MDAwMDAwMDAxLCA5LjUwMDAwMDAwMDEsIDkuNTAwMDAwMDAwMSkiLCJsaW5lQ29sb3IiOiIjMzMzMzMzIiwidGV4dENvbG9yIjoiIzMzMyIsIm1haW5Ca2ciOiIjRUNFQ0ZGIiwic2Vjb25kQmtnIjoiI2ZmZmZkZSIsImJvcmRlcjEiOiIjOTM3MERCIiwiYm9yZGVyMiI6IiNhYWFhMzMiLCJhcnJvd2hlYWRDb2xvciI6IiMzMzMzMzMiLCJmb250RmFtaWx5IjoiXCJ0cmVidWNoZXQgbXNcIiwgdmVyZGFuYSwgYXJpYWwiLCJmb250U2l6ZSI6IjE2cHgiLCJsYWJlbEJhY2tncm91bmQiOiIjZThlOGU4Iiwibm9kZUJrZyI6IiNFQ0VDRkYiLCJub2RlQm9yZGVyIjoiIzkzNzBEQiIsImNsdXN0ZXJCa2ciOiIjZmZmZmRlIiwiY2x1c3RlckJvcmRlciI6IiNhYWFhMzMiLCJkZWZhdWx0TGlua0NvbG9yIjoiIzMzMzMzMyIsInRpdGxlQ29sb3IiOiIjMzMzIiwiZWRnZUxhYmVsQmFja2dyb3VuZCI6IiNlOGU4ZTgiLCJhY3RvckJvcmRlciI6ImhzbCgyNTkuNjI2MTY4MjI0MywgNTkuNzc2NTM2MzEyOCUsIDg3LjkwMTk2MDc4NDMlKSIsImFjdG9yQmtnIjoiI0VDRUNGRiIsImFjdG9yVGV4dENvbG9yIjoiYmxhY2siLCJhY3RvckxpbmVDb2xvciI6ImdyZXkiLCJzaWduYWxDb2xvciI6IiMzMzMiLCJzaWduYWxUZXh0Q29sb3IiOiIjMzMzIiwibGFiZWxCb3hCa2dDb2xvciI6IiNFQ0VDRkYiLCJsYWJlbEJveEJvcmRlckNvbG9yIjoiaHNsKDI1OS42MjYxNjgyMjQzLCA1OS43NzY1MzYzMTI4JSwgODcuOTAxOTYwNzg0MyUpIiwibGFiZWxUZXh0Q29sb3IiOiJibGFjayIsImxvb3BUZXh0Q29sb3IiOiJibGFjayIsIm5vdGVCb3JkZXJDb2xvciI6IiNhYWFhMzMiLCJub3RlQmtnQ29sb3IiOiIjZmZmNWFkIiwibm90ZVRleHRDb2xvciI6ImJsYWNrIiwiYWN0aXZhdGlvbkJvcmRlckNvbG9yIjoiIzY2NiIsImFjdGl2YXRpb25Ca2dDb2xvciI6IiNmNGY0ZjQiLCJzZXF1ZW5jZU51bWJlckNvbG9yIjoid2hpdGUiLCJzZWN0aW9uQmtnQ29sb3IiOiJyZ2JhKDEwMiwgMTAyLCAyNTUsIDAuNDkpIiwiYWx0U2VjdGlvbkJrZ0NvbG9yIjoid2hpdGUiLCJzZWN0aW9uQmtnQ29sb3IyIjoiI2ZmZjQwMCIsInRhc2tCb3JkZXJDb2xvciI6IiM1MzRmYmMiLCJ0YXNrQmtnQ29sb3IiOiIjOGE5MGRkIiwidGFza1RleHRMaWdodENvbG9yIjoid2hpdGUiLCJ0YXNrVGV4dENvbG9yIjoid2hpdGUiLCJ0YXNrVGV4dERhcmtDb2xvciI6ImJsYWNrIiwidGFza1RleHRPdXRzaWRlQ29sb3IiOiJibGFjayIsInRhc2tUZXh0Q2xpY2thYmxlQ29sb3IiOiIjMDAzMTYzIiwiYWN0aXZlVGFza0JvcmRlckNvbG9yIjoiIzUzNGZiYyIsImFjdGl2ZVRhc2tCa2dDb2xvciI6IiNiZmM3ZmYiLCJncmlkQ29sb3IiOiJsaWdodGdyZXkiLCJkb25lVGFza0JrZ0NvbG9yIjoibGlnaHRncmV5IiwiZG9uZVRhc2tCb3JkZXJDb2xvciI6ImdyZXkiLCJjcml0Qm9yZGVyQ29sb3IiOiIjZmY4ODg4IiwiY3JpdEJrZ0NvbG9yIjoicmVkIiwidG9kYXlMaW5lQ29sb3IiOiJyZWQiLCJsYWJlbENvbG9yIjoiYmxhY2siLCJlcnJvckJrZ0NvbG9yIjoiIzU1MjIyMiIsImVycm9yVGV4dENvbG9yIjoiIzU1MjIyMiIsImNsYXNzVGV4dCI6IiMxMzEzMDAiLCJmaWxsVHlwZTAiOiIjRUNFQ0ZGIiwiZmlsbFR5cGUxIjoiI2ZmZmZkZSIsImZpbGxUeXBlMiI6ImhzbCgzMDQsIDEwMCUsIDk2LjI3NDUwOTgwMzklKSIsImZpbGxUeXBlMyI6ImhzbCgxMjQsIDEwMCUsIDkzLjUyOTQxMTc2NDclKSIsImZpbGxUeXBlNCI6ImhzbCgxNzYsIDEwMCUsIDk2LjI3NDUwOTgwMzklKSIsImZpbGxUeXBlNSI6ImhzbCgtNCwgMTAwJSwgOTMuNTI5NDExNzY0NyUpIiwiZmlsbFR5cGU2IjoiaHNsKDgsIDEwMCUsIDk2LjI3NDUwOTgwMzklKSIsImZpbGxUeXBlNyI6ImhzbCgxODgsIDEwMCUsIDkzLjUyOTQxMTc2NDclKSJ9fSwidXBkYXRlRWRpdG9yIjpmYWxzZX0)

## Explicatii suplimentare

### Modulul `init`
Este un modul de initializare, comun celor 3 noduri. Ofera o metoda de recuperare a vectorului de initializare `iv` si o metoda de aflare a datelor necesare pentru conectarea la un nod oferit ca parametru, adica `HOST` si `PORT`

### Modulul `functions`
Modul comun celor 3 noduri. Contine metode utile precum:
 * `pad` -> primeste un sir si il intoarce padat
 * `get_encoded_string` -> primeste un sir clar si un cifru si intoarce sirul initial criptat cu cifrul respectiv
 * `get_decoded_string` -> primeste un sir criptat si un cifru, intoarce sirul in clar decriptat cu cifrul respectiv
 * `string_xor` -> primeste doua siruri si intoarce operatia de xor asupra celor 2 siruri
 * `split_string_into_chunks` -> primeste un sir si o dismensiune si intoarce sirul initial impartit in bucati de dimensiunea ceruta
 * `send_message_request` -> primeste numele unui nod si un mesaj si incearca sa trimita mesajul la nodul respectiv folosind protocolul `UDP`
 * `encrypt_message` -> primeste un mesaj, o cheie, un mod de operare si un vector de initializare; aplica OFB sau ECB pe mesaj folosind cheia si eventual vectorul de initializare; la `ECB` imparte mesajul in bucati si le cripteaza pe fiecare cu cheia data; la `OFB` imparte mesajul in bucati, cripteaz vectorul de initializare pentru fiecare bucata si face `xor` intre fiecare rezultat al criptarii si bucata de mesaj
 * `decrypt_message` -> la fel ca `encrypt_message`, numai ca invers

### Nodul `KM`
Este un server `UDP` pe mai multe fire de executie, ruleaza in permanenta pana la primirea de pe `stdin` a unui mesaj oarecare.

Asculta mesaje si daca mesajul primit este `ECB` sau `OFB`, citeste din fisiere `key_1` si `key_2`, le cripteaza cu `key_3` si `ECB` (cheile sunt un bloc unitar, de maxim 32 de caractere) si le trimite inapoi.

### Nodul `A`

Primeste de la linia de comanda modul de operare si fisierul unde se afla mesajul care trebuie timis la `B`. Il anunta pe `B` de iminenta unei comunicari si de modul de operare, pentru a face pregatirile de cuviinta.

Obtine datele necesare pentru criptare prin trimiterea unui mesaj la serverul `UDP` `KM`, de la care primeste o cheie criptata cu `key_3`, comuna celor 3 noduri. 

Asteapta sub forma de server `UDP` mesajul in care `B` confirma ca e pregatit pentru comunicare. Intrerupe modul de server si ii trimite un mesaj `UDP` lui B.

### Nodul `B`

Este pornit ca server `UDP` care asteapta modul de operare de la `A`. La primirea mesajului, iese din modul server si cere de la `KM` cheia corespunzatoare. Dupa ce primeste si decripteaza cheia, il anunta pe `A` ca poate sa inceapa trimiterea mesajului. Imediat dupa, intra in modul de server `UDP`.


# Tema 1 Securitatea Informatiei

Trei scripturi in python care comunica intre ele prin UDP pentru a trimite un mesaj criptat prin ECB sau OFB de la un nod la celalalt.


## Pregatirea mediului de lucru
  * Conditii necesare:
    * Windows sau o arhitectura de Linux pe 64 de biti
    * Un environment de python3.6.9 sau orice versiune ulterioara
    * Existenta in environmentul de python curent a bibliotecilor `pycrypto` si inexistenta bibliotecii `pycryptodome`
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
    * `KM` va asculta in permanenta pentru mesaje de tipul `ECB` sau `OFB` si de fiecare data va trimite inapoi `cheia 1` sau `cheia 2` incriptata cu `cheia 3` 
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
    * `<file-to-be-sent>` este un fisier text cu mesajul care se vrea incriptat
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

### Nodul `KM`

### Nodul `A`

### Nodul `B`


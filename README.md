#nump Emulatore di un cubo di Rubik

Questo programma ha lo scopo di consentire all'utente di utilizzare un cubo di Rubik digitale: su un display vengono visualizzate tutte le facce del cubo ed è possibile ruotare il cubo nei modi standard, che sono spiegati poco sotto, come si farebbe con un cubo reale.
E' anche possibile, grazie alle funzioni della libreria `pyvista`, avere una vista cartesiana in 3D del cubo (è possibile anche, con una leggera modifica al codice - bisogna inserire il parametro `True` alla chimata della funzione `plt.plot_cube()` alla riga 182 del file `app.py` - passare ad una vista isometrica).

## Possibili Mosse
|Mossa |Rispettivo nel cubo |
|:----------: |:----------: |
|U |Gira il lato sopra in senso orario|
|U'|Gira il lato sopra in senso antiorario|
|F|Gira il lato frontale in senso orario|
|F'|Gira il lato frontale in senso antiorario|
|R|Gira il lato a destra in senso orario|
|R'|Gira il lato a destra in senso antiorario|
|L|Gira il lato a sinista in senso orario|
|L'|Gira il lato a sinista in senso antiorario|
|B|Gira il lato a dietro in senso orario|
|B'|Gira il lato a dietro in senso antiorario|
|D|Gira il lato sotto in senso orario|
|D'|Gira il lato sotto in senso antiorario|

## Installazione dei requisiti

### <font color="red" > ATTENZIONE </font>
> Questo programma è in gardo di funzionare solo su sistemi operativi Windows

Per utilizzare il programma è necessario Python 3 (che deve essere **incluso nel path**), che è installabile in Windows direttamente da MS Store.
OLtre alla librerie di sistema, è necessario installare le librerie `numpy`, `colorama` e `pyvista`. E' possibile farlo tramite l'installer di pacchetti Python `pip`:
```bash
pip install numpy pyvista colorama
```
Per il software di Intelligenza artificiale, viene usata la libreria `PyTorch`. Amch'essa deve essere installata tramite `pip`, ma bisogna configurare l'installazione dal sito ufficiale di [`PyTorch`](https://pytorch.org/get-started/locally/) perché nel caso in cui si disponesse di una **GPU Nvidia** è consigliabile eseguire i calcoli di AI sui **CUDA Cores**. IL programma è in grado di passare automaticamente su CUDA in caso fossero disponibili; nel caso non si disponesse di una GPU Nvidia, installare solo la versione di `PyTorch` per CPU.

### <font color="red" > ATTENZIONE </font>
> Nel caso si installasse `PyTorch` con supporto CUDA, verrà scaricata l'intera suite di CUDA che può arrivare a pesare diversi gigabite (3.6GB nel caso della versione 12.9 supportata dalla mia 5060 ti).

## Clonaggio del reperstory
E' possibile conare il reperstory con `git` tramite il protocollo `https`:
```cmd
git clone https://github.com/giacobarzo08/Rubiks_cube_AI_emulator.git
```
E' necessario installare `git` nel caso non lo fosse già.
Installazione dal terminale (PowerShell o cmd) di windows:
```cmd
winget install git
REM riavviare il computer
```

## Utilizzo del programma
E' possibile accedere a tutte le risorse lanciando il file `main.py`. Il dispaly mostrerà tutte le possibilità.

```cmd
python main.py
```

E' consigliato eseguire prima il file `ai_lerner.py` per addestrare il modello di intelligenza artificiale, almeno finché il livello ri ramdonnes non scende al di sotto del 5%.
```cmd
python ai_lerner.py
```

## Ancora in elaborazione
Stiamo ancora migliorando questo progetto. Se notate bug, per favore fatecelo sapere.

# Licenza
Questo progetto è protetto da **licenza LGPL-3.0** - di cui copia conservata in questo reperstory - perché la stessa usata da altre persone per proteggere i propri lavori sfruttati per la realizzazione di questo progetto (che si trovano esclusivamente nei file `ai_lerner` e `rubiks.py`). Sentitevi liberi di applicare a tutte le altre parti del progetto le clausole della **licenza MIT**.

### <font color="red" > ATTENZIONE </font>
> Ci teniamo a ringraziare [scumaym](https://github.com/shumaym) per avere creato [questo](https://github.com/shumaym/Rubiks_Cube_AI) reperstory che ci ha aiutato molto nel nostro progetto.

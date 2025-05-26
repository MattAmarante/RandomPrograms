# IMPORTANTE
Questo programma è leggermente diverso da quello del professore, quindi non aspettatevi una
replica 1:1..

Sono riuscito a risolvere il problema che avevamo in classe e se ve lo chiedete è una stronzata.
Nel file "Dispatcher.py", nella funzione che io ho chiamato "prc_HandleConnection", separiamo
con la split il messaggio decodificato. Il problema è che la split restituisce la lista

["getCmd ","Parametro"]

Ma "getCmd " != "getCmd" (lo spazio rompe le palle) quindi praticamente saltavamo sempre l'if.

Il secondo problema è particolare ed è qualcosa che dobbiamo chiedere al professore, poichè ho
notato che a volte due pacchetti TCP si uniscono, quindi l'aggregator si ritrova pacchetti del
tipo "1ACK" che darebbe problemi per come ho implementato la funzione di getCmd.
Per risolvere ho messo una sleep dopo la chiamata getCmd per dare tempo al server di mandare il
pacchetto originale.

Infine vorrei dire che si, il mio codice è molto ingarbugliato, ma scovare il secondo errore
mi ha fatto cambiare molte cose inutili che mi scoccio di rimettere a posto. Forse in futuro
riscriverò tutto in maniera ordinata.
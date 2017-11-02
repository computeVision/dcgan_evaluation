TODO Liste

[] assets, checkpoints, data, logs auf ~/gan verschieben


[] Implementierung aller Möglichkeiten in der Tabelle.

[] Alle Möglichkeiten durchlaufen lassen.

[] PixelWiseNN aufstellen.

[] Nearest Neighbour Imlementierung aufstellen als Ground Truth.

--------------------------------------------------------------------------------
Generator                                  | Degenerator
-------------------------------------------|------------------------------------
ReLU | L. ReLU | Tanh | Pooling | Batch N. | ReLU | L. ReLU | Tanh | Batch N.
-------------------------------------------|------------------------------------
     |         |      |         |          |      |         |      |
     |         |      |         |          |      |         |      |
     |         |      |         |          |      |         |      |
     |         |      |         |          |      |         |      |
     |         |      |         |          |      |         |      |
     |         |      |         |          |      |         |      |
     |         |      |         |          |      |         |      |
     |         |      |         |          |      |         |      |
     |         |      |         |          |      |         |      |
     |         |      |         |          |      |         |      |
     |         |      |         |          |      |         |      |
     |         |      |         |          |      |         |      |

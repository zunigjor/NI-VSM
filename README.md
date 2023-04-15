# VSM

| Členové               |                      |
|-----------------------|----------------------|
| **Kristýna Janovská** | janovkri@fit.cvut.cz |
| Jakub Rigoci          | rigocjak@fit.cvut.cz |
| Jorge Zuňiga          | zunigjor@fit.cvut.cz |

| Úkol | Body |
|------|------|
| 1    | 5/6  |
| 2    | 0/6  |
| 3    | 0/6  |
| 4    | 0/6  |

## Domácí úkol 1

* (1b) Z obou datových souborů načtěte texty k analýze. Pro každý text zvlášť odhadněte pravděpodobnosti znaků (symbolů včetně mezery), které se v textech vyskytují. Výsledné pravděpodobnosti graficky znázorněte.
* (1b) Pro každý text zvlášť spočtěte entropii odhadnutého rozdělení znaků.
* (2b) Nalezněte optimální binární instantní kód C pro kódování znaků prvního z textů.
* (2b) Pro každý text zvlášť spočtěte střední délku kódu C a porovnejte ji s entropií rozdělení znaků. Je kód
C optimální i pro druhý text?

## Domácí úkol 2

* (1b) Z obou datových souborů načtěte texty k analýze. Pro každý text zvlášť odhadněte základní charakteristiky délek slov, tj. střední hodnotu a rozptyl. Graficky znázorněte rozdělení délek slov.
* (1b) Pro každý text zvlášť odhadněte pravděpodobnosti písmen (symbolů mimo mezery), které se v textech vyskytují. Výsledné pravděpodobnosti graficky znázorněte.
* (1.5b) Na hladině významnosti 5% otestujte hypotézu, že rozdělení délek slov nezávisí na tom, o který jde text. Určete také p-hodnotu testu.
* (1.5b) Na hladině významnosti 5% otestujte hypotézu, že se střední délky slov v obou textech rovnají. Určete také p-hodnotu testu.
* (1b) Na hladině významnosti 5% otestujte hypotézu, že rozdělení písmen nezávisí na tom, o který jde text. Určete také p-hodnotu testu.

Nápověda k bodům 3 a 5: Proveďte test nezávislosti v kontingenční tabulce.

## Domácí úkol 3

Z obou datových souborů načtěte texty k analýze. Pro každý text zvlášť zjistěte absolutní četnosti jednotlivých znaků (symbolů včetně mezery), které se v textech vyskytují. Dále předpokládejme, že první text je vygenerován z homogenního markovského řetězce s diskrétním časem.

* (2b) Za předpokladu výše odhadněte matici přechodu markovského řetězce pro první text. Pro odhad matice přechodu vizte přednášku 17. Odhadnuté pravděpodobnosti přechodu vhodně graficky znázorněte, např. použitím heatmapy.
* (2b) Na základě matice z předchozího bodu najděte stacionární rozdělení π tohoto řetězce pro první text.
* (2b) Porovnejte rozdělení znaků druhého textu se stacionárním rozdělením π, tj. na hladině významnosti 5 % otestujte hypotézu, že rozdělení znaků druhého testu se rovná rozdělení π z předchozího bodu.

## Domácí úkol 4

### Popis problému
Uvažujte model hromadné obsluhy M∣G∣∞.

* Požadavky přichází podle Poissonova procesu s intenzitou λ = 10s<sup>-1</sup>.
* Doba obsluhy jednoho požadavku (v sekundách) má rozdělení S∼Ga(4,2), tj. Gamma s parametry *a* = 4, *p* = 2.
* Časy mezi příchody a časy obsluhy jsou nezávislé.
* Systém má (teoreticky) nekonečně paralelních obslužných míst (každý příchozí je rovnou obsluhován).

Označme N<sub>t</sub> počet zákazníků v systému v čase *t*. Předpokládejme, že na začátku je systém prázdný, tj. N<sub>0</sub> = 0.


* (2b) Simulujte jednu trajektorii { N<sub>t</sub>(ω) ∣ t ∈ (0,10 s)}. Průběh trajektorie graficky znázorněte.
* (2b) Simulujte n = 500 nezávislých trajektorií pro t ∈ (0,100). Na základě těchto simulací odhadněte rozdělení náhodné veličiny N<sub>100</sub>.
* (2b) Diskutujte, jaké je limitní rozdělení tohoto systému pro t → +∞ (vizte přednášku 23.). Pomocí vhodného testu otestujte na hladině významnosti 5%, zda výsledky simulace N<sub>100</sub> odpovídají tomuto rozdělení.

**Upozornění:** Při simulování z Gamma rozdělení si řádně v dokumentaci prostudujte, jaké parametry vámi zvolený nástroj používá. Často je používaná dvojice: shape parameter *k* = *p* a scale parameter *θ* = *1/a*.

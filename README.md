# [cite_start] Inteligentne Rolnictwo – Rekomendacja upraw na podstawie warunków glebowych i pogodowych [cite: 5]

[cite_start]**Autor:** Łukasz Wołoszyn [cite: 1]

##  Charakterystyka projektu
[cite_start]Projekt rozwiązuje problem optymalizacji decyzji w rolnictwie poprzez zastosowanie algorytmów uczenia maszynowego (uczenie nadzorowane)[cite: 7]. [cite_start]Głównym celem jest zbudowanie modelu, który na podstawie zebranych pomiarów środowiskowych (temperatura, opady, minerały w glebie) automatycznie doradza rolnikowi, jaki gatunek rośliny należy zasadzić na danym polu w celu zmaksymalizacji plonów[cite: 8]. 

[cite_start]Jest to klasyczny problem klasyfikacji wieloklasowej, w którym zestaw cech wejściowych przyporządkowywany jest do jednej z 22 możliwych klas docelowych[cite: 9].

##  Zbiór danych
[cite_start]Zbiór danych składa się z **2200 instancji** i nie zawiera braków danych[cite: 11, 12]. [cite_start]Obejmuje 7 cech numerycznych oraz 1 zmienną kategoryczną (docelową)[cite: 11]:

* [cite_start]`N` – zawartość azotu w glebie[cite: 13].
* [cite_start]`P` – zawartość fosforu w glebie[cite: 14].
* [cite_start]`K` – zawartość potasu w glebie[cite: 15].
* [cite_start]`temperature` – temperatura otoczenia w °C[cite: 16].
* [cite_start]`humidity` – wilgotność względna powietrza w %[cite: 17].
* [cite_start]`ph` – odczyn pH gleby[cite: 18].
* [cite_start]`rainfall` – średnia ilość opadów w mm[cite: 19].
* [cite_start]`label` **(Target)** – optymalny gatunek rośliny (łącznie 22 unikalne kategorie, np. ryż, kukurydza, kawa)[cite: 20].

##  Preprocessing i Metodologia
* [cite_start]**Podział danych (Stratyfikacja):** Zastosowano parametr `stratify=y` w celu zachowania reprezentatywnych, równych proporcji każdej z 22 klas w zbiorze treningowym i testowym[cite: 22, 23].
* [cite_start]**Skalowanie cech:** Ze względu na zróżnicowane rzędy wielkości atrybutów (np. setki milimetrów opadów vs. skala pH 0-14), dane poddano standaryzacji przy użyciu `StandardScaler`[cite: 24]. [cite_start]Było to kluczowe zwłaszcza dla optymalnego działania algorytmu k-NN[cite: 25, 37].

##  Modele i Optymalizacja
[cite_start]W ramach projektu zaimplementowano i porównano dwa algorytmy klasyfikacyjne przy użyciu biblioteki `scikit-learn`[cite: 27]:

1. [cite_start]**Random Forest Classifier (Model główny)** [cite: 28]
   * [cite_start]Wykorzystano technikę zespołową (ensemble learning) dla lepszego wychwytywania nieliniowych zależności[cite: 29, 30].
   * [cite_start]Optymalizacja hiperparametrów za pomocą `GridSearchCV` z 5-krotną walidacją krzyżową (CV=5)[cite: 31, 33].
   * [cite_start]Przeszukana siatka: `n_estimators`: [50, 100, 200], `max_depth`: [None, 10, 20][cite: 32].
   * [cite_start]Optymalne parametry: `n_estimators=100`, `max_depth=None`[cite: 41].

2. [cite_start]**k-Nearest Neighbors (Model porównawczy)** [cite: 35]
   * [cite_start]Zaimplementowano z parametrem `k=5`[cite: 35].

##  Wyniki
[cite_start]Modele ewaluowano na zbiorze testowym liczącym 440 instancji[cite: 39]. [cite_start]Algorytm **Random Forest** osiągnął znakomitą skuteczność, przewyższając model porównawczy[cite: 40]:

* [cite_start]**Accuracy (Random Forest):** 99.55% [cite: 40]
* [cite_start]**Accuracy (k-NN):** 97.95% [cite: 40]

Analiza szczegółowych metryk dla modelu Lasu Losowego wykazuje niemal bezbłędną zdolność predykcyjną. [cite_start]Dla zdecydowanej większości z 22 klas metryki **Precision**, **Recall** oraz **F1-score** wynoszą perfekcyjne **1.00**[cite: 42, 43, 46]. [cite_start]Zaledwie w dwóch przypadkach (uprawy o zbliżonych wymaganiach) wystąpiły marginalne pomyłki (np. `rice` sklasyfikowany jako `jute`)[cite: 50, 51].

### Kluczowe wnioski z analizy ważności cech (Feature Importance)
[cite_start]Analiza wykazała jednoznacznie, że w badanym zbiorze czynnikami najbardziej determinującymi sukces danej uprawy są warunki klimatyczne: **dostępność wody (opady)** oraz **wilgotność powietrza**[cite: 52, 62]. [cite_start]Mają one znacznie większe znaczenie decyzyjne niż sam skład chemiczny gleby, podczas gdy najmniej istotnym parametrem okazało się pH gleby[cite: 53, 62].

##  Wizualizacje

*(Dodaj poniżej pliki z wykresami do folderu w swoim repozytorium, np. do folderu `images/`, a następnie odkomentuj poniższe linie)*

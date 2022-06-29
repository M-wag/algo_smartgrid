# Smart Grid

Groene energie is de energie van de toekomst, en zelf produceren is de mode van nu. Veel huizen hebben tegenwoordig zonnepanelen, windmolens of andere installaties om zelf energie mee te produceren. Fortuinlijk genoeg produceren die installaties vaak meer dan voor eigen consumptie nodig is. Het overschot zou kunnen worden terugverkocht aan de leverancier, maar de infrastructuur (het grid) is daar veelal niet op berekend. Om de pieken in consumptie en produktie te kunnen managen moeten er batterijen geplaatst worden.

---

## Vereisten 

Deze codebase is geschreven in Python 3.10

Requirements:

    pip install -r requirements.txt

## Gebruik

Een voorbeeldje kan gerund worden door aanroepen van:

    python main.py [algorithm]

Hierna worden enkele parameters aangevraagd.

### Paramters per Algorithm
base parameters:
- neighborhoud: bepaalde welke wijk word verwerkt
- iteration amount: totale aantal iteraties
- type of wires: mate waarop wires worden aangemaakt
    - hor_ver: wires gaan eerst horizontaal daarna vertical
    - straight: wires gaan rechtstreeks naar hun doel
- number of runs: aantal runs per algorithm

hillclimber:
- restart boundary: aantal runs tot een nieuwe grid wordt aangemaakt

simulated_annealing:
- temperature: temperatuur voor simulated_annealing
- temperate change: temperatuur verandering voor simulated_annealing

k_mean:
- temperature: temperatuur voor simulated_annealing
- temperate change: temperatuur verandering voor simulated_annealing
- begin state: bepaal welke algorithm is gebruikt voor het begin grid (aanbevolen: simulated annealing)

random

### Structuur 

```
algosmartgrid
│   README.md
│   main.py    
│
└───code: bevat alle code van het project
│   └─── code/algorithms: bevat alle code dat nodig is voor het runnen van het project
│   └─── code/classes: bevat de belangrijkste classes van het project
│   └─── code/visualization: bevat de code dat nodig is voor visualize
│   
└───data : benodigde data om grids aan te maken
└───output: bevat de output van de run. elke folder is verdeeld op basis van algorithm characteristics
│   └─── output/hillclimber
│   └─── output/random
│   └─── output/kmean
│   └─── output/simulated_annealing

```

### Auteurs
- Brandon Chin-A-Lien
- Thomas Been
- Stephan Visser

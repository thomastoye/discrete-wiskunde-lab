#!/usr/bin/env python

from pprint import pprint
import sys
from tabulate import tabulate

sys.setrecursionlimit(1500)

"""
Gegeven een restklassenring Zn,+,*. Bepaal de deelgroepen <x> voor alle elementen x e Zxn en controleer de stelling van Lagrange.
"""

n = 126

# Dit laat toe om een argument mee te geven bij het uitvoeren, bv. `./main.py 13`
if (len(sys.argv) > 1):
    n = int(sys.argv[1])

# De klassen Restklassenring
class Restklassenring:

    # Constructor
    def __init__(self, n):
        self.n = n
        print("Restklassenring Z%s,+,* gemaakt" % n)

    # Methode om een Cayleytabel voor * op te stellen
    def cayley_tabel_maal(self):
        return self.cayley_tabel(lambda x, y: x * y)

    # Methode om een Cayleytabel voor + op te stellen
    def cayley_tabel_plus(self):
        return self.cayley_tabel(lambda x, y: x + y)

    # Algemene methode om een Cayleytabel op te stellen. bewerking is een functie (lambda)
    def cayley_tabel(self, bewerking):
        header = [self._make_overline(x) for x in range(0, self.n)]

        tabel = [[self._make_overline(bewerking(row, col) % self.n) for col in range(0, self.n)] for row in
                 range(0, self.n)]

        return tabel

    # Functie die de headers voor de Cayleytabel maakt
    def headers(self):
        header = [self._make_overline(x) for x in range(0, self.n)]
        return header

    # Berekent de eenheden van de restklassenring (retourneert een arary)
    def eenheden(self):
        # waar je 1 uitkomt bij *
        tabel = zip(range(0, self.n), self.cayley_tabel_maal())

        return [x[0] for x in tabel if self._make_overline(1) in x[1]]

    # Berekent de orde van de restklassenring
    def orde(self):
        return len(self.eenheden())

    # Berekent de deelgroepen
    def deelgroepen_Zxn_maal(self):
        # oplopende machten
        inhoud = self.eenheden()

        inhoud_mapped = {}

        def bepaal_distincte_machten_eenheden(eenheden, distinct, current_value):
            """<x> = { x^0, x^1, ..., x^n }"""
            new_value = (x * current_value) % self.n

            if(new_value in distinct):
                return distinct

            distinct.add(new_value)

            return bepaal_distincte_machten_eenheden(eenheden, distinct, new_value) # recursieve definitie


        for x in inhoud:
            start = (x * x) % self.n
            distinct = bepaal_distincte_machten_eenheden(inhoud, {start}, start)

            inhoud_mapped[x] = len(distinct)

        return inhoud_mapped

    # Berekent de generatoren
    def generatoren(self):
        result = []

        d = self.deelgroepen_Zxn_maal()
        for key in d:
            if (d[key] == self.n - 1):
                result.append(key)

        return result

    # Plaats een streepje boven getallen (met Unicode) voor de duidelijkheid
    def _make_overline(self, x):
        return ''.join([char + '\u0305' for char in str(x)])


r = Restklassenring(n)
orde = r.orde()

print('Cayleytabel voor +')
print(tabulate(r.cayley_tabel_plus(), r.headers(), showindex=True))
print('\n')

print('Cayleytabel voor *')
print(tabulate(r.cayley_tabel_maal(), r.headers(), showindex=True))
print('\n')

print('Eenheden')
pprint(r.eenheden())
print('\n')

print('Orde: ' + str(r.orde()))
print('\n')

print('Deelgroepen voortgebracht door x\u0305 element van Zx%s,*' % n)
deelgroepen = r.deelgroepen_Zxn_maal()
lagrange_klopt = True

for key in deelgroepen:
    print(' |<' + str(key) + '\u0305>| = ' + str(deelgroepen[key]) + '\t\t' + str(orde) + ' % ' + str(deelgroepen[key]) + '\t = ' + str(orde % deelgroepen[key]) + ' (Lagrange)')

    if orde % deelgroepen[key] != 0:
        lagrange_klopt = False

if lagrange_klopt:
    print('\n ==> De stelling van Lagrange klopt')
else:
    print('\n ==> De stelling van Lagrange klopt NIET')

print('\n\n')

print('Generatoren')
print(r.generatoren())

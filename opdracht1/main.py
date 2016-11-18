#!/usr/bin/env python

from pprint import pprint
import sys
from tabulate import tabulate

"""
Gegeven een restklassenring Zn,+,*. Bepaal de deelgroepen <x> voor alle elementen x e Zxn en controleer de stelling van Lagrange.
"""

n = int(sys.argv[1])
#n = 5

class Restklassenring:

  def __init__(self, n):
    self.n = n
    print("Restklassenring Z%s,+,* gemaakt" % n)

  def cayley_tabel_maal(self):
    return self.cayley_tabel(lambda x, y: x * y)

  def cayley_tabel_plus(self):
    return self.cayley_tabel(lambda x, y: x + y)

  def cayley_tabel(self, bewerking):
    header = [self._make_overline(x) for x in range(0, self.n)]

    tabel = [ [ self._make_overline(bewerking(row, col) % self.n) for col in range(0, self.n) ] for row in range(0, self.n) ]

    return tabel

  def headers(self):
    header = [self._make_overline(x) for x in range(0, self.n)]
    return header

  def eenheden(self):
    # waar je 0 uitkomt bij *
   tabel = zip(range(0, self.n), self.cayley_tabel_maal())

   return [x[0] for x in tabel if self._make_overline(1) in x[1]]

  def generatoren(self):
    return [x[0] for x in zip(range(0, self.n), self.cayley_tabel_maal()) if set(x[1]) == set(range(self.n))]

  def orde(self):
    return len(self.eenheden())

  def deelgroepen1(self):
    return self.deelgroepen(self.cayley_tabel_maal())

  def deelgroepen2(self):
    inhoud = self.generatoren()

    lookup = { x: {} for x in inhoud } # will be 2D, e.g. lookup[1][3]

    for x in inhoud:
      for y in inhoud:
        lookup[x][y] = (x * y) % self.n

    inhoud_mapped = {}

    for x in inhoud:
      start = lookup[x][x]
      distinct = {start}
      current_value = start

      while(True):
        new_value = lookup[x][current_value]

        if(new_value in distinct):
          break

        distinct.add(new_value)
        current_value = new_value

      inhoud_mapped[x] = len(distinct)

    return inhoud_mapped

  def deelgroepen(self, tabel):
    result = {}

    for el in zip(range(0, self.n), tabel):
      result[el[0]] = len(set(el[1]))

    return result

  def totient(self, n):
      """
      totient(n) = aantal getallen 0 < x < n met ggd(x, n) = 1 = orde eenhedengroep Zxn
      """


      pass


  def _make_overline(self, x):
    return x
    #return ''.join([char + '\u0305' for char in str(x)])

r = Restklassenring(n)
print('Cayleytabel voor +')
print(tabulate(r.cayley_tabel_plus(), r.headers(), showindex=True))
print('\n')

print('Cayleytabel voor *')
print(tabulate(r.cayley_tabel_maal(), r.headers(), showindex=True))
print('\n')

print('Eenheden')
pprint(r.eenheden())
print('\n')

print('Generatoren')
pprint(r.generatoren())
print('\n')

print('Orde: ' + str(r.orde()))
print('\n')

print('Deelgroepen voortgebracht door x\u0305 element van Z%s,+' % n)
deelgroepen = r.deelgroepen1()
orde = r.orde()
for key in deelgroepen:
  print(' <' + str(key) + '\u0305> = ' + str(deelgroepen[key]))
print('\n')

print('Deelgroepen voortgebracht door x\u0305 element van Zx%s,*' % n)
deelgroepen = r.deelgroepen2()
orde = r.orde()
for key in deelgroepen:
  print(' <' + str(key) + '\u0305> = ' + str(deelgroepen[key]))

print('\n\n')


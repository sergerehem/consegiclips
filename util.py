meses = ['janeiro','fevereiro',u'mar\u00e7o','abril','maio','junho','julho','agosto','setembro','outubro','novembro','dezembro']

def formata_dia_mes(dia, mes):
  return dia + " de " + nome_mes(int(mes) - 1)
  
def nome_mes(mes):
  return meses[mes]


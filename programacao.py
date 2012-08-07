class Consegi:
    
  def obtem_dias():
    response = urllib2.urlopen(url)
    tree = etree.fromstring(response.read())
    dias = []
    for d in tree.findall('grouped-summary/summary'):
      dias.append(d.attrib['id'])   
    return dias    


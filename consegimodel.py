import urllib2
import logging
import util
from xml.etree import ElementTree as etree
from google.appengine.ext.webapp import template
from google.appengine.api import memcache
from google.appengine.api.logservice import logservice


cache = 3600
consegi_url = 'http://fisl.org.br/13/papers_ng/public/fast_grid?event_id=3'

class ConsegiModel:
      
  def obtem_dias(self):
    dias = {}
    for d in self.obtem_xml().findall('grouped-summary/summary'):
      ano, mes, dia = (d.attrib['id']).split('-')
      dias[d.attrib['id']] = util.formata_dia_mes(dia, mes) # + "/" + ano dia + " de " + meses[int(mes)-1]
    return dias #sorted(dias.iteritems(), key=lambda (k,v): (v,k))

  def obtem_salas(self): 
    salas = memcache.get("salas")
    if salas is not None:
      logging.info("Obtendo salas do memcache")
      return salas
    else:  
      logging.info("Obtendo salas do site do CONSEGI")
      salas = {}
      for s in self.obtem_xml().findall('rooms/room'):
        salas[s.attrib['id']] = s.find('name').text
      if not memcache.add("salas", salas, cache):
        logging.error("Memcache falhou ao incluir salas")            
      return salas
      
  def obtem_trilhas(self):
    trilhas = memcache.get("trilhas")
    if trilhas is not None:
      logging.info("Obtendo trilhas do memcache")
      return trilhas
    else:    
      logging.info("Obtendo trilhas do site do CONSEGI")
      trilhas = {} 
      for t in self.obtem_xml().findall('zones/zone'):
        trilhas[t.attrib['id']] = t.find('name').text.replace('/','&')
      if not memcache.add("trilhas", trilhas, cache):
        logging.error("Memcache falhou ao incluir trilhas")         
      return trilhas
            
  def obtem_areas(self):
    areas = memcache.get("areas")
    if areas is not None:
      logging.info("Obtendo areas do memcache")
      return areas
    else:    
      areas = {} 
      for a in self.obtem_xml().findall('areas/area'):
        areas[a.attrib['id']] = {'nome': a.find('name').text.replace('/','&'), 'zona':a.find('zone').text}
      if not memcache.add("areas", areas, cache):
          logging.error("Memcache falhou ao incluir trilhas")         
      return areas      
            
  def obtem_palestras_por_dia(self, data):
    return self.obtem_palestras('@date="' + data + '"')
    
  def obtem_palestras_por_sala(self, sala):
    return self.obtem_palestras('@room="' + sala + '"')
        
  def obtem_palestras_por_trilha(self, trilha):
    return self.obtem_palestras('@zone="' + trilha + '"')
  
  def obtem_palestras_por_area(self, area):
    return self.obtem_palestras('@area="' + area + '"')
      
  def obtem_palestras(self, criterio):
    tree = self.obtem_xml()
    palestras = {}
    for p in tree.findall("slots/slot[" + criterio + ']'):
      dia_hora_id = p.attrib['date'] + " " + p.attrib['hour'] + ":" + p.attrib['minute'] + " " + p.attrib['id']
      palestras[dia_hora_id] = {
        "titulo" : p.attrib['title'],
        "data" : p.attrib['date'],
        "hora" : p.attrib['hour'] + ":" + p.attrib['minute'],
        "resumo" : p.attrib['abstract'],
        "trilha_id" : p.attrib['zone'],
        "trilha_nome" : self.obtem_trilhas()[p.attrib['zone']],
        "sala_id" : p.attrib['room'],
        "sala_nome" : self.obtem_salas()[p.attrib['room']],
        "area_id" : p.attrib['area'],
        "area_nome" : (self.obtem_areas()[p.attrib['area']]),
      }
    logging.info(palestras)
    return palestras  

  def obtem_xml(self):   
    xml = memcache.get("consegi_xml")
    if xml is not None:
      logging.info("Obtendo consegi xml do memcache")
      return xml    
    else:
      logging.info("Obtendo consegi xml do site do CONSEGI")
      response = urllib2.urlopen(consegi_url)
      xml = etree.fromstring(response.read())
      if not memcache.add("consegi_xml", xml, cache):
        logging.error("Memcache falhou ao incluir consegi xml")
      return xml     


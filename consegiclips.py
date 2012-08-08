import os 
import webapp2
import util
from consegimodel import ConsegiModel
from google.appengine.ext.webapp import template

url = 'http://fisl.org.br/13/papers_ng/public/fast_grid?event_id=3'
cache = 3600
model = ConsegiModel()

class MainPage(webapp2.RequestHandler):
  def get(self):
      path = os.path.join(os.path.dirname( __file__ ), 'index.html' )
      self.response.out.write(template.render(path, {}))

class ProgramacaoAgora(webapp2.RequestHandler):
  def get(self):
      self.response.headers['Content-Type'] = 'text/plain'
      self.response.out.write('CONSEGI Clips - Agora!')

class ProgramacaoDias(webapp2.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname( __file__ ), 'dias.html' )
    self.response.out.write(template.render(path, { 'dias': sort(model.obtem_dias()) }))

class ProgramacaoPorDia(webapp2.RequestHandler):
  def get(self, data):
    ano, mes, dia = data.split('-')
    path = os.path.join(os.path.dirname( __file__ ), 'palestras.html' )
    self.response.out.write(template.render(path, { 'titulo': "Palestras do dia " + util.formata_dia_mes(dia, mes), 'palestras': sort_by_key(model.obtem_palestras_por_dia(data)) } ))
      
class ProgramacaoSalas(webapp2.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname( __file__ ), 'salas.html' )
    self.response.out.write(template.render(path, { 'salas': sort(model.obtem_salas()) }))
      
class ProgramacaoPorSala(webapp2.RequestHandler):
  def get(self, sala, nome):
    path = os.path.join(os.path.dirname( __file__ ), 'palestras.html' )
    self.response.out.write(template.render(path, { 'titulo': "Palestras da sala " + nome, 'palestras': sort_by_key(model.obtem_palestras_por_sala(sala)) }))

class ProgramacaoTrilhas(webapp2.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname( __file__ ), 'trilhas.html' )
    self.response.out.write(template.render(path, { 'trilhas': sort(model.obtem_trilhas()) }))
      
class ProgramacaoPorTrilha(webapp2.RequestHandler):
  def get(self, trilha, nome):
    path = os.path.join(os.path.dirname( __file__ ), 'palestras.html' )
    self.response.out.write(template.render(path, { 'titulo': "Palestras da trilha " + nome, 'palestras': sort_by_key(model.obtem_palestras_por_trilha(trilha)_ }))

class ProgramacaoAreas(webapp2.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname( __file__ ), 'areas.html' )
    self.response.out.write(template.render(path, { 'areas': sort(model.obtem_areas()) }))
    
class ProgramacaoPorArea(webapp2.RequestHandler):
  def get(self, area, nome):
    path = os.path.join(os.path.dirname( __file__ ), 'palestras.html' )
    self.response.out.write(template.render(path, { 'titulo': "Palestras do tema " + nome, 'palestras': sort_by_key(model.obtem_palestras_por_area(area)) }))

def sort(unsorted):
  return sorted(unsorted.iteritems(), key=lambda (k,v): (v,k))     
   
def sort_by_key(unsorted):
  return sorted(unsorted.items())     
         
app = webapp2.WSGIApplication([('/', MainPage),
                               ('/agora', ProgramacaoAgora),                                
                               ('/dias', ProgramacaoDias),
                                webapp2.Route(r'/dia/<data>', ProgramacaoPorDia),
                               ('/salas', ProgramacaoSalas),
                                webapp2.Route(r'/sala/<sala>/<nome>', ProgramacaoPorSala),                              
                               ('/trilhas', ProgramacaoTrilhas),
                                 webapp2.Route(r'/trilha/<trilha>/<nome>', ProgramacaoPorTrilha),
                               ('/areas', ProgramacaoAreas),                                        
                                 webapp2.Route(r'/area/<area>/<nome>', ProgramacaoPorArea),                               
                               ],debug=True)

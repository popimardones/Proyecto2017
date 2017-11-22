from language_detector import LanguageDetector
from corpus import CorpusHelper, CorpusModel
import json
import facebook

ch = CorpusHelper(language='spanish')
ch.load()
cm=CorpusModel(corpus=ch)
params = cm.fit()
print('Our model has an AUC of {}'.format(cm.x_validation(params)))
linea= []
with open ('data.json', mode = 'r', encoding='utf-8',) as file:
	prueba = json.load(file)
	comentarios = []
	for x in range(0, 25):
		for i in range(0, len(prueba['posts']['data'][x]['comments']['data'])):	
			comentarios.append(prueba['posts']['data'][x]['comments']['data'][i]['message'])
Id = LanguageDetector()
comentarios = [text for text in comentarios if Id.detect(text) == 'es']
lista=cm.predict(comentarios, params)
print(lista)
comentariosPositivos = 0
total= len(lista)
for holi in range(0, len(lista)):
	comentariosPositivos += lista[holi]
print(((comentariosPositivos/total)*100))
comentariosNegativos = total - comentariosPositivos
print(((comentariosNegativos/total)*100))




from language_detector import LanguageDetector
from corpus import CorpusHelper, CorpusModel
import json
import facebook

ch = CorpusHelper(language='spanish')
ch.load()
cm=CorpusModel(corpus=ch)
params = cm.fit()
print('Our model has an AUC of {}'.format(cm.x_validation(params)))
#el data_json hay que rellenarlo con un ciclo para que vaya cambiando los candidatos y el post
#ocupando lo que había hecho la popi, les cambié los nombres a esto para que sea más fácil jeje
datas_json = ['data1.json', 'data2.json', 'data3.json', 'data4.json','data5.json','data6.json', 'data7.json', 'data8.json', 'data9.json', 'data10.json']
for data_json in datas_json:
	with open (data_json, mode = 'r', encoding='utf-8',) as file:
		lector = json.load(file) #esto lee el json
		comentarios = []
		for x in range(0, len(lector)):	
			comentarios.append(lector[x]['message'])	 #aqui accede al indice x del arreglo y al contenido 'message'
	Id = LanguageDetector()
	comentarios = [text for text in comentarios if Id.detect(text) == 'es']
	lista=cm.predict(comentarios, params) #esto es magia
	print(lista)
	comentariosPositivos = 0
	total= len(lista)
	for index in range(0, len(lista)):
		comentariosPositivos += lista[index]
	porcentajePositivo = ((comentariosPositivos/total)*100)
	print(porcentajePositivo)
	print("% aprobación")
	comentariosNegativos = total - comentariosPositivos
	porcentajeNegativo = ((comentariosNegativos/total)*100)
	print(porcentajeNegativo)
	print("% de reprobación")




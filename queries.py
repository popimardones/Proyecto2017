from pymongo import MongoClient
import sys
import io
from language_detector import LanguageDetector
from corpus import CorpusHelper, CorpusModel
import json
import facebook
ch = CorpusHelper(language='spanish')
ch.load()
cm = CorpusModel(corpus=ch)
params = cm.fit()
print('Our model has an AUC of {}'.format(cm.x_validation(params)))
candidatos = ['AlejandroGuillier', 'SebastianPiñera', 'AlejandroNavarro', 'CarolinaGoic', 'BeatrizSanchez', 'JoseAntonioKast', 'EduardoArtes', 'MarcoEnriquez-Ominami']
client = MongoClient('localhost', 27017)
candidatoId = ['1481491872064849', '553775568008058', '10152723078', '377671865775887', '137510593443379', '881095048648989', '321406001578434', '386634201382499'] 
#candidatoId ordenado segun la lista "candidatos"
posicionId = 0
meses = ['Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre']
for candidato in candidatos:
	totalComentarios = 0
	totalPositivos = 0
	for mes in meses:
		positivosEnMes = 0
		comentariosEnMes = 0
		IdCandidatoActual = candidatoId[posicionId]
		database = client[candidato+"JSONcomments"]
		sys.stdout = io.TextIOWrapper(sys.stdout.detach(), sys.stdout.encoding, 'backslashreplace')
		fileRead = open(candidato+'_postIds_'+mes+'.txt', 'r')
		presidente_txtList = fileRead.readlines()
		# saca el \n de todos los item de la lista
		presidenteSacarSlashNList = [i.replace('\n', '') for i in presidente_txtList]
		# saca el user_id_ de todos los item de la lista porque queremos una lista de solo los postIds
		presidenteSoloPostId_List = [i.replace(IdCandidatoActual+'_', '') for i in presidenteSacarSlashNList]
		# sacar el ultimo termino de la lista porque por alguna razon es un item empty
		presidenteSoloPostId_List = presidenteSoloPostId_List[:-1]
		comments = []
		for x in range(0, len(presidenteSoloPostId_List)):
			collection = database[candidato+"CommentsOfPost"+presidenteSoloPostId_List[x]]

			# Created with Studio 3T, the IDE for MongoDB - https://studio3t.com/
			query = {}
			projection = {}
			projection["message"] = 1

			cursor = collection.find(query, projection = projection)
			try:
			    for doc in cursor:
			        comments.append(doc["message"])
			finally:
			    cursor.close()
		lista = cm.predict(comments, params)
		#print(comments)
		comentariosEnMes = len(comments)
		print(candidato)
		print(mes)
		print(comentariosEnMes)
		for index in range(0, len(lista)):
			positivosEnMes += lista[index]
		porcentajePositivoEnMes = ((positivosEnMes / comentariosEnMes) * 100)
		print("{0:0.2f}% aprobación".format(porcentajePositivoEnMes))
		totalComentarios += comentariosEnMes
		totalPositivos += positivosEnMes
		posicionId +=1
	print('Total comentarios: ')
	print(totalComentarios)
	porcentajePositivoTotal = ((totalPositivos/ totalComentarios)*100)
	print("{0:0.2f}% aprobación".format(porcentajePositivoTotal))
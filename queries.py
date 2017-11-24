from pymongo import MongoClient
import sys
import io
candidatos = ['AlejandroGuillier', 'SebastianPiñera']
client = MongoClient('localhost', 27017)
candidatoId = ['1481491872064849', '553775568008058']
posicionId = 0
for candidato in candidatos:
	IdCandidatoActual = candidatoId[posicionId]
	database = client[candidato+"JSONcomments"]
	sys.stdout = io.TextIOWrapper(sys.stdout.detach(), sys.stdout.encoding, 'backslashreplace')
	fileRead = open(candidato+'_postIds_desdeLasPrimarias.txt', 'r')
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
	print(comments)
	print(candidato)
	posicionId +=1
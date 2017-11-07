import facebook
import requests

access_token = 'EAAN614qceX8BAN3CZBL97wvFsRhZAAP3yR6GKvScj7CUDNPXPeaNNFFsw57vffb4lLY1GOZB57y8UKvAimYX65v67NKkQ0xZAqWik6A3ElMzc8Wd6p9UhCK3xi8PaROjOlNY6GD7zgc8msTbcNdHrqZCiqluWo9pcxhxXL3giCxPCyRWMfS8mDT5v7zO2LZBEZD'
post_id='250192832175154'
user_id = '137510593443379'
#graph = facebook.GraphAPI(access_token=access_token, version="2.10")
#posts = graph.get_object(id=user_id, fields='posts{id}')
graph_api_version = 'v2.9'
url = 'https://graph.facebook.com/{}/{}_{}/comments'.format(graph_api_version, user_id, post_id)
comments = []
r=requests.get(url, params={'access_token': access_token})

while True:
	data = r.json()

	if 'error' in data:
		raise Exception(data['error']['message'])

	for comment in data['data']:

		text = comment['message'].replace('\n', ' ')
		comments.append(text)

	(print('got {} comments'.format(len(data['data']))))

	if 'paging' in data and 'next' in data['paging']:
		r=requests.get(data['paging']['next'])
	else:
		break

with open('comments.txt', 'w', encoding='utf-8') as f:
	for comments in comments:
		f.write(comments + '\n')
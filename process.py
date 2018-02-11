from spidermar import proxy_requests
import pandas as pd
from pandas.io.json import json_normalize
import json

base = 'https://www.leforem.be/recherche-offres-emploi/rest/'
u1 = 'searchJob/fromQuickSearch?query=&lieu_trav=&start='
u2 = 'jobService/jobDetail/'

def get_count():
	df = pd.read_json(base+u1)['count'].unique()
	return int(df)

def get_ten_last():
	return pd.read_json(base+u1)['offers'].apply(pd.Series)

def get_refs():
	N = get_count()
	try:
		with open('refs', 'r') as f:
			refs = json.load(f)
	except:
		refs = [c['id'] for i in range(1,N) for c in proxy_requests(base+u1+str(i)\
			+str(1)).json()['offers']]
		with open('refs', 'w') as g:
			json.dump(refs, g, ensure_ascii=False)
	return refs

def get_data():
	try:
		with open('offres', 'r') as f:
			offres = json.load(f)
	except:
		refs = get_refs()
		offres = [proxy_requests(base+u2+str(j)).json() for j in refs[0:31]]
		with open('offres', 'w') as g:
			json.dump(offres, g, ensure_ascii=False)
	return json_normalize(offres)

if __name__ == '__main__':
	x = get_data()
	print (x)


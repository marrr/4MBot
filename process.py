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
	try:
		with open('refs', 'r') as f:
			refs = json.load(f)
	except:
		refs = [c['id'] for i in range(11) for c in proxy_requests(base+u1+str(i)\
			+str(1)).json()['offers']]
		with open('refs', 'w') as g:
			json.dump(refs, g, ensure_ascii=False)
	return refs

if __name__ == '__main__':
	get_refs()


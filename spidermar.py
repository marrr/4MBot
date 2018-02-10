import pickle, requests, bs4, os, time
from random import choice
from selenium import webdriver

def UAS():
	'''returns a random User Agent among nearly 3000 UAs
	Source : http://sql.sh/ressources/sql-user-agents/'''
	path = 'uas'
	try:
		uas = pickle.load(open(path,'rb'))
	except (OSError, IOError):	
		url = 'http://sql.sh/ressources/sql-user-agents/user_agents.xml'
		r = requests.get(url).text
		s = bs4.BeautifulSoup(r, "lxml")
		uas = [u.get_text() for u in s.find_all('column',{'name':'useragents'})]
		pickle.dump(uas,open(path,'wb'))
	return choice(uas)

def safe_requests(url):
	response = None
	ua = {'User-Agent':UAS()}
	while response is None:
		try:
			response = requests.get(url, headers=ua, timeout=30)
		except:
			print ('On recommence, ya un truc qui a pas marché')
			pass
	return response

def get_proxies():
	url = 'http://proxy-daily.com/'
	rep = safe_requests(url)
	soup = bs4.BeautifulSoup(rep.text, 'html.parser')
	base = soup.find('div',{'id':'posts'})
	lien = base.find('div').find('h2').find('a').get('href')
	rr = safe_requests(lien)
	sup = bs4.BeautifulSoup(rr.text, 'html.parser')
	all_p = sup.find('div',{'class':'post-content'}).find_all('p')[3:]
	pre_prox = [p.text.split(' ')[5:] for p in all_p]
	# Flatten list
	proxies = [item for sublist in pre_prox for item in sublist]
	pickle.dump(proxies, open('proxies', 'wb'))
	return proxies

def proxies():
	path = 'proxies'
	try:
		proxies = pickle.load(open(path,'rb'))
	except (OSError, IOError):
		proxies = get_proxies()
	stat = os.stat(path).st_mtime
	now = time.time()
	diff = now - stat
	if diff <= 43200:
		pass
	else:
		proxies = get_proxies()
	return choice(proxies)

def proxy_requests(url):
	response = None
	ua = {'User-Agent':UAS()}
	proxy = proxies()
	while response is None:
		try:
			response = requests.get(url, headers=ua, proxies={'http':'http://'+proxy}, timeout=10)
		except:
			pass
	return response

def chunks(l, n):
    """Yield successive n-sized chunks from a list"""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def navigo():
	'''returns a selenium webdriver with a different 
	User Agent on each call''' 
	profile = webdriver.FirefoxProfile()
	profile.set_preference("general.useragent.override", UAS())
	proxy = proxies().split(':')
	profile.set_preference('network.proxy.type',1)
	profile.set_preference('network.proxy.http',proxy[0])
	profile.set_preference('network.proxy.http_port',proxy[1])
	nav = webdriver.Firefox(profile)
	return nav

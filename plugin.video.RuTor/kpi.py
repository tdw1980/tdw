# -*- coding: utf-8 -*-
siteUrl = 'www.KinoPoisk.ru'
httpSiteUrl = 'http://' + siteUrl
import xbmc, os, urllib, time, codecs, httplib, urllib2

headers  = {
	'User-Agent' : 'Opera/9.80 (X11; Linux i686; U; ru) Presto/2.7.62 Version/11.00',
	'Accept'     :' text/html, application/xml, application/xhtml+xml, image/png, image/jpeg, image/gif, image/x-xbitmap, */*',
	'Accept-Language':'ru-RU,ru;q=0.9,en;q=0.8',
	'Accept-Charset' :'utf-8, utf-16, *;q=0.1',
	'Accept-Encoding':'identity, *;q=0'
}

def GET(target, referer, post_params = None, accept_redirect = True, get_redirect_url = False, siteUrl='www.KinoPoisk.ru'):
	try:
		connection = httplib.HTTPConnection(siteUrl)

		if post_params == None:
			method = 'GET'
			post = None
		else:
			method = 'POST'
			post = urllib.urlencode(post_params)
			headers['Content-Type'] = 'application/x-www-form-urlencoded'
		
		sid_file = os.path.join(xbmc.translatePath('special://temp/'), 'KP.ru.cookies.sid')
		if os.path.isfile(sid_file):
			fh = open(sid_file, 'r')
			csid = fh.read()
			fh.close()
			headers['Cookie'] = 'session=%s' % csid

		headers['Referer'] = referer
		connection.request(method, target, post, headers = headers)
		response = connection.getresponse()

		if response.status == 403:
			raise Exception("Forbidden, check credentials")
		if response.status == 404:
			raise Exception("File not found")
		if accept_redirect and response.status in (301, 302):
			target = response.getheader('location', '')
			if target.find("://") < 0:
				target = httpSiteUrl + target
			if get_redirect_url:
				return target
			else:
				return GET(target, referer, post_params, False)

		try:
			sc = Cookie.SimpleCookie()
			sc.load(response.msg.getheader('Set-Cookie'))
			fh = open(sid_file, 'w')
			fh.write(sc['session'].value)
			fh.close()
		except: pass

		if get_redirect_url:
			return False
		else:
			http = response.read()
			return http

	except Exception, e:
		print 'Error '+str(e)
		return ""

def GET2(target, referer, post=None):
	try:
		req = urllib2.Request(url = target, data = post)
		req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)')
		resp = urllib2.urlopen(req)
		http = resp.read()
		resp.close()
		return http
	except Exception, e:
		print e

def mfindal(http, ss, es):
	L=[]
	while http.find(es)>0:
		s=http.find(ss)
		e=http.find(es)
		i=http[s:e]
		L.append(i)
		http=http[e+2:]
	return L

def fs(s):
	s=str(repr(s))[1:-1]
	s=s.replace('\\xb8','ё')
	s=s.replace('\\xe0','a')
	s=s.replace('\\xe1','б')
	s=s.replace('\\xe2','в')
	s=s.replace('\\xe3','г')
	s=s.replace('\\xe4','д')
	s=s.replace('\\xe5','е')
	s=s.replace('\\xe6','ж')
	s=s.replace('\\xe7','з')
	s=s.replace('\\xe8','и')
	s=s.replace('\\xe9','й')
	s=s.replace('\\xea','к')
	s=s.replace('\\xeb','л')
	s=s.replace('\\xec','м')
	s=s.replace('\\xed','н')
	s=s.replace('\\xee','о')
	s=s.replace('\\xef','п')
	s=s.replace('\\xf0','р')
	s=s.replace('\\xf1','с')
	s=s.replace('\\xf2','т')
	s=s.replace('\\xf3','у')
	s=s.replace('\\xf4','ф')
	s=s.replace('\\xf5','х')
	s=s.replace('\\xf6','ц')
	s=s.replace('\\xf7','ч')
	s=s.replace('\\xf8','ш')
	s=s.replace('\\xf9','щ')
	s=s.replace('\\xfa','ъ')
	s=s.replace('\\xfb','ы')
	s=s.replace('\\xfc','ь')
	s=s.replace('\\xfd','э')
	s=s.replace('\\xfe','ю')
	s=s.replace('\\xff','я')
	
	s=s.replace('\\xa8','Ё')
	s=s.replace('\\xc0','А')
	s=s.replace('\\xc1','Б')
	s=s.replace('\\xc2','В')
	s=s.replace('\\xc3','Г')
	s=s.replace('\\xc4','Д')
	s=s.replace('\\xc5','Е')
	s=s.replace('\\xc6','Ж')
	s=s.replace('\\xc7','З')
	s=s.replace('\\xc8','И')
	s=s.replace('\\xc9','Й')
	s=s.replace('\\xca','К')
	s=s.replace('\\xcb','Л')
	s=s.replace('\\xcc','М')
	s=s.replace('\\xcd','Н')
	s=s.replace('\\xce','О')
	s=s.replace('\\xcf','П')
	s=s.replace('\\xd0','Р')
	s=s.replace('\\xd1','С')
	s=s.replace('\\xd2','Т')
	s=s.replace('\\xd3','У')
	s=s.replace('\\xd4','Ф')
	s=s.replace('\\xd5','Х')
	s=s.replace('\\xd6','Ц')
	s=s.replace('\\xd7','Ч')
	s=s.replace('\\xd8','Ш')
	s=s.replace('\\xd9','Щ')
	s=s.replace('\\xda','Ъ')
	s=s.replace('\\xdb','Ы')
	s=s.replace('\\xdc','Ь')
	s=s.replace('\\xdd','Э')
	s=s.replace('\\xde','Ю')
	s=s.replace('\\xdf','Я')
	
	s=s.replace('\\xab','"')
	s=s.replace('\\xbb','"')
	s=s.replace('\\r','')
	s=s.replace('\\n','\n')
	s=s.replace('\\t','\t')
	s=s.replace("\\x85",'...')
	s=s.replace("\\x97",'-')
	s=s.replace("\\xb7","·")
	s=s.replace("\\x96",'-')
	s=s.replace("\\x92",'')
	s=s.replace("\\xb9",'№')
	s=s.replace("\\xa0",' ')
	s=s.replace('&laquo;','"')
	s=s.replace('&raquo;','"')
	s=s.replace('&#38;','&')
	s=s.replace('&#233;','é')
	s=s.replace('&#232;','è')
	s=s.replace('&#224;','à')
	s=s.replace('&#244;','ô')
	s=s.replace('&#246;','ö')
	
	s=s.replace('"','“')
	s=s.replace("'",'’')
	
	return s

def rt(x):
	L=[('&#39;','’'), ('&#145;','‘'), ('&#146;','’'), ('&#147;','“'), ('&#148;','”'), ('&#149;','•'), ('&#150;','–'), ('&#151;','—'), ('&#152;','?'), ('&#153;','™'), ('&#154;','s'), ('&#155;','›'), ('&#156;','?'), ('&#157;',''), ('&#158;','z'), ('&#159;','Y'), ('&#160;',''), ('&#161;','?'), ('&#162;','?'), ('&#163;','?'), ('&#164;','¤'), ('&#165;','?'), ('&#166;','¦'), ('&#167;','§'), ('&#168;','?'), ('&#169;','©'), ('&#170;','?'), ('&#171;','«'), ('&#172;','¬'), ('&#173;',''), ('&#174;','®'), ('&#175;','?'), ('&#176;','°'), ('&#177;','±'), ('&#178;','?'), ('&#179;','?'), ('&#180;','?'), ('&#181;','µ'), ('&#182;','¶'), ('&#183;','·'), ('&#184;','?'), ('&#185;','?'), ('&#186;','?'), ('&#187;','»'), ('&#188;','?'), ('&#189;','?'), ('&#190;','?'), ('&#191;','?'), ('&#192;','A'), ('&#193;','A'), ('&#194;','A'), ('&#195;','A'), ('&#196;','A'), ('&#197;','A'), ('&#198;','?'), ('&#199;','C'), ('&#200;','E'), ('&#201;','E'), ('&#202;','E'), ('&#203;','E'), ('&#204;','I'), ('&#205;','I'), ('&#206;','I'), ('&#207;','I'), ('&#208;','?'), ('&#209;','N'), ('&#210;','O'), ('&#211;','O'), ('&#212;','O'), ('&#213;','O'), ('&#214;','O'), ('&#215;','?'), ('&#216;','O'), ('&#217;','U'), ('&#218;','U'), ('&#219;','U'), ('&#220;','U'), ('&#221;','Y'), ('&#222;','?'), ('&#223;','?'), ('&#224;','a'), ('&#225;','a'), ('&#226;','a'), ('&#227;','a'), ('&#228;','a'), ('&#229;','a'), ('&#230;','?'), ('&#231;','c'), ('&#232;','e'), ('&#233;','e'), ('&#234;','e'), ('&#235;','e'), ('&#236;','i'), ('&#237;','i'), ('&#238;','i'), ('&#239;','i'), ('&#240;','?'), ('&#241;','n'), ('&#242;','o'), ('&#243;','o'), ('&#244;','o'), ('&#245;','o'), ('&#246;','o'), ('&#247;','?'), ('&#248;','o'), ('&#249;','u'), ('&#250;','u'), ('&#251;','u'), ('&#252;','u'), ('&#253;','y'), ('&#254;','?'), ('&#255;','y')]
	for i in L:
		x=x.replace(i[0], i[1])
	return x

def info(id):
		try:
			url="http://m.kinopoisk.ru/movie/"+id
			http = GET (url, httpSiteUrl)
			http = rt(http)
			
			# ------------- ищем описание -----------------
			s='<div id="content">'
			e='<br><div class="city">'
			try: Info=mfindal(http, s, e)[0]
			except: Info=""
			
			# ------------- название -----------------
			s='<p class="title">'
			e='<img src="http://m.kinopoisk.ru/images/star'
			if Info.find(e)<0: e='<div class="block film">'
			try: 
				nbl=mfindal(Info, s, e)[0][len(s):]
			except:
				nbl=""
			
			if nbl <> "":
				# ---------------- ru -------------------
				s='<b>'
				e='</b>'
				nru=mfindal(nbl, s, e)[0][len(s):]
				
				# ---------------- en yar time -------------------
				s='<span>'
				e='</span>'
				nen=mfindal(nbl, s, e)[0][len(s):]
				vrn=nen.replace("'","#^").replace(",", "','")
				tmps="['"+vrn+"']"
				Lt=eval(tmps)
				n=len(Lt)
				year=0
				duration=""
				for i in Lt:
					try: year=int(i)
					except: pass
					if i[-1:]==".": duration=i
				if year>0: n2= nen.find(str(year))
				else: n2=-1
				if duration<>"":n3=nen.find(duration)
				else: n3=-1
				if n3>0 and n3<n2: n2=n3
				if n2>1: nen=nen[:n2-2]
				else: nen=nru
				
				# ---------------- жанр  страна ----------
				s='<div class="block film">'
				e='<span class="clear"'
				try:
					b2=mfindal(Info, s, e)[0][len(s):]
					s='<span>'
					e='</span>'
					genre=mfindal(b2, s, e)[0][len(s):]
					studio=mfindal(b2, s, e)[1][len(s):]
				except:
					genre=""
					studio=""
				# ---------------- режисер ----------
				s='<span class="clear">'
				e='</a></span>'
				try:
					directors=mfindal(Info, s, e)[0][len(s):]
					s='/">'
					e='</a>'
					try: 
						director1=mfindal(directors, s, e)[0][len(s):]
						nn=directors.rfind('/">')
						director=director1+", "+directors[nn+3:]
					except:
						nn=directors.rfind('/">')
						director=directors[nn+3:]
				except:
					director=""
					
				# --------------- актеры ------------
				if director!="":
					s=directors#'<span class="clear">'
					e='<p class="descr">'
					if Info.find(e)<0:e='">...</a>'
					
					try:bcast=mfindal(Info, s, e)[0][len(s):]
					except: bcast=""
					s='/">'
					e='</a>,'
					lcast=mfindal(bcast, s, e)
					cast=[]
					for i in lcast:
						cast.append(fs(i[3:]))
				else:
					cast=[]
				# ----------------  описание ----------
				s='<p class="descr">'
				e='<span class="link">'
				if Info.find(e)<0: e='<p class="margin"'
				#debug (Info)
				try:plotand=mfindal(Info, s, e)[0][len(s):]
				except:plotand=""# -----------------------------------------------------------  доделать ----------
				nn=plotand.find("</p>")
				plot=plotand[:nn].replace("<br>","").replace("<br />","")
				# ----------------- оценки ------------
				tale=plotand[nn:]
				s='</b> <i>'
				e='</i> ('
				ratings=mfindal(Info, s, e)
				try:rating_kp=float(ratings[0][len(s):])
				except:rating_kp=0
				try:rating_IMDB=float(ratings[1][len(s):])
				except: rating_IMDB=0
				
				
				# ------------------ обложка ----------
				s='//st.kp.yandex.net/images/sm_'
				e='.jpg" width="'
				try:cover='http:'+mfindal(Info, s, e)[0].replace('sm_film/','film_iphone/iphone360_')+'.jpg'
				except:cover="http://st.kp.yandex.net/images/image_none_no_border.gif"
				# ------------------ фанарт ----------
				s='//st.kp.yandex.net/images/kadr'
				e='.jpg"/></div>'
				try:fanart='http:'+mfindal(Info, s, e)[0].replace('sm_','')+'.jpg'
				except:fanart=""
				
				info = {"title":fs(nru), 
						"originaltitle":fs(nen), 
						"year":year, 
						"duration":duration[:-5].strip(),
						"genre":fs(genre), 
						"studio":fs(studio),
						"director":fs(director),
						"cast":cast,
						"rating":rating_kp,
						"cover":cover,
						"fanart":fanart,
						"plot":fs(plot)
						}
				info["id"] = id
				return info
		except: 
			return {}

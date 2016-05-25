# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, os, urllib, sys, urllib2, time

PLUGIN_NAME   = 'plugin.video.viks.tv'
handle = int(sys.argv[1])
addon = xbmcaddon.Addon(id='plugin.video.viks.tv')
__settings__ = xbmcaddon.Addon(id='plugin.video.viks.tv')

siteUrl = 'viks.tv'
httpSiteUrl = 'http://' + siteUrl

Pdir = addon.getAddonInfo('path')
icon = xbmc.translatePath(os.path.join(addon.getAddonInfo('path'), 'icon.png'))
xbmcplugin.setContent(int(sys.argv[1]), 'movies')

def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)
	
def showMessage(heading, message, times = 3000):
	xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s, "%s")'%(heading, message, times, icon))

def getURL(url,Referer = 'http://viks.tv/'):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Opera/10.60 (X11; openSUSE 11.3/Linux i686; U; ru) Presto/2.6.30 Version/10.60')
	req.add_header('Accept', 'text/html, application/xml, application/xhtml+xml, */*')
	req.add_header('Accept-Language', 'ru,en;q=0.9')
	req.add_header('Referer', Referer)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def mfindal(http, ss, es):
	L=[]
	while http.find(es)>0:
		s=http.find(ss)
		#sn=http[s:]
		e=http.find(es)
		i=http[s:e]
		L.append(i)
		http=http[e+2:]
	return L

def debug(s):
	fl = open(ru(os.path.join( addon.getAddonInfo('path'),"test.txt")), "w")
	fl.write(s)
	fl.close()

def inputbox(t):
	skbd = xbmc.Keyboard(t, 'Название:')
	skbd.doModal()
	if skbd.isConfirmed():
		SearchStr = skbd.getText()
		return SearchStr
	else:
		return t



def play(url, name ,cover):
		pDialog = xbmcgui.DialogProgressBG()
		pDialog.create('Viks.tv', 'Поиск потоков ...')
		#Lpurl=get_stream(url)
		try: Lpurl=get_stream(url)
		except:
			Lpurl=[]
			showMessage('viks.tv', 'Канал недоступен')
		
		print '--==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-'
		
		playlist = xbmc.PlayList (xbmc.PLAYLIST_VIDEO)
		playlist.clear()
		
		k=0
		
		for purl in Lpurl:
			k+=1
			#print purl
			item = xbmcgui.ListItem(name+" [ "+str(k)+"/"+str(len(Lpurl))+" ]", path=purl, thumbnailImage=cover, iconImage=cover)
			playlist.add(url=purl, listitem=item)
		
		xbmc.Player().stop()
		xbmc.Player().play(playlist)#, item
		pDialog.close()
		xbmc.sleep(10000)
		
		#print "======================== isPlaying ======================"
		#print xbmc.Player().isPlaying()
		
		while  xbmc.Player().isPlaying():#not
			xbmc.sleep(1000)
			print "========================  playing ======================"
		xbmc.sleep(1000)
		print "========================  Refresh ======================"
		xbmc.executebuiltin("Container.Refresh")

def get_ttv(url):
		print url
		http=getURL(url)
		#debug(http)
		ss='this.loadPlayer("'
		es='",{autoplay: true})'
		srv=__settings__.getSetting("p2p_serv")
		prt=__settings__.getSetting("p2p_port")
		
		try:
			CID=mfindal(http,ss,es)[0][len(ss):]
			lnk='http://'+srv+':'+prt+'/ace/getstream?id='+CID
			return lnk
		except:
			return ""

def get_stream(url):
	if 'viks.tv' in url:
		http=getURL(url)
		
		
		ss='//m3u8'
		es='//m3u8 names'
		tmp=mfindal(http,ss,es)[0]
		
		#ss='//mob srcs'
		#es='jQuery(document)'
		#tmp2=mfindal(http,ss,es)[0]

		#tmp=tmp2+tmp
		
		ss="]='"
		es="';"
		Lp=[]
		
		L=mfindal(tmp,ss,es)
		L.reverse()
		for i in L:
			if i not in Lp and 'peers' not in i: Lp.append(i[len(ss):])
		
		if __settings__.getSetting("p2p")=='true':
			ss='//torrent codes'
			es='//mob names'
			tmp3=mfindal(http,ss,es)[0]
		
			ss='src=\\"'
			es='\\" width='
			Lt=mfindal(tmp3,ss,es)
		
			Lp2=[]
			for t in Lt:
				trst=get_ttv(t[len(ss):])
				Lp2.append(trst)
			if __settings__.getSetting("p2p_start")=='true':
				Lp2.extend(Lp)
				Lp=Lp2
			else:
				Lp.extend(Lp2)
		
		return Lp
	else:
		Lp=[]
		http=getURL(url)
		ss='&file='
		es='&st='
		L=mfindal(http,ss,es)
		for i in L:
			tmp=i[len(ss):]
			if 'm3u8' in tmp:
				#print "M3U8"
				purl = tmp
			else:
				#print "RTMP"
				purl = tmp
				purl += " swfUrl=http://tivix.net/templates/Default/style/uppod.swf"
				purl += " pageURL=http://tivix.net"
				purl += " swfVfy=true live=true"
			if i not in Lp and 'peers' not in i: Lp.append(purl)
		return Lp



def get_cepg_old(id, serv):
	import time
	url='http://schedule.tivix.net/channels/'+serv+'/program/'+id+'/today/'
	udd = int(time.strftime('%Y%m%d'))
	#if 1==1:
	if serv=='tivix': id='t'+id
	try:
		E=__settings__.getSetting(id)
		EPG=eval(E)
		udata = int(EPG[0]['start_at'][:11].replace('-',''))
		cdata = int(time.strftime('%Y%m%d'))
		#print str(udata)+" - "+str(cdata)
		if cdata>udata:
			E=getURL(url)
			__settings__.setSetting(id,E)
			print 'обновлена устаревшая программа: '+id
	except:
		try:
			E=getURL(url)
			__settings__.setSetting(id,E)
			print 'обновлена отсутствующая программа: '+id
		except:
			E='[{"name":"", "start_at": "'+time.strftime('%Y-%m-%d')+' --:--:--"}]'
			__settings__.setSetting(id,E)
			print 'неудалось загрузить программу: '+id

	try:
		#E=getURL(url)
		L=eval(E)
		#L=EPG[id]
		itm=''
		n=0
		stt=int(__settings__.getSetting('shift'))-6
		#print stt
		for i in L:
			n+=1
			h=int(time.strftime('%H'))
			m=int(time.strftime('%M'))
			name=eval("u'"+i['name']+"'")
			try:
				h3 = int(i['start_at'][11:13])-stt
				m3 = int(i['start_at'][14:15])
			except:
				h3=h
				m3=m
			try:
				h2 = int(L[n]['start_at'][11:13])-stt
				m2 = int(L[n]['start_at'][14:15])
			except:
				h2=h
				m2=m
			t1=h*60+m
			t2=h2*60+m2
			if h3>9:hh=str(h3)
			else:   hh="0"+str(h3)
			if m3>9:mm=str(m3)
			else:   mm="0"+str(m3)

			stm =hh+":"+mm
			if t2>=t1: itm+= stm+' '+name+'\n'
		return itm
	except:
		return ''

def get_cepg(id, serv):
	url='http://schedule.tivix.net/channels/'+serv+'/program/'+id+'/today/'
	if serv=='tivix': id='t'+id
	
	try:
		E=get_inf_db(id)
		L=eval(E)
		itm=''
		n=0
		n2=0
		stt=int(__settings__.getSetting('shift'))-6
		
		udata = int(L[0]['start_at'][:11].replace('-',''))
		cdata = int(time.strftime('%Y%m%d'))
		if cdata!=udata: L=[]
		
		for i in L:
			n+=1
			h=int(time.strftime('%H'))
			m=int(time.strftime('%M'))
			name=eval("u'"+i['name']+"'")
			try:
				h3 = int(i['start_at'][11:13])-stt
				m3 = int(i['start_at'][14:16])
			except:
				h3=h
				m3=m
			try:
				h2 = int(L[n]['start_at'][11:13])-stt
				m2 = int(L[n]['start_at'][14:16])
			except:
				h2=h
				m2=m
			t1=h*60+m
			t2=h2*60+m2
			if h3>9:hh=str(h3)
			else:   hh="0"+str(h3)
			if m3>9:mm=str(m3)
			else:   mm="0"+str(m3)

			stm =hh+":"+mm
			if t2>=t1: 
				n2+=1
				# ------ Прогресс бар
				if n2==1:
					t3=h3*60+m3
					vv=t2-t3
					vp=t2-t1
					prc=20-(vp*20/vv)
					
					if h2>9:hh2=str(h2)
					else:   hh2="0"+str(h2)
					if m2>9:mm2=str(m2)
					else:   mm2="0"+str(m2)
					etm =hh2+":"+mm2

					iii='---------------------------'
					pb1='[COLOR FF5555FF][B]'+iii[:prc]+"[/B][/COLOR]"
					pb2='[COLOR FFFFFFFF][B]'+iii[:20-prc]+"[/B][/COLOR]"
					
					itm+= " "+stm+" "+pb1+pb2+" "+etm+'\n'
					itm+='[COLOR FFFFFFFF][B]'+name+'[/B][/COLOR]'+'\n'
				else:
					itm+= '[COLOR FF888888]'+stm+' '+name+"[/COLOR]"'\n'
			
		return itm
	except:
		return ""

def get_cgide(id, serv):
	if serv=='tivix': id='t'+id
	try:
		E=get_inf_db(id)
		L=eval(E)
		itm=''
		n=0
		n2=0
		stt=int(__settings__.getSetting('shift'))-6
		
		udata = int(L[0]['start_at'][:11].replace('-',''))
		cdata = int(time.strftime('%Y%m%d'))
		if cdata!=udata: L=[]
		
		for i in L:
			n+=1
			h=int(time.strftime('%H'))
			m=int(time.strftime('%M'))
			name=eval("u'"+i['name']+"'")
			try:
				h3 = int(i['start_at'][11:13])-stt
				m3 = int(i['start_at'][14:16])
			except:
				h3=h
				m3=m
			try:
				h2 = int(L[n]['start_at'][11:13])-stt
				m2 = int(L[n]['start_at'][14:16])
			except:
				h2=h
				m2=m
			t1=h*60+m
			t2=h2*60+m2
			if h3>9:hh=str(h3)
			else:   hh="0"+str(h3)
			if m3>9:mm=str(m3)
			else:   mm="0"+str(m3)

			stm =hh+":"+mm
			if t2>=t1: 
				#n2+=1
				# ------ Прогресс бар
				#if n2==1:
					t3=h3*60+m3
					vv=t2-t3
					vp=t2-t1
					prc=20-(vp*20/vv)
					
					if h2>9:hh2=str(h2)
					else:   hh2="0"+str(h2)
					if m2>9:mm2=str(m2)
					else:   mm2="0"+str(m2)
					etm =hh2+":"+mm2

					iii='---------------------------'
					pb1='[COLOR FF5555FF][B]'+iii[:prc]+"[/B][/COLOR]"
					pb2='[COLOR FFFFFFFF][B]'+iii[:20-prc]+"[/B][/COLOR]"
					
					itm+= stm+" "+pb1+pb2+" "+etm+'[COLOR FFFFFFFF][B] '+name+'[/COLOR]'#[/B]
					return itm
	except:
		return ""

def tvgide():
	try:
		SG=__settings__.getSetting("Sel_gr")
	except:
		SG=''
	if SG=='':
		SG='Все каналы'
		__settings__.setSetting("Sel_gr",SG)
	add_item ('[COLOR FF55FF55]Группа: '+SG+'[/COLOR]', 'select_gr')
	
	CL=get_gr()
	ttl=len(CL)
	if ttl==0:ttl=250
	Lnm=[]
	
	#try: 
	#	getURL('http://viks.tv/new/logggas.png')
	#	serv1den=1
	#except:serv1den=0
	
	if __settings__.getSetting("serv1")=='true' :
		try:L1=eval(__settings__.getSetting("Channels"))
		except:L1=[]
		if L1==[]: L1=upd_canals_db()
	else: L1=[]
	
	
	if __settings__.getSetting("serv2")=='true':
		try:L2=eval(__settings__.getSetting("Channels2"))
		except:L2=[]
		if L2==[]: L2=upd_canals_db2()
	else: L2=[]

	L1.extend(L2)
	L=L1
	if SG=='Все каналы':
			for i in L:
				namec  = i['title']
				url   = i['url']
				cover = i['img']
				id = get_id(url)
				if 'viks.tv' in url: serv = 'viks'
				else:                serv = 'tivix'
				name=get_cgide(id, serv)
				#if SG=='Все каналы' or name in CL:
				if name!="" and namec not in Lnm: 
					add_item (name, 'play', url, ttl, cover)
					Lnm.append(namec)

	else:
			for k in CL:
				for i in L:
					namec  = i['title']
					if k==namec:
						url   = i['url']
						cover = i['img']
						id = get_id(url)
						if 'viks.tv' in url: serv = 'viks'
						else:                serv = 'tivix'
						name=get_cgide(id, serv)
						if name!="" and namec not in Lnm: 
							add_item (name, 'play', url, ttl, cover)
							Lnm.append(namec)
	
	xbmcplugin.endOfDirectory(handle)


def get_epg(id, serv):
	import time
	url='http://schedule.tivix.net/channels/'+serv+'/program/'+id+'/today/'
	udd = int(time.strftime('%Y%m%d'))
	#if 1==1:
	if serv=='tivix': id='t'+id
	try:
			E=getURL(url)
			add_to_db(id, E)
			print 'обновлена устаревшая программа: '+id
	except:
			E='[{"name":"", "start_at": "'+time.strftime('%Y-%m-%d')+' --:--:--"}]'
			add_to_db(id, E)
			print 'неудалось загрузить программу: '+id


def add_item (name, mode="", path = Pdir, ind="0", cover=None, funart=None):
	#print name
	#print path
	if __settings__.getSetting("fanart")=='true':funart=cover
	else: funart=icon
	if __settings__.getSetting("icons")!='true':cover=icon

	listitem = xbmcgui.ListItem("[B]"+name+"[/B]", iconImage=cover)
	listitem.setProperty('fanart_image', funart)
	uri = sys.argv[0] + '?mode='+mode
	uri += '&url='  + urllib.quote_plus(path.encode('utf-8'))
	uri += '&name='  + urllib.quote_plus(xt(name))
	uri += '&ind='  + urllib.quote_plus(str(ind))
	if cover!=None:uri += '&cover='  + urllib.quote_plus(cover)
	if funart!=None and funart!="":uri += '&funart='  + urllib.quote_plus(funart)
	
	if mode=="play":
		id = get_id(path)
		if __settings__.getSetting("epgon")=='true':
			if 'viks.tv' in path:dict={"plot":get_cepg(id,'viks')}
			else:                dict={"plot":get_cepg(id,'tivix')}
		else: dict={}
		try:listitem.setInfo(type = "Video", infoLabels = dict)
		except: pass

		fld=False
		#listitem.setProperty('IsPlayable', 'true')
		listitem.addContextMenuItems([
			('[COLOR FF55FF55][B]+ Добавить в группу[/B][/COLOR]', 'Container.Update("plugin://plugin.video.viks.tv/?mode=add&name='+name+'")'),
			('[COLOR FFFF5555][B]- Удалить из группы[/B][/COLOR]', 'Container.Update("plugin://plugin.video.viks.tv/?mode=rem&name='+name+'")'),
			('[COLOR FF55FF55][B]<> Переместить канал[/B][/COLOR]', 'Container.Update("plugin://plugin.video.viks.tv/?mode=set_num&name='+name+'")'),
			('[COLOR FF55FF55][B]ГРУППА[/B][/COLOR]', 'Container.Update("plugin://plugin.video.viks.tv/?mode=select_gr")'),
			('[COLOR FF55FF55][B]= Передачи[/B][/COLOR]', 'Container.Update("plugin://plugin.video.viks.tv/?mode=tvgide")'),
			('[COLOR FFFFFF55][B]* Обновить каналы[/B][/COLOR]', 'Container.Update("plugin://plugin.video.viks.tv/?mode=update")'),])
		
	else: 
		ind=1
		fld=True
		listitem.addContextMenuItems([
			('[COLOR FF55FF55][B]+ Создать группу[/B][/COLOR]', 'Container.Update("plugin://plugin.video.viks.tv/?mode=addgr")'),
			('[COLOR FFFF5555][B]- Удалить группу[/B][/COLOR]', 'Container.Update("plugin://plugin.video.viks.tv/?mode=remgr")'),])
	
	xbmcplugin.addDirectoryItem(handle, uri, listitem, fld, ind)

def set_num_cn(name):
	try:L=eval(__settings__.getSetting("Groups"))
	except:
		L=Ldf
		__settings__.setSetting("Groups",repr(L))

	try:SG=__settings__.getSetting("Sel_gr")
	except:SG=''
	if SG=='':SG='Все каналы'
	
	if SG!='Все каналы':
		CL=get_gr()
		n=CL.index(name)
		sel = xbmcgui.Dialog()
		CL.append(' - В конец списка - ')
		r = sel.select("Перед каналом:", CL)
		CL=get_gr()
		if r>=0 :#and r<len(CL)
			CL.remove(name)
			CL.insert(r, name)
			k=0
			for i in L:
				if i[0]==SG:
					#L[k][1]=CL
					L[k]=(SG,CL)
					__settings__.setSetting("Groups",repr(L))
				k+=1
	xbmc.sleep(300)
	xbmc.executebuiltin("Container.Refresh")


def upd_canals_db():
	LL=[]
	for pg in range(1,5):
		url=httpSiteUrl+'/page/'+str(pg)
		http=getURL(url)
		
		ss='<div class="all_tv">'
		es='an></a>'
		L=mfindal(http,ss,es)
		
		CL=get_gr()
		for i in L:
			ss='http://viks.tv/'
			es='"> <img'
			url=mfindal(i,ss,es)[0]
		
			ss='<img src="'
			es='"><span>'
			img='http://viks.tv/'+mfindal(i,ss,es)[0][len(ss):]

			ss='<span>'
			es='</sp'
			title=mfindal(i,ss,es)[0][len(ss):]
			
			LL.append({'url':url, 'img':img, 'title':title})
			
	__settings__.setSetting("Channels",repr(LL))
	return LL

def upd_canals_db2():
	LL=[]
	for pg in range(1,5):
		url='http://tivix.net/page/'+str(pg)
		http=getURL(url)
		
		ss='<div class="all_tv"'
		es='style="f"> <br><b>'
		L=mfindal(http,ss,es)
		
		CL=get_gr()
		for i in L:
			ss='http://tivix.net/'
			es='.html">'
			url=mfindal(i,ss,es)[0]+'.html'
		
			ss='uploads/posts'
			es='" alt="'
			img='http://tivix.net/'+mfindal(i,ss,es)[0]

			ss='title="'
			es='">'
			title=mfindal(i,ss,es)[0][len(ss):]
			
			LL.append({'url':url, 'img':img, 'title':title})
			
	__settings__.setSetting("Channels2",repr(LL))
	return LL

def upd_EPG():
	if __settings__.getSetting("serv1")=='true' :
		try:L1=eval(__settings__.getSetting("Channels"))
		except:L1=[]
		if L1==[]: L1=upd_canals_db()
	else: L1=[]
	
	if __settings__.getSetting("serv2")=='true':
		try:L2=eval(__settings__.getSetting("Channels2"))
		except:L2=[]
		if L2==[]: L2=upd_canals_db2()
	else: L2=[]

	L1.extend(L2)
	L=L1

	for i in L:
				name  = i['title']
				url   = i['url']
				id = get_id(url)
				if 'viks.tv' in url: serv = 'viks'
				else:                serv = 'tivix'
				get_epg(id, serv)


Ldf=[('Основные',['РТР Планета','5 Канал','НТВ','Пятница!','Че ТВ','Звезда','СТС','ТВЦ','Рен ТВ','ТВ3','Россия 1','Пятый','Первый канал','Домашний','Культура','Россия 24','ТНТ']),
	('Детские',['СоюзМультфильм','Nick Jr','Том и Джерри','Ginger','Nickelodeon','Cartoon Network','2х2','Disney','Карусель']),
	('Познавательные',['Discovery','Моя планета','Охотник и рыболов','Охота и рыбалка','Viasat Explorer','Viasat Nature','Animal Family','Живая планета','National Geographic','История','Viasat History','History','Animal Planet']),
	('Музыкальные',['RU TV','VH1 Europe','Муз ТВ']),
	('Новостные',['CNN','РБК','LifeNews','Россия 1','Первый канал','Россия 24']),
	('Спортивные',['МАТЧ! Арена','Спорт 1','Спорт 2','Футбол 2','Футбол 1','МАТЧ! Футбол 3','Бокс','Матч! Боец','Беларусь 24','КХЛ','Матч! Футбол 1','Матч! Наш футбол','Евроспорт','Евроспорт 2','Матч'])]

def select_gr():
	try:L=eval(__settings__.getSetting("Groups"))
	except:
		L=Ldf
		__settings__.setSetting("Groups",repr(L))
	
	Lg=['Все каналы',]
	for i in L:
		Lg.append(i[0])
		
	if Lg!=[]:
		sel = xbmcgui.Dialog()
		r = sel.select("Группа:", Lg)
	if r>=0:
		SG=Lg[r]
		__settings__.setSetting("Sel_gr",SG)
	if __settings__.getSetting("frsup")=='true': 
		xbmc.sleep(500)
		xbmc.executebuiltin("Container.Refresh")
	
def get_gr():
	try:SG=__settings__.getSetting("Sel_gr")
	except:
		SG=''
	if SG=='': 
		SG='Все каналы'
		__settings__.setSetting("Sel_gr",SG)
	try:L=eval(__settings__.getSetting("Groups"))
	except:L=[]
	CL=[]
	for i in L:
		if i[0]==SG: CL=i[1]
	return CL

def add(id):
	try:L=eval(__settings__.getSetting("Groups"))
	except:L=Ldf
	Lg=[]
	for i in L:
		Lg.append(i[0])
		
	if Lg!=[]:
		sel = xbmcgui.Dialog()
		r = sel.select("Группа:", Lg)
		COG=L[r][1].append(id)
		
	__settings__.setSetting("Groups",repr(L))

def rem(id):
	try:L=eval(__settings__.getSetting("Groups"))
	except:L=Ldf
	L2=[]
	for i in L:
			lj=[]
			for j in i[1]:
				if j!=id: 
					lj.append(j)
			L2.append([i[0],lj])
	__settings__.setSetting("Groups",repr(L2))
	xbmc.executebuiltin("Container.Refresh")

def add_gr():
	name=inputbox('')
	try:L=eval(__settings__.getSetting("Groups"))
	except:L=Ldf
	st=(name,[])
	if st not in L:L.append(st)
	__settings__.setSetting("Groups",repr(L))

def rem_gr():
	try:L=eval(__settings__.getSetting("Groups"))
	except:L=Ldf
	Lg=[]
	for i in L:
		Lg.append(i[0])
		
	if Lg!=[]:
		sel = xbmcgui.Dialog()
		r = sel.select("Группа:", Lg)
	if r>=0:
		name=Lg[r]
	
		L2=[]
		for i in L:
			if i[0]!=name: L2.append(i)
		__settings__.setSetting("Groups",repr(L2))


def root():
	try:
		SG=__settings__.getSetting("Sel_gr")
	except:
		SG=''
	if SG=='':
		SG='Все каналы'
		__settings__.setSetting("Sel_gr",SG)
	add_item ('[COLOR FF55FF55]Группа: '+SG+'[/COLOR]', 'select_gr')
	
	CL=get_gr()
	ttl=len(CL)
	if ttl==0:ttl=250
	Lnm=[]
	
	#try: 
	#	getURL('http://viks.tv/new/logggas.png')
	#	serv1den=1
	#except:serv1den=0
	
	if __settings__.getSetting("serv1")=='true' :
		try:L1=eval(__settings__.getSetting("Channels"))
		except:L1=[]
		if L1==[]: L1=upd_canals_db()
	else: L1=[]
	
	
	if __settings__.getSetting("serv2")=='true':
		try:L2=eval(__settings__.getSetting("Channels2"))
		except:L2=[]
		if L2==[]: L2=upd_canals_db2()
	else: L2=[]

	L1.extend(L2)
	L=L1
	if SG=='Все каналы':
			for i in L:
				name  = i['title']
				url   = i['url']
				cover = i['img']
				
				#if SG=='Все каналы' or name in CL:
				if name not in Lnm:
					add_item (name, 'play', url, ttl, cover)
					Lnm.append(name)
	else:
			for k in CL:
				for i in L:
					name  = i['title']
					if k==name and name not in Lnm:
						url   = i['url']
						cover = i['img']
						add_item (name, 'play', url, ttl, cover)
						Lnm.append(name)
	
	xbmcplugin.endOfDirectory(handle)


def get_id(url):
			if 'viks.tv' in url:ss='viks.tv/'
			else:               ss='tivix.net/'
			es='-'
			id=mfindal(url,ss,es)[0][len(ss):]
			return id



import sqlite3 as db
db_name = os.path.join( addon.getAddonInfo('path'), "epg.db" )
c = db.connect(database=db_name)
cu = c.cursor()
def add_to_db(n, item):
		item=item.replace("'","XXCC").replace('"',"XXDD")
		err=0
		tor_id="n"+n
		litm=str(len(item))
		try:
			cu.execute("DROP TABLE "+tor_id+";")
			c.commit()
		except: pass
		try:
			cu.execute("CREATE TABLE "+tor_id+" (db_item VARCHAR("+litm+"), i VARCHAR(1));")
			c.commit()
		except: 
			err=1
			print "Ошибка БД"
		if err==0:
			cu.execute('INSERT INTO '+tor_id+' (db_item, i) VALUES ("'+item+'", "1");')
			c.commit()
			#c.close()

def get_inf_db(n):
		tor_id="n"+n
		cu.execute(str('SELECT db_item FROM '+tor_id+';'))
		c.commit()
		Linfo = cu.fetchall()
		info=Linfo[0][0].replace("XXCC","'").replace("XXDD",'"')
		return info




def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
	return param

params = get_params()

try:mode = urllib.unquote_plus(params["mode"])
except:mode =""
try:name = urllib.unquote_plus(params["name"])
except:name =""
try:url = urllib.unquote_plus(params["url"])
except:url =""
try:cover = urllib.unquote_plus(params["cover"])
except:cover =""
try:ind = urllib.unquote_plus(params["ind"])
except:ind ="0"


if mode==""         : #root
	root()
	if __settings__.getSetting("epgon")=='true':
		cdata = int(time.strftime('%Y%m%d'))
		try:udata = int(__settings__.getSetting('udata'))
		except: udata = 0
		if cdata>udata:
			__settings__.setSetting("udata",str(cdata))
			upd_EPG()
			xbmc.executebuiltin("Container.Refresh")
if mode=="tvgide"   : tvgide()
if mode=="add"      : add(name)
if mode=="rem"      : rem(name)
if mode=="addgr"    : add_gr()
if mode=="remgr"    : rem_gr()
if mode=="set_num"  : set_num_cn(name)
if mode=="update"   : upd_canals_db()
if mode=="select_gr": select_gr()
if mode=="play"     : play(url, name, cover)
if mode=="rename"   : updatetc.rename_list(int(ind))
#xbmc.executebuiltin("Container.Refresh")

c.close()
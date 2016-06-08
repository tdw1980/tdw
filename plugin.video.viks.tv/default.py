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

from xid import *

def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)

def showMessage(heading, message, times = 3000):
	xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s, "%s")'%(heading, message, times, icon))

def fs_enc(path):
    sys_enc = sys.getfilesystemencoding() if sys.getfilesystemencoding() else 'utf-8'
    return path.decode('utf-8').encode(sys_enc)

def fs_dec(path):
    sys_enc = sys.getfilesystemencoding() if sys.getfilesystemencoding() else 'utf-8'
    return path.decode(sys_enc).encode('utf-8')



class xPlayer(xbmc.Player):

	def __init__(self):
		self.tsserv = None
		self.active = True
		self.started = False
		self.ended = False
		self.paused = False
		self.buffering = False
		xbmc.Player.__init__(self)
		width, height = xPlayer.get_skin_resolution()
		w = width
		h = int(0.14 * height)
		x = 0
		y = (height - h) / 2
		self._ov_window = xbmcgui.Window(12005)
		self._ov_label = xbmcgui.ControlLabel(x, y, w, h, '', alignment=6)
		self._ov_background = xbmcgui.ControlImage(x, y, w, h, fs_dec(xPlayer.get_ov_image()))
		self._ov_background.setColorDiffuse('0xD0000000')
		self.ov_visible = False


	def onPlayBackPaused(self):
		xbmc.sleep(500)
		self.ov_show()
		cnn=__settings__.getSetting("cplayed")
		if __settings__.getSetting("epgosd")=='true':
			cgide=get_cgide(get_idx(cnn), 'serv')
		else:
			cgide=""
		self.ov_update("[B]I I\n[COLOR FFFFFF00]"+cnn+"[/COLOR][/B]\n"+xt(cgide))

	def onPlayBackStarted(self):
		pass
		self.ov_hide()
		#xbmc.executebuiltin('XBMC.ActivateWindow(12005)')

	def onPlayBackResumed(self):
		self.ov_hide()

	def onPlayBackEnded(self):
		pass

	def onPlayBackStopped(self):
		self.ov_hide()

	def onPlayBackSeek(self, ctime, ofs):
		print ofs
		ct=int(time.strftime('%Y%m%d%H%M%S'))
		pt=int(__settings__.getSetting("play_tm"))
		tt=ct-pt
		print tt
		if tt>8:
			print ">8"
			if ofs>0: #след. канал
				self.ov_show()
				#self.ov_update(">I")
				#print '>>>>>>>>>>>>>>>>>>>>>>'
				next ('>')
			elif ofs<0: # пред. канал
				self.ov_show()
				#self.ov_update("I<")
				#print '<<<<<<<<<<<<<<<<<<<<<<'
				next ('<')
		else:
			print "<8"

	def __del__(self):
		self.ov_hide()

	@staticmethod
	def get_ov_image():
		import base64
		ov_image = fs_enc(os.path.join(addon.getAddonInfo('path'), 'bg.png'))
		if not os.path.isfile(ov_image):
			fl = open(ov_image, 'wb')
			fl.write(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII='))
			fl.close()
		return ov_image

	@staticmethod
	def get_skin_resolution():
		import xml.etree.ElementTree as Et
		skin_path = fs_enc(xbmc.translatePath('special://skin/'))
		tree = Et.parse(os.path.join(skin_path, 'addon.xml'))
		res = tree.findall('./extension/res')[0]
		return int(res.attrib['width']), int(res.attrib['height'])

	def ov_show(self):
		if not self.ov_visible:
			self._ov_window.addControls([self._ov_background, self._ov_label])
			self.ov_visible = True

	def ov_hide(self):
		if self.ov_visible:
			self._ov_window.removeControls([self._ov_background, self._ov_label])
			self.ov_visible = False

	def ov_update(self, txt=" "):
		if self.ov_visible:
			self._ov_label.setLabel(txt)#'[B]'+txt+'[/B]'



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

def next (dr='>'):
	ccn=__settings__.getSetting("cplayed")
	print ccn
	try:
		SG=__settings__.getSetting("Sel_gr")
	except:
		SG=''
	if SG=='':
		SG='Все каналы'
		__settings__.setSetting("Sel_gr",SG)
	
	if SG!='Все каналы':
	
		CL=get_gr()
		Lnm=[]
		Lnu=[]
	
		if __settings__.getSetting("serv1")=='true' :
			try:L1=eval(__settings__.getSetting("Channels"))
			except:L1=[]
		else: L1=[]
	
		if __settings__.getSetting("serv2")=='true':
			try:L2=eval(__settings__.getSetting("Channels2"))
			except:L2=[]
		else: L2=[]
	
		if __settings__.getSetting("serv3")=='true':
			try:L3=eval(__settings__.getSetting("Channels3"))
			except:L3=[]
		else: L3=[]
	
		L1.extend(L2)
		L1.extend(L3)
		L=L1
		#print ">"
		for k in CL:
			for i in L:
					name  = i['title']
					if k==name and name not in Lnm:
						url   = i['url']
						cover = i['img']
						#add_item (name, 'play', url, name, cover)
						Lnm.append(name)
						Lnu.append([url,name,cover])
		if dr=='>':
			n=0
			drs='>> \n'
		else: 
			n=-2
			drs='<< \n'
		for p in Lnm:
			n+=1
			if n>=len(Lnm):n=0
			if p==ccn: 
				if __settings__.getSetting("epgosd")=='true':
					cgide=get_cgide(get_idx(Lnu[n][1]), 'serv')
				else:
					cgide=""
				Player.ov_update('[B]'+drs+"[COLOR FFFFFF00]"+Lnu[n][1]+"[/COLOR][/B]\n"+xt(cgide))
				play(Lnu[n][0],Lnu[n][1],Lnu[n][2], False)


if __settings__.getSetting("xplay")=='true': 
	Player=xPlayer()
else:
	Player=xbmc.Player()

def play(url, name ,cover, ref=True):
		__settings__.setSetting("play_tm",time.strftime('%Y%m%d%H%M%S'))
		#Player=xPlayer()#xbmc.Player()
		if ref==True:Player.stop()
		pDialog = xbmcgui.DialogProgressBG()
		pDialog.create('Viks.tv', 'Поиск потоков ...')
		Lpurl=get_stream(url)
		#print url
		try: Lpurl=get_stream(url)
		except:
			Lpurl=[]
			showMessage('viks.tv', 'Канал недоступен')
			return ""
		
		#print '--==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-'
		
		playlist = xbmc.PlayList (xbmc.PLAYLIST_VIDEO)
		playlist.clear()
		
		k=0
		
		for purl in Lpurl:
			k+=1
			print purl
			item = xbmcgui.ListItem(name+" [ "+str(k)+"/"+str(len(Lpurl))+" ]", path=purl, thumbnailImage=cover, iconImage=cover)
			playlist.add(url=purl, listitem=item)
		pDialog.close()
		
		__settings__.setSetting("cplayed",name)
		Player.play(playlist)
		#xbmc.Player().play(playlist)#, item
		
		xbmc.sleep(6000)
		#while  xbmc.Player().isPlaying():
		#		xbmc.sleep(1000)
		
		xbmc.sleep(6000)
		while  xbmc.Player().isPlaying():
				xbmc.sleep(1000)
				#print "========================  playing ======================"
			#
			#print "========================  Refresh ======================"
		if __settings__.getSetting("epgon")=='true':
			if ref==True: 
				xbmc.sleep(300)
				xbmc.executebuiltin("Container.Refresh")

def get_ttv(url):
		#print url
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

def pars_m3u8(url):
	if __settings__.getSetting("pm3u")=='true':
		print 'pars_m3u8'
		print url
		#http://testlivestream.rfn.ru/live/smil:r1.smil/playlist.m3u8
		k1=url.find(".m3u8")
		tmp=url[:k1]
		k2=tmp.rfind("/")
		u2=url[:k2+1]
		try:http=getURL(url)
		except: return []
		debug(http)
		L=http.splitlines()
		L2=[]
		for i in L:
			#ls=len(i)
			if '.m3u8' in i: L2.append(u2+i)
		if len(L2)>1:
			L2.reverse()
			return L2
		else: return [url,]
	else:
		return [url,]

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
			if '.m3u8' in i : 
				if __settings__.getSetting("m3u8")=='true':
					L3u=pars_m3u8(i[len(ss):])
					Lp.extend(L3u)
			elif i not in Lp and 'peers' not in i: 
					Lp.append(i[len(ss):])
		
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
	
	elif 'torrentstream.tv' in url:
		
		if __settings__.getSetting("p2p")=='true':
				http=getURL(url)
				#debug(http)
				ss='<iframe src="'
				es='" style="width:650'
				t=mfindal(http,ss,es)[0][len(ss):]
				trst=get_ttv(t)
				return [trst,]
		else:[]
		
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
				if __settings__.getSetting("m3u8")=='true':
					L3u=pars_m3u8(tmp)
					Lp.extend(L3u)
			else:
				#print "RTMP"
				if __settings__.getSetting("rtmp")=='true':
					purl = tmp
					purl += " swfUrl=http://tivix.net/templates/Default/style/uppod.swf"
					purl += " pageURL=http://tivix.net"
					purl += " swfVfy=true live=true"
					if i not in Lp and 'peers' not in i: Lp.append(purl)
		return Lp


def get_cepg(id, serv):
	#url='http://schedule.tivix.net/channels/'+serv+'/program/'+id+'/today/'
	if serv=='tivix': id='t'+id
	#elif serv=='xmltv': id='x'+id
	try:
		#print id
		E=get_inf_db(id)
		#print E
		L=eval(E)
		#print L
		itm=''
		n=0
		n2=0
		stt=int(__settings__.getSetting('shift'))-6
		h=int(time.strftime('%H'))
		m=int(time.strftime('%M'))
		
		#udata = int(L[10]['start_at'][:11].replace('-',''))
		cdata = int(time.strftime('%Y%m%d'))
		#if cdata!=udata: L=[]
		Ln=[]
		
		for i in L:
			if int(i['start_at'][:11].replace('-',''))==cdata: Ln.append(i)
		#for i in Ln:
		#	n+=1
		for n in range (1,len(Ln)):
			i=Ln[n-1]
			
			#if serv=='xmltv':name=i['name']
			#else:name=eval("u'"+i['name']+"'")
			name=i['name']
			if '\\u0' in name: name=eval("u'"+i['name']+"'")
			try:
				h3 = int(L[n-1]['start_at'][11:13])-stt
				m3 = int(L[n-1]['start_at'][14:16])
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
			if h3>23:hh=str(h3-24)
			elif h3>9:hh=str(h3)
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
					if vv>600:vv=1440-vv
					vp=t2-t1
					if vp>600:vp=1440-vp
					prc=20-(vp*20/vv)
					
					if h2>23:hh2=str(h2-24)
					elif h2>9:hh2=str(h2)
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
					if n2>3: return itm
			
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
		h=int(time.strftime('%H'))
		m=int(time.strftime('%M'))
		
		
		
		#udata = int(L[0]['start_at'][:11].replace('-',''))
		cdata = int(time.strftime('%Y%m%d'))
		#if cdata!=udata: L=[]
		Ln=[]
		
		for i in L:
			#print i['start_at'][:11].replace('-','')
			if int(i['start_at'][:11].replace('-',''))==cdata: Ln.append(i)
		#print Ln
		for i in Ln:
			n+=1
			
			#if serv=='xmltv':
			name=i['name']
			#else: name=eval("u'"+i['name']+"'")
			if '\\u0' in name: name=eval("u'"+name+"'")
			try:
				h3 = int(L[n-1]['start_at'][11:13])-stt
				m3 = int(L[n-1]['start_at'][14:16])
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
			if h3>23:hh=str(h3-24)
			elif h3>9:hh=str(h3)
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
					if vv>600:vv=1440-vv
					vp=t2-t1
					if vp>600:vp=1440-vp
					prc=20-(vp*20/vv)
					
					if h2>23:hh2=str(h2-24)
					elif h2>9:hh2=str(h2)
					else:   hh2="0"+str(h2)
					if m2>9:mm2=str(m2)
					else:   mm2="0"+str(m2)
					etm =hh2+":"+mm2

					iii='---------------------------'
					pb1='[B][COLOR FF5555FF]'+iii[:prc]+"[/COLOR]"
					pb2='[COLOR FFFFFFFF]'+iii[:20-prc]+"[/COLOR][/B]"
					
					itm+= stm+" "+pb1+pb2+" "+etm+'[COLOR FFFFFFFF][B] '+name+'[/B][/COLOR]'#
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
	add_item ('[COLOR FF55FF55][B]Группа: '+SG+'[/B][/COLOR]', 'select_gr')
	
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
	
	
	if __settings__.getSetting("serv3")=='true':
		try:L3=eval(__settings__.getSetting("Channels3"))
		except:L3=[]
		if L3==[]: L3=upd_canals_db3()
	else: L3=[]
	
	
	L1.extend(L2)
	L1.extend(L3)
	
	L=L1
	if SG=='Все каналы':
			for i in L:
				id = ""
				namec  = i['title']
				url   = i['url']
				cover = i['img']
				serv = 'xmltv'
				id = get_idx(namec)
				name=get_cgide(id, serv)
				
				#if SG=='Все каналы' or name in CL:
				if name!="" and name!=None and namec not in Lnm:
						add_item (name, 'play', url, namec, cover)
						Lnm.append(namec)

	else:
			for k in CL:
				for i in L:
					namec  = i['title']
					if k==namec:
						url   = i['url']
						cover = i['img']
						id = get_id(url)
						#if 'viks.tv' in url: serv = 'viks'
						#elif 'tivix' in url: serv = 'tivix'
						#else:
						serv = 'xmltv'
						id = get_idx(namec)
						name=get_cgide(id, serv)
						if name!="" and name!=None and namec not in Lnm: 
							add_item (name, 'play', url, namec, cover)
							Lnm.append(namec)
	
	xbmcplugin.endOfDirectory(handle)


def get_epg(id, serv, name=''):
	import time
	url='http://schedule.tivix.net/channels/'+serv+'/program/'+id+'/today/'
	udd = int(time.strftime('%Y%m%d'))
	#if 1==1:
	if serv=='tivix': id='t'+id
	try:
			E=getURL(url)
			L=eval(E)
			L2=[]
			for i in L:
					desc=i['name']
					h2 = int(i['start_at'][11:13])+3
					if h2>23:hh2=str(h2-24)
					elif h2>9:hh2=str(h2)
					else:   hh2="0"+str(h2)
					start_at=i['start_at'][:11]+hh2+i['start_at'][13:]
					#print start_at
					j={'name':desc,'start_at':start_at}
					L2.append(j)
			E2=repr(L2)

			idx=get_idx(name)
			if idx!="": add_to_db(idx, E2)
			
			#print 'обновлена устаревшая программа: '+id
	except:
			print 'неудалось загрузить программу: '+id

#import YaTv
def add_item (name, mode="", path = Pdir, ind="0", cover=None, funart=None):
	#print name
	#print path
	if __settings__.getSetting("fanart")=='true':funart=cover
	else: funart=icon
	if __settings__.getSetting("icons")!='true':cover=icon

	listitem = xbmcgui.ListItem(name, iconImage=cover)#"[B]"++"[/B]"
	listitem.setProperty('fanart_image', funart)
	uri = sys.argv[0] + '?mode='+mode
	uri += '&url='  + urllib.quote_plus(path)#.encode('utf-8')
	uri += '&name='  + urllib.quote_plus(xt(ind))
	uri += '&ind='  + urllib.quote_plus(str(ind))
	if cover!=None:uri += '&cover='  + urllib.quote_plus(cover)
	if funart!=None and funart!="":uri += '&funart='  + urllib.quote_plus(funart)
	
	if mode=="play":
		#id = get_id(path)
		if __settings__.getSetting("epgon")=='true':
			#if __settings__.getSetting("epgtvx")=='true':
			#	if 'viks.tv' in path:dict={"plot":get_cepg(id,'viks')}
			#	else:                dict={"plot":get_cepg(id,'tivix')}
			#else:
			#	dict={"plot":''}
				
			#if dict['plot']=='':
				id = get_idx(ind)
				#if id=='': print ind
				dict={"plot":get_cepg(id,'xmltv').replace('&quot;','"').replace('&apos;',"'")}
				
				#dict=YaTv.GetPr('308')
				#print dict
		else: dict={}
		try:listitem.setInfo(type = "Video", infoLabels = dict)
		except: pass

		fld=False
		#listitem.setProperty('IsPlayable', 'true')
		ContextGr=[('[B]Все каналы[/B]', 'Container.Update("plugin://plugin.video.viks.tv/?mode=context_gr&name=Все каналы")'),]
		for grn in list_gr():
			ContextGr.append(('[B]'+grn+'[/B]','Container.Update("plugin://plugin.video.viks.tv/?mode=context_gr&name='+grn+'")'))
		ContextGr.append(('[COLOR FF55FF55][B]ПЕРЕДАЧИ[/B][/COLOR]', 'Container.Update("plugin://plugin.video.viks.tv/?mode=tvgide")'))

		ContextCmd=[
			('[COLOR FF55FF55][B]ГРУППА[/B][/COLOR]', 'Container.Update("plugin://plugin.video.viks.tv/?mode=select_gr")'),
			('[COLOR FF55FF55][B]+ Добавить в группу[/B][/COLOR]', 'Container.Update("plugin://plugin.video.viks.tv/?mode=add&name='+ind+'")'),
			('[COLOR FFFF5555][B]- Удалить из группы[/B][/COLOR]', 'Container.Update("plugin://plugin.video.viks.tv/?mode=rem&name='+ind+'")'),
			('[COLOR FF55FF55][B]<> Переместить канал[/B][/COLOR]', 'Container.Update("plugin://plugin.video.viks.tv/?mode=set_num&name='+ind+'")'),
		('[COLOR FFFFFF55][B]* Обновить каналы[/B][/COLOR]', 'Container.Update("plugin://plugin.video.viks.tv/?mode=update")'),
			('[COLOR FFFFFF55][B]* Обновить программу[/B][/COLOR]', 'Container.Update("plugin://plugin.video.viks.tv/?mode=updateepg")'),
			('[COLOR FF55FF55][B]ПЕРЕДАЧИ[/B][/COLOR]', 'Container.Update("plugin://plugin.video.viks.tv/?mode=tvgide")')]#, replaceItems=True)
			
		#ContextGr.extend(Lcmd)
		if __settings__.getSetting("grincm")=='true':listitem.addContextMenuItems(ContextGr, replaceItems=True)
		else:										listitem.addContextMenuItems(ContextCmd, replaceItems=True)
	else: 
		#ind=1
		fld=True
		listitem.addContextMenuItems([
			('[COLOR FF55FF55][B]+ Создать группу[/B][/COLOR]', 'Container.Update("plugin://plugin.video.viks.tv/?mode=addgr")'),
			('[COLOR FFFF5555][B]- Удалить группу[/B][/COLOR]', 'Container.Update("plugin://plugin.video.viks.tv/?mode=remgr")'),
			('[COLOR FFFFFF55][B]* Обновить каналы[/B][/COLOR]', 'Container.Update("plugin://plugin.video.viks.tv/?mode=update")'),
			('[COLOR FFFFFF55][B]* Обновить программу[/B][/COLOR]', 'Container.Update("plugin://plugin.video.viks.tv/?mode=updateepg")'),
			('[COLOR FFFFFF55][B]Управление каналами[/B][/COLOR]', 'Container.Update("plugin://plugin.video.viks.tv/?mode=grman")'),])
	xbmcplugin.addDirectoryItem(handle, uri, listitem, fld)#, ind)

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
			es='.html'
			url=mfindal(i,ss,es)[0]+es
		
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
def upd_canals_db3():
	LL=[]
	url='http://torrentstream.tv/browse-vse-kanali-tv-videos-1-date.html'
	http=getURL(url)
		
	ss='<li>'
	es='</li>'
	L=mfindal(http,ss,es)
	
	#CL=get_gr()
	for i in L:
		try:
			#debug (i)
			ss='<h3><a href="'
			es='" class="pm-title-link'
			url=mfindal(i,ss,es)[0][len(ss):]
			#print url
		
			ss='<img src="'
			es='" alt="'
			img=mfindal(i,ss,es)[0][len(ss):]

			ss='pm-title-link " title="'
			es='</a></h3>'
			title=mfindal(i,ss,es)[0]#[len(ss):]
			r=title.find('">')+2
			title=title[r:]
			
			LL.append({'url':url, 'img':img, 'title':title})
		except: pass
	__settings__.setSetting("Channels3",repr(LL))
	return LL

def upd_EPG():
	#if __settings__.getSetting("serv1")=='true' :
	try:L1=eval(__settings__.getSetting("Channels"))
	except:L1=[]
	#	if L1==[]: L1=upd_canals_db()
	#else: L1=[]
	
	#if __settings__.getSetting("serv2")=='true':
	try:L2=eval(__settings__.getSetting("Channels2"))
	except:L2=[]
	#	if L2==[]: L2=upd_canals_db2()
	#else: L2=[]

	L1.extend(L2)
	L=L1
	j=0
	t=len(L)
	for i in L:
				j+=1
				name  = i['title']
				url   = i['url']
				id = get_id(url)
				if 'viks.tv' in url: serv = 'viks'
				else:                serv = 'tivix'
				get_epg(id, serv, name)
				pDialog.update(int(j*100/t), message=name+' ...')

def upd_EPG_xmltv():
	d=pars_xmltv(dload_epg_xml())
	j=0
	for id in d.keys():
		j+=1
		#print d[id]
		add_to_db("x"+id, repr(d[id]))
		pDialog.update(j/3, message='xmltv ...')

def upd_EPG_itv():
	d=intertv()
	j=1
	for id in d.keys():
		j+=1
		#print d[id]
		add_to_db(id, repr(d[id]))
		pDialog.update(j/4, message='itv ...')


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
	
	xbmc.sleep(300)
	xbmc.executebuiltin("Container.Refresh")

def list_gr():
	try:L=eval(__settings__.getSetting("Groups"))
	except:
		L=Ldf
		__settings__.setSetting("Groups",repr(L))
	Lg=[]
	for i in L:
		Lg.append(i[0])
		
	return Lg

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
	add_item ('[COLOR FF55FF55][B]Группа: '+SG+'[/B][/COLOR]', 'select_gr')
	
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
	
	
	if __settings__.getSetting("serv3")=='true':
		try:L3=eval(__settings__.getSetting("Channels3"))
		except:L3=[]
		if L3==[]: L3=upd_canals_db3()
	else: L3=[]
	
	
	L1.extend(L2)
	L1.extend(L3)
	L=L1
	if SG=='Все каналы':
		if __settings__.getSetting("abc")=='false':
			for i in L:
				name  = i['title']
				url   = i['url']
				cover = i['img']
				#print name
				#if SG=='Все каналы' or name in CL:
				if __settings__.getSetting("grinnm")=='true': name=add_grn(name)
				if name not in Lnm:
					add_item ("[B]"+name+"[/B]", 'play', url, name, cover)
					Lnm.append(name)
		else:
			CL=[]
			for i in L:
				CL.append(i['title'])
			CL.sort()
			
			for k in CL:
				for i in L:
					name  = i['title']
					if k==name and name not in Lnm:
						url   = i['url']
						cover = i['img']
						add_item ("[B]"+name+"[/B]", 'play', url, name, cover)
						Lnm.append(name)

	else:
			for k in CL:
				for i in L:
					name  = i['title']
					if k==name and name not in Lnm:
						url   = i['url']
						cover = i['img']
						add_item ("[B]"+name+"[/B]", 'play', url, name, cover)
						Lnm.append(name)
	
	xbmcplugin.endOfDirectory(handle)

def add_grn(name):
	try:L=eval(__settings__.getSetting("Groups"))
	except:L=[]
	for i in L:
		gr=i[0]
		if name in i[1]: name=name+"   [COLOR 40FFFFFF]["+gr+"][/COLOR]"
	return name


def get_id(url):
		try:
			if 'viks.tv' in url:ss='viks.tv/'
			else:               ss='tivix.net/'
			es='-'
			id=mfindal(url,ss,es)[0][len(ss):]
			return id
		except:
			return '0'

def get_idx(name):
	try:
		id="x"+xmlid[name]
		#print id
	except: id=''
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



def dload_epg_xml():
	try:
			target='http://programtv.ru/xmltv.xml.gz'
			fp = xbmc.translatePath(os.path.join(addon.getAddonInfo('path'), 'tmp.zip'))
			
			req = urllib2.Request(url = target, data = None)
			req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)')
			resp = urllib2.urlopen(req)
			fl = open(fp, "wb")
			fl.write(resp.read())
			fl.close()
			
			xml=ungz(fp)
			#os.remove(fp)
			return xml
	except Exception, e:
			print 'HTTP ERROR ' + str(e)
			return ''


def ungz(filename):
	import gzip
	with gzip.open(filename, 'rb') as f:
		file_content = f.read()
		return file_content

def pars_xmltv(xml):
	ss="<programme "
	es="</programme>"
	L=mfindal(xml,ss,es)
	epg={}
	for i in L:
		ss='start="'
		es=' +0300" stop="'
		st=mfindal(i,ss,es)[0][len(ss):]
		
		ss='stop="'
		es=' +0300" channel'
		et=mfindal(i,ss,es)[0][len(ss):]
		
		ss=' channel="'
		es='">'
		id=mfindal(i,ss,es)[0][len(ss):]
		
		ss='<title>'
		es='</title>'
		title=mfindal(i,ss,es)[0][len(ss):]
		
		try:Le=epg[id]
		except: Le=[]
		
		n=len(Le)
		sc=int(st[8:10])-3
		if sc<0 and n>8: sc+=24
		elif sc<0 and n<8: ssc="00"
		elif sc<10: ssc="0"+str(sc)
		else:ssc=str(sc)

		start_at=xt(st[0:4]+"-"+st[4:6]+"-"+st[6:8]+" "+ssc+":"+st[10:12]+":00")
		#print start_at+" "+title
		try:
			Le.append({"name":title, "start_at":start_at})
			epg[id]=Le
		except: 
			pass
			#print id+"  :  "+start_at+"  :  "+title
	return epg

def dload_epg_inter():
	try:
			target='http://www.teleguide.info/download/new3/inter-tv.zip'
			fp = xbmc.translatePath(os.path.join(addon.getAddonInfo('path'), 'inter-tv.zip'))
			
			req = urllib2.Request(url = target, data = None)
			req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)')
			resp = urllib2.urlopen(req)
			fl = open(fp, "wb")
			fl.write(resp.read())
			fl.close()
			
			itv=unzip(fp)
			#os.remove(fp)
			return itv
	except Exception, e:
			print 'HTTP ERROR ' + str(e)
			return ''

def unzip(filename):
	from zipfile import ZipFile
	fil = ZipFile(filename, 'r')
	for name in fil.namelist():
		f=fil.read(name)
		return f

Lv=['понед', 'вторн', 'среда', 'четве', 'пятни', 'суббо', 'воскре', 'ПОНЕД', 'ВТОРН', 'СРЕДА', 'ЧЕТВЕ', 'ПЯТНИ', 'СУББО', 'ВОСКР']

def intertv():
	itv=dload_epg_inter()
	itv=itv.decode('windows-1251')
	L=itv.splitlines()
	L2=[]
	L3={}
	n=0
	for i in L:
		if i[:3]!='   ' and i!='tv.all' and i!='':
			t=i[:5].encode('utf-8')
			#print t
			if t in Lv :
				n+=1
				try:
					try:
						if idx!='':
							Lpr=L3[idx]
							Lpr.extend(L2)
					except:
						L3[idx]=L2
				except:pass
				tmp=eval('["'+i.replace('. ','", "')+'"]')
				#print tmp
				data=tmp[1].replace(' января', '-01').replace(' февраля', '-02').replace(' марта', '-03').replace(' апреля', '-04').replace(' мая', '-05').replace(' июня', '-06').replace(' июля', '-07').replace(' августа', '-08').replace(' сентября', '-09').replace(' октября', '-10').replace(' ноября', '-11').replace(' декабря', '-12')
				data=data.replace(' Январь', '-01').replace(' Февраль', '-02').replace(' Март', '-03').replace(' Апрель', '-04').replace(' Май', '-05').replace(' Июнь', '-06').replace(' Июль', '-07').replace(' Август', '-08').replace(' Сентябрь', '-09').replace(' Октябрь', '-10').replace(' Ноябрь', '-11').replace(' Декабрь', '-12')

				fdata=time.strftime('%Y-')+data[3:]+"-"+data[:2]
				name=tmp[2]
				idx=get_idx(name)
				#if idx=='0': print name
				#if n>5:
				#	debug(repr(L3))
				#	return ""
				L2=[]
			else:
				pr_nm = i[6:]
				#stm = i[:5]
				sc=int(i[:2])-3
				if sc<0: sc+=24
				if sc<10: ssc="0"+str(sc)
				else:ssc=str(sc)
				stm=ssc+i[2:5]
				
				start_at=fdata+" "+stm+":00"
				#print start_at
				if sc<24:L2.append({"name":pr_nm, "start_at": start_at})
	#debug (repr(L3['x146']))
	return L3

def upd_stv():
	opener = urllib2.build_opener()
	opener.addheaders.append(('Cookie', 'favorites=1TV%3BRTR%3BNTV%3BMIR%3BTVC%3BKUL%3BMatchTV%3BTNT%3BDOMASHNIY%3BRenTV%3BSTS%3BPiter5_RUS%3BZVEZDA%3BChe%3BKarusel%3B2X2%3BDisney%3BU%3BTV3%3BOTR%3BFriday%3BVesti%3BTNT_4%3BEhoFilm%3B360d%3B360dHD%3BVKT%3BMOSCOW-24%3BDOVERIE%3BPingLolo%3BFAMILY%3Bntv%2B41%3BAMEDIA%3BAmediaHit%3BAmedia1%3BBollywood%3BDrama%3BFOX%20CRIME%3BFOX%20LIFE%3BHDKino%3BPARAMAUNT%3BParamounHD%3BParaComedy%3BSET_RUSSIA%3BAXNSciFi%3BSonyTurbo%3BTV1000%3BTV1000_Act%3BTV1000_RK%3BTV21%3BZee-TV%3BDomKino%3BDomKinoP%3BEuroKINO%3BILLUSION%2B%3BIndia%3Bntv%2B34%3BKinoTV%3Bntv%2B4%3BKinipokaz%3BKinop_HD-1%3BKinop_HD-2%3BKinoPrHD%3Bntv%2B40%3BKomedia1%3BKomedia%3BMir_serial%3BmnogoTV%3BMenKino%3BNSTV%3Bntv%2B3%3Bntv%2B7%3BNacheHD%3BOstroHD%3Bntv%2B10%3BRTVi-LK%3BRTVi-NK%3BRus-Bestst%3BRuDetektiv%3BRU_ILLusio%3BRusRoman%3BSemeynoeHD%3BStrahnoeHD%3BSTSLove%3Bntv%2B39%3BFeniks%3BMatchTV%3BABMotors%3Bntv%2B13%3BEuro-2%3BEurospNews%3Bntv%2B23%3BVia_Sport%3BBoxingTV%3Bntv%2B9%3BKHL_HD%3BMatcharena%3Bboets%3BMatchigra%3BMatchsport%3Bntv%2B11%3Bntv%2B44%3BSporthit%3BNautical%3Bntv%2B1%3BRU_Extrem%3BFootBallTV%3BArirang%3Bntv%2B25%3BBBC_Entert%3BBBC-World%3Bntv%2B33%3BCCTVNews%3BCNBC%3Bntv%2B30%3BCNN_ENG%3BDW%3BDW_DEU%3Bntv%2B19%3BFrance24%3BFrance_FR%3BJSTV%3BNewsOne%3BNHK_World%3BRus_Today%3BRT_Doc%3BRTEspanol%3BRTDrus%3BRAIN%3BKommers_TV%3BLDPR%3BMir24%3BRBK%3B4P.INFO%3B24_DOC%3B365_day%3Bntv%2B17%3BDa%20Vinci%3Bntv%2B16%3Bntv%2B28%3BDiscov_VE%3BGalaxy_TV%3BHistor%20%3BHistoryENG%3Bntv%2B18%3BOCEAN-TV%3BENCYCLO%3BExplorer%3BHistory%3BNature_CEE%3BZooTV%3BZoopark%3BViM%3BVopr-Otvet%3BEGE%3BGivPlaneta%3BJivPriroda%3BIstoria%3BWho_is_who%3BMy_Planet%3BNANO_TV%3BNauka_2.0%3B1Obrazovat%3BProsvejeni%3BTop_secret%3BSTRANA%3BTNV_PL%3B1HD%3BA-OnHipHop%3BBizTV%3BBridge-TV%3BC_Music_TV%3BDangeTV%3BEuropaPlus%3BHardLifeTV%3BiConcerts%3BJuCeTV%3BMCMPOP%3BMCMTOP%3Bntv%2B26%3BMTV_Dance%3BMTVDI%3BMTV_Europ%3BMTV_Hits%3BMTVHI%3BMTV_Music%3BMTV_ROCKS%3BMTVRI%3BMTVRus%3BMTV_AM%3BMusicBox-R%3BMusicBox-T%3BRAP%3BRU-TV%3BRusong_TV%3BTOPSONG_T%3BTRACE_URBA%3BTVMChannel%3BVH1_Class%3BVH1_EURO%3BW_Music_Ch%3BLa-minor%3BMUZ_TVnew%3BMuZ-One%3BO2TV%3BA-ONE%3BSHANSON%3BAmazing%3BAngelTV%3BReality%3BCCTV%3BDTXEMEA%3BEnglishClu%3BFash_One%3BFashion_TV%3BFLN%3BFoodNet%3BFuel_TV_HD%3BGame_Show%3BGlobalStar%3BInsiUlHD%3BLuxe_TV%3BMAN_TV%3BMotors_TV%3BMuseum_HD%3BmyZen.tv%3Bntv%2B20%3BOutdoor%3Bprodengi%3BRTGInt%3BRTG_TV%3BStyle%26moda%3BTTS%3BShoppingLi%3BBulvar%3BStyle_TV%3BTDK%3BTLC%3BTop%20Shop%20T%3BTrChenel%3BTravel%2BAdv%3BTVclub%3BTV_Mail%3BTV_SALE%3Bntv%2B32%3BVintage_%3BWBC%3BW_Fashion%3Bautoplus%3BAGRO-TV%3BBalansTV%3BBober%3BVremya%3BD_Jivotnie%3BDrive_MTU%3BEDA%3BJiVi%3BZagorod_zh%3Bzagorodny%3BZdorov_MTU%3BKuhna%3BMirUvlech%3BMuzhskoj%3BNedvigim%3BNostalgi%3BWeapons%3BHa%26Fi_MTU%3BOhot%26Ribal%3BPark_Razvl%3B1InternetK%3BPsihology%3BRaz-TV%3BRetro_MTU%3Bsarafan-tv%3BSojuz%3BSPAS%3BTeatr%3BTeledom%3BTelekafe%3BTeletravel%3BTehno24%3BTONUS-TV%3B3Angela%3BTurInfo%3BUsadba_MTU%3BUspeh%3BEgoist-TV%3BHUMOUR-TV%3BAni%3BBaby_TV%3BBoomerang%3Bntv%2B29%3BGingerHD%3BGulli%3BJIMJAM%3BNick_Jr%3Bntv%2B15%3BNickelodHD%3BTiJi%3BDetskiy%3Bntv%2B8%3BMother%26Chi%3BMult%3BMultimania%3BRadost_moj%3BUlibkaRebe%3BAmediaPRHD%3BAnFamilHD%3BAnimalPlHD%3BArteHD%3BEurekaHD%3BEuroSporHD%3BFashiOneHD%3BFashion_HD%3BFOXLIFE_HD%3BHD-Life%3BHD_Media%3BHD_Media3D%3BLuxe_TV_HD%3BMezzoLive%3BMGM_HD%3BMTV_LiveHD%3BNatGeoW_HD%3BNat_Geo_HD%3BOutdoor%20HD%3BRTDrushd%3BSET_HD%3BTeleTravHD%3BTrace_SpHD%3BTr_Chan_HD%3BTravAdHD%3BTV1000Come%3BTV1000Mega%3BTV1000Prem%3BRAIN_HD%3BEDA_HD%3BMatchareHD%3BMirHD%3BOhotRybHD%3B1TVHD%3BIQHD%3BRTRHD%3BBlueHust%3BBrazzEuro%3BCandy3D%3BCandy%3BDaring!TV%3BFrench_Lov%3BHustle3DHD%3BHustler%3BPlayboy_TV%3BXXL%3BIskushenie%3BNightClub%3BRusnight%3B8_KANAL%3BHistor2%3BBelarus-TV%3BDomMagazin%3BInva_Media%3BKaleidosco%3BKVNTV%3BMatchKmir%3BKrasLin%3BLiderTV%3BNadegda%3BNasheTV%3B1_Meteo%3BProdvigeni%3BRGD%3BRigiy%3BTBN%3BTvoy%3BTNV%3BToshkaTV%3BTRO%3BUvelir'))
	urllib2.install_opener(opener)
	url = 'http://new.s-tv.ru/tv/'
	http = getURL(url)
	#debug (http)
	ss='<td class="channel">'
	es='<table class="item_table">'
	L=mfindal(http,ss,es)
	epg={}
	#debug (repr(L))
	n=0
	t=len(L)
	for i in L:
		n+=1
		#try:
		if i!="":
			#debug (i)
			ss='width="45px" title="'
			es='" />'
			cnl_nm=mfindal(i,ss,es)[0][len(ss):]
			idx=get_idx(cnl_nm)
			if idx!="":
				ss='<div class="prg_item">'
				es='</div>'
				L2=mfindal(i,ss,es)
				Le=[]
				
				for j in L2:
					
					j=j.replace('</span></span>','').replace('<span class="prg_item_cc">&lowast;</span>','')
					#debug (j)
					ss='href="#'
					es='</a>'
					if ss not in j: 
						ss='prg_item_no'
						es='</span>'
					tmp=j[j.find(ss):]
					title=mfindal(tmp,ss,es)[0][len(ss):]
					title=title[title.find('>')+1:]
			
					ss='class="prg_item_time">'
					es='</span>'
					st=mfindal(j,ss,es)[0][len(ss):]
			
					start_at=time.strftime('%Y-%m-%d')+" "+st+":00"
					#print start_at+" "+title
		
					Le.append({"name":title, "start_at":start_at})
				#epg[idx]=Le
				pDialog.update(int(n*100/t), message=cnl_nm)
				add_to_db(idx, repr(Le))
			#else:
			#	print cnl_nm
				#debug (repr(Le))
		#except: print i
			
			#[{"name":"", "start_at": "2016-05-26 --:--:--"}]
	
	#return epg


#upd_yatv()

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
		if cdata>udata and __settings__.getSetting("epgon")=='true':
			pDialog = xbmcgui.DialogProgressBG()
			pDialog.create('Viks.tv', 'Обновление EPG ...')
			__settings__.setSetting("udata",str(cdata))
			#if __settings__.getSetting('epgxml')=='true': upd_EPG_xmltv()
			#if __settings__.getSetting('epgitv')=='true': upd_EPG_itv()
			if __settings__.getSetting('stv')=='true': upd_stv()
			if __settings__.getSetting('epgtvx')=='true': upd_EPG()
			pDialog.close()
			xbmc.executebuiltin("Container.Refresh")

if mode=="context_gr"  :
		__settings__.setSetting("Sel_gr",name)
		xbmc.sleep(300)
		xbmc.executebuiltin("Container.Refresh")

if mode=="updateepg"   :
			cdata = int(time.strftime('%Y%m%d'))
			try:udata = int(__settings__.getSetting('udata'))
			except: udata = 0
			pDialog = xbmcgui.DialogProgressBG()
			pDialog.create('Viks.tv', 'Обновление EPG ...')
			__settings__.setSetting("udata",str(cdata))
			#if __settings__.getSetting('epgxml')=='true': upd_EPG_xmltv()
			#if __settings__.getSetting('epgitv')=='true': upd_EPG_itv()
			if __settings__.getSetting('stv')=='true': upd_stv()
			if __settings__.getSetting('epgtvx')=='true': upd_EPG()
			
			pDialog.close()

if mode=="grman"   :
	import GrBox
	GrBox.run("GrBox")

if mode=="tvgide"   : tvgide()
if mode=="add"      : add(name)
if mode=="rem"      : rem(name)
if mode=="addgr"    : add_gr()
if mode=="remgr"    : rem_gr()
if mode=="set_num"  : set_num_cn(name)
if mode=="update"   : 
			pDialog = xbmcgui.DialogProgressBG()
			pDialog.create('Viks.tv', 'Обновление списка каналов ...')
			upd_canals_db()
			pDialog.update(33, message='Обновление списка каналов ...')
			upd_canals_db2()
			pDialog.update(66, message='Обновление списка каналов ...')
			upd_canals_db3()
			pDialog.close()
if mode=="select_gr": select_gr()
if mode=="play"     : play(url, name, cover)
if mode=="rename"   : updatetc.rename_list(int(ind))

c.close()



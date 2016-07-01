# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, os, urllib, sys, urllib2, time

PLUGIN_NAME   = 'plugin.video.pazl.tv'
handle = int(sys.argv[1])
addon = xbmcaddon.Addon(id='plugin.video.pazl.tv')
__settings__ = xbmcaddon.Addon(id='plugin.video.pazl.tv')

siteUrl = 'viks.tv'
httpSiteUrl = 'http://' + siteUrl

Pdir = addon.getAddonInfo('path')
icon = xbmc.translatePath(os.path.join(addon.getAddonInfo('path'), 'icon.png'))
fanart = xbmc.translatePath(os.path.join(addon.getAddonInfo('path'), 'fanart.png'))
Logo = xbmc.translatePath(os.path.join(addon.getAddonInfo('path'), 'logo'))
UserDir = xbmc.translatePath(os.path.join(xbmc.translatePath("special://masterprofile/"),"addon_data","plugin.video.pazl.tv"))

xbmcplugin.setContent(int(sys.argv[1]), 'movies')

from xid import *
from DefGR import *
#Ldf=eval(__settings__.getSetting("Groups"))
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

def lower(s):
	try:s=s.decode('utf-8')
	except: pass
	try:s=s.decode('windows-1251')
	except: pass
	s=s.lower().encode('utf-8')
	return s

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
		xbmc.sleep(300)
		self.ov_show()
		self.ov_update('[B]I I[/B]')
		if __settings__.getSetting("split")=='true':  cnn=__settings__.getSetting("cplayed").replace(" #1","").replace(" #2","").replace(" #3","").replace(" #4","")
		else:                                         cnn=__settings__.getSetting("cplayed").replace(" #1","[COLOR 40FFFFFF] #1[/COLOR]").replace(" #2","[COLOR 40FFFFFF] #2[/COLOR]").replace(" #3","[COLOR 40FFFFFF] #3[/COLOR]").replace(" #4","[COLOR 40FFFFFF] #4[/COLOR]")
		if __settings__.getSetting("epgosd")=='true':
			cgide=get_cgide(get_idx(cnn), 'serv')
		else:
			cgide=""
		self.ov_update("[B]I I\n[COLOR FFFFFF00]"+cnn+"[/COLOR][/B]\n"+xt(cgide))

	def onPlayBackStarted(self):
		self.ov_hide()

	def onPlayBackResumed(self):
		self.ov_hide()

	def onPlayBackEnded(self):
		pass

	def onPlayBackStopped(self):
		self.ov_hide()
	
	def onPlayBackSpeedChanged(self, ofs):
		ct=int(time.strftime('%Y%m%d%H%M%S'))
		pt=int(__settings__.getSetting("play_tm"))
		tt=ct-pt
		if tt>6:
			if ofs>1: #след. канал
				self.ov_show()
				self.ov_update('[B]>>[/B]')
				__settings__.setSetting("n_play","0")
				__settings__.setSetting("lastnx",">")
				next ('>')
			elif ofs<0: # пред. канал
				self.ov_show()
				self.ov_update('[B]<<[/B]')
				__settings__.setSetting("n_play","0")
				__settings__.setSetting("lastnx","<")
				next ('<')
		else:
			print "<8"

	def onPlayBackSeek(self, ctime, ofs):
		ct=int(time.strftime('%Y%m%d%H%M%S'))
		pt=int(__settings__.getSetting("play_tm"))
		tt=ct-pt
		if tt>6:
			if ofs>0: #след. канал
				self.ov_show()
				self.ov_update('[B]>>[/B]')
				__settings__.setSetting("n_play","0")
				__settings__.setSetting("lastnx",">")
				next ('>')
			elif ofs<0: # пред. канал
				self.ov_show()
				self.ov_update('[B]<<[/B]')
				__settings__.setSetting("n_play","0")
				__settings__.setSetting("lastnx","<")
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

def GETimg(target, nmi):
	#lfimg=os.listdir(Logo)
	if nmi =='':
		#print target
		return target
	LogoDir=__settings__.getSetting("logodir")
	if LogoDir=="":LogoDir=Logo
	path1 = fs_enc(os.path.join(LogoDir,nmi+'.png'))
	path2 = fs_enc(os.path.join(Logo,nmi+'.png'))
	try:
		try:
			sz=os.path.getsize(path1)
			path=path1
		except:
			try:
				sz=os.path.getsize(path2)
				path=path2
			except:
				sz=0
				path=path2
		
		if sz > 0:
			return path
		else:
			if __settings__.getSetting("dllogo")=='true': return target
			
			pDialog = xbmcgui.DialogProgressBG()
			pDialog.create('Пазл ТВ', 'Загрузка логотипа: '+ nmi)
			req = urllib2.Request(url = target, data = None)
			req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)')
			resp = urllib2.urlopen(req)
			fl = open(path, "wb")
			fl.write(resp.read())
			fl.close()
			pDialog.close()
			return path
	except:
			print "err:  "+target
			return target


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
	print "next ok"
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
		Lid=[]
		
		L=get_all_channeles()
		
		for k in CL:
			for i in L:
					name  = i['title']
					name2  = i['title']
					id=get_idx(name)
					#if __settings__.getSetting("split")=='true':
					#	urls=get_allurls(id, L)
					#else:
					#	urls=[]
					if k==name and id not in Lid:
						
						cover = i['img']
						if __settings__.getSetting("intlogo")=='true':  cover = GETimg(cover, id.replace("xttv",""))
						if __settings__.getSetting("split")=='true':
																		urls=get_allurls(id, L)
																		name=name.replace(" #1","").replace(" #2","").replace(" #3","").replace(" #4","")
						else: urls = [i['url'],]
						
						#add_item ("[B]"+name+"[/B]", 'play', urls, name, cover)
						if id!="" and __settings__.getSetting("split")=='true':Lid.append(id)
						Lnm.append(name2)
						Lnu.append([urls,name2,cover])
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
				if __settings__.getSetting("split")=='true':nmc=Lnu[n][1].replace(" #1","").replace(" #2","").replace(" #3","").replace(" #4","")
				else: nmc=Lnu[n][1]
				Player.ov_update('[B]'+drs+"[COLOR FFFFFF00]"+nmc+"[/COLOR][/B]\n"+xt(cgide))
				play(Lnu[n][0],Lnu[n][1],Lnu[n][2], False)
	else:
		Player.ov_update('[B][COLOR FFFF0000][ ! ][/COLOR]\nПереключение каналов\nдоступно только в группах.[/B]')
		xbmc.sleep(3000)
		Player.ov_hide()
		
if __settings__.getSetting("xplay")=='true': 
	Player=xPlayer()
else:
	Player=xbmc.Player()

def play(urls, name ,cover, ref=True):
	#print urls
	__settings__.setSetting("play_tm",time.strftime('%Y%m%d%H%M%S'))
	if ref==True:Player.stop()
	pDialog = xbmcgui.DialogProgressBG()
	pDialog.create('Пазл ТВ', 'Поиск потоков ...')
	Lpurl=[]
	for url in urls:
		#Lcurl=get_stream(url)
		try: Lcurl=get_stream(url)
		except:Lcurl=[]
		try:Lpurl.extend(Lcurl)
		except:Lcurl=[]
	
	Lpurl2=[]
	Lm3u8 =[]
	Lrtmp =[]
	Lp2p  =[]
	Lourl =[]
	Ltmp=[]
	
	for i in Lpurl:
		if '.m3u8' in i and i not in Lm3u8:  Lm3u8.append(i)
		elif 'rtmp' in i and i not in Lrtmp: Lrtmp.append(i)
		elif '/ace/' in i and i not in Lp2p: Lp2p.append(i)
		elif i not in Ltmp:                  Lourl.append(i)
		Ltmp.extend(Lp2p)
		Ltmp.extend(Lm3u8)
		Ltmp.extend(Lrtmp)
		Ltmp.extend(Lourl)
		
	if __settings__.getSetting("p2p_start")=='true':
			Lpurl2.extend(Lp2p)
			Lpurl2.extend(Lm3u8)
			Lpurl2.extend(Lrtmp)
			Lpurl2.extend(Lourl)
	else:
			Lpurl2.extend(Lm3u8)
			Lpurl2.extend(Lp2p)
			Lpurl2.extend(Lrtmp)
			Lpurl2.extend(Lourl)
	
	if Lpurl2==[]:
		pDialog.close()
		showMessage('Пазл ТВ', 'Канал недоступен')
		__settings__.setSetting("cplayed",name)
		try:n_play=int(__settings__.getSetting("n_play"))
		except:n_play=0
		if n_play<3:
			__settings__.setSetting("n_play",str(n_play+1))
			next (__settings__.getSetting("lastnx"))
		else:
			return ""
		
	else:
		playlist = xbmc.PlayList (xbmc.PLAYLIST_VIDEO)
		playlist.clear()
		
		for j in range (0,3): # несколько копий в плейлист
			k=0
			for purl in Lpurl2:
				k+=1
				if __settings__.getSetting("split")=='true':name2=name.replace(" #1","").replace(" #2","").replace(" #3","").replace(" #4","")
				else:name2=name.replace(" #1","[COLOR 40FFFFFF] #1[/COLOR]").replace(" #2","[COLOR 40FFFFFF] #2[/COLOR]").replace(" #3","[COLOR 40FFFFFF] #3[/COLOR]").replace(" #4","[COLOR 40FFFFFF] #4[/COLOR]")
				item = xbmcgui.ListItem(name2+" [ "+str(k)+"/"+str(len(Lpurl2))+" ]", path=purl, thumbnailImage=cover, iconImage=cover)
				playlist.add(url=purl, listitem=item)
		
		pDialog.close()
		
		__settings__.setSetting("cplayed",name)
		
		Player.play(playlist)
		
		xbmc.sleep(6000)
		xbmc.sleep(6000)
		while  xbmc.Player().isPlaying():
				xbmc.sleep(1000)
				#print "========================  playing ======================"
		if __settings__.getSetting("epgon")=='true':
			if ref==True: 
				xbmc.sleep(300)
				xbmc.executebuiltin("Container.Refresh")
				#print "========================  Refresh ======================"

def get_ttv(url):
		http=getURL(url)
		print http
		ss1='this.loadPlayer("'
		ss2='this.loadTorrent("'
		es='",{autoplay: true})'
		srv=__settings__.getSetting("p2p_serv")
		prt=__settings__.getSetting("p2p_port")
		
		try:
			if ss1 in http:
				CID=mfindal(http,ss1,es)[0][len(ss1):]
				lnk='http://'+srv+':'+prt+'/ace/getstream?id='+CID
				if len(CID)<30:lnk=''
				return lnk
			elif ss2 in http:
				AL=mfindal(http,ss2,es)[0][len(ss2):]
				lnk='http://'+srv+':'+prt+'/ace/getstream?url='+AL
				if len(AL)<30:lnk=''
				return lnk
			else: return ""
		except:
			return ""

def pars_m3u8(url):
	if __settings__.getSetting("pm3u")=='true':
		#print 'pars_m3u8'
		k1=url.find(".m3u8")
		tmp=url[:k1]
		k2=tmp.rfind("/")
		u2=url[:k2+1]
		try:http=getURL(url)
		except: return []
		L=http.splitlines()
		L2=[]
		for i in L:
			if '.m3u8' in i: L2.append(u2+i)
		if len(L2)>1:
			L2.reverse()
			return L2
		else: return [url,]
	else:
		return [url,]

def get_stream(url):
	print url
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
		#L.reverse()
		for i in L:
			srim=i[len(ss):]
			if '.m3u8' in srim and __settings__.getSetting("m3u8-1")=='true':
				if __settings__.getSetting("pm3u-1")=='true':
					L3u=pars_m3u8(srim)
					Lp.extend(L3u)
				else:
					Lp.append(srim)
			elif 'rtmp' in srim and __settings__.getSetting("rtmp-1")=='true':
				Lp.append(srim)
			elif 'peers' not in srim:
					Lp.append(srim)
		
		if __settings__.getSetting("p2p-1")=='true':
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
			#if __settings__.getSetting("p2p_start")=='true':
			#	Lp2.extend(Lp)
			#	Lp=Lp2
			#else:
			Lp.extend(Lp2)
		return Lp
	
	elif 'torrentstream.tv' in url:
		
		if __settings__.getSetting("serv3")=='true':
				http=getURL(url)
				ss='<iframe src="'
				es='" style="width:650'
				t=mfindal(http,ss,es)[0][len(ss):]
				trst=get_ttv(t)
				if trst=="":return []
				else:      return [trst,]
		else:
			return []
	
	elif 'televizorhd.ru' in url:
		
		if __settings__.getSetting("serv4")=='true':
			if __settings__.getSetting("SID-4")=='true' or __settings__.getSetting("ALV-4")=='true':
				http=getURL(url)
				if __settings__.getSetting("ALV-4")=='true':
					ss='this.loadTorrent("'
					es='",{autoplay: true});}catch(e)'
					try:t1=mfindal(http,ss,es)[0][len(ss):]
					except:t1=""
				
					if 'content.asplaylist.net' in t1: t=['http://127.0.0.1:6878/ace/getstream?url='+t1,]
					else: t=[]
				else:t=[]
				if __settings__.getSetting("SID-4")=='true':
					ss='http://1ttv.net/iframe.php?'
					es='" rel="nofollow" width="100%" height="570"'
					
					try:
						t2=mfindal(http,ss,es)[0]
						if t2!="" and t2!=None: t.append(t2)
					except:pass
					
				
				return t
		else:
			return []

	elif 'asplaylist.net' in url:
		srv=__settings__.getSetting("p2p_serv")
		prt=__settings__.getSetting("p2p_port")
		return ['http://'+srv+':'+prt+'/ace/getstream?url='+url,]

	elif '1ttv.net' in url:
		try:
				trst=get_ttv(url)
				if trst=="":return []
				else:      return [trst,]
		except:
			return []


	elif 'peers.tv' in url:
		try:
				url1=urllib.unquote_plus(url)+'|User-Agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:35.0) Gecko/20100101 Firefox/35.0'
				url2=urllib.unquote_plus(url.replace('/126/','/16/'))+ '|User-Agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:35.0) Gecko/20100101 Firefox/35.0'
				return [url1, url2]
		except:
			return []
	
	elif 'ok-tv.org' in url:
		try:
			L=[]
			try:
				
				http=getURL(url)
				#print http
				ss='frameborder="0" scrolling="no" src="'
				es='" bgcolor="#000000" allowtransparency="true"'
				pl=mfindal(http,ss,es)[0][len(ss):]
				print pl
				
				http2=getURL(pl)
				#print http2
				ss='file='
				es='"></object>'
				st=mfindal(http2,ss,es)[0][len(ss):]
				print st
				L=[st,]
			except: pass
				
			if True:#__settings__.getSetting("p2p-2")=='true':
				try:
					ss='http://1ttv.net'
					es='" width="660" height="450" bgcolor="#000000"'
					Lt=mfindal(http,ss,es)#[0]
					Lp2=[]
					for t in Lt:
						t=t.replace('site=1906','site=1714')
						trst=get_ttv(t)
						print trst
						Lp2.append(trst)
					L.extend(Lp2)
				except: pass

			return L
				
		except:
			return []
	
	
	elif 'tivix.net' in url:
		Lp=[]
		http=getURL(url)
		#ss='&file='
		#es='&st='
		#L=mfindal(http,ss,es)
#		for i in L:
#			tmp=i[len(ss):]
#			if 'm3u8' in tmp:
#				#print "M3U8"
#				if __settings__.getSetting("m3u8-2")=='true':
#					if __settings__.getSetting("pm3u-2")=='true':
#						L3u=pars_m3u8(tmp)
#						Lp.extend(L3u)
#					else:
#						Lp.append(tmp)
#			else:
				#print "RTMP"
#				if __settings__.getSetting("rtmp-2")=='true':
#					purl = tmp
#					purl += " swfUrl=http://tivix.net/templates/Default/style/uppod.swf"
#					purl += " pageURL=http://tivix.net"
#					purl += " swfVfy=true live=true"
#					if 'peers' not in purl: Lp.append(purl)
		
		if True:#__settings__.getSetting("p2p-2")=='true':
			ss='http://1ttv.net'
			es='\\" width=\\"800\\" height='
			Lt=mfindal(http,ss,es)#[0]
			Lp2=[]
			for t in Lt:
				t=t.replace('site=1510','site=1714')
				trst=get_ttv(t)
				print trst
				Lp2.append(trst)
			Lp.extend(Lp2)

		return Lp
	else:
		return []

def get_cepg(id, serv):
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
		
		cdata = int(time.strftime('%Y%m%d'))
		Ln=[]
		
		for i in L:
			if int(i['start_at'][:11].replace('-',''))==cdata: Ln.append(i)
		
		for n in range (1,len(Ln)):
			i=Ln[n-1]
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
			t3=h3*60+m3
			if (t2>=t1 and t1>=t3) or n2>0: 
				n2+=1
				# ------ Прогресс бар
				if n2==1:
					
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
		
		cdata = int(time.strftime('%Y%m%d'))
		Ln=[]
		
		for i in L:
			if int(i['start_at'][:11].replace('-',''))==cdata: Ln.append(i)
		
		for i in Ln:
			n+=1
			name=i['name']
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
			t3=h3*60+m3
			if t2>=t1 and t1>=t3: 
				#n2+=1
					#print '------ Прогресс бар'
				#if n2==1:
					
					#print t3 #нач
					#print t2 #кон
					#print t1 #вр
					vv=t2-t3
					#print str(t2)+'-'+str(t3)+'='+str(vv)
					if vv>800:vv=1440-vv
					vp=t2-t1
					#print str(t2)+'-'+str(t1)+'='+str(vp)
					if vp>800:vp=1440-vp
					prc=vp*100/vv
					#print prc
					p2=20*prc/100
					p1=20-p2
					
					if h2>23:hh2=str(h2-24)
					elif h2>9:hh2=str(h2)
					else:   hh2="0"+str(h2)
					if m2>9:mm2=str(m2)
					else:   mm2="0"+str(m2)
					etm =hh2+":"+mm2
					#print stm
					#print etm
					iii='----------------------------------'
					#pb1='[B][COLOR FF5555FF]'+iii[:prc]+"[/COLOR]"
					#pb2='[COLOR FFFFFFFF]'+iii[:20-prc]+"[/COLOR][/B]"
					
					pb1='[COLOR FF5555FF]'+iii[:p1]+"[/COLOR]"
					pb2='[COLOR FFFFFFFF]'+iii[:p2]+"[/COLOR]"
					
					itm+= stm+" [B]"+pb1+pb2+"[/B] "+etm+'[COLOR FFFFFFFF][B] '+name+'[/B][/COLOR]'#
					return itm
	except:
		return ""

def tvgide():
	try:SG=__settings__.getSetting("Sel_gr")
	except:SG=''
	
	if SG=='':
		SG='Все каналы'
		__settings__.setSetting("Sel_gr",SG)
	add_item ('[COLOR FF55FF55][B]Группа: '+SG+'[/B][/COLOR]', 'select_gr')
	
	CL=get_gr()
	ttl=len(CL)
	if ttl==0:ttl=250
	Lnm=[]
	
	L=get_all_channeles()
	
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
						add_item (name, 'play', [url,], namec, cover)
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
							add_item (name, 'play', [url,], namec, cover)
							Lnm.append(namec)
	
	xbmcplugin.endOfDirectory(handle)




def set_num_cn(name):
	try:L=open_Groups()
	except:
		L=Ldf
		save_Groups(L)

	try:SG=__settings__.getSetting("Sel_gr")
	except:SG=''
	if SG=='':SG='Все каналы'
	
	if SG!='Все каналы':
		CLc=get_gr()
		n=CLc.index(name)
		sel = xbmcgui.Dialog()
		CLc.append(' - В конец списка - ')
		r = sel.select("Перед каналом:", CLc)
		CL=CLc[:-1]
		if r>=0 :#and r<len(CL)
			CL.remove(name)
			CL.insert(r, name)
			k=0
			for i in L:
				if i[0]==SG:
					L[k]=(SG,CL)
					save_Groups(L)
				k+=1
	xbmc.sleep(300)
	xbmc.executebuiltin("Container.Refresh")


def upd_canals_db0():
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
			
			LL.append({'url':url, 'img':img, 'title':title+" #1"})
			
	if LL!=[]:save_channels(1, LL)
	else:showMessage('viks.tv', 'Не удалось загрузить каналы', times = 3000)
		
	return LL

def upd_canals_db1():
		LL=[]
	#for pg in range(1,5):
		url='http://api.peers.tv/peerstv/2/'
		http=getURL(url)
		
		ss='<track>'
		es='</track>'
		L=mfindal(http,ss,es)
		
		for i in L:
			
			ss='<location>'
			es='</location>'
			url=mfindal(i,ss,es)[0][len(ss):]
		
			ss='<image>'
			es='</image>'
			img=mfindal(i,ss,es)[0][len(ss):]

			ss='<title>'
			es='</title>'
			title=mfindal(i,ss,es)[0][len(ss):]
			
			LL.append({'url':url, 'img':img, 'title':title+" #1"})
			
		if LL!=[]:save_channels(1, LL)
		else:showMessage('peers.tv', 'Не удалось загрузить каналы', times = 3000)
		
		return LL


def upd_canals_db2():
	LL=[]
	for pg in range(1,5):
		url='http://tivix.net/page/'+str(pg)
		http=getURL(url)
		n=http.find("<div id='dle-content'>")
		http=http[n:]
		ss='<div class="all_tv"'
		es='</div>'
		L=mfindal(http,ss,es)
		
		CL=get_gr()
		for i in L:
			try:
				ss='http://tivix.net/'
				es='.html'
				url=mfindal(i,ss,es)[0]+'.html'
		
				ss='uploads/'
				es='.png"'
				img='http://tivix.net/'+mfindal(i,ss,es)[0]+'.png'

				ss='title="'
				es='">'
				title=mfindal(i,ss,es)[0][len(ss):]
			
				LL.append({'url':url, 'img':img, 'title':title+" #2"})
			except:
				pass
			
	if LL!=[]:save_channels(2, LL)
	else:showMessage('tivix.net', 'Не удалось загрузить каналы', times = 3000)
		
	return LL

def upd_canals_db3():  #xml
	import cnl
	import logodb
	Ldb=logodb.ttvlogo
	LL=[]
	Lu=[]
	for i in cnl.ttvcnl:
		LL.append({'url':i['url'], 'img':i['img'], 'title':i['title']+" #3"})
		Lu.append(i['url'])
	pref='http://1ttv.net/iframe.php?site=1714&channel='
	xml=dload_epg_xml()
	n=xml.find('<channel id')
	k=xml.find('<programme ')
	xml=xml[n:k]
	xml=xml.replace(chr(10),"").replace(chr(13),"").replace("<channel id", "\n<channel id")
	L=xml.splitlines()
	#debug (xml)
	#LL=[]
	fdbc=False
	for i in L:
		if 'id="ttv' in i:
			try:
				ss='id="ttv'
				es='"><display-name lang="ru">'
				id=mfindal(i,ss,es)[0][len(ss):]
				url=pref+id
				if url not in Lu:
					Lu.append(url)
					#print url
					ss='<display-name lang="ru">'
					es='</display-name>'
					title=mfindal(i,ss,es)[0][len(ss):]
					#print title
					
					try:
						img=Ldb[id]
					except:
						print "################ Логотип отсутствует в БД #################"
						print url
						tmp=getURL(url)
						ss='http://torrent-tv.ru/uploads/'
						es='.png" style="vertical-align'
						img=mfindal(tmp,ss,es)[0]+'.png'
						print '"'+id+'":"'+img+'"'
						Ldb[id]=img
						fdbc=True
						print "################ Логотип сохранен в БД #################"
					
					LL.append({'url':url, 'img':img, 'title':title+" #3"})
			except:
					pass
					print "!_!_!_!_!_!_!_!_ Ошибка получения канала TTB !_!_!_!_!_!_!_!_"
					print i
					print "!_!_!_!_!_!_!_!_!_!_!_!_!_!_!_!_!_!_!_!_!_!_!_!_!_!_!_!_!_!_!_"
	if fdbc:
		fp=xbmc.translatePath(os.path.join(addon.getAddonInfo('path'), 'logodb.py'))
		fl = open(fp, "w")
		fl.write('# -*- coding: utf-8 -*-\n')
		fl.write('ttvlogo={\n')
		for i in Ldb.items():
			fl.write('"'+i[0]+'":"'+i[1]+'",\n')
		fl.write('}')
		fl.close()

	if LL!=[]: save_channels(3, LL)
	else: showMessage('torrent-tv.ru', 'Не удалось загрузить каналы', times = 3000)

	return LL

def upd_canals_db41(): #http://televizorhd.ru
	import logodb
	Ldb=logodb.ttvlogo
	LL=[]
	url='http://televizorhd.ru'
	#pref='http://1ttv.net/iframe.php?site=1714&channel='
	http=getURL(url)
		
	ss='<li>'
	es='</li>'
	L=mfindal(http,ss,es)
	fdbc=False
	no_err=True
	for i in L:
		try:
			ss='<a href="'
			es='"><div class="openPart">'
			url=mfindal(i,ss,es)[0][len(ss):]
			#print url
			
			ss='<div class="openPart">'
			es='</div></a>'
			title=mfindal(i,ss,es)[0][len(ss):]
			try:
				title=title.decode('windows-1251')
				title=title.encode('utf-8')
			except: pass
				
			id = get_idx(title)
			if id=="":
				try:
					#print "-=======================================================-"
					#print "-------------------- нет ID канала в БД -----------------------"
					#print lower(title)
					#print "-------------------- поиск ID на сайте  -----------------------"
					#print url
					h=getURL(url)
					ss='http://1ttv.net/iframe.php?site=1714&channel='
					es='" rel="nofollow" width="100%" height="570"'
					id=mfindal(h,ss,es)[0][len(ss):]
					#print '"'+lower(title)+'":"ttv'+id+'"'
				except:
					#print "-------------------- ID на сайте не найден -----------------------"
					id=""
			if id!="":
				try:
					#print "-------------------- Поиск логотипа в БД по ID -------------------"
					img=Ldb[id]
					#print img
				except:
					#try:
					#	#print "------------ Логотип отсутствует в БД > Грузим с 1ttv ------------"
					#	u2='http://1ttv.net/iframe.php?site=2252&channel='+id
					#	tmp=getURL(u2)
					#	ss='http://torrent-tv.ru/uploads/'
					#	es='.png" style="vertical-align'
					#	img=mfindal(tmp,ss,es)[0]+'.png'
					#	#print '"'+id+'":"'+img+'"'
					#	Ldb[id]=img
					#	fdbc=True
					#	#print "-------------------- Логотип сохранен в БД -------------------------"
					#except:
						#print "---------------------- Ошибка поиска на 1ttv > ищем локально -----------------------"
						path = fs_enc(os.path.join(Logo, id.replace("xttv","")+'.png'))
						try: sz=os.path.getsize(path)
						except: sz=0
						if sz >0:
							img=path
						else:
							#try:
							#	h=getURL(url)
							#	ss='http://televizorhd.ru/uploads/posts'
							#	es='_1.png'
							#	img=mfindal(h,ss,es)[0]+es
							#except:
								#print "------------------! Логотип незвестен !-------------------------"
								#print url
								#print id
								#print lower(title)
								img="http://televizorhd.ru/templates/Server-Torrent-TV/dleimages/no_image.jpg"
				
			else:
				#print " --------------- ОШИБКА ЗАГРУЗКИ КАНАЛА ----------------- "
				#print i
				no_err=False
			if no_err: LL.append({'url':url, 'img':img, 'title':title+' #4'})
		except: 
			#print " --------------- ОШИБКА  ----------------- "
			#print i
			pass
			
	if fdbc:
		fp=xbmc.translatePath(os.path.join(addon.getAddonInfo('path'), 'logodb.py'))
		fl = open(fp, "w")
		fl.write('# -*- coding: utf-8 -*-\n')
		fl.write('ttvlogo={\n')
		for i in Ldb.items():
			fl.write('"'+i[0]+'":"'+i[1]+'",\n')
		fl.write('}')
		fl.close()

	if LL!=[]:save_channels(4, LL)
	else: showMessage('televizorhd.ru', 'Не удалось загрузить каналы', 3000)
	return LL

def upd_canals_db4():
	import logodb
	Ldb=logodb.ttvlogo
	LL=[]
	url='http://www.trambroid.com/playlist.xspf'
	http=getURL(url)
	http=http.replace(chr(10),"").replace(chr(13),"").replace("<track>", "\n<track>")
	#debug (http)
	L=http.splitlines()
	Lu=[]
	fdbc=False
	for i in L:
		no_err=True
		try:
		#if '<location>' in i:
			#print "=================================================================="
			ss='<location>'
			es='</location>'
			url=mfindal(i,ss,es)[0][len(ss):]
			
			#print url
				
			ss='<title>'
			es='</title>'
			title=mfindal(i,ss,es)[0][len(ss):]
			#print title
			
			id = get_idx(title).replace("xttv","")
			if id=="":
					#print "-------------------- Нет ID -------------------"
					print lower(title)

			if id!="" and url not in Lu:
				#print id
				
				try:
					#print "-------------------- Поиск логотипа в БД по ID -------------------"
					img=Ldb[id]
					#print img
				except:
					#try:
						#print "------------ Логотип отсутствует в БД > Грузим с 1ttv ------------"
						#u2='http://1ttv.net/iframe.php?site=1714&channel='+id
						#tmp=getURL(u2)
						#ss='http://torrent-tv.ru/uploads/'
						#es='.png" style="vertical-align'
						#img=mfindal(tmp,ss,es)[0]+'.png'
						#print '"'+id+'":"'+img+'"'
						#Ldb[id]=img
						#fdbc=True
						#print "-------------------- Логотип сохранен в БД -------------------------"
					#except:
						#print "---------------------- Ошибка поиска на 1ttv > ищем локально -----------------------"
						path = fs_enc(os.path.join(Logo, id+'.png'))
						try: sz=os.path.getsize(path)
						except: sz=0
						if sz >0:
							img=path
						else:
								#print "------------------! Логотип незвестен !-------------------------"
								#print url
								#print id
								#print lower(title)
								img="http://televizorhd.ru/templates/Server-Torrent-TV/dleimages/no_image.jpg"
								no_err=False
				
			else:
				#print " --------------- ОШИБКА ЗАГРУЗКИ КАНАЛА ----------------- "
				#print i
				no_err=False
				img="http://televizorhd.ru/templates/Server-Torrent-TV/dleimages/no_image.jpg"
				
			if no_err: 
				LL.append({'url':url, 'img':img, 'title':title+' #4'})
				Lu.append(url)
			
		except: 
		#else:
			print " --------------- ОШИБКА  ----------------- "
			print i
			pass
			
	if fdbc:
		fp=xbmc.translatePath(os.path.join(addon.getAddonInfo('path'), 'logodb.py'))
		fl = open(fp, "w")
		fl.write('# -*- coding: utf-8 -*-\n')
		fl.write('ttvlogo={\n')
		for i in Ldb.items():
			fl.write('"'+i[0]+'":"'+i[1]+'",\n')
		fl.write('}')
		fl.close()

	if LL!=[]:save_channels(4, LL)
	else: showMessage('televizorhd.ru', 'Не удалось загрузить каналы', 3000)

	return LL


def upd_canals_db2():
		LL=[]
	#for pg in range(1,5):
		url='http://ok-tv.org'
		http=getURL(url)
		
		ss='<a target="_blank"'
		es='style="width:100px;"'
		L=mfindal(http,ss,es)
		
		for i in L:
			ss='href="'
			es='.html'
			url='http://ok-tv.org'+mfindal(i,ss,es)[0][len(ss):]+es
		
			ss='src="'
			es='" alt="'
			img='http://ok-tv.org'+mfindal(i,ss,es)[0][len(ss):]

			ss='title="'
			es='" href'
			title=mfindal(i,ss,es)[0][len(ss):]
			#try: tiitle=title.decode('windows-1251')
			#except:pass
			try: tiitle=title.encode('utf-8')
			except:pass
			#print title
			title=title.replace('смотреть','').replace('смотреть','').replace('Cмотреть','').replace('онлайн','').replace('прямой эфир','').replace('прямо эфир','').replace('прямую трансляцию','').replace('бесплатно','').strip()
			#tiitle=title.replace(u'смотреть','').replace(u'Cмотреть','').replace(u'онлайн','').replace(u'прямой эфир','').replace(u'бесплатно','').strip()
			
			LL.append({'url':url, 'img':img, 'title':title+" #2"})
			
		if LL!=[]:save_channels(2, LL)
		else:showMessage('ok-tv.org', 'Не удалось загрузить каналы', times = 3000)
		
		return LL



def televizorhd(url):
	#url='http://www.trambroid.com/playlist.xspf'
	L1=['a','e','l','d','y','f','r','c','w','x','.','/','h']
	n=55
	for i in L1:
		n+=3
		j=chr(n)
		url=url.replace(i,j)
	return url

#print televizorhd("http://www.trambroid.com/playlist.xspf")

def save_channels(n, L):
		ns=str(n)
		fp=xbmc.translatePath(os.path.join(addon.getAddonInfo('path'), 'Channels'+ns+'.py'))
		fl = open(fp, "w")
		fl.write('# -*- coding: utf-8 -*-\n')
		fl.write('Channels=[\n')
		for i in L:
			fl.write(repr(i)+',\n')
		fl.write(']\n')
		fl.close()




def select_gr():
	try:L=open_Groups()
	except:
		L=Ldf
		save_Groups(L)
	
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
	try:L=open_Groups()
	except:
		L=Ldf
		save_Groups(L)
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
	try:L=open_Groups()
	except:L=[]
	CL=[]
	for i in L:
		if i[0]==SG: CL=i[1]
	return CL

def add(id):
	try:L=open_Groups()#L=open_Groups()
	except:L=Ldf
	Lg=[]
	for i in L:
		Lg.append(i[0])
		
	if Lg!=[]:
		sel = xbmcgui.Dialog()
		r = sel.select("Группа:", Lg)
		if id not in L[r][1]:
			L[r][1].append(id)
		
	save_Groups(L)

def open_Groups():
		fp=xbmc.translatePath(os.path.join(UserDir, 'UserGR.py'))
		
		try:sz=os.path.getsize(fp)
		except:sz=0
		if sz==0:
			save_Groups(Ldf)
			return Ldf
		
		fl = open(fp, "r")
		ls=fl.read().replace('\n','')#.replace('# -*- coding: utf-8 -*-Lgr=','')
		fl.close()
		return eval(ls)

def save_Groups(L):
		fp=xbmc.translatePath(os.path.join(UserDir, 'UserGR.py'))
		fl = open(fp, "w")
		#fl.write('# -*- coding: utf-8 -*-\n')
		#fl.write('Lgr=[\n')
		fl.write('[\n')
		for i in L:
			fl.write(repr(i)+',\n')
		fl.write(']\n')
		fl.close()


def rem(id):
	try:L=open_Groups()
	except:L=Ldf
	L2=[]
	for i in L:
			lj=[]
			for j in i[1]:
				if __settings__.getSetting("split")=='true': nm=id[:-1]
				else: nm=id
				if nm not in j:
				#if j!=id: 
					lj.append(j)
			L2.append([i[0],lj])
	save_Groups(L2)#__settings__.setSetting("Groups",repr(L2))
	xbmc.executebuiltin("Container.Refresh")

def add_gr():
	name=inputbox('')
	try:L=open_Groups()
	except:L=Ldf
	st=(name,[])
	if st not in L:L.append(st)
	save_Groups(L)

def rem_gr():
	try:L=open_Groups()
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
		save_Groups(L2)#__settings__.setSetting("Groups",repr(L2))


def get_all_channeles():
	pDialog = xbmcgui.DialogProgressBG()
	
	if __settings__.getSetting("serv1")=='true' :
		try:
			import Channels1
			L1=Channels1.Channels
		except:L1=[]
		if L1==[]: 
			pDialog.create('Пазл ТВ', 'Обновление списка каналов #1 ...')
			L1=upd_canals_db1()
			pDialog.close()
	else: L1=[]
	
	if __settings__.getSetting("serv2")=='true':
		try:
			import Channels2
			L2=Channels2.Channels
		except:L2=[]
		if L2==[]: 
			pDialog.create('Пазл ТВ', 'Обновление списка каналов #2 ...')
			L2=upd_canals_db2()
			pDialog.close()
	else: L2=[]
	
	if __settings__.getSetting("serv3")=='true':
		try:
			import Channels3
			L3=Channels3.Channels
		except:L3=[]
		if L3==[]: 
			pDialog.create('Пазл ТВ', 'Обновление списка каналов #3 ...')
			L3=upd_canals_db3()
			pDialog.close()
	else: L3=[]

	if __settings__.getSetting("serv4")=='true':
		try:
			import Channels4
			L4=Channels4.Channels
		except:L4=[]
		if L4==[]: 
			pDialog.create('Пазл ТВ', 'Обновление списка каналов #4 ...')
			L4=upd_canals_db4()
			pDialog.close()
	else: L4=[]
	
	try: pDialog.close()
	except: pass
	L1.extend(L2)
	L1.extend(L3)
	L1.extend(L4)
	
	return L1


def add_item (name, mode="", path = Pdir, ind="0", cover=None, funart=None):
	if __settings__.getSetting("fanart")=='true':funart=cover
	else: funart=fanart
		
	if __settings__.getSetting("icons")!='true':cover=icon

	listitem = xbmcgui.ListItem(name, iconImage=cover)
	listitem.setProperty('fanart_image', funart)
	uri = sys.argv[0] + '?mode='+mode
	uri += '&url='  + urllib.quote_plus(repr(path))
	uri += '&name='  + urllib.quote_plus(xt(ind))
	uri += '&ind='  + urllib.quote_plus(str(ind))
	if cover!=None:uri += '&cover='  + urllib.quote_plus(cover)
	if funart!=None and funart!="":uri += '&funart='  + urllib.quote_plus(funart)
	
	if mode=="play":
		if __settings__.getSetting("epgon")=='true':
				id = get_idx(ind)
				#if id=='': print ind
				dict={"plot":get_cepg(id,'xmltv').replace('&quot;','"').replace('&apos;',"'")}
		else: dict={}
		try:listitem.setInfo(type = "Video", infoLabels = dict)
		except: pass

		fld=False
		ContextGr=[('[B]Все каналы[/B]', 'Container.Update("plugin://plugin.video.pazl.tv/?mode=context_gr&name=Все каналы")'),]
		for grn in list_gr():
			ContextGr.append(('[B]'+grn+'[/B]','Container.Update("plugin://plugin.video.pazl.tv/?mode=context_gr&name='+urllib.quote_plus(grn)+'")'))
		ContextGr.append(('[COLOR FF55FF55][B]ПЕРЕДАЧИ[/B][/COLOR]', 'Container.Update("plugin://plugin.video.pazl.tv/?mode=tvgide")'))

		ContextCmd=[
			('[COLOR FF55FF55][B]ГРУППА[/B][/COLOR]', 'Container.Update("plugin://plugin.video.pazl.tv/?mode=select_gr")'),
			('[COLOR FF55FF55][B]+ Добавить в группу[/B][/COLOR]', 'Container.Update("plugin://plugin.video.pazl.tv/?mode=add&name='+urllib.quote_plus(ind)+'")'),
			('[COLOR FFFF5555][B]- Удалить из группы[/B][/COLOR]', 'Container.Update("plugin://plugin.video.pazl.tv/?mode=rem&name='+urllib.quote_plus(ind)+'")'),
			('[COLOR FF55FF55][B]<> Переместить канал[/B][/COLOR]', 'Container.Update("plugin://plugin.video.pazl.tv/?mode=set_num&name='+urllib.quote_plus(ind)+'")'),
		('[COLOR FFFFFF55][B]* Обновить каналы[/B][/COLOR]', 'Container.Update("plugin://plugin.video.pazl.tv/?mode=update")'),
			('[COLOR FFFFFF55][B]* Обновить программу[/B][/COLOR]', 'Container.Update("plugin://plugin.video.pazl.tv/?mode=updateepg")'),
			('[COLOR FF55FF55][B]ПЕРЕДАЧИ[/B][/COLOR]', 'Container.Update("plugin://plugin.video.pazl.tv/?mode=tvgide")')]
			
		if __settings__.getSetting("grincm")=='true':listitem.addContextMenuItems(ContextGr, replaceItems=True)
		else:										listitem.addContextMenuItems(ContextCmd, replaceItems=True)
	else: 
		fld=True
		listitem.addContextMenuItems([
			('[COLOR FF55FF55][B]+ Создать группу[/B][/COLOR]', 'Container.Update("plugin://plugin.video.pazl.tv/?mode=addgr")'),
			('[COLOR FFFF5555][B]- Удалить группу[/B][/COLOR]', 'Container.Update("plugin://plugin.video.pazl.tv/?mode=remgr")'),
			('[COLOR FFFFFF55][B]* Обновить каналы[/B][/COLOR]', 'Container.Update("plugin://plugin.video.pazl.tv/?mode=update")'),
			('[COLOR FFFFFF55][B]* Обновить программу[/B][/COLOR]', 'Container.Update("plugin://plugin.video.pazl.tv/?mode=updateepg")'),
			('[COLOR FFFFFF55][B]Управление каналами[/B][/COLOR]', 'Container.Update("plugin://plugin.video.pazl.tv/?mode=grman")'),])
	xbmcplugin.addDirectoryItem(handle, uri, listitem, fld)#, ind)


def root():
	try:	SG=__settings__.getSetting("Sel_gr")
	except: SG=''
		
	if SG=='':
		SG='Все каналы'
		__settings__.setSetting("Sel_gr",SG)
	add_item ('[COLOR FF55FF55][B]Группа: '+SG+'[/B][/COLOR]', 'select_gr', cover=icon)
	
	CL=get_gr()
	ttl=len(CL)
	if ttl==0:ttl=250
	Lnm=[]
	nserv=0
	for k in ['1','2','3','4']:
		if __settings__.getSetting("serv"+k)=='true': nserv+=1
	
	L=get_all_channeles()
	
	intlogo =__settings__.getSetting("intlogo")
	grinnm  =__settings__.getSetting("grinnm")
	splitcn   =__settings__.getSetting("split")
	
	ct= time.time()
	if SG=='Все каналы':
		for i in L:
				name  = i['title']
				url   = i['url']
				cover = i['img']
				id=get_idx(name)
				if id=="": print lower(name).replace(" #1","").replace(" #2","").replace(" #3","").replace(" #4","")
				if intlogo == 'true': cover = GETimg(cover, id.replace("xttv",""))
				if grinnm =='true': name2=add_grn(name)
				else: name2=name
				
				if __settings__.getSetting("split")=='true' or nserv==1: name2=name2.replace(" #1","").replace(" #2","").replace(" #3","").replace(" #4","")
				else: name2=name2.replace(" #1","[COLOR 40FFFFFF] #1[/COLOR]").replace(" #2","[COLOR 40FFFFFF] #2[/COLOR]").replace(" #3","[COLOR 40FFFFFF] #3[/COLOR]").replace(" #4","[COLOR 40FFFFFF] #4[/COLOR]")
				
				if id not in Lnm:
					add_item ("[B]"+name2+"[/B]", 'play', [url,], name, cover)
					if id!="" and splitcn =='true': Lnm.append(id)
		if __settings__.getSetting("abc")=='true':  xbmcplugin.addSortMethod(handle, xbmcplugin.SORT_METHOD_LABEL)

	else: # Группы
		for k in CL:
				for i in L:
					name = i['title']
					name2 = i['title']
					id=get_idx(name)
					if k==name and id not in Lnm:
						cover = i['img']
						if intlogo == 'true':  cover = GETimg(cover, id.replace("xttv",""))
						#if id=='': print name+' : '+i['url']
						if splitcn =='true':	urls=get_allurls(id, L)
						else: 					urls = [i['url'],]
						
						if splitcn =='true' or nserv==1: name=name.replace(" #1","").replace(" #2","").replace(" #3","").replace(" #4","")
						else: name=name.replace(" #1","[COLOR 40FFFFFF] #1[/COLOR]").replace(" #2","[COLOR 40FFFFFF] #2[/COLOR]").replace(" #3","[COLOR 40FFFFFF] #3[/COLOR]").replace(" #4","[COLOR 40FFFFFF] #4[/COLOR]")
						
						add_item ("[B]"+name+"[/B]", 'play', urls, name2, cover)
						if id!="" and splitcn =='true':Lnm.append(id)
	
	if intlogo =='true': ctd=False
	else:                ctd=True
	#print "------ time"
	#print time.time()-ct
	xbmcplugin.endOfDirectory(handle, cacheToDisc=ctd)

def get_allurls(xid, L):
	id=xid[1:]
	L2=[]
	for i in xmlid.items():
		if i[1]==id:
			L2.append(i[0])
	L3=[]
	for j in L:
		name = lower(j['title']).replace(" #1","").replace(" #2","").replace(" #3","").replace(" #4","")
		if name in L2:
			L3.append(j['url'])
	return L3

def add_grn(name):
	try:L=open_Groups()
	except:L=[]
	for i in L:
		gr=i[0]
		if name in i[1]: name=name+"  [COLOR 40FFFFFF]["+gr+"][/COLOR]"
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
	name=lower(name).replace(" #1","").replace(" #2","").replace(" #3","").replace(" #4","")
	try:
		id="x"+xmlid[name]
	except: 
		id=''
	return id

# ------------------------------------ БД ------------------------------------------------
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
# ----------------------------------- данные ----------------------------------------------------
def dload_epg_xml():
	try:
			target='http://api.torrent-tv.ru/ttv.xmltv.xml.gz'
			#print "-==-=-=-=-=-=-=- download =-=-=-=-=-=-=-=-=-=-"
			fp = xbmc.translatePath(os.path.join(addon.getAddonInfo('path'), 'tmp.zip'))
			
			req = urllib2.Request(url = target, data = None)
			req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)')
			resp = urllib2.urlopen(req)
			fl = open(fp, "wb")
			fl.write(resp.read())
			fl.close()
			#print "-==-=-=-=-=-=-=- unpak =-=-=-=-=-=-=-=-=-=-"
			xml=ungz(fp)
			#print "-==-=-=-=-=-=-=- unpak ok =-=-=-=-=-=-=-=-=-=-"
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

def unzip(filename):
	from zipfile import ZipFile
	fil = ZipFile(filename, 'r')
	for name in fil.namelist():
		f=fil.read(name)
		return f

# ------------------------------------- выкл -------------------------------------------


def get_epg_off(id, serv, name=''):
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
			pass
			#print 'неудалось загрузить программу: '+id


def upd_EPG_off():
	try:
		import Channels1
		L1=Channels1.Channels
	except:L1=[]
	
	try:
		import Channels2
		L2=Channels2.Channels
	except:L2=[]
	
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

def upd_EPG_xmltv_off():
	xml=dload_epg_xml()
	if xml=="": xml=dload_epg_xml()
	if xml!="":
		d=pars_xmltv(xml)
		j=0
		for id in d.keys():
			j+=1
			#print d[id]
			add_to_db("x"+id, repr(d[id]))
			pDialog.update(j/4, message='xmltv ...')
	else:
		pDialog.update(0, message='Не удалось загрузить xml.')

def upd_EPG_itv_off():
	d=intertv()
	j=1
	for id in d.keys():
		j+=1
		#print d[id]
		add_to_db(id, repr(d[id]))
		pDialog.update(j/4, message='itv ...')



def pars_xmltv_off(xml):
	#print "-==-=-=-=-=-=-=- parsing =-=-=-=-=-=-=-=-=-=-"
	#debug (xml)
	xml=xml.replace(chr(10),"").replace(chr(13),"").replace("<programme ", "\n<programme ")
	ss="<programme "
	es="</programme>"
	L=xml.splitlines()
	#L=mfindal(xml,ss,es)
	epg={}
	for i in L:
		if "<programme " in i:
			#print "-==-=-=-=-=-=-=- parsing i =-=-=-=-=-=-=-=-=-=-"
			#debug i
			ss='start="'
			es=' +0300" stop="'
			st=mfindal(i,ss,es)[0][len(ss):]
			
			ss='stop="'
			es=' +0300" channel'
			et=mfindal(i,ss,es)[0][len(ss):]
			
			ss=' channel="'
			es='">'
			id=mfindal(i,ss,es)[0][len(ss):]
			
			ss='<title'
			es='</title>'
			title=mfindal(i,ss,es)[0][len(ss):].replace(' lang="ru">',"")
			
			try:Le=epg[id]
			except: Le=[]
		
			n=len(Le)
			start_at=xt(st[0:4]+"-"+st[4:6]+"-"+st[6:8]+" "+st[8:10]+":"+st[10:12]+":00")
		
			#print start_at+" "+title
			try:
				Le.append({"name":title, "start_at":start_at})
				epg[id]=Le
				#print id
			except: 
				pass
			#print id+"  :  "+start_at+"  :  "+title
	return epg

def dload_epg_inter_off():
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


#Lv=['понед', 'вторн', 'среда', 'четве', 'пятни', 'суббо', 'воскре', 'ПОНЕД', 'ВТОРН', 'СРЕДА', 'ЧЕТВЕ', 'ПЯТНИ', 'СУББО', 'ВОСКР']

def intertv_off():
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

def upd_stv_off():
	opener = urllib2.build_opener()
	opener.addheaders.append(('Cookie', 'favorites=1TV%3BRTR%3BNTV%3BMIR%3BTVC%3BKUL%3BMatchTV%3BTNT%3BDOMASHNIY%3BRenTV%3BSTS%3BPiter5_RUS%3BZVEZDA%3BChe%3BKarusel%3B2X2%3BDisney%3BU%3BTV3%3BOTR%3BFriday%3BVesti%3BTNT_4%3BEhoFilm%3B360d%3B360dHD%3BVKT%3BMOSCOW-24%3BDOVERIE%3BPingLolo%3BFAMILY%3Bntv%2B41%3BAMEDIA%3BAmediaHit%3BAmedia1%3BBollywood%3BDrama%3BFOX%20CRIME%3BFOX%20LIFE%3BHDKino%3BPARAMAUNT%3BParamounHD%3BParaComedy%3BSET_RUSSIA%3BAXNSciFi%3BSonyTurbo%3BTV1000%3BTV1000_Act%3BTV1000_RK%3BTV21%3BZee-TV%3BDomKino%3BDomKinoP%3BEuroKINO%3BILLUSION%2B%3BIndia%3Bntv%2B34%3BKinoTV%3Bntv%2B4%3BKinipokaz%3BKinop_HD-1%3BKinop_HD-2%3BKinoPrHD%3Bntv%2B40%3BKomedia1%3BKomedia%3BMir_serial%3BmnogoTV%3BMenKino%3BNSTV%3Bntv%2B3%3Bntv%2B7%3BNacheHD%3BOstroHD%3Bntv%2B10%3BRTVi-LK%3BRTVi-NK%3BRus-Bestst%3BRuDetektiv%3BRU_ILLusio%3BRusRoman%3BSemeynoeHD%3BStrahnoeHD%3BSTSLove%3Bntv%2B39%3BFeniks%3BMatchTV%3BABMotors%3Bntv%2B13%3BEuro-2%3BEurospNews%3Bntv%2B23%3BVia_Sport%3BBoxingTV%3Bntv%2B9%3BKHL_HD%3BMatcharena%3Bboets%3BMatchigra%3BMatchsport%3Bntv%2B11%3Bntv%2B44%3BSporthit%3BNautical%3Bntv%2B1%3BRU_Extrem%3BFootBallTV%3BArirang%3Bntv%2B25%3BBBC_Entert%3BBBC-World%3Bntv%2B33%3BCCTVNews%3BCNBC%3Bntv%2B30%3BCNN_ENG%3BDW%3BDW_DEU%3Bntv%2B19%3BFrance24%3BFrance_FR%3BJSTV%3BNewsOne%3BNHK_World%3BRus_Today%3BRT_Doc%3BRTEspanol%3BRTDrus%3BRAIN%3BKommers_TV%3BLDPR%3BMir24%3BRBK%3B4P.INFO%3B24_DOC%3B365_day%3Bntv%2B17%3BDa%20Vinci%3Bntv%2B16%3Bntv%2B28%3BDiscov_VE%3BGalaxy_TV%3BHistor%20%3BHistoryENG%3Bntv%2B18%3BOCEAN-TV%3BENCYCLO%3BExplorer%3BHistory%3BNature_CEE%3BZooTV%3BZoopark%3BViM%3BVopr-Otvet%3BEGE%3BGivPlaneta%3BJivPriroda%3BIstoria%3BWho_is_who%3BMy_Planet%3BNANO_TV%3BNauka_2.0%3B1Obrazovat%3BProsvejeni%3BTop_secret%3BSTRANA%3BTNV_PL%3B1HD%3BA-OnHipHop%3BBizTV%3BBridge-TV%3BC_Music_TV%3BDangeTV%3BEuropaPlus%3BHardLifeTV%3BiConcerts%3BJuCeTV%3BMCMPOP%3BMCMTOP%3Bntv%2B26%3BMTV_Dance%3BMTVDI%3BMTV_Europ%3BMTV_Hits%3BMTVHI%3BMTV_Music%3BMTV_ROCKS%3BMTVRI%3BMTVRus%3BMTV_AM%3BMusicBox-R%3BMusicBox-T%3BRAP%3BRU-TV%3BRusong_TV%3BTOPSONG_T%3BTRACE_URBA%3BTVMChannel%3BVH1_Class%3BVH1_EURO%3BW_Music_Ch%3BLa-minor%3BMUZ_TVnew%3BMuZ-One%3BO2TV%3BA-ONE%3BSHANSON%3BAmazing%3BAngelTV%3BReality%3BCCTV%3BDTXEMEA%3BEnglishClu%3BFash_One%3BFashion_TV%3BFLN%3BFoodNet%3BFuel_TV_HD%3BGame_Show%3BGlobalStar%3BInsiUlHD%3BLuxe_TV%3BMAN_TV%3BMotors_TV%3BMuseum_HD%3BmyZen.tv%3Bntv%2B20%3BOutdoor%3Bprodengi%3BRTGInt%3BRTG_TV%3BStyle%26moda%3BTTS%3BShoppingLi%3BBulvar%3BStyle_TV%3BTDK%3BTLC%3BTop%20Shop%20T%3BTrChenel%3BTravel%2BAdv%3BTVclub%3BTV_Mail%3BTV_SALE%3Bntv%2B32%3BVintage_%3BWBC%3BW_Fashion%3Bautoplus%3BAGRO-TV%3BBalansTV%3BBober%3BVremya%3BD_Jivotnie%3BDrive_MTU%3BEDA%3BJiVi%3BZagorod_zh%3Bzagorodny%3BZdorov_MTU%3BKuhna%3BMirUvlech%3BMuzhskoj%3BNedvigim%3BNostalgi%3BWeapons%3BHa%26Fi_MTU%3BOhot%26Ribal%3BPark_Razvl%3B1InternetK%3BPsihology%3BRaz-TV%3BRetro_MTU%3Bsarafan-tv%3BSojuz%3BSPAS%3BTeatr%3BTeledom%3BTelekafe%3BTeletravel%3BTehno24%3BTONUS-TV%3B3Angela%3BTurInfo%3BUsadba_MTU%3BUspeh%3BEgoist-TV%3BHUMOUR-TV%3BAni%3BBaby_TV%3BBoomerang%3Bntv%2B29%3BGingerHD%3BGulli%3BJIMJAM%3BNick_Jr%3Bntv%2B15%3BNickelodHD%3BTiJi%3BDetskiy%3Bntv%2B8%3BMother%26Chi%3BMult%3BMultimania%3BRadost_moj%3BUlibkaRebe%3BAmediaPRHD%3BAnFamilHD%3BAnimalPlHD%3BArteHD%3BEurekaHD%3BEuroSporHD%3BFashiOneHD%3BFashion_HD%3BFOXLIFE_HD%3BHD-Life%3BHD_Media%3BHD_Media3D%3BLuxe_TV_HD%3BMezzoLive%3BMGM_HD%3BMTV_LiveHD%3BNatGeoW_HD%3BNat_Geo_HD%3BOutdoor%20HD%3BRTDrushd%3BSET_HD%3BTeleTravHD%3BTrace_SpHD%3BTr_Chan_HD%3BTravAdHD%3BTV1000Come%3BTV1000Mega%3BTV1000Prem%3BRAIN_HD%3BEDA_HD%3BMatchareHD%3BMirHD%3BOhotRybHD%3B1TVHD%3BIQHD%3BRTRHD%3BBlueHust%3BBrazzEuro%3BCandy3D%3BCandy%3BDaring!TV%3BFrench_Lov%3BHustle3DHD%3BHustler%3BPlayboy_TV%3BXXL%3BIskushenie%3BNightClub%3BRusnight%3B8_KANAL%3BHistor2%3BBelarus-TV%3BDomMagazin%3BInva_Media%3BKaleidosco%3BKVNTV%3BMatchKmir%3BKrasLin%3BLiderTV%3BNadegda%3BNasheTV%3B1_Meteo%3BProdvigeni%3BRGD%3BRigiy%3BTBN%3BTvoy%3BTNV%3BToshkaTV%3BTRO%3BUvelir'))
	urllib2.install_opener(opener)
	url = 'http://new.s-tv.ru/tv/'
	http = getURL(url)
	ss='<td class="channel">'
	es='<table class="item_table">'
	L=mfindal(http,ss,es)
	epg={}
	n=0
	t=len(L)
	for i in L:
		n+=1
		#try:
		if i!="":
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



def upepg_off():
			pDialog.create('Пазл ТВ', 'Обновление EPG ...')
			#if __settings__.getSetting('epgitv')=='true': upd_EPG_itv()
			if __settings__.getSetting('stv')=='true': upd_stv()
			if __settings__.getSetting('epgxml')=='true': upd_EPG_xmltv()
			if __settings__.getSetting('epgtvx')=='true': upd_EPG()
			#xbmc.executebuiltin("Container.Refresh")
			pDialog.close()
# ========================================================================================

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
try:url = eval(urllib.unquote_plus(params["url"]))
except:url =[]
try:cover = urllib.unquote_plus(params["cover"])
except:cover =""
try:ind = urllib.unquote_plus(params["ind"])
except:ind ="0"
pDialog = xbmcgui.DialogProgressBG()

if mode==""         : #root
	root()
	if __settings__.getSetting("epgon")=='true':
		cdata = int(time.strftime('%Y%m%d'))
		try:
			udata =int(get_inf_db('udata'))
			#udata = int(__settings__.getSetting('udata'))
		except: udata = 0
		#print "-=-=-=-=-=-=- udata ------ - - - - - "
		#print udata
		#if cdata>udata and __settings__.getSetting("epgon")=='true':
		#	add_to_db ("udata", str(cdata))
			#__settings__.setSetting("udata",str(cdata))
			#upepg()
			

if mode=="context_gr"  :
		__settings__.setSetting("Sel_gr",name)
		xbmc.sleep(300)
		xbmc.executebuiltin("Container.Refresh")

if mode=="updateepg"   :
			cdata = int(time.strftime('%Y%m%d'))
			try:
				udata =int(get_inf_db('udata'))
				#udata = int(__settings__.getSetting('udata'))
			except: udata = 0
			add_to_db ("udata", str(0))
			#__settings__.setSetting("udata",str(cdata))
			
			xbmcplugin.endOfDirectory(handle, False, False)
			#xbmc.executebuiltin('Container.Update("plugin://plugin.video.viks.tv/?mode=updateepg2")')
			#import server
			#server.upepg()
			#upepg()
			#xbmc.executebuiltin("Container.Refresh")

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
			xbmcplugin.endOfDirectory(handle, False, False)
			pDialog = xbmcgui.DialogProgressBG()
			pDialog.create('Пазл ТВ', 'Обновление списка каналов 1 ...')
			if __settings__.getSetting("serv1")=='true' :upd_canals_db1()
			pDialog.update(25, message='Обновление списка каналов 2 ...')
			if __settings__.getSetting("serv2")=='true' :upd_canals_db2()
			pDialog.update(50, message='Обновление списка каналов 3 ...')
			if __settings__.getSetting("serv3")=='true' :upd_canals_db3()
			pDialog.update(75, message='Обновление списка каналов 4 ...')
			if __settings__.getSetting("serv4")=='true' :upd_canals_db4()
			pDialog.close()
if mode=="select_gr": select_gr()
if mode=="play"     : play(url, name, cover)
if mode=="next"     : 
	#video=xbmc.translatePath(os.path.join(addon.getAddonInfo('path'), '1.wmv'))
	xbmc.executebuiltin('Container.Update("plugin://plugin.video.pazl.tv/?mode=next2")')

if mode=="next2"     : next ('>')

if mode=="rename"   : updatetc.rename_list(int(ind))
#upd_canals_db3()

def upd_EPG_vsetv():
	url = 'http://www.vsetv.com/schedule_package_bybase_day.html'
	http = getURL(url)
	ss='<div class=chlogo>'
	es='></div><div class="clear'
	L=mfindal(http,ss,es)
	epg={}
	n=0
	t=len(L)
	for i in L:
		#print i
		try:
			i=i.decode('windows-1251')
			i=i.encode('utf-8')
		except: pass
		i=i.replace(chr(10),"").replace(chr(13),"").replace("\t","")
		#debug (i)
		n+=1
		if i!="":
			
			ss='class="channeltitle">'
			es='</td><td width="99%"'
			cnl_nm=mfindal(i,ss,es)[0][len(ss):]
			#print cnl_nm
			idx=get_idx(cnl_nm)
			if idx=="": idx=get_idx(cnl_nm.replace(" Россия",""))
			
			if idx!="":
				tmp=i.replace('class="past','class="').replace('class="onair"','class="time"')
				tmp=tmp.replace('</div><div class="prname2">','<:--:>').replace('align="absmiddle">&nbsp;','-:>').replace('.html>','-:>').replace('.html class=b>','-:>')
				tmp=tmp.replace('-:><','')
				sdn=tmp.find('chnum')
				tmp=tmp[sdn:]
				ss='class="time"'
				es='div><div'
				#print tmp
				L2=mfindal(tmp,ss,es)
				Le=[]
				for j in L2:
					try:
						ss='"time">'
						es='<:'
						stm=mfindal(j,ss,es)[0][len(ss):]
						
						ss=':>'
						es='</'
						pr_nm=mfindal(j,ss,es)[0][len(ss):]
						if pr_nm=="": print j
						
						start_at=time.strftime('%Y-%m-%d')+" "+stm+":00"
						#print start_at +" - "+pr_nm
						Le.append({"name":pr_nm, "start_at":start_at})
					except: 
						print j
						pass
				try:pDialog.update(int(n*100/t), message=cnl_nm)
				except: pass
				if len(Le)>0:add_to_db(idx, repr(Le))

			else:
				print "NO_ID: "+cnl_nm
		#if n>13: break
#upd_EPG_vsetv()

c.close()


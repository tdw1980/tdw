# -*- coding: utf-8 -*-
# CONSTANTS
#__author__ = 'TDW'
#__version__ = '1.0.0'
#__url__ = 'http://xbmc.ru'
#__date__ = '2/2015'

# IMPORTS
import sys, os
import urllib, urllib2
import xbmcaddon
import xbmcgui
import xbmcplugin
import subprocess
#import rarfile

# custom
#lib_path = xbmcaddon.Addon('plugin.program.isybrowse'). \
#    getAddonInfo('path') + '/resources/lib/'
#sys.path.append(lib_path)
#import shared
#import actions
#import menus

addon=xbmcaddon.Addon('plugin.program.retrogames')
handle=int(sys.argv[1])

try:
	if addon.getSetting("RD")<>"":
		RDir = os.path.join( addon.getSetting("RD"), "roms" )
		if os.path.exists(RDir) == False: os.makedirs(RDir)
	else: RDir = os.path.join( addon.getAddonInfo('path'), "roms" )
except:
	RDir = os.path.join( addon.getAddonInfo('path'), "roms" )

TMPdir = os.path.join( addon.getAddonInfo('path'), "temp" )
CDir = os.path.join( addon.getAddonInfo('path'), "images", "covers" )

#Mpath = "D:\\1\\med\\mednafen.exe"
Mpath = addon.getSetting("MD")
fsp=' -video.fs "1" '
MedList=[".nes", ".gen", ".gbc", ".gba", ".ngp", ".snes", ".sms", ".smc", ".pce", ".gg", ".lnx", ".ngc", ".vb",".32x" ,".32X" ,".a26" ,".A26" ,".a78" ,".A78" ,".adf" ,".ADF" ,".bin" ,".BIN" ,".bin" ,".BIN" ,".bin" ,".BIN" ,".bin" ,".BIN" ,".bin" ,".BIN" ,".bin" ,".BIN" ,".bin" ,".BIN" ,".bin" ,".BIN" ,".bin" ,".BIN" ,".bin" ,".BIN" ,".ccd" ,".CCD" ,".cdi" ,".CDI" ,".col" ,".COL" ,".cso" ,".CSO" ,".cue" ,".CUE" ,".cue" ,".CUE" ,".cue" ,".CUE" ,".cue" ,".CUE" ,".dsk" ,".DSK" ,".dsk" ,".DSK" ,".fba" ,".FBA" ,".gb" ,".GB" ,".gba" ,".GBA" ,".gbc" ,".GBC" ,".gdi" ,".GDI" ,".gen" ,".GEN" ,".gg" ,".GG" ,".gz" ,".GZ" ,".img" ,".IMG" ,".img" ,".iso" ,".ISO" ,".iso" ,".ISO" ,".j64" ,".J64" ,".jag" ,".JAG" ,".lnx" ,".LNX" ,".md" ,".MD" ,".md" ,".MD" ,".md" ,".MD" ,".mdf" ,".MDF" ,".mds" ,".MDS" ,".mgt" ,".MGT" ,".mx1" ,".MX1" ,".mx2" ,".MX2" ,".n64" ,".N64" ,".nds" ,".NDS" ,".nes" ,".NES" ,".ngc" ,".ngp" ,".pce" ,".PCE" ,".rom" ,".ROM" ,".scl" ,".SCL" ,".sfc" ,".SFC" ,".sg" ,".SG" ,".smc" ,".SMC" ,".smd" ,".SMD" ,".sms" ,".SMS" ,".sna" ,".st" ,".stx" ,".szx" ,".SZX" ,".tap" ,".TAP" ,".trd" ,".TRD" ,".tzx" ,".TZX" ,".udi" ,".UDI" ,".v64" ,".V64" ,".vb" ,".VB" ,".ws" ,".wsc" ,".z64" ,".Z64" ,".z80" ,".Z80" ,".zip" ,".ZIP" ,"SNA"]

def rt(x):
	L=[('&#8216;',''), ('&#8212;','-'), ('&#133;','…'), ('&#34;','&'), ('&#39;','’'), ('&#145;','‘'), ('&#146;','’'), ('&#147;','“'), ('&#148;','”'), ('&#149;','•'), ('&#150;','–'), ('&#151;','—'), ('&#152;','?'), ('&#153;','™'), ('&#154;','s'), ('&#155;','›'), ('&#156;','?'), ('&#157;',''), ('&#158;','z'), ('&#159;','Y'), ('&#160;',''), ('&#161;','?'), ('&#162;','?'), ('&#163;','?'), ('&#164;','¤'), ('&#165;','?'), ('&#166;','¦'), ('&#167;','§'), ('&#168;','?'), ('&#169;','©'), ('&#170;','?'), ('&#171;','«'), ('&#172;','¬'), ('&#173;',''), ('&#174;','®'), ('&#175;','?'), ('&#176;','°'), ('&#177;','±'), ('&#178;','?'), ('&#179;','?'), ('&#180;','?'), ('&#181;','µ'), ('&#182;','¶'), ('&#183;','·'), ('&#184;','?'), ('&#185;','?'), ('&#186;','?'), ('&#187;','»'), ('&#188;','?'), ('&#189;','?'), ('&#190;','?'), ('&#191;','?'), ('&#192;','A'), ('&#193;','A'), ('&#194;','A'), ('&#195;','A'), ('&#196;','A'), ('&#197;','A'), ('&#198;','?'), ('&#199;','C'), ('&#200;','E'), ('&#201;','E'), ('&#202;','E'), ('&#203;','E'), ('&#204;','I'), ('&#205;','I'), ('&#206;','I'), ('&#207;','I'), ('&#208;','?'), ('&#209;','N'), ('&#210;','O'), ('&#211;','O'), ('&#212;','O'), ('&#213;','O'), ('&#214;','O'), ('&#215;','?'), ('&#216;','O'), ('&#217;','U'), ('&#218;','U'), ('&#219;','U'), ('&#220;','U'), ('&#221;','Y'), ('&#222;','?'), ('&#223;','?'), ('&#224;','a'), ('&#225;','a'), ('&#226;','a'), ('&#227;','a'), ('&#228;','a'), ('&#229;','a'), ('&#230;','?'), ('&#231;','c'), ('&#232;','e'), ('&#233;','e'), ('&#234;','e'), ('&#235;','e'), ('&#236;','i'), ('&#237;','i'), ('&#238;','i'), ('&#239;','i'), ('&#240;','?'), ('&#241;','n'), ('&#242;','o'), ('&#243;','o'), ('&#244;','o'), ('&#245;','o'), ('&#246;','o'), ('&#247;','?'), ('&#248;','o'), ('&#249;','u'), ('&#250;','u'), ('&#251;','u'), ('&#252;','u'), ('&#253;','y'), ('&#254;','?'), ('&#255;','y'), ('&laquo;','"'), ('&raquo;','"'), ('&nbsp;',' ')]
	for i in L:
		x=x.replace(i[0], i[1])
	return x


from core_conf import*
#try:
if addon.getSetting("cores")<>"":
		user_set = addon.getSetting("cores")
		user_list= eval("[('."+user_set.replace(" ","").replace(",","'),('.").replace(";","'),('.").replace("=","','")+"'),]")
		for i in user_list:
			CoreDict[i[0]]=i[1]
#except:pass

#rarfile.UNRAR_TOOL=os.path.join( addon.getAddonInfo('path'), 'resources','lib','unrar.exe')

if os.name=="nt":	Z7path=os.path.join( addon.getAddonInfo('path'), 'resources','lib','7za.exe')
else:				Z7path=os.path.join( addon.getAddonInfo('path'), 'resources','lib','7za_rpi')

xbmcplugin.setContent(int(sys.argv[1]), 'movies')

cover=os.path.join( addon.getAddonInfo('path'), "icon.png" )
def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)

def showMessage(heading, message, times = 3000):
	xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s, "%s")'%(heading, message, times, cover))

CList=[
("http://emu-russia.net/data/logo/dendy_logo.jpg", "NES", "Dendy(NES)", "http://emu-russia.net/ru/roms/nes/", "Dendy/Денди (NES)"), 
("http://emu-russia.net/data/logo/snes_logo.jpg", "Super Nintendo", "Super Nintendo", "http://emu-russia.net/ru/roms/snes/", "Super Nintendo(SNES)"), 
("http://emu-russia.net/data/logo/md_logo.jpg", "Sega", "Sega MegaDrive", "http://emu-russia.net/ru/roms/gen/", "Sega MegaDrive Сега (GEN)"), 
("http://emu-russia.net/data/logo/sms_logo.jpg", "Sega Master System", "Sega Master System", "http://emu-russia.net/ru/roms/sms/", "Sega Master System (SMS)"), 
("http://emu-russia.net/data/logo/gg_logo.jpg", "GameGear", "GameGear", "http://emu-russia.net/ru/roms/gg/", "GameGear (GG)"), 
("http://emu-russia.net/data/logo/lynx_logo.jpg", "Lynx", "Lynx", "http://emu-russia.net/ru/roms/lynx/", "Lynx (LYNX)"), 
("http://emu-russia.net/data/logo/ngpc_logo.jpg", "NeoGeo Color", "NeoGeo Pocket Color", "http://emu-russia.net/ru/roms/ngpc/", "NeoGeo Pocket Color (NGPC)"), 
("http://emu-russia.net/data/logo/gbc_logo.jpg", "GameBoy Color", "GameBoy Color", "http://emu-russia.net/ru/roms/gbc/", "GameBoy Color (GBC)"), 
("http://emu-russia.net/data/logo/tg16_logo.jpg", "TurboGrafx-16", "TurboGrafx-16", "http://emu-russia.net/ru/roms/tg16/", "TurboGrafx-16 (TG16)"), 
("http://emu-russia.net/data/logo/vboy_logo.jpg", "Virtual Boy", "Virtual Boy", "http://emu-russia.net/ru/roms/vboy/", "Virtual Boy (VBOY)")
]

GList=[
("/gba/rus-1/","На русском"),
("/gba/action/","Экшен"),
("/gba/strategy/","Стратегия"),
("/gba/puzzle/","Паззл"),
("/gba/rpg/","РПГ"),
("/gba/racing/","Гонки"),
("/gba/simulation/","Симулятор"),
("/gba/fighting/","Драки"),
("/gba/shooter/","Шутер"),
("/gba/sport/","Спорт")
]
def getURL(url,Referer = 'http://emulations.ru/'):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Opera/10.60 (X11; openSUSE 11.3/Linux i686; U; ru) Presto/2.6.30 Version/10.60')
	req.add_header('Accept', 'text/html, application/xml, application/xhtml+xml, */*')
	req.add_header('Accept-Language', 'ru,en;q=0.9')
	req.add_header('Referer', Referer)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def add_item (name, mode="", path = RDir, cover=None, funart=None, type="x"):
	if cover==None:	listitem = xbmcgui.ListItem(name)
	else:			listitem = xbmcgui.ListItem(name, iconImage=cover, thumbnailImage=cover)
	listitem.setProperty('fanart_image', funart)
	uri = sys.argv[0] + '?mode='+mode
	uri += '&path='  + urllib.quote_plus(path)
	uri += '&name='  + urllib.quote_plus(name)
	uri += '&type='  + urllib.quote_plus(type)
	if cover!=None:uri += '&cover='  + urllib.quote_plus(cover)
	if funart!=None and funart!="":uri += '&funart='  + urllib.quote_plus(funart)
	
	urr = sys.argv[0] + '?mode=rem'
	urr += '&path='  + urllib.quote_plus(path)
	
	urr2 = sys.argv[0] + '?mode=rem2'
	urr2 += '&path='  + urllib.quote_plus(path)

	if mode=="run":listitem.addContextMenuItems([('[COLOR F050F050] Удалить [/COLOR]', 'Container.Update("plugin://plugin.program.retrogames/'+urr+'")'),('[COLOR F050F050] Оставить только это [/COLOR]', 'Container.Update("plugin://plugin.program.retrogames/'+urr2+'")')])

	xbmcplugin.addDirectoryItem(handle, uri, listitem, True)

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

def root():
	cover=os.path.join(CDir, "Download.png")
	add_item ("Каталог", 'OnlRoot', RDir, cover)
	try:dir(RDir)
	except:xbmcplugin.endOfDirectory(handle)

def OnlRoot():
	# emurussia
	#add_item("NES", 'Genre', "http://emu-russia.net/ru/roms/nes/", 'http://emu-russia.net/data/logo/dendy_logo.jpg',type='NES')
	for i in CList:
		add_item(i[2], 'Genre',i[3],i[0],type=i[1])
	# GBA
	add_item("GBA", 'GBAGenre', "http://gbaroms.ru/gba/rus-1/", 'http://emu-russia.net/data/logo/gba_logo.jpg',type='GBA')
	xbmcplugin.endOfDirectory(handle)
	
def GBAGenre(url, t):
	for i in GList:
		add_item(i[1], 'GBAList', 'http://gbaroms.ru'+i[0], 'http://emu-russia.net/data/logo/gba_logo.jpg',type='GBA')
	xbmcplugin.endOfDirectory(handle)

def Genre(url, t):
	#url='http://emu-russia.net/ru/roms/nes/'
	add_item ("Все", "OnlList", url+'0-Z/full/', type=t)
	http=getURL(url)
	ss='<!-- Genre listing -->'
	es='<!-- End of genre listing -->'
	http=mfindal(http, ss, es)[0]
	#print http
	ss="http://emu-russia.net/ru/rom"
	es='</a><br>'
	L=mfindal(http, ss, es)
	for i in L:
		ss='http://emu-russia.net/ru'
		es='"><b>'
		url=mfindal(i, ss, es)[0]
		ss='"><b>'
		es='</b>'
		title=mfindal(i, ss, es)[0][5:]
		
		add_item (title, "OnlList", url, type=t)
	xbmcplugin.endOfDirectory(handle)

def OnlList(url, type):
	http=getURL(url)
	#debug (http)
	nd=http.find('<!-- End of Keyword search -->')
	http=http[nd:]
	ss="<tr><td>"+chr(13)
	es="</table><br>"
	L=mfindal(http, ss, es)
	n=0
	for i in L:
		n+=1
		
		ss='http://emu-russia.net/ru/dl_roms'
		if i.find(ss)<0:ss='http://dl.emu-russia.net/get/'
		es='</b></td></tr>'
		t1=mfindal(i, ss, es)[0]
		#ss='http://emu-russia.net/ru/dl_roms'
		es='" title="'
		url=mfindal(t1, ss, es)[0]
		ss=')">'
		es='</a>'
		title=mfindal(t1, ss, es)[0][3:]
		
		ss='http://emu-russia.net/gdb'
		es='" alt="Показать все картинки'
		try:funart=mfindal(i, ss, es)[0]
		except: funart=""
		cover=funart.replace("_1.","_0.")
		#print n
		#print title
		#print cover
		#print url
		add_item (title, "dload", url, cover, funart, type)
		
	xbmcplugin.endOfDirectory(handle)

def GBAList(url, type, np="1"):
	oldurl=url
	p="page/"+str(np)+"/"
	if np=="1" or len(p)> 10: p=""
	print url+p
	http=getURL(url+p)
	#debug (http)
	nd=http.find('<!-- main START -->')
	http=http[nd:]
	ss='<div class="post" id="post-'
	es='<div class="under">'
	L=mfindal(http, ss, es)
	n=0
	for i in L:
		n+=1
		ss='<img class="alignleft"  src="'
		es='.jpg" width="200" height="200"'
		try:
			img=mfindal(i, ss, es)[0][len(ss):]
			cover=img+".jpg"
			funart=img+"-1.png"
		except: 
			cover=""
			funart=""
		
		ss='<a class="title" href="http://gbaroms.ru/'
		es='/" rel="bookmark">'
		url="http://gbaroms.ru/"+mfindal(i, ss, es)[0][len(ss):]
		
		ss='/" rel="bookmark">'
		es='</a></h2>'
		try:title=mfindal(i, ss, es)[0][len(ss):].replace("&#8211;","-").replace("&#8217;","'")
		except: title="ERROR"
		
		#print n
		#print title
		#print cover
		#print url
		add_item (rt(title), "sel_dload", url, cover, funart, type)
	try:npg=str(int(np)+1)
	except: npg="2"
	add_item("Далее >", 'GBAList', oldurl, npg, type='GBA')
	
	xbmcplugin.endOfDirectory(handle)

def debug(s):
	fl = open(os.path.join( ru(RDir),"test.txt"), "w")
	fl.write(s)
	fl.close()


def dir(path, cover=None):
	hide=[".png", ".jpg", ".7z"]
	ld=os.listdir(path)
	for i in ld:
		if os.path.isdir(path):
			ncover=os.path.join(path, i, "cover.png")
			if os.path.exists(ncover): cover=ncover
			else: cover=None
			nart=os.path.join(path, i, "funart.png")
			if os.path.exists(nart): funart=nart
			else: funart=None
		ecover=os.path.join(path, os.path.splitext(i)[0]+".png")
		if os.path.exists(ecover):cover=ecover
		ext=os.path.splitext(i)[1]
		cl_name=i.replace(ext,"")
		if cover==None:
			lcover=os.path.join(CDir, cl_name+".png")
			if os.path.exists(lcover):cover=lcover
		if ext not in hide: add_item(cl_name, "run", os.path.join(path, i),cover, funart)
	xbmcplugin.endOfDirectory(handle)

def drl(path):
	rlst=[]
	ld=os.listdir(path)
	for i in ld:
		ext=os.path.splitext(i)[1]
		if ext in MedList: rlst.append(i)
	return rlst

def tolnx(s):
	lstr="'"+s.replace("'","'\\''")+"'"
	return lstr

def run_off(path):
	if Mpath.find("mednafen")>0:
		command=Mpath+fsp+'"'+path+'"'
	elif Mpath.find("retroarch")>0:
		ext=os.path.splitext(path)[1]
		try:core=CoreDict[ext]
		except: core=''
		print '-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-='
		print os.name
		if os.name=="nt":command=Mpath+' -L '+os.path.join(os.path.split(Mpath)[0], "cores", core)+'_libretro "'+path+'"'
		else:command=Mpath+' '+core+' '+tolnx(path)
	else:
		command=Mpath+' "'+path+'"'
	#print command +' , --subsystem='
	ext=os.path.splitext(path)[1]
	if os.path.isdir(path):
		#print ext
		if ext ==".dr":
			rlst=drl(path)
			if len(rlst)==1:
				newpath=os.path.join(path,rlst[0])
				print newpath
				if Mpath.find("mednafen")>0:
					command2=Mpath+fsp+'"'+newpath+'"'
				elif Mpath.find("retroarch")>0:
					ext=os.path.splitext(newpath)[1]
					try:core=CoreDict[ext]
					except: core=""
					if os.name=="nt":
						command2=Mpath+' -L '+os.path.join(os.path.split(Mpath)[0], "cores", core)+'_libretro "'+newpath+'"'
					else:command2=Mpath+' '+core+' '+tolnx(newpath)
				else:
					command2=Mpath+' "'+newpath+'"'
				print command2
				os.system(command2)
			else:dir(path)
		else:dir(path)
	else:
		if ext in MedList:
			print command
			os.system(command)
			#subprocess.call(command)
			print '-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-='
		else:os.system(path)

def run(path):
	ext=os.path.splitext(path)[1]
	if os.path.isdir(path):
		#print ext
		if ext ==".dr":
			rlst=drl(path)
			if len(rlst)==1:
				newpath=os.path.join(path,rlst[0])
				print newpath
				gameplay(newpath)
			else:dir(path)
		else:dir(path)
	else:
		if ext in MedList:
			gameplay(path)
		else:
			if os.name=="nt":os.system('"'+path+'"')
			else:os.system(tolnx(path))

def gameplay(path):
	if Mpath.find("mednafen")>0:
		command=Mpath+fsp+'"'+path+'"'
	elif Mpath.find("retroarch")>0:
		ext=os.path.splitext(path)[1]
		try:core=CoreDict[ext]
		except: core=''
		print '-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-='
		print os.name
		if os.name=="nt":command=Mpath+' -L '+os.path.join(os.path.split(Mpath)[0], "cores", core)+'_libretro "'+path+'"'
		else:command=Mpath+' '+core+' '+tolnx(path)
	else:
		command=Mpath+' "'+path+'"'
	print command
	print '-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-='
	#subprocess.call(command)
	subprocess.Popen(command, shell = True)
	#os.system(command)

def gameplay_off(path):
	print '-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-='
	if Mpath.find("mednafen")>0:
		command = [Mpath,'-video.fs','1',path]
	elif Mpath.find("retroarch")>0:
		ext=os.path.splitext(path)[1]
		try:core=CoreDict[ext]
		except: core=''
		print os.name
		if os.name=="nt":
			#command=Mpath+' -L '+os.path.join(os.path.split(Mpath)[0], "cores", core)+'_libretro "'+path+'"'
			command=[Mpath,'-L'+os.path.join(os.path.split(Mpath)[0], "cores", core)+'_libretro',path]
		else:
			#command=Mpath+' '+core+' '+tolnx(path)
			command=[Mpath, core, path]
	else:
		command=[Mpath, path]
	print command
	print '-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-='
	#subprocess.call(command)
	subprocess.Popen(command, shell = True)
	#os.system(command)


def sel_dload(title, type, url, cover, funart):
		http=getURL(url)
		#debug(http)
		ss='<center><div class="preview-pp2"><img src="'
		es='" width="240" height="160" alt='
		funart=mfindal(http, ss, es)[0][len(ss):]
		
		ss='<div style="margin-left:5px;">'
		es='.rar"><img src="/wp'
		t1=mfindal(http, ss, es)[0]
		n=t1.find("http://gbaroms.ru/")
		url=t1[n:]+".rar"
		
		#print title
		#print funart
		#print url
		dload(title, type, url, cover, funart)
		#add_item (title, "sel_dload", url, cover, funart, type)


def dload(title, type, target, cover, funart):
	title=ru(title.replace('\\','').replace('?',''))
	#print target
	Dldir = RDir
	if Dldir == "":Dldir = os.path.join( addon.getAddonInfo('path'), "roms" )
	
	fp = os.path.join(ru(Dldir), type, title+'.dr')
	if os.path.exists(fp)== False: os.makedirs(fp)
	cp=os.path.join(fp, "cover.png")
	ap=os.path.join(fp, "funart.png")
	fp = os.path.join(fp, title+".7z")
	
	try:
	#if 1==1:
			#debug( getURL(target))
			target=sevn2zip(target)
			req = urllib2.Request(url = target, data = None)
			req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)')
			resp = urllib2.urlopen(req)
			fl = open(fp, "wb")
			fl.write(resp.read())
			fl.close()
			try:
				req = urllib2.Request(url = cover, data = None)
				req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)')
				resp = urllib2.urlopen(req)
				fl = open(cp, "wb")
				fl.write(resp.read())
				fl.close()
				
				if funart=="":req = urllib2.Request(url = cover.replace("_0.","_1."), data = None)
				else:req = urllib2.Request(url = funart, data = None)
				req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)')
				resp = urllib2.urlopen(req)
				fl = open(ap, "wb")
				fl.write(resp.read())
				fl.close()
			except: pass
			#un7zip(fp)
			unzip(fp)
			os.remove(fp)
			return os.path.join( ru(Dldir),nmi)
	except Exception, e:
			#xbmc.log( '[%s]: GET EXCEPT [%s]' % (addon_id, e), 4 )
			return target
			print 'HTTP ERROR ' + str(e)

def rem(path):
	if os.path.isdir(path):
		lst=os.listdir(path)
		for i in lst:
			pf=os.path.join(path, i)
			os.remove(pf)
		os.rmdir(path)
	else:
		d=os.path.split(path)[0]
		sp=path
		if len(os.listdir(d))<=4:dir(os.path.split(d)[0])
		try:os.remove(sp)
		except: pass

def rem2(path):
	dr=os.path.split(path)[0]
	hide=[".png", ".jpg", ".7z"]
	if os.path.isdir(path)==False:
		lst=os.listdir(dr)
		for i in lst:
			ext=os.path.splitext(i)[1]
			pf=os.path.join(dr, i)
			if pf!=path and ext not in hide: os.remove(pf)
	xbmc.executebuiltin('Container.Refresh')


def sel_play(url):
		http=getURL(url)
		
		ss='<div style="margin-left:5px;">'
		es='.rar"><img src="/wp'
		t1=mfindal(http, ss, es)[0]
		n=t1.find("http://gbaroms.ru/")
		url=t1[n:]+".rar"
		
		play(url)


def play(target):
		rem(TMPdir)
		if os.path.exists(TMPdir)== False: os.makedirs(TMPdir)
		fp = os.path.join(TMPdir, "tmp.7z")
		target=sevn2zip(target)
		try:
			req = urllib2.Request(url = target, data = None)
			req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)')
			resp = urllib2.urlopen(req)
			fl = open(fp, "wb")
			fl.write(resp.read())
			fl.close()
			#un7zip(fp)
			unzip(fp)
			os.remove(fp)
			dir(TMPdir)
		except: pass

def unzip(filename):
	from zipfile import ZipFile
	fil = ZipFile(filename, 'r')
	for name in fil.namelist():
		#print name
		try:
			unicode_name = name.decode('UTF-8').encode('UTF-8')
		except UnicodeDecodeError:
			unicode_name = name.decode('cp866').encode('UTF-8')
		# открываем файл и пишем в него из архива
		f2 = open(os.path.join(os.path.split(filename)[0],unicode_name), 'wb')
		f2.write(fil.read(name))
		f2.close()
	fil.close()

def un7zip(path):
	
	dp=os.path.split(path)[0]
	if os.name=="nt":	command=Z7path+' x '+'"'+path+'" -y -o"'+dp+'"'
	else:				command=Z7path+' x '+tolnx(path)+' -y -o'+tolnx(dp)
	print command
	#subprocess.call(command)
	os.system(command)

def unrar(filename):
	rar = rarfile.RarFile(filename)
	rar.extractall(os.path.split(filename)[0],None,None) 


def get_HTML(url, post = None, ref = None, get_redirect = False):
	request = urllib2.Request(url, post)
	import urlparse
	#import HTMLParser
	#hpar = HTMLParser.HTMLParser()
	host = urlparse.urlsplit(url).hostname
	if ref==None:
		try:   ref='http://'+host
		except:ref='localhost'

	request.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)')
	request.add_header('Host',   host)
	request.add_header('Accept', 'text/html, application/xhtml+xml, */*')
	request.add_header('Accept-Language', 'ru-RU')
	request.add_header('Referer',             ref)
	request.add_header('Content-Type','application/x-www-form-urlencoded')
	try:
		f = urllib2.urlopen(request)
	except IOError, e:
		if hasattr(e, 'reason'):
			print('We failed to reach a server.')
		elif hasattr(e, 'code'):
			print('The server couldn\'t fulfill the request.')
		return None
	if get_redirect == True:
		html = f.geturl()
	else:
		html = f.read()
	return html

def getID():
	l=["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q" ,"r","s","t","u","v","w","x","y","z"]
	id=""
	import random
	for i in range (0,14):
		id+=random.choice(l)
	return id


def sevn2zip(url7z):
	print url7z
	if url7z[-3:]=="rar": format=".rar"
	else: format=".7z"
	categoryUrl="http://www.convertfiles.com/converter.php"
	#url7z="http://emu-russia.net/ru/dl_roms/nes/83e74a69ae372f6804f72e65901121c2/High_Speed.7z"
	id="f0i4kpk7jh9tai"
	id=getID()
	post = "APC_UPLOAD_PROGRESS="+id+"&FileOrURLFlag=url&file_or_url=url&download_url="+url7z+"&input_format="+format+"&output_format=.zip"
	http = get_HTML(categoryUrl, post)
	#print http
	
	categoryUrl="http://www.convertfiles.com/getprogress.php?progress_key="+id
	for i in range(0,10):
		showMessage("Загрузка", "0 %", 2000)
		xbmc.sleep(2000)
		progress = get_HTML(categoryUrl)
		showMessage("Загрузка", str(progress)+" %", 2000)
		if len(progress)>2:
			categoryUrl="http://www.convertfiles.com/convertrogressbar.php?progress_key="+id+"&i=1"
			html = get_HTML(categoryUrl)
			for i in range(0,10):
				if len(html)<5:
					showMessage("Конвертирование", html, 2000)
					xbmc.sleep(3000)
					html = get_HTML(categoryUrl)

			ss='converted file: <a href="'
			es='" target="_blank'
			try:link=mfindal(html,ss,es)[0][len(ss):]
			except: 
				link=""
				showMessage("Ошибка", str(html), 2000)
			#debug(link)
			return link
		else:
			try: pr=int(progress)
			except: pr=0
			showMessage("Загрузка", str(progress), 2000)



def select(name, cover, funart=""):#,type, path
	
	if funart=="": funart=cover.replace('_0.png','_1.png')
	
	addon.setSetting(id="id_name", value=name)
	#addon.setSetting(id="id_type", value=type)
	addon.setSetting(id="id_funart", value=funart)
	addon.setSetting(id="id_cover", value=cover)
	import SelectBox
	SelectBox.run("w1")
	return addon.getSetting("w1")


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
try:path = urllib.unquote_plus(params["path"])
except:path = RDir
try:name = urllib.unquote_plus(params["name"])
except:name = "noname"
try:cover = urllib.unquote_plus(params["cover"])
except:cover = ""
try:funart = urllib.unquote_plus(params["funart"])
except:funart = ""

try:type = urllib.unquote_plus(params["type"])
except:type = "x"



if mode=="":root()
if mode=="run":run(path)
if mode=="OnlRoot":OnlRoot()
if mode=="OnlList":OnlList(path, type)
if mode=="GBAList":GBAList(path, type, cover)
if mode=="GBAGenre":GBAGenre(path, type)
if mode=="Genre":Genre(path, type)
if mode=="sel_dload":
	try:
		r=select(name, cover, funart)
		if r=="save":sel_dload(name, type, path, cover, funart)
		if r=="run":sel_play(path)
	except:
		sel_dload(name, type, path, cover, funart)

if mode=="dload":
	try:
		r=select(name, cover)
		if r=="save":dload(name, type, path, cover, funart)
		if r=="run":play(path)
	except:
		dload(name, type, path, cover, funart)

if mode=="rem":rem(path)
if mode=="rem2":rem2(path)
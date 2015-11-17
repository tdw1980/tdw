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
MedList=[".nes", ".gen", ".gbc", ".gba", ".ngp", ".snes", ".sms", ".smc", ".pce", ".gg", ".lnx", ".ngc", ".vb"]

from core_conf import*

#rarfile.UNRAR_TOOL=os.path.join( addon.getAddonInfo('path'), 'resources','lib','unrar.exe')

if os.name=="nt":	Z7path=os.path.join( addon.getAddonInfo('path'), 'resources','lib','7za.exe')
else:				Z7path=os.path.join( addon.getAddonInfo('path'), 'resources','lib','7za_rpi')

xbmcplugin.setContent(int(sys.argv[1]), 'movies')

cover=os.path.join( addon.getAddonInfo('path'), "icon.png" )
def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)

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

def add_item (name, mode="", path = RDir, cover=None, funart="", type="x"):
	if cover==None:	listitem = xbmcgui.ListItem(name)
	else:			listitem = xbmcgui.ListItem(name, iconImage=cover)
	listitem.setProperty('fanart_image', funart)
	uri = sys.argv[0] + '?mode='+mode
	uri += '&path='  + urllib.quote_plus(path)
	uri += '&name='  + urllib.quote_plus(name)
	uri += '&type='  + urllib.quote_plus(type)
	if cover!=None:uri += '&cover='  + urllib.quote_plus(cover)
	
	urr = sys.argv[0] + '?mode=rem'
	urr += '&path='  + urllib.quote_plus(path)
	if mode=="run":listitem.addContextMenuItems([('[COLOR F050F050] Удалить [/COLOR]', 'Container.Update("plugin://plugin.program.retrogames/'+urr+'")'),])

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
	for i in CList:
		add_item(i[2], 'Genre',i[3],i[0],type=i[1])
	
	#add_item("NES", 'Genre', "http://emu-russia.net/ru/roms/nes/", 'http://emu-russia.net/data/logo/dendy_logo.jpg',type='NES')
	#add_item ("Sega", 'Genre', 'http://emu-russia.net/ru/roms/gen/', 'http://emu-russia.net/data/logo/md_logo.jpg', type="Sega")
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
		ecover=os.path.splitext(i)[1]+".png"
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

def run(path):
	if Mpath.find("mednafen")>0:
		command=Mpath+fsp+'"'+path+'"'
	elif Mpath.find("retroarch")>0:
		ext=os.path.splitext(path)[1]
		try:core=CoreDict[ext]
		except: core=''
		print '-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-='
		print os.name
		if os.name=="nt":command=Mpath+' -L '+os.path.join(os.path.split(Mpath)[0], "cores", core)+'_libretro "'+path+'"'
		else:command=Mpath+' '+core+' '+path.replace(" ", "\\ ").replace("'", "\\'")
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
				if Mpath.find("mednafen")>0:
					command2=Mpath+fsp+'"'+newpath+'"'
				elif Mpath.find("retroarch")>0:
					ext=os.path.splitext(newpath)[1]
					try:core=CoreDict[ext]
					except: core=""
					if os.name=="nt":
						command2=Mpath+' -L '+os.path.join(os.path.split(Mpath)[0], "cores", core)+'_libretro "'+newpath+'"'
					else:command2=Mpath+' '+core+' '+newpath.replace(" ", "\\ ").replace("'", "\\'")
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


def dload(title, type, target, cover):
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
				
				req = urllib2.Request(url = cover.replace("_0.","_1."), data = None)
				req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)')
				resp = urllib2.urlopen(req)
				fl = open(ap, "wb")
				fl.write(resp.read())
				fl.close()
			except: pass
			un7zip(fp)
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

def play(target):
		rem(TMPdir)
		if os.path.exists(TMPdir)== False: os.makedirs(TMPdir)
		fp = os.path.join(TMPdir, "tmp.7z")
		try:
			req = urllib2.Request(url = target, data = None)
			req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)')
			resp = urllib2.urlopen(req)
			fl = open(fp, "wb")
			fl.write(resp.read())
			fl.close()
			un7zip(fp)
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
		f2 = open(os.path.join(os.path.split(filename)[0],unicode_name), 'w')
		f2.write(fil.read(name))
		f2.close()
	fil.close()

def un7zip(path):
	
	dp=os.path.split(path)[0]
	command=Z7path+' x '+'"'+path+'" -y -o"'+dp+'"'
	#print command
	subprocess.call(command)
	#os.system(command)

def unrar(filename):
	rar = rarfile.RarFile(filename)
	rar.extractall(os.path.split(filename)[0],None,None) 


def select(name, cover):#,type, path
	addon.setSetting(id="id_name", value=name)
	#addon.setSetting(id="id_type", value=type)
	#addon.setSetting(id="id_path", value=path)
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
try:type = urllib.unquote_plus(params["type"])
except:type = "x"

#un7zip("d:\\1\\2\\3.7z")

if mode=="":root()
if mode=="run":run(path)
if mode=="OnlRoot":OnlRoot()
if mode=="OnlList":OnlList(path, type)
if mode=="Genre":Genre(path, type)
if mode=="dload":
	try:
		r=select(name, cover)
		if r=="save":dload(name, type, path, cover)
		if r=="run":play(path)
	except:
		dload(name, type, path, cover)

if mode=="rem":rem(path)
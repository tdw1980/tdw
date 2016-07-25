# coding: utf-8
# Module: server
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import sys, os
import xbmc, xbmcgui, xbmcaddon
import time
import urllib2
__settings__ = xbmcaddon.Addon(id='plugin.video.pazl.tv')
addon = xbmcaddon.Addon(id='plugin.video.pazl.tv')
icon=None
pDialog = xbmcgui.DialogProgressBG()

#time.sleep(10)
xbmc.sleep(10000)
print('----- Starting PTV -----')
start_trigger = True
#n=0
# =========================== Базовые функции ================================
from xid import *

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

def getURL(url, Referer = 'http://viks.tv/'):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Opera/10.60 (X11; openSUSE 11.3/Linux i686; U; ru) Presto/2.6.30 Version/10.60')
	req.add_header('Accept', 'text/html, application/xml, application/xhtml+xml, */*')
	req.add_header('Accept-Language', 'ru,en;q=0.9')
	req.add_header('Referer', Referer)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

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

def debug(s):
	fl = open(ru(os.path.join( addon.getAddonInfo('path'),"test.txt")), "w")
	fl.write(s)
	fl.close()

# ================================ БД =======================================
import sqlite3 as db
db_name = os.path.join( addon.getAddonInfo('path'), "epg.db" )
c = db.connect(database=db_name)
cu = c.cursor()

def add_to_db(n, item):
	if len(item)>4:
		c = db.connect(database=db_name)
		cu = c.cursor()
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
		c.close()
		xbmc.sleep(30)


def get_inf_db(n):
		c = db.connect(database=db_name)
		cu = c.cursor()
		tor_id="n"+n
		cu.execute(str('SELECT db_item FROM '+tor_id+';'))
		c.commit()
		Linfo = cu.fetchall()
		info=Linfo[0][0].replace("XXCC","'").replace("XXDD",'"')
		return info
		c.close()

# ================================ EPG =======================================

def upepg():
			pDialog.create('Пазл ТВ', 'Обновление EPG ...')
			#if __settings__.getSetting('epgitv')=='true': upd_EPG_itv()
			if __settings__.getSetting('stv')=='true': upd_stv()
			if __settings__.getSetting('epgxml')=='true': upd_EPG_xmltv()
			if __settings__.getSetting('epgtvx')=='true': yatv()#upd_EPG()
			if __settings__.getSetting('vsetv_ru')=='true': upd_EPG_vsetv("rubase")
			if __settings__.getSetting('vsetv_ua')=='true': upd_EPG_vsetv("uabase")
			if __settings__.getSetting('vsetv_by')=='true': upd_EPG_vsetv("bybase")
			#xbmc.executebuiltin("Container.Refresh")
			pDialog.close()


def yatv():
	for n in range(0,31):
		ncrd=str(long(time.time())*1000+1080)
		dtm=time.strftime('%Y-%m-%d')
		url='https://m.tv.yandex.ru/ajax/i-tv-region/get?params=%7B%22channelLimit%22%3A'+str(10)+'%2C%22channelOffset%22%3A'+str(n*10)+'%2C%22fields%22%3A%22channel%2Ctitle%2Clogo%2Cchannel%2Csynonyms%2Cfavourite%2Cid%2CsiteUrl%2CbroadcastUrl%2ConlinesPlayer%2Ctitle%2Clogo%2Csizes%2Cwidth%2Cheight%2Csrc%2Ccopyright%2Cschedules%2Cchannels%2Cfinish%2Cchannel%2Cid%2Ctitle%2Cfavourite%2CchannelsCountPerGenre%2CavailableProgramTypes%2CavailableChannels%2Celement%2Cid%2Cname%2Cevents%2Cid%2CchannelId%2Clive%2Crecommended%2ChasReminder%2Cepisode%2CseasonName%2CseasonNumber%2Cid%2CprogramId%2Ctitle%2Cstart%2Cfinish%2Cprogram%2Cid%2Ctype%2Cid%2Cname%2Ctitle%2Csizes%2Ccopyright%2C100%2C120%2C160%2C200%2C300%2C400%2Cwidth%2Cheight%2Csrc%22%2C%22channelIds%22%3A%22146%2C109%2C1593%2C162%2C427%2C187%2C1683%2C740%2C1000%2C529%2C689%2C447%2C79%2C114%2C279%2C1003%2C405%2C726%2C350%2C897%2C150%2C1598%2C1649%2C898%2C323%2C1048%2C1624%2C1046%2C127%2C267%2C123%2C462%2C22%2C542%2C566%2C145%2C125%2C477%2C401%2C994%2C911%2C615%2C935%2C1371%2C1037%2C918%2C309%2C311%2C53%2C485%2C163%2C518%2C821%2C659%2C686%2C516%2C352%2C1570%2C12%2C644%2C608%2C798%2C834%2C1584%2C799%2C1674%2C1620%2C1680%2C55%2C675%2C794%2C520%2C648%2C731%2C333%2C774%2C723%2C367%2C322%2C928%2C35%2C273%2C1036%2C996%2C613%2C912%2C409%2C102%2C365%2C325%2C277%2C521%2C1394%2C1330%2C1436%2C765%2C757%2C223%2C769%2C685%2C1365%2C1562%2C16%2C669%2C1585%2C250%2C406%2C328%2C481%2C531%2C563%2C455%2C288%2C737%2C499%2C850%2C454%2C1039%2C664%2C1376%2C1667%2C1668%2C1669%2C567%2C410%2C308%2C929%2C555%2C747%2C601%2C917%2C31%2C494%2C810%2C66%2C1332%2C1578%2C76%2C828%2C743%2C502%2C278%2C831%2C384%2C214%2C921%2C313%2C1032%2C463%2C495%2C23%2C247%2C461%2C355%2C315%2C1331%2C589%2C59%2C922%2C575%2C715%2C797%2C319%2C804%2C533%2C642%2C591%2C91%2C332%2C849%2C388%2C258%2C927%2C270%2C430%2C473%2C681%2C151%2C1021%2C662%2C25%2C680%2C1561%2C156%2C491%2C257%2C1673%2C393%2C82%2C132%2C434%2C119%2C376%2C705%2C637%2C153%2C614%2C931%2C113%2C21%2C547%2C595%2C346%2C779%2C617%2C661%2C919%2C505%2C173%2C1571%2C776%2C425%2C1397%2C1660%2C1662%2C1679%2C1322%2C777%2C412%2C165%2C925%2C1026%2C1329%2C663%2C920%2C1676%2C312%2C631%2C801%2C121%2C415%2C930%2C990%2C560%2C1030%2C464%2C934%2C382%2C1033%2C124%2C807%2C987%2C983%2C1013%2C1372%2C1035%2C984%2C1031%2C1034%2C1042%2C1043%2C331%2C1012%2C1011%2C1612%2C389%2C1395%2C1377%2C138%2C741%2C1038%2C423%2C1586%2C1588%2C1589%2C1587%2C1681%2C1657%2C1663%2C1670%2C1672%2C756%2C442%2C15%2C552%2C626%2C933%2C431%2C923%2C11%2C789%2C349%2C638%2C217%2C300%2C284%2C1425%2C618%2C275%2C783%2C6%2C37%2C141%2C576%2C1396%2C1378%2C730%2C916%2C509%2C180%2C248%2C363%2C1666%2C1699%2C1700%2C1698%22%2C%22start%22%3A%22'+dtm+'T00%3A00%3A00%2B03%3A00%22%2C%22duration%22%3A86400%2C%22channelProgramsLimit%22%3A500%2C%22genresIds%22%3A%5B%5D%2C%22lang%22%3A%22ru%22%7D&cacheKey=schedule%3Fparams%3D%7B%22channelLimit%22%3A4%2C%22channelOffset%22%3A17%2C%22fields%22%3A%5B%22channel%22%2C%22title%22%2C%22logo%22%2C%22channel%22%2C%22synonyms%22%2C%22favourite%22%2C%22id%22%2C%22siteUrl%22%2C%22broadcastUrl%22%2C%22onlinesPlayer%22%2C%22title%22%2C%22logo%22%2C%22sizes%22%2C%22width%22%2C%22height%22%2C%22src%22%2C%22copyright%22%2C%22schedules%22%2C%22channels%22%2C%22finish%22%2C%22channel%22%2C%22id%22%2C%22title%22%2C%22favourite%22%2C%22channelsCountPerGenre%22%2C%22availableProgramTypes%22%2C%22availableChannels%22%2C%22element%22%2C%22id%22%2C%22name%22%2C%22events%22%2C%22id%22%2C%22channelId%22%2C%22live%22%2C%22recommended%22%2C%22hasReminder%22%2C%22episode%22%2C%22seasonName%22%2C%22seasonNumber%22%2C%22id%22%2C%22programId%22%2C%22title%22%2C%22start%22%2C%22finish%22%2C%22program%22%2C%22id%22%2C%22type%22%2C%22id%22%2C%22name%22%2C%22title%22%2C%22sizes%22%2C%22copyright%22%2C%22100%22%2C%22120%22%2C%22160%22%2C%22200%22%2C%22300%22%2C%22400%22%2C%22width%22%2C%22height%22%2C%22src%22%5D%2C%22channelIds%22%3A%22146%2C109%2C1593%2C162%2C427%2C187%2C1683%2C740%2C1000%2C529%2C689%2C447%2C79%2C114%2C279%2C1003%2C405%2C726%2C350%2C897%2C150%2C1598%2C1649%2C898%2C323%2C1048%2C1624%2C1046%2C127%2C267%2C123%2C462%2C22%2C542%2C566%2C145%2C125%2C477%2C401%2C994%2C911%2C615%2C935%2C1371%2C1037%2C918%2C309%2C311%2C53%2C485%2C163%2C518%2C821%2C659%2C686%2C516%2C352%2C1570%2C12%2C644%2C608%2C798%2C834%2C1584%2C799%2C1674%2C1620%2C1680%2C55%2C675%2C794%2C520%2C648%2C731%2C333%2C774%2C723%2C367%2C322%2C928%2C35%2C273%2C1036%2C996%2C613%2C912%2C409%2C102%2C365%2C325%2C277%2C521%2C1394%2C1330%2C1436%2C765%2C757%2C223%2C769%2C685%2C1365%2C1562%2C16%2C669%2C1585%2C250%2C406%2C328%2C481%2C531%2C563%2C455%2C288%2C737%2C499%2C850%2C454%2C1039%2C664%2C1376%2C1667%2C1668%2C1669%2C567%2C410%2C308%2C929%2C555%2C747%2C601%2C917%2C31%2C494%2C810%2C66%2C1332%2C1578%2C76%2C828%2C743%2C502%2C278%2C831%2C384%2C214%2C921%2C313%2C1032%2C463%2C495%2C23%2C247%2C461%2C355%2C315%2C1331%2C589%2C59%2C922%2C575%2C715%2C797%2C319%2C804%2C533%2C642%2C591%2C91%2C332%2C849%2C388%2C258%2C927%2C270%2C430%2C473%2C681%2C151%2C1021%2C662%2C25%2C680%2C1561%2C156%2C491%2C257%2C1673%2C393%2C82%2C132%2C434%2C119%2C376%2C705%2C637%2C153%2C614%2C931%2C113%2C21%2C547%2C595%2C346%2C779%2C617%2C661%2C919%2C505%2C173%2C1571%2C776%2C425%2C1397%2C1660%2C1662%2C1679%2C1322%2C777%2C412%2C165%2C925%2C1026%2C1329%2C663%2C920%2C1676%2C312%2C631%2C801%2C121%2C415%2C930%2C990%2C560%2C1030%2C464%2C934%2C382%2C1033%2C124%2C807%2C987%2C983%2C1013%2C1372%2C1035%2C984%2C1031%2C1034%2C1042%2C1043%2C331%2C1012%2C1011%2C1612%2C389%2C1395%2C1377%2C138%2C741%2C1038%2C423%2C1586%2C1588%2C1589%2C1587%2C1681%2C1657%2C1663%2C1670%2C1672%2C756%2C442%2C15%2C552%2C626%2C933%2C431%2C923%2C11%2C789%2C349%2C638%2C217%2C300%2C284%2C1425%2C618%2C275%2C783%2C6%2C37%2C141%2C576%2C1396%2C1378%2C730%2C916%2C509%2C180%2C248%2C363%2C1666%2C1699%2C1700%2C1698%22%2C%22start%22%3A%22'+dtm+'T00%3A00%3A00%2B03%3A00%22%2C%22duration%22%3A86400%2C%22channelProgramsLimit%22%3A500%2C%22genresIds%22%3A%5B%5D%7D&userRegion=4&resource=schedule&ncrd='+ncrd
		
		#1469175651563
		try:E=getURL(url)
		except:
			try:E=getURL(url)
			except:
				print 'yatv сервер недоступен'
				return False
		e=E.replace('\\/','/').replace('false','False').replace('true','True').replace('\\"',"'")
		#debug (e)
		D=eval(e)
		L=D['schedules']
		#DCnl={}
		for i in L:
			title=i['channel']['title']
			id=i['channel']['id']
			idx=get_idx(title)
			
			if idx=="": 
				idx='ytv'+str(id)
				#print '"'+lower(title)+'":"'+str(id)+'",'
			Le=[]
			L2=i['events']
			for j in L2:
				ptitle=j['program']['title']
				start =j['start']
				
				cdata = time.strftime('%Y%m%d')
				pdata = start[:10].replace('-','')
				if pdata==cdata:
					start_at=start.replace('+03:00','').replace('T',' ')#2016-07-22T04:20:00+03:00
					Le.append({"name":ptitle, "start_at":start_at})
			E2=repr(Le)
			pDialog.update(int(n*100/31), message=title)
			if idx!="": add_to_db(idx, E2)
			#epg[idx]=Le

def upd_stv():
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
				if len(Le)>0:add_to_db(idx, repr(Le))


def upd_EPG_vsetv(pack):
	url = 'http://www.vsetv.com/schedule_package_'+pack+'_day.html'
	#url = 'http://www.vsetv.com/schedule_package_bybase_day.html'
	#url = 'http://www.vsetv.com/schedule_package_rubase_day.html'
	#url = 'http://www.vsetv.com/schedule_package_uabase_day.html'
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
			if idx=="": idx=get_idx(cnl_nm.replace(" Россия","").replace(" (Россия)","").replace(" (Международный)",""))
			
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


def upd_EPG_xmltv():
	xml=dload_epg_xml()
	if xml=="": xml=dload_epg_xml()
	if xml!="":
		d=pars_xmltv(xml)
		j=0
		dk=d.keys()
		for id in dk:
			j+=1
			#print d[id]
			add_to_db("x"+id, repr(d[id]))
			pDialog.update(j/4, message='xmltv '+id)
	else:
		pDialog.update(0, message='Не удалось загрузить xml.')


def dload_epg_xml():
	try:
			#target='http://programtv.ru/xmltv.xml.gz'
			target='http://api.torrent-tv.ru/ttv.xmltv.xml.gz'
			#print "-==-=-=-=-=-=-=- download =-=-=-=-=-=-=-=-=-=-"
			fp = xbmc.translatePath(os.path.join(addon.getAddonInfo('path'), 'tmp.zip'))
			
			req = urllib2.Request(url = target, data = None)
			req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)')
			resp = urllib2.urlopen(req)
			fl = open(fp, "wb")
			fl.write(resp.read())
			fl.close()
			#time.sleep(1)
			xbmc.sleep(1000)
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


def pars_xmltv(xml):
	#print "-==-=-=-=-=-=-=- parsing =-=-=-=-=-=-=-=-=-=-"
	#debug (xml)
	xml=xml.replace(chr(10),"").replace(chr(13),"").replace("<programme ", "\n<programme ")
	ss="<programme "
	es="</programme>"
	L=xml.splitlines()
	#L=mfindal(xml,ss,es)
	epg={}
	n=0
	t=len(L)
	cdata = time.strftime('%Y%m%d')
	for i in L:
		n+=1
		if "<programme " in i:
			#print "-==-=-=-=-=-=-=- parsing i =-=-=-=-=-=-=-=-=-=-"
			#debug i
			ss='start="'
			es=' +0300" stop="'
			st=mfindal(i,ss,es)[0][len(ss):]
			
			pdata=st[:8]
			#print pdata+' '+cdata
			if pdata==cdata:
				#ss='stop="'
				#es=' +0300" channel'
				#et=mfindal(i,ss,es)[0][len(ss):]
				
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
					#pDialog.update(int(n*100/t), message=title)
					#print id
				except:
					pass
				#print id+"  :  "+start_at+"  :  "+title
	return epg


def upd_EPG():
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
				get_epg(id, 'serv', name)
				pDialog.update(int(j*100/t), message=name+' ...')


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
	except:
			pass

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
	name=lower(name).replace(" #1","").replace(" #2","").replace(" #3","").replace(" #4","").replace(" #5","").replace(" #6","").replace(" #7","").replace(" #8","").replace(" #9","").replace(" #10","").replace(" #11","").replace(" #12","").replace(" #13","").replace(" #14","")
	try:
		id="x"+xmlid[name]
	except: 
		id=''
	return id


# ================================ server =====================================

while not xbmc.abortRequested:
		if start_trigger:
			#time.sleep(10)
			print('----- PTV Запущен -----')
			#xbmcgui.Dialog().notification('PTV', 'Запущен', icon, 1000, False)
			start_trigger = False
		# ---------------------------------
		try:udata = int(get_inf_db('udata'))
		except: udata = 0
		cdata = int(time.strftime('%Y%m%d'))
		#print('----- PTV ud:'+str(udata))
		#print('----- PTV сd:'+str(cdata))
		
		if cdata>udata and __settings__.getSetting("epgon")=='true': 
			add_to_db ("udata", str(cdata))
			print('----- PTV обновление -----')
			upepg()
			xbmc.executebuiltin("Container.Refresh")
		
		for i in range(0, 10):
			xbmc.sleep(3000)
			#time.sleep(3)
			if xbmc.abortRequested:
				print ('----- PTV break -----')
				break

print('----- PTV stopped -----')


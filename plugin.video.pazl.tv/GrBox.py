# -*- coding: utf-8 -*-
# Licence: GPL v.3 http://www.gnu.org/licenses/gpl.html

import sys, os, time
import xbmcaddon, xbmcgui, xbmc

_ADDON_NAME = 'plugin.video.pazl.tv'
_addon = xbmcaddon.Addon(id=_ADDON_NAME)
addon = xbmcaddon.Addon(id=_ADDON_NAME)
__settings__ = xbmcaddon.Addon(id=_ADDON_NAME)
handle = int(sys.argv[1])

_addon_path = _addon.getAddonInfo('path')
sys.path.append(os.path.join(_addon_path, 'lib'))
from xbmcwindow import *

images = os.path.join(_addon_path, 'images')
UserDir = xbmc.translatePath(os.path.join(xbmc.translatePath("special://masterprofile/"),"addon_data","plugin.video.pazl.tv"))
ld=os.listdir(os.path.join(addon.getAddonInfo('path'),"serv"))
Lserv=[]
for i in ld:
	if '.pyo' not in i: Lserv.append(i[:-3])

class MyVideoAddon(AddonDialogWindow):

    def __init__(self, title):
        AddonDialogWindow.__init__(self)#, "title")
        self.setGeometry(1200, 600)
        self.setGrid(13, 7)
        self.set_controls()
        self.set_navigation()

    def setImages(self):
        self.X_MARGIN = 5
        self.Y_MARGIN = 5
        self.Y_SHIFT = 4
        self.HEADER_HEIGHT = 35
#        self.main_bg_img = os.path.join(images, 'SKINDEFAULT.jpg')
        self.background_img = os.path.join(images, 'ContentPanel.png')
        self.title_background_img = os.path.join(images, 'dialogheader.png')
        self.list_bg_Nofocus = os.path.join(images, 'MenuItemNF.png')
        self.list_bg_focus = os.path.join(images, 'MenuItemFO.png')
        self.button_bg_Nofocus = os.path.join(images, 'KeyboardKeyNF.png')
        self.button_bg_focus = os.path.join(images, 'KeyboardKey.png')

    def set_controls(self):
        idw=__settings__.getSetting("idw")
        L=List_gr()
        # При первоначальном создании задаются фиктивные координаты и размеры: 1, 1, 1, 1.
        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, 'Управление каналами:', alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, -1, 0, 1, 7)
        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, 'Группы:', alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, 0, 0, 1, 2)
        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, 'Каналы:', alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, 0, 2, 1, 2)
        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, 'Порядок:', alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, 0, 4, 1, 2)
        # ControlButton
        self.button = xbmcgui.ControlButton(1, 1, 1, 1, u'ОК', focusTexture=self.button_bg_focus,
                                                        noFocusTexture=self.button_bg_Nofocus, alignment=ALIGN_CENTER)
        self.placeControl(self.button, 12, 6)
        
        self.button_addg = xbmcgui.ControlButton(1, 1, 1, 1, u'+', focusTexture=self.button_bg_focus,
                                                        noFocusTexture=self.button_bg_Nofocus, alignment=ALIGN_CENTER)
        self.placeControl(self.button_addg, 12, 0)
        
        self.button_remg = xbmcgui.ControlButton(1, 1, 1, 1, u'-', focusTexture=self.button_bg_focus,
                                                        noFocusTexture=self.button_bg_Nofocus, alignment=ALIGN_CENTER)
        self.placeControl(self.button_remg, 12, 1)
        
        # ControlList
        self.list = xbmcgui.ControlList(1, 1, 1, 1, buttonTexture=self.list_bg_Nofocus, buttonFocusTexture=self.list_bg_focus)
        self.placeControl(self.list, 1, 0, 11, 2)
        self.list.addItems(L)

        self.list2 = xbmcgui.ControlList(1, 1, 1, 1, buttonTexture=self.list_bg_Nofocus, buttonFocusTexture=self.list_bg_focus)
        self.placeControl(self.list2, 1, 2, 12, 2)
        self.list2.addItems(List_cn())

        self.list3 = xbmcgui.ControlList(1, 1, 1, 1, buttonTexture=self.list_bg_Nofocus, buttonFocusTexture=self.list_bg_focus)
        self.placeControl(self.list3, 1, 4, 12, 2)
        self.list3.addItems(get_gr())


    def set_navigation(self):
        self.button.controlUp(self.list)
        self.button.controlLeft(self.list3)
        self.list3.controlLeft(self.list2)
        self.list2.controlLeft(self.list)
        self.list.controlRight(self.list2)
        self.list2.controlRight(self.list3)
        self.list3.controlRight(self.button)
        self.button.controlDown(self.list3)
        self.list.controlDown(self.button_addg)
        self.button_addg.controlUp(self.list)
        self.button_remg.controlUp(self.list)
        self.button_addg.controlRight(self.button_remg)
        self.button_remg.controlLeft(self.button_addg)
        self.setFocus(self.list)

    def onControl(self, control):
        if control == self.button:
            self.close()
            #progress = xbmcgui.DialogProgress()
            #progress.create(u'Диалог хода выполнения:')
            #for i in range(0, 100, 5):
            #    progress.update(i)
            #    time.sleep(0.2)
        if control == self.button_addg:
            add_gr()
            i=self.list.getSelectedPosition()
            self.list.reset()
            self.list.addItems(List_gr())
            self.list.selectItem(i)
            
        if control == self.button_remg:
            rem_gr()
            __settings__.setSetting(id='edgrp', value=List_gr()[0])
            i=self.list.getSelectedPosition()
            
            self.list.reset()
            self.list.addItems(List_gr())
            self.list.selectItem(i)
            
            self.list2.reset()
            self.list2.addItems(List_cn())
            
            self.list3.reset()
            self.list3.addItems(get_gr())

        if control == self.list:
            #idw=__settings__.getSetting("idw")
            L=List_gr()
            i=self.list.getSelectedPosition()
            __settings__.setSetting(id='edgrp', value=L[i])
            #L2=[]
            #for j in L:
            #    if j==L[i]: L2.append(sel(L[i]))
            #    else: L2.append(j)

            self.list.reset()
            self.list.addItems(List_gr())
            self.list.selectItem(i)
            
            self.list2.reset()
            self.list2.addItems(List_cn())
            
            self.list3.reset()
            self.list3.addItems(get_gr())
            
        if control == self.list2:
            try:SG=__settings__.getSetting("edgrp")
            except:SG=''
            if SG!='':
                L=List_cn()
                i=self.list2.getSelectedPosition()
                id=L[i].replace("[COLOR FFFFFF00]","").replace("[/COLOR]","")
                Lc=get_gr()
                if id in Lc: rem(id)
                else:add(id, SG)
                
            self.list2.reset()
            self.list2.addItems(List_cn())
            self.list2.selectItem(i)
            
            self.list3.reset()
            self.list3.addItems(get_gr())
            
        if control == self.list3:
            m=['Переместить','Удалить','Отмена']
            #n=CL.index(name)
            sel = xbmcgui.Dialog()
            r = sel.select("", m)
            
            L=get_gr()
            i=self.list3.getSelectedPosition()
            name=L[i]
            if r==0:set_num_cn(name)
            elif r==1: rem(name)
            
            self.list3.reset()
            self.list3.addItems(get_gr())
            self.list3.selectItem(i)
            #print self.list.getSelectedPosition()#self.list.getListItem()
            #__settings__.setSetting(id=idw, value=repr(L2))

    def onAction(self, action):
        AddonFullWindow.onAction(self, action)

def sel(s):
        if s[:6] == "[COLOR":
            s=s[16:-8]
        else:
            s="[COLOR FFFFFF00]"+s+"[/COLOR]"
        return s
    

def unsel(L):
        s=repr(L)
        s=s.replace("[COLOR FFFFFF00]","").replace("[/COLOR]","")
        L=eval(s)
        return L


def run(id):
    __settings__.setSetting(id="idw", value=id)
    window = MyVideoAddon(id)
    window.doModal()
    del window


def List_gr():
	try:L=open_Groups()
	except:
		L=Ldf
		save_Groups(L)
	try:SG=__settings__.getSetting("edgrp")
	except:SG=''
	
	Lg=[]
	for i in L:
		if SG==i[0]: Lg.append(sel(i[0]))
		else: Lg.append(i[0])
		
	return Lg


def get_all_channeles():
	pDialog = xbmcgui.DialogProgressBG()
	L=[]
	for i in Lserv:
		serv_id=str(int(i[1:3]))
		if __settings__.getSetting("serv"+serv_id+"")=='true' :
			
			try: exec ("import Channels"+serv_id+"; Ls=Channels"+serv_id+".Channels")
			except:Ls=[]
			if Ls==[]: 
				pDialog.create('Пазл ТВ', 'Обновление списка каналов #'+serv_id+' ...')
				Ls=upd_canals_db(i)
				pDialog.close()
		else: Ls=[]
		L.extend(Ls)
	return L

def List_cn():
	L=get_all_channeles()
	Lg=get_gr()
	Lnm=[]
	for i in L:
				name  = i['title']
				url   = i['url']
				cover = i['img']

				if name not in Lnm:
					Lnm.append(name)
	Lnm.sort()
	Lc=[]
	for name in Lnm:
					if name in Lg: name=sel(name)
					Lc.append(name)
	return Lc


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

def open_Groups():
		fp=xbmc.translatePath(os.path.join(UserDir, 'UserGR.py'))
		fl = open(fp, "r")
		ls=fl.read().replace('\n','')#.replace('# -*- coding: utf-8 -*-Lgr=','')
		fl.close()
		return eval(ls)

def get_gr():
	try:SG1=__settings__.getSetting("edgrp")
	except:SG1=''
		
	try:
		L1=open_Groups()
		#print L
	except:L1=[]
	CL1=[]
	for i in L1:
		if i[0]==SG1: CL1=i[1]
	return CL1

def add(id, gr):
	try:L=open_Groups()
	except:L=Ldf
	r=0
	for i in L:
		if i[0]==gr:COG=L[r][1].append(id)
		r+=1
		
	save_Groups(L)

def rem(id):
	try:L=open_Groups()
	except:L=Ldf
	L2=[]
	for i in L:
			lj=[]
			for j in i[1]:
				if j!=id: 
					lj.append(j)
			L2.append([i[0],lj])
	save_Groups(L2)#__settings__.setSetting("Groups",repr(L2))
	__settings__.getSetting("edgrp")
	#xbmc.executebuiltin("Container.Refresh")

def set_num_cn(name):
	try:L1=open_Groups()
	except:
		L1=Ldf
		save_Groups(L1)

	try:SGc=__settings__.getSetting("edgrp")
	except:SGc=''
	
	if SGc!='':
		CLc=get_gr()
		#CL2=get_gr()
		#n=CL.index(name)
		sel = xbmcgui.Dialog()
		CLc.append(' - В конец списка - ')
		r = sel.select("Перед каналом:", CLc)
		CL2=CLc[:-1]
		print CL2
		if r>=0 :#and r<len(CL)
			CL2.remove(name)
			CL2.insert(r, name)
			k=0
			for i in L1:
				if i[0]==SGc:
					#L[k][1]=CL
					L1[k]=[SGc,CL2]
				k+=1
			save_Groups(L1)
			__settings__.getSetting("edgrp")
	#xbmc.sleep(300)
	#xbmc.executebuiltin("Container.Refresh")

def add_gr():
	name=inputbox('')
	try:L=open_Groups()
	except:L=Ldf
	st=(name,[])
	if st not in L:L.append(st)
	save_Groups(L)

def inputbox(t):
	skbd = xbmc.Keyboard(t, 'Название:')
	skbd.doModal()
	if skbd.isConfirmed():
		SearchStr = skbd.getText()
		return SearchStr
	else:
		return t

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


#if __name__ == '__main__':
#    main()
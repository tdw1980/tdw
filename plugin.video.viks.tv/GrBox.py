# -*- coding: utf-8 -*-
# Licence: GPL v.3 http://www.gnu.org/licenses/gpl.html

import sys, os, time
import xbmcaddon, xbmcgui, xbmc

_ADDON_NAME = 'plugin.video.viks.tv'
_addon = xbmcaddon.Addon(id=_ADDON_NAME)
__settings__ = xbmcaddon.Addon(id=_ADDON_NAME)
handle = int(sys.argv[1])

_addon_path = _addon.getAddonInfo('path')
sys.path.append(os.path.join(_addon_path, 'lib'))
from xbmcwindow import *

images = os.path.join(_addon_path, 'images')


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
##        self.main_bg_img = os.path.join(images, 'SKINDEFAULT.jpg')
        self.background_img = os.path.join(images, 'ContentPanel.png')
        self.title_background_img = os.path.join(images, 'dialogheader.png')
        self.list_bg_Nofocus = os.path.join(images, 'MenuItemNF.png')
        self.list_bg_focus = os.path.join(images, 'MenuItemFO.png')
        self.button_bg_Nofocus = os.path.join(images, 'KeyboardKeyNF.png')
        self.button_bg_focus = os.path.join(images, 'KeyboardKey.png')
        self.radio_focus = os.path.join(images, 'radiobutton-focus.png')
        self.radio_Nofocus = os.path.join(images, 'radiobutton-nofocus.png')
        self.check_focus = os.path.join(images, 'OverlayWatched.png')
        self.edit_focus = os.path.join(images, 'button-focus.png')
        self.slider_bg = os.path.join(images, 'osd_slider_bg_2.png')
        self.slider_nib = os.path.join(images, 'osd_slider_nib.png')
        self.slider_nib_nf = os.path.join(images, 'osd_slider_nibNF.png')

    def set_controls(self):
        idw=__settings__.getSetting("idw")
        L=List_gr()
        # Демонстрация основных контролов XBMC UI.
        # При первоначальном создании задаются фиктивные координаты и размеры: 1, 1, 1, 1.
        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, 'Управление каналами:', alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, -1, 0, 1, 7)
        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, 'Группы:', alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, 0, 0, 1, 2)
        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, 'Каналы:', alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, 0, 2, 1, 2)
        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, 'Порядок:', alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, 0, 4, 1, 2)
        #label_label = xbmcgui.ControlLabel(1, 1, 1, 1, 'ControlLabel')
        #self.placeControl(label_label, 1, 0)
        # ControlLabel
        #self.label = xbmcgui.ControlLabel(1, 1, 1, 1, u'Простая надпись')
        #self.placeControl(self.label, 1, 1)
        #fadelabel_label = xbmcgui.ControlLabel(1, 1, 1, 1, 'ControlFadeLabel')
        #self.placeControl(fadelabel_label, 2, 0)
        # ControlFadeLabel
        #self.fade_label = xbmcgui.ControlFadeLabel(1, 1, 1, 1)
        #self.placeControl(self.fade_label, 2, 1)
        # Дополнительные свойства определяем после (!!!) отображения контрола.
        #self.fade_label.addLabel(u'Здесь может быть очень длинная строка.')
        #textbox_label = xbmcgui.ControlLabel(1, 1, 1, 1, 'ControlTextBox')
        #self.placeControl(textbox_label, 3, 0)
        # ControlTextBox
        #self.textbox = xbmcgui.ControlTextBox(1, 1, 1, 1)
        #self.placeControl(self.textbox, 3, 1, 2, 1)
        #self.textbox.setText(u'Текстовое окно.\n'
        #                        u'Здесь может быть несколько строк.\n')
        #image_label = xbmcgui.ControlLabel(1, 1, 1, 1, 'ControlImage')
        #self.placeControl(image_label, 5, 0)
        # ControlImage
        #self.image = xbmcgui.ControlImage(1, 1, 1, 1, os.path.join(images, 'banner.jpg'))
        #self.placeControl(self.image, 5, 1)
        #no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, 'Интерактивные элементы', alignment=ALIGN_CENTER)
        #self.placeControl(no_int_label, 6, 0, 1, 2)
        #button_label = xbmcgui.ControlLabel(1, 1, 1, 1, 'ControlButton')
        #self.placeControl(button_label, 7, 0)
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
        
        #radiobutton_label = xbmcgui.ControlLabel(1, 1, 1, 1, 'ControlRadioButton')
        #self.placeControl(radiobutton_label, 8, 0)
        # ControlRadioButton
        #self.radiobutton = xbmcgui.ControlRadioButton(1, 1, 1, 1, u'Радиокнопка',
        #                                    focusTexture=self.list_bg_focus, noFocusTexture=self.list_bg_Nofocus,
        #                                    TextureRadioFocus=self.radio_focus, TextureRadioNoFocus=self.radio_Nofocus)
        #self.placeControl(self.radiobutton, 8, 1)
        #edit_label = xbmcgui.ControlLabel(1, 1, 1, 1, 'ControlEdit')
        #self.placeControl(edit_label, 9, 0)
        # ControlEdit
        #self.edit = xbmcgui.ControlEdit(1, 1, 1, 1, '',
        #                focusTexture=self.edit_focus, noFocusTexture=self.button_bg_Nofocus, _alignment=ALIGN_LEFT)
        #self.placeControl(self.edit, 9, 1)
        #self.edit.setText(u'Введите текст сюда')
        #list_label = xbmcgui.ControlLabel(1, 1, 1, 1, 'ControlList')
        #self.placeControl(list_label, 10, 0)
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

        #slider_label = xbmcgui.ControlLabel(1, 1, 1, 1, 'ControlSlider')
        #self.placeControl(slider_label, 13, 0)
        # ControlSlider
        #self.slider = xbmcgui.ControlSlider(1, 1, 1, 1 ,
        #                        textureback=self.slider_bg, texture=self.slider_nib_nf, texturefocus=self.slider_nib)
        #self.placeControl(self.slider, 13, 1)
        #self.slider.setPercent(25)

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
        #self.radiobutton.controlUp(self.button)
        #self.radiobutton.controlDown(self.edit)
        #self.edit.controlUp(self.radiobutton)
        #self.edit.controlDown(self.list)
        #self.list.controlUp(self.edit)
        #self.list.controlDown(self.button)
        #self.slider.controlUp(self.list)
        #self.slider.controlDown(self.button)
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
	try:L=eval(__settings__.getSetting("Groups"))
	except:
		L=Ldf
		__settings__.setSetting("Groups",repr(L))
	try:SG=__settings__.getSetting("edgrp")
	except:SG=''
	
	Lg=[]
	for i in L:
		if SG==i[0]: Lg.append(sel(i[0]))
		else: Lg.append(i[0])
		
	return Lg

def List_cn():
	
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
	Lc=[]
	Lnm=[]
	L1.extend(L2)
	L1.extend(L3)
	L=L1
	Lg=get_gr()
	for i in L:
				name  = i['title']
				url   = i['url']
				cover = i['img']

				if name not in Lnm:
					Lnm.append(name)
	Lnm.sort()
	for name in Lnm:
					if name in Lg: name=sel(name)
					Lc.append(name)
	
	#Lc.sort()
	return Lc


def get_gr():
	try:SG=__settings__.getSetting("edgrp")
	except:SG=''
		
	try:L=eval(__settings__.getSetting("Groups"))
	except:L=[]
	CL=[]
	for i in L:
		if i[0]==SG: CL=i[1]
	return CL

def add(id, gr):
	try:L=eval(__settings__.getSetting("Groups"))
	except:L=Ldf
	r=0
	for i in L:
		if i[0]==gr:COG=L[r][1].append(id)
		r+=1
		
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

def set_num_cn(name):
	try:L=eval(__settings__.getSetting("Groups"))
	except:
		L=Ldf
		__settings__.setSetting("Groups",repr(L))

	try:SG=__settings__.getSetting("edgrp")
	except:SG=''
	
	if SG!='':
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

def add_gr():
	name=inputbox('')
	try:L=eval(__settings__.getSetting("Groups"))
	except:L=Ldf
	st=(name,[])
	if st not in L:L.append(st)
	__settings__.setSetting("Groups",repr(L))

def inputbox(t):
	skbd = xbmc.Keyboard(t, 'Название:')
	skbd.doModal()
	if skbd.isConfirmed():
		SearchStr = skbd.getText()
		return SearchStr
	else:
		return t

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

#if __name__ == '__main__':
#    main()
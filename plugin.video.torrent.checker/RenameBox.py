# -*- coding: utf-8 -*-
# Licence: GPL v.3 http://www.gnu.org/licenses/gpl.html

import sys, os, time, urllib
import xbmcaddon, xbmcgui, xbmc

_ADDON_NAME = 'plugin.video.torrent.checker'
_addon = xbmcaddon.Addon(id=_ADDON_NAME)
_addon_path = _addon.getAddonInfo('path')#.decode(sys.getfilesystemencoding())
__settings__ = xbmcaddon.Addon(id='plugin.video.torrent.checker')

sys.path.append(os.path.join(_addon_path, 'lib'))
from xbmcwindow import *

images = os.path.join(_addon_path, 'images')

def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)


def inputbox(t):
	skbd = xbmc.Keyboard(t, 'Название:')
	skbd.doModal()
	if skbd.isConfirmed():
		SearchStr = skbd.getText()
		return SearchStr
	else:
		return t

def find_s(t):
    S=['s','S']
    n=["0","1","2","3","4","5","6","7","8","9"]
    for i in S:
        for j in n:
            for k in n:
                ss=i+j+k
                if t.find(ss)>0: return t.find(ss)+1
    return -1

def find_e(t):
    S=['e','E']
    n=["0","1","2","3","4","5","6","7","8","9"]
    for i in S:
        for j in n:
            for k in n:
                ss=i+j+k
                if t.find(ss)>0: return t.find(ss)+1
    return -1

class MyVideoAddon(AddonDialogWindow):

    def __init__(self, title):
        AddonDialogWindow.__init__(self)#, "title")
        self.setGeometry(800, 600)
        self.setGrid(13, 5)
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
        #__settings__.setSetting(id=idw, value=repr(L))
        print __settings__.getSetting(idw)
        
        
        try:
            L = eval(__settings__.getSetting(idw))
        except:
            L = []
            __settings__.setSetting(id=idw, value=repr(L))
        # Демонстрация основных контролов XBMC UI.
        # При первоначальном создании задаются фиктивные координаты и размеры: 1, 1, 1, 1.
        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, 'Переименование:', alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, 0, 0, 1, 5)
        
        no_int_label2 = xbmcgui.ControlLabel(1, 1, 1, 1, 'Предварительный просмотр:', alignment=ALIGN_CENTER)
        self.placeControl(no_int_label2, 4, 0, 1, 5)

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
        self.placeControl(self.button, 1, 4)

        self.button2 = xbmcgui.ControlButton(1, 1, 1, 1, u'Отмена', focusTexture=self.button_bg_focus,
                                                        noFocusTexture=self.button_bg_Nofocus, alignment=ALIGN_CENTER)
        self.placeControl(self.button2, 2, 4)

        #radiobutton_label = xbmcgui.ControlLabel(1, 1, 1, 1, 'ControlRadioButton')
        #self.placeControl(radiobutton_label, 8, 0)
        # ControlRadioButton
        #self.radiobutton = xbmcgui.ControlRadioButton(1, 1, 1, 1, u'Радиокнопка',
        #                                    focusTexture=self.list_bg_focus, noFocusTexture=self.list_bg_Nofocus,
        #                                    TextureRadioFocus=self.radio_focus, TextureRadioNoFocus=self.radio_Nofocus)
        #self.placeControl(self.radiobutton, 8, 1, 1, 5)
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
        sf=find_s(L[3][0])
        if sf>0:L[1]=[sf,sf+2]
        ef=find_e(L[3][0])
        if ef>0:L[2]=[ef,ef+2]
        __settings__.setSetting(id=idw, value=repr(L))
        
        self.list3 = xbmcgui.ControlList(1, 1, 1, 1, buttonTexture=self.list_bg_Nofocus, buttonFocusTexture=self.list_bg_focus)
        self.placeControl(self.list3, 1, 0, 12, 2)
        self.list3.addItems(['Название:','Сезон:','Эпизод:','NFO-файл:'])
        
        self.list = xbmcgui.ControlList(1, 1, 1, 1, buttonTexture=self.list_bg_Nofocus, buttonFocusTexture=self.list_bg_focus)
        self.placeControl(self.list, 1, 0, 12, 4)
        nm="                      "+L[0][1]
        sz="                      "+repr(L[1])+' '+L[3][0][L[1][0]:L[1][1]]
        ep="                      "+repr(L[2])+' '+L[3][0][L[2][0]:L[2][1]]
        self.list.addItems([nm,sz,ep,'                      Нет'])
        
        self.list2 = xbmcgui.ControlList(1, 1, 1, 1, buttonTexture=self.list_bg_Nofocus, buttonFocusTexture=self.list_bg_focus)
        self.placeControl(self.list2, 5, 0, 8, 5)
        self.list2.addItems(L[4])
        #slider_label = xbmcgui.ControlLabel(1, 1, 1, 1, 'ControlSlider')
        #self.placeControl(slider_label, 13, 0)
        # ControlSlider
        #self.slider = xbmcgui.ControlSlider(1, 1, 1, 1 ,
        #                        textureback=self.slider_bg, texture=self.slider_nib_nf, texturefocus=self.slider_nib)
        #self.placeControl(self.slider, 13, 1)
        #self.slider.setPercent(25)

    def set_navigation(self):
        self.button.controlUp(self.button2)
        self.button.controlDown(self.button2)
        self.button.controlLeft(self.list)
        self.list.controlRight(self.button)
        self.list.controlDown(self.list2)
        self.list2.controlUp(self.list)
        self.list2.controlRight(self.button)
        self.button2.controlUp(self.button)
        self.button2.controlDown(self.button)
        self.button2.controlLeft(self.list)
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
            idw=__settings__.getSetting("idw")
            L = eval(__settings__.getSetting(idw))
            Ls=[]
            Le=[]
            for i in L[3]:
                sz=i[L[1][0]:L[1][1]]
                ep=i[L[2][0]:L[2][1]]
                Ls.append(sz)
                Le.append(ep)

            name=urllib.quote_plus(L[0][1])
            url=urllib.quote_plus(L[6])
            L2=urllib.quote_plus(repr(L[4]))
            nf=urllib.quote_plus(str(L[5]))
            s=urllib.quote_plus(repr(Ls))
            e=urllib.quote_plus(repr(Le))
            
            xbmc.executebuiltin('Container.Update("plugin://plugin.video.torrent.checker/?mode=save_episodes_ext&name='+name+'&url='+url+'&L='+L2+'&s='+s+'&e='+e+'&nf='+nf+'")')
            time.sleep(1)
            self.close()
            #progress = xbmcgui.DialogProgress()
            #progress.create(u'Диалог хода выполнения:')
            #for i in range(0, 100, 5):
            #    progress.update(i)
            #    time.sleep(0.2)
        if control == self.button2:
            idw=__settings__.getSetting("idw")
            __settings__.setSetting(id=idw, value='[]')
            self.close()
            
        if control == self.list:
            idw=__settings__.getSetting("idw")
            L = eval(__settings__.getSetting(idw))
            i=self.list.getSelectedPosition()
            #itm=L[i]
            nf="                      Нет"
            if i==0:
                t=inputbox(L[0][1])
                
                L[0]=['t',t]
            elif i==1:
                sl = xbmcgui.Dialog()
                s=L[3][0]
                n = sl.select("Начало диапазона:", list(s))
                k = sl.select("Конец диапазона:", list(s))+1
                if k<n: k=n
                L[1]=[n,k]
            elif i==2:
                sl = xbmcgui.Dialog()
                s=L[3][0]
                n = sl.select("Начало диапазона:", list(s))
                k = sl.select("Конец диапазона:", list(s))+1
                if k<n: k=n
                L[2]=[n,k]
            elif i==3:
                f=L[5]
                if f == 0: 
                    L[5]=1
                    nf="                      Да"
                else:
                    L[5]=0
                    nf="                      Нет"
            nm="                     "+L[0][1]
            sz="                     "+repr(L[1])+' '+L[3][0][L[1][0]:L[1][1]]
            ep="                     "+repr(L[2])+' '+L[3][0][L[2][0]:L[2][1]]
            
            self.list.reset()
            self.list.addItems([nm,sz,ep,nf])
            self.list.selectItem(i)
            L2=[]
            for i in L[3]:
                L2.append(ru(L[0][1])+'.S'+i[L[1][0]:L[1][1]]+'.E'+i[L[2][0]:L[2][1]]+'.strm')
            L[4]=L2
            self.list2.reset()
            self.list2.addItems(L2)
            
            __settings__.setSetting(id=idw, value=repr(L))

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

#if __name__ == '__main__':
#    main()
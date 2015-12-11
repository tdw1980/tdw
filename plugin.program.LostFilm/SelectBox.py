# -*- coding: utf-8 -*-
# Licence: GPL v.3 http://www.gnu.org/licenses/gpl.html

import sys, os, time
import xbmcaddon, xbmcgui, xbmc

_ADDON_NAME = 'plugin.program.LostFilm'
_addon = xbmcaddon.Addon(id=_ADDON_NAME)
_addon_path = _addon.getAddonInfo('path').decode(sys.getfilesystemencoding())
__settings__ = xbmcaddon.Addon(id='plugin.video.LostFilm')

sys.path.append(os.path.join(_addon_path, 'lib'))
from xbmcwindow import *

def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)
	


images = os.path.join(_addon_path, 'images')
#images = "c:\\images"

class MyVideoAddon(AddonFullWindow):#AddonDialogWindow

    def __init__(self, title=''):
        AddonFullWindow.__init__(self)#, "title")
        self.setGeometry(1280, 720,0,0)
        self.setGrid(72-6, 128-2)
        self.set_controls()
        self.set_navigation()

    def setImages(self):
        self.X_MARGIN = 0
        self.Y_MARGIN = 0
        self.Y_SHIFT = 0
        self.X_SHIFT = 0
        self.HEADER_HEIGHT = 0
        self.main_bg_img = os.path.join(images, 'SKINDEFAULT.jpg')
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
        params=__settings__.getSetting("id_params")
        L=eval(params)
        #print L
        #type=__settings__.getSetting("id_type")
        funart=__settings__.getSetting("id_funart")
        cover=__settings__.getSetting("id_cover")
        
        name=L[0][0]
        cover=L[0][1]
        
        print (cover, name)
        
        idw="w1"#__settings__.getSetting("idw")
        #__settings__.setSetting(id=idw, value=repr(L))
        #try:L = eval(__settings__.getSetting(idw))
        #except:
        #    L = []
        #    __settings__.setSetting(id=idw, value=repr(L))
        
        # Демонстрация основных контролов XBMC UI.
        # При первоначальном создании задаются фиктивные координаты и размеры: 1, 1, 1, 1.
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
        
        self.image = xbmcgui.ControlImage(1, 1, 1, 1, os.path.join(images, 'SKINDEFAULT.jpg'))#os.path.join(images, 'banner.jpg')
        self.placeControl(self.image, -2, -2,72+2,128+2)

        #no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, 'Интерактивные элементы', alignment=ALIGN_CENTER)
        #self.placeControl(no_int_label, 6, 0, 1, 2)
        #button_label = xbmcgui.ControlLabel(1, 1, 1, 1, 'ControlButton')
        #self.placeControl(button_label, 7, 0)
        # ControlButton

        self.button11 = xbmcgui.ControlButton(1, 1, 1, 1, u'', focusTexture=self.button_bg_focus,
                                                        noFocusTexture=self.background_img, alignment=ALIGN_CENTER)
        self.placeControl(self.button11, 14, 1,13,41)

        self.button12 = xbmcgui.ControlButton(1, 1, 1, 1, u'', focusTexture=self.button_bg_focus,
                                                        noFocusTexture=self.background_img, alignment=ALIGN_CENTER)
        self.placeControl(self.button12, 14, 1+41+1,13,41)

        self.button13 = xbmcgui.ControlButton(1, 1, 1, 1, u'', focusTexture=self.button_bg_focus,
                                                        noFocusTexture=self.background_img, alignment=ALIGN_CENTER)
        self.placeControl(self.button13, 14, 1+41+1+41+1,13,41)


        self.button21 = xbmcgui.ControlButton(1, 1, 1, 1, u'', focusTexture=self.button_bg_focus,
                                                        noFocusTexture=self.background_img, alignment=ALIGN_CENTER)
        self.placeControl(self.button21, 14+14, 1,13,41)

        self.button22 = xbmcgui.ControlButton(1, 1, 1, 1, u'', focusTexture=self.button_bg_focus,
                                                        noFocusTexture=self.background_img, alignment=ALIGN_CENTER)
        self.placeControl(self.button22, 14+14, 1+41+1,13,41)

        self.button23 = xbmcgui.ControlButton(1, 1, 1, 1, u'', focusTexture=self.button_bg_focus,
                                                        noFocusTexture=self.background_img, alignment=ALIGN_CENTER)
        self.placeControl(self.button23, 14+14, 1+41+1+41+1,13,41)


        self.button31 = xbmcgui.ControlButton(1, 1, 1, 1, u'', focusTexture=self.button_bg_focus,
                                                        noFocusTexture=self.background_img, alignment=ALIGN_CENTER)
        self.placeControl(self.button31, 14+14+14, 1,13,41)

        self.button32 = xbmcgui.ControlButton(1, 1, 1, 1, u'', focusTexture=self.button_bg_focus,
                                                        noFocusTexture=self.background_img, alignment=ALIGN_CENTER)
        self.placeControl(self.button32, 14+14+14, 1+41+1,13,41)

        self.button33 = xbmcgui.ControlButton(1, 1, 1, 1, u'', focusTexture=self.button_bg_focus,
                                                        noFocusTexture=self.background_img, alignment=ALIGN_CENTER)
        self.placeControl(self.button33, 14+14+14, 1+41+1+41+1,13,41)


        self.button41 = xbmcgui.ControlButton(1, 1, 1, 1, u'', focusTexture=self.button_bg_focus,
                                                        noFocusTexture=self.background_img, alignment=ALIGN_CENTER)
        self.placeControl(self.button41, 14+14+14+14, 1,13,41)

        self.button42 = xbmcgui.ControlButton(1, 1, 1, 1, u'', focusTexture=self.button_bg_focus,
                                                        noFocusTexture=self.background_img, alignment=ALIGN_CENTER)
        self.placeControl(self.button42, 14+14+14+14, 1+41+1,13,41)

        self.button43 = xbmcgui.ControlButton(1, 1, 1, 1, u'', focusTexture=self.button_bg_focus,
                                                        noFocusTexture=self.background_img, alignment=ALIGN_CENTER)
        self.placeControl(self.button43, 14+14+14+14, 1+41+1+41+1,13,41)



        tb=15
        lr=2
        ind=0
        self.image11 = xbmcgui.ControlImage(1, 1, 1, 1, L[ind][1].replace('/posters/poster_','/icons/cat_'))#os.path.join(images, 'banner.jpg')
        self.placeControl(self.image11, tb, lr,11,13)

        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, "[B][COLOR FFFFFFFF]"+L[ind][3]+"[/COLOR][/B]", alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, tb+2, lr+13, 1, 26)
        
        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, L[ind][2], alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, tb+5, lr+13, 1, 26)
        
        n=L[ind][4].find("(")
        if L[ind][5]==0: ep=L[ind][4][:n]
        else: ep="[COLOR FFFFFF00]"+L[ind][4][:n]+"[/COLOR]"
        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, ep, alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, tb+8, lr+13, 1, 26)


        tb=15
        lr=2+42
        ind=1
        self.image11 = xbmcgui.ControlImage(1, 1, 1, 1, L[ind][1].replace('/posters/poster_','/icons/cat_'))#os.path.join(images, 'banner.jpg')
        self.placeControl(self.image11, tb, lr,11,13)

        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, "[B][COLOR FFFFFFFF]"+L[ind][3]+"[/COLOR][/B]", alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, tb+2, lr+13, 1, 26)

        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, L[ind][2], alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, tb+5, lr+13, 1, 26)
        n=L[ind][4].find("(")
        if L[ind][5]==0: ep=L[ind][4][:n]
        else: ep="[COLOR FFFFFF00]"+L[ind][4][:n]+"[/COLOR]"
        print L[ind][5]
        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, ep, alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, tb+8, lr+13, 1, 26)


        tb=15
        lr=2+42+42
        ind=2
        self.image11 = xbmcgui.ControlImage(1, 1, 1, 1, L[ind][1].replace('/posters/poster_','/icons/cat_'))#os.path.join(images, 'banner.jpg')
        self.placeControl(self.image11, tb, lr,11,13)

        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, "[B][COLOR FFFFFFFF]"+L[ind][3]+"[/COLOR][/B]", alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, tb+2, lr+13, 1, 26)

        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, L[ind][2], alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, tb+5, lr+13, 1, 26)
        n=L[ind][4].find("(")
        if L[ind][5]==0: ep=L[ind][4][:n]
        else: ep="[COLOR FFFFFF00]"+L[ind][4][:n]+"[/COLOR]"
        print L[ind][5]
        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, ep, alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, tb+8, lr+13, 1, 26)




        tb=15+14
        lr=2
        ind=3
        self.image11 = xbmcgui.ControlImage(1, 1, 1, 1, L[ind][1].replace('/posters/poster_','/icons/cat_'))#os.path.join(images, 'banner.jpg')
        self.placeControl(self.image11, tb, lr,11,13)

        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, "[B][COLOR FFFFFFFF]"+L[ind][3]+"[/COLOR][/B]", alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, tb+2, lr+13, 1, 26)
        
        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, L[ind][2], alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, tb+5, lr+13, 1, 26)
        
        n=L[ind][4].find("(")
        if L[ind][5]==0: ep=L[ind][4][:n]
        else: ep="[COLOR FFFFFF00]"+L[ind][4][:n]+"[/COLOR]"
        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, ep, alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, tb+8, lr+13, 1, 26)


        tb=15+14
        lr=2+42
        ind=4
        self.image11 = xbmcgui.ControlImage(1, 1, 1, 1, L[ind][1].replace('/posters/poster_','/icons/cat_'))#os.path.join(images, 'banner.jpg')
        self.placeControl(self.image11, tb, lr,11,13)

        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, "[B][COLOR FFFFFFFF]"+L[ind][3]+"[/COLOR][/B]", alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, tb+2, lr+13, 1, 26)

        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, L[ind][2], alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, tb+5, lr+13, 1, 26)
        n=L[ind][4].find("(")
        if L[ind][5]==0: ep=L[ind][4][:n]
        else: ep="[COLOR FFFFFF00]"+L[ind][4][:n]+"[/COLOR]"
        print L[ind][5]
        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, ep, alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, tb+8, lr+13, 1, 26)


        tb=15+14
        lr=2+42+42
        ind=5
        self.image11 = xbmcgui.ControlImage(1, 1, 1, 1, L[ind][1].replace('/posters/poster_','/icons/cat_'))#os.path.join(images, 'banner.jpg')
        self.placeControl(self.image11, tb, lr,11,13)

        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, "[B][COLOR FFFFFFFF]"+L[ind][3]+"[/COLOR][/B]", alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, tb+2, lr+13, 1, 26)

        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, L[ind][2], alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, tb+5, lr+13, 1, 26)
        n=L[ind][4].find("(")
        if L[ind][5]==0: ep=L[ind][4][:n]
        else: ep="[COLOR FFFFFF00]"+L[ind][4][:n]+"[/COLOR]"
        print L[ind][5]
        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, ep, alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, tb+8, lr+13, 1, 26)






        tb=15+14+14
        lr=2
        ind=6
        self.image11 = xbmcgui.ControlImage(1, 1, 1, 1, L[ind][1].replace('/posters/poster_','/icons/cat_'))#os.path.join(images, 'banner.jpg')
        self.placeControl(self.image11, tb, lr,11,13)

        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, "[B][COLOR FFFFFFFF]"+L[ind][3]+"[/COLOR][/B]", alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, tb+2, lr+13, 1, 26)
        
        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, L[ind][2], alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, tb+5, lr+13, 1, 26)
        
        n=L[ind][4].find("(")
        if L[ind][5]==0: ep=L[ind][4][:n]
        else: ep="[COLOR FFFFFF00]"+L[ind][4][:n]+"[/COLOR]"
        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, ep, alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, tb+8, lr+13, 1, 26)


        tb=15+14+14
        lr=2+42
        ind=7
        self.image11 = xbmcgui.ControlImage(1, 1, 1, 1, L[ind][1].replace('/posters/poster_','/icons/cat_'))#os.path.join(images, 'banner.jpg')
        self.placeControl(self.image11, tb, lr,11,13)

        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, "[B][COLOR FFFFFFFF]"+L[ind][3]+"[/COLOR][/B]", alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, tb+2, lr+13, 1, 26)

        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, L[ind][2], alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, tb+5, lr+13, 1, 26)
        n=L[ind][4].find("(")
        if L[ind][5]==0: ep=L[ind][4][:n]
        else: ep="[COLOR FFFFFF00]"+L[ind][4][:n]+"[/COLOR]"
        print L[ind][5]
        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, ep, alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, tb+8, lr+13, 1, 26)


        tb=15+14+14
        lr=2+42+42
        ind=8
        self.image11 = xbmcgui.ControlImage(1, 1, 1, 1, L[ind][1].replace('/posters/poster_','/icons/cat_'))#os.path.join(images, 'banner.jpg')
        self.placeControl(self.image11, tb, lr,11,13)

        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, "[B][COLOR FFFFFFFF]"+L[ind][3]+"[/COLOR][/B]", alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, tb+2, lr+13, 1, 26)

        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, L[ind][2], alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, tb+5, lr+13, 1, 26)
        n=L[ind][4].find("(")
        if L[ind][5]==0: ep=L[ind][4][:n]
        else: ep="[COLOR FFFFFF00]"+L[ind][4][:n]+"[/COLOR]"
        print L[ind][5]
        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, ep, alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, tb+8, lr+13, 1, 26)




        tb=15+14+14+14
        lr=2
        ind=9
        self.image11 = xbmcgui.ControlImage(1, 1, 1, 1, L[ind][1].replace('/posters/poster_','/icons/cat_'))#os.path.join(images, 'banner.jpg')
        self.placeControl(self.image11, tb, lr,11,13)

        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, "[B][COLOR FFFFFFFF]"+L[ind][3]+"[/COLOR][/B]", alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, tb+2, lr+13, 1, 26)
        
        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, L[ind][2], alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, tb+5, lr+13, 1, 26)
        
        n=L[ind][4].find("(")
        if L[ind][5]==0: ep=L[ind][4][:n]
        else: ep="[COLOR FFFFFF00]"+L[ind][4][:n]+"[/COLOR]"
        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, ep, alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, tb+8, lr+13, 1, 26)


        tb=15+14+14+14
        lr=2+42
        ind=10
        self.image11 = xbmcgui.ControlImage(1, 1, 1, 1, L[ind][1].replace('/posters/poster_','/icons/cat_'))#os.path.join(images, 'banner.jpg')
        self.placeControl(self.image11, tb, lr,11,13)

        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, "[B][COLOR FFFFFFFF]"+L[ind][3]+"[/COLOR][/B]", alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, tb+2, lr+13, 1, 26)

        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, L[ind][2], alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, tb+5, lr+13, 1, 26)
        n=L[ind][4].find("(")
        if L[ind][5]==0: ep=L[ind][4][:n]
        else: ep="[COLOR FFFFFF00]"+L[ind][4][:n]+"[/COLOR]"
        print L[ind][5]
        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, ep, alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, tb+8, lr+13, 1, 26)


        tb=15+14+14+14
        lr=2+42+42
        ind=11
        self.image11 = xbmcgui.ControlImage(1, 1, 1, 1, L[ind][1].replace('/posters/poster_','/icons/cat_'))#os.path.join(images, 'banner.jpg')
        self.placeControl(self.image11, tb, lr,11,13)

        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, "[B][COLOR FFFFFFFF]"+L[ind][3]+"[/COLOR][/B]", alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, tb+2, lr+13, 1, 26)

        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, L[ind][2], alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, tb+5, lr+13, 1, 26)
        n=L[ind][4].find("(")
        if L[ind][5]==0: ep=L[ind][4][:n]
        else: ep="[COLOR FFFFFF00]"+L[ind][4][:n]+"[/COLOR]"
        print L[ind][5]
        no_int_label = xbmcgui.ControlLabel(1, 1, 1, 1, ep, alignment=ALIGN_CENTER)
        self.placeControl(no_int_label, tb+8, lr+13, 1, 26)




        self.button = xbmcgui.ControlButton(1, 1, 1, 1, '', focusTexture=os.path.join(images, 'top-2.png'), noFocusTexture=os.path.join(images, 'top-1.png'), alignment=ALIGN_CENTER)
        self.placeControl(self.button, -2, -2,20,130)

        self.image2 = xbmcgui.ControlImage(1, 1, 1, 1, os.path.join(images, 'LF.png'))#os.path.join(images, 'banner.jpg')
        self.placeControl(self.image2, 0, 43,11,40)




        #self.textbox = xbmcgui.ControlTextBox(1, 1, 1, 1)
        #self.placeControl(self.textbox, 15+1+3+1, 2+13, 8, 26)
        #self.textbox.setText(L[1][4])

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
        
        #self.list = xbmcgui.ControlList(1, 1, 1, 1, buttonTexture=self.list_bg_Nofocus, buttonFocusTexture=self.list_bg_focus)
        #self.placeControl(self.list, 1, 0, 12, 4)
        #self.list.addItems(L)
        
        #slider_label = xbmcgui.ControlLabel(1, 1, 1, 1, 'ControlSlider')
        #self.placeControl(slider_label, 13, 0)
        # ControlSlider
        #self.slider = xbmcgui.ControlSlider(1, 1, 1, 1 ,
        #                        textureback=self.slider_bg, texture=self.slider_nib_nf, texturefocus=self.slider_nib)
        #self.placeControl(self.slider, 13, 1)
        #self.slider.setPercent(25)

    def set_navigation(self):
        self.button.controlDown(self.button12)
        
        self.button11.controlRight(self.button12)
        self.button12.controlRight(self.button13)
        self.button13.controlRight(self.button11)

        self.button21.controlRight(self.button22)
        self.button22.controlRight(self.button23)
        self.button23.controlRight(self.button21)

        self.button31.controlRight(self.button32)
        self.button32.controlRight(self.button33)
        self.button33.controlRight(self.button31)

        self.button41.controlRight(self.button42)
        self.button42.controlRight(self.button43)
        self.button43.controlRight(self.button41)



        self.button11.controlLeft(self.button13)
        self.button12.controlLeft(self.button11)
        self.button13.controlLeft(self.button12)

        self.button21.controlLeft(self.button23)
        self.button22.controlLeft(self.button21)
        self.button23.controlLeft(self.button22)

        self.button31.controlLeft(self.button33)
        self.button32.controlLeft(self.button31)
        self.button33.controlLeft(self.button32)

        self.button41.controlLeft(self.button43)
        self.button42.controlLeft(self.button41)
        self.button43.controlLeft(self.button42)



        self.button11.controlDown(self.button21)
        self.button21.controlDown(self.button31)
        self.button31.controlDown(self.button41)
        self.button41.controlDown(self.button11)

        self.button12.controlDown(self.button22)
        self.button22.controlDown(self.button32)
        self.button32.controlDown(self.button42)
        self.button42.controlDown(self.button12)

        self.button13.controlDown(self.button23)
        self.button23.controlDown(self.button33)
        self.button33.controlDown(self.button43)
        self.button43.controlDown(self.button13)



        self.button11.controlUp(self.button)
        self.button21.controlUp(self.button11)
        self.button31.controlUp(self.button21)
        self.button41.controlUp(self.button31)

        self.button12.controlUp(self.button)
        self.button22.controlUp(self.button12)
        self.button32.controlUp(self.button22)
        self.button42.controlUp(self.button32)

        self.button13.controlUp(self.button)
        self.button23.controlUp(self.button13)
        self.button33.controlUp(self.button23)
        self.button43.controlUp(self.button33)



        #self.list.controlRight(self.button)
        #self.button.controlDown(self.list)
        #self.radiobutton.controlUp(self.button)
        #self.radiobutton.controlDown(self.edit)
        #self.edit.controlUp(self.radiobutton)
        #self.edit.controlDown(self.list)
        #self.list.controlUp(self.edit)
        #self.list.controlDown(self.button)
        #self.slider.controlUp(self.list)
        #self.slider.controlDown(self.button)
        self.setFocus(self.button11)

    def onControl(self, control):
        import urllib
        L=eval(__settings__.getSetting("id_params"))
        idw='w1'
        LF=xt('plugin://plugin.video.LostFilm/?mode=OpenLF')
        if control == self.button:
            xbmc.executebuiltin("ActivateWindow(10025,"+LF+",return)")
        #    __settings__.setSetting(id=idw, value="cancel")
        #    self.close()
        if control == self.button11:xbmc.executebuiltin("ActivateWindow(10025,"+L[0][7]+",return)")
        if control == self.button12:xbmc.executebuiltin("ActivateWindow(10025,"+L[1][7]+",return)")
        if control == self.button13:xbmc.executebuiltin("ActivateWindow(10025,"+L[2][7]+",return)")
        if control == self.button21:xbmc.executebuiltin("ActivateWindow(10025,"+L[3][7]+",return)")
        if control == self.button22:xbmc.executebuiltin("ActivateWindow(10025,"+L[4][7]+",return)")
        if control == self.button23:xbmc.executebuiltin("ActivateWindow(10025,"+L[5][7]+",return)")
        if control == self.button31:xbmc.executebuiltin("ActivateWindow(10025,"+L[6][7]+",return)")
        if control == self.button31:xbmc.executebuiltin("ActivateWindow(10025,"+L[7][7]+",return)")
        if control == self.button33:xbmc.executebuiltin("ActivateWindow(10025,"+L[8][7]+",return)")
        if control == self.button41:xbmc.executebuiltin("ActivateWindow(10025,"+L[9][7]+",return)")
        if control == self.button42:xbmc.executebuiltin("ActivateWindow(10025,"+L[10][7]+",return)")
        if control == self.button43:xbmc.executebuiltin("ActivateWindow(10025,"+L[11][7]+",return)")

    def onAction(self, action):
        # Если нажали ESC или Backspace...
        if action == ACTION_NAV_BACK or action == ACTION_PREVIOUS_MENU:
            # ...закрываем плагин.
            self.close()

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
    __settings__.setSetting(id="idw", value=str(id))
    window = MyVideoAddon()
    window.doModal()
    del window

#if __name__ == '__main__':
#    main()
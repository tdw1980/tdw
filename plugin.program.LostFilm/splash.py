# -*- coding: utf-8 -*-
# Licence: GPL v.3 http://www.gnu.org/licenses/gpl.html

import sys, os, time
import xbmcaddon, xbmcgui, xbmc

_ADDON_NAME = 'plugin.video.LostFilm'
_addon = xbmcaddon.Addon(id=_ADDON_NAME)
_addon_path = _addon.getAddonInfo('path').decode(sys.getfilesystemencoding())
__settings__ = xbmcaddon.Addon(id='plugin.video.LostFilm')

sys.path.append(os.path.join(_addon_path, 'lib'))
#from xbmcwindow import *


images = os.path.join(_addon_path, 'images')
#images = "c:\\images"



# Text alighnment constants. Mixed variants are obtained by bit OR (|)
ALIGN_LEFT = 0
ALIGN_RIGHT = 1
ALIGN_CENTER_X = 2
ALIGN_CENTER_Y = 4
ALIGN_CENTER = 6
ALIGN_TRUNCATED = 8
ALIGN_JUSTIFY = 10

# XBMC key action codes.
# More codes at https://github.com/xbmc/xbmc/blob/master/xbmc/guilib/Key.h
ACTION_PREVIOUS_MENU = 10
ACTION_NAV_BACK = 92
ACTION_MOVE_LEFT = 1
ACTION_MOVE_RIGHT = 2
ACTION_MOVE_UP = 3
ACTION_MOVE_DOWN = 4
title=""

class VideoAddon(xbmcgui.Window):#AddonDialogWindow

    def __init__(self):
        #AddonDialogWindow.__init__(self)#, "title")
        #AddonFullWindow.__init__(self)
        self.setGeometry(1280, 720,0,0)
        self.setGrid(72-6, 128-2)
        self.setImages()
        self.set_controls()
        self.set_navigation()

    def setImages(self):
        """
        Set paths to images.

        The code below is the minimal example for implementation in a grand-child class.
        setImages method must have at least 2 image paths - self.background_img and self.title_background_img -
        and all geometry adjustment constants fully defined in a grand-child class.
        """
        # Window background image
        self.background_img = 'SKINDEFAULT.jpg'
        # Background for the window header
        self.title_background_img = 'dialogheader.png'
        # Horisontal adjustment for a header background if the main background has transparent edges.
        self.X_MARGIN = 5
        # Vertical adjustment for a header background if the main background has transparent edges
        self.Y_MARGIN = 5
        # Header position adjustment if the main backround has visible borders.
        self.Y_SHIFT = 4
        # The height of a window header (for the title background and the title label).
        self.HEADER_HEIGHT = 35
        raise NotImplementedError('setImages method must be fully implemented in a child class!')

    def setGeometry(self, width_, height_, pos_x=0, pos_y=0):
        self.title_bar = xbmcgui.ControlLabel(-10, -10, 1, 1, title, alignment=ALIGN_CENTER)
        self.X_MARGIN = 5
        # Vertical adjustment for a header background if the main background has transparent edges
        self.Y_MARGIN = 5
        # Header position adjustment if the main backround has visible borders.
        self.Y_SHIFT = 4
        # The height of a window header (for the title background and the title label).
        self.HEADER_HEIGHT = 35
        self.title_background_img = 'dialogheader.png'
        self.background_img = 'SKINDEFAULT.jpg'
        """
        Create a new window with given width and height, and set a backgroudnd and a title bar.
        x_, y_ - coordinates of the top level corner of the window.
        if x_=0, y_=0, the window will be placed at the center of the screen.
        """
        self.width = width_
        self.height = height_
        if pos_x and pos_y:
            self.x = pos_x
            self.y = pos_y
        else:
            self.x = 0 #- self.width/2
            self.y = 0 #- self.height/2
        self.background = xbmcgui.ControlImage(self.x, self.y, self.width, self.height, self.background_img)
        self.addControl(self.background)
        try:
            self.title_background = xbmcgui.ControlImage(self.x + self.X_MARGIN, self.y + self.Y_MARGIN + self.Y_SHIFT,
                                        self.width - 2 * self.X_MARGIN, self.HEADER_HEIGHT, self.title_background_img)
            self.addControl(self.title_background)
            self.title_bar.setPosition(self.x + self.X_MARGIN, self.y + self.Y_MARGIN + self.Y_SHIFT)
            self.title_bar.setWidth(self.width - 2 * self.X_MARGIN)
            self.title_bar.setHeight(self.HEADER_HEIGHT)
            self.addControl(self.title_bar)
        except NameError:
            raise NotImplementedError('setImages method must be fully implemented in a child class!')

    def setGrid(self, rows_, columns_, padding=10):
        """Set window grid layout of rows * columns."""
        self.rows = rows_
        self.columns = columns_
        self.grid_x = self.x + self.X_MARGIN + padding
        self.grid_y = self.y + self.Y_MARGIN + self.Y_SHIFT + self.HEADER_HEIGHT + padding
        self.tile_width = (self.width - 2 * (self.X_MARGIN + padding))/self.columns
        self.tile_height = (self.height - self.HEADER_HEIGHT - self.Y_SHIFT - 2 * (self.Y_MARGIN + padding))/self.rows

    def placeControl(self, control, row, column, rowspan=1, columnspan=1, padding=5):
        """Place control within the window grid layout."""
        control_x = (self.grid_x + self.tile_width * column) + padding
        control_y = (self.grid_y + self.tile_height * row) + padding
        control_width = self.tile_width * columnspan - 2 * padding
        control_height = self.tile_height * rowspan - 2 * padding
        control.setPosition(control_x, control_y)
        control.setWidth(control_width)
        control.setHeight(control_height)
        self.addControl(control)

    def getX(self):
        """Get X coordinate of the top-left corner of the window."""
        return self.x

    def getY(self):
        """Get Y coordinate of the top-left corner of the window."""
        return self.y

    def getWindowWidth(self):
        """Get window width."""
        return self.width

    def getWindowHeight(self):
        """Get window height."""
        return self.height



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
        
        #name=L[0][0]
        #cover=L[0][1]
                
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
        self.button.controlDown(self.button)
        
        #self.slider.controlDown(self.button)
        self.setFocus(self.button)

    def onControl(self, control):
        params=__settings__.getSetting("id_params")
        L=eval(params)

        idw='w1'
        if control == self.button:
            __settings__.setSetting(id=idw, value="cancel")
            self.close()
        if control == self.button:
            __settings__.setSetting(id=idw, value="0")
            #xbmc.executebuiltin("ActivateWindow(10025,'plugin://plugin.video.LostFilm/?mode=OpenRel&text=0&title=text&url="+L[0][6]+"',return)")
            #xbmc.executebuiltin("ActivateWindow(10001)")
            #xbmc.executebuiltin("Container.Update("+L[0][7]+","+L[0][7]+")")
            #xbmc.executebuiltin("xbmc.RunPlugin("+L[0][7]+")")
        time.sleep(3)
        self.close()
            #xbmc.executebuiltin("Container.Update()")
            #
            #    time.sleep(0.2)
            
        if control == "self.list":
            idw=__settings__.getSetting("idw")
            L = eval(__settings__.getSetting(idw))
            i=self.list.getSelectedPosition()
            #itm=L[i]
            if i==0: 
                L=unsel(L)
                La=L[:i]
                La.append(sel(L[i]))
                L2=La+L[i+1:]
            else:
                v=L[0].replace("[COLOR FFFFFF00]","").replace("[/COLOR]","")
                La=L[1:i]
                La.append(sel(L[i]))
                L2=[v]+La+L[i+1:]

            self.list.reset()
            self.list.addItems(L2)
            self.list.selectItem(i)
            #print self.list.getSelectedPosition()#self.list.getListItem()
            __settings__.setSetting(id=idw, value=repr(L2))

    def onAction(self, action):
        # Если нажали ESC или Backspace...
        if action == ACTION_NAV_BACK or action == ACTION_PREVIOUS_MENU:
            # ...закрываем плагин.
            self.close()

def run():
    window1 = VideoAddon()
    window1.doModal()
    del window1

#if __name__ == '__main__':
#    main()
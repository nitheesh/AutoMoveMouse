#!/usr/bin/env python
#

import pygtk
pygtk.require('2.0')
import gtk
import appindicator

class AppIndicatorMouse:
  def __init__(self):
    self.ind = appindicator.Indicator ("AutoMouseMove-Indicator", "indicator-messages", appindicator.CATEGORY_APPLICATION_STATUS)
    self.ind.set_status (appindicator.STATUS_ACTIVE)
    self.ind.set_attention_icon ("indicator-messages-new")
    self.ind.set_icon("distributor-logo")

    # create a menu
    self.menu = gtk.Menu()

    radio = gtk.RadioMenuItem(None, "Start")
    radio.connect("activate", self.start_btn_pressed)
    radio.show()
    self.menu.append(radio)

    radio1 = gtk.RadioMenuItem(radio, "Pause")
    radio1.connect("activate", self.pause_btn_pressed)
    radio1.show()
    self.menu.append(radio1)

    radio2 = gtk.RadioMenuItem(radio, "Stop")
    radio2.connect("activate", self.stop_btn_pressed)
    radio2.show()
    self.menu.append(radio2)

    image = gtk.ImageMenuItem(gtk.STOCK_QUIT)
    image.connect("activate", self.quit)
    image.show()
    self.menu.append(image)
                
    self.menu.show()

    self.ind.set_menu(self.menu)

  def quit(self, widget, data=None):
    gtk.main_quit()

  def start_btn_pressed(self, widget):
    self.ind.set_label("Running")
    print "Start clicked."

  def pause_btn_pressed(self, widget):
    self.ind.set_label("Paused")
    print "pause clicked."

  def stop_btn_pressed(self, widget):
    self.ind.set_label("Stopped")
    print "Stop clicked."


if __name__ == "__main__":
    indicator = AppIndicatorMouse()
    gtk.main()


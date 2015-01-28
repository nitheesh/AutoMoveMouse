#!/usr/bin/env python

import os
import pygtk
pygtk.require('2.0')
import gtk
import subprocess
import threading
import atexit
import appindicator

class AppIndicatorMouse:
  def __init__(self):
    self.ind = appindicator.Indicator ("AutoMouseMove-Indicator", "indicator-messages", appindicator.CATEGORY_APPLICATION_STATUS)
    self.ind.set_status (appindicator.STATUS_ACTIVE)
    self.ind.set_attention_icon ("indicator-messages-new")
    self.ind.set_icon("distributor-logo")

    thread = threading.Thread(target=self.StartBashScript)
    thread.daemon = True
    thread.start()

    # create a menu
    self.menu = gtk.Menu()

    _radio = gtk.RadioMenuItem(None, "Demo")

    radio = gtk.RadioMenuItem(_radio, "Start")
    radio.connect("activate", self.start_btn_pressed)
    radio.show()
    self.menu.append(radio)

    radio1 = gtk.RadioMenuItem(_radio, "Stop")
    radio1.connect("activate", self.stop_btn_pressed)
    radio1.show()
    self.menu.append(radio1)

    image = gtk.ImageMenuItem(gtk.STOCK_QUIT)
    image.connect("activate", self.quit)
    image.show()
    self.menu.append(image)
                
    self.menu.show()

    self.ind.set_menu(self.menu)

  def quit(self, widget, data=None):
    print thread
    atexit.register(thread.terminate)
    gtk.main_quit()

  def start_btn_pressed(self, widget):
    self.ind.set_label("Running")
    try:
      os.remove('/tmp/automove-stopped.do')
    except:
      print "Unable to remove file"  
    print "Start clicked."

  def stop_btn_pressed(self, widget):
    self.ind.set_label("Stopped")
    open('/tmp/automove-stopped.do', 'a').close()
    print "Stop clicked."

  def StartBashScript(self):
    self._bash = subprocess.Popen("./start-mouse.sh", shell=True)
    print self._bash.pid

if __name__ == "__main__":
    indicator = AppIndicatorMouse()
    gtk.main()


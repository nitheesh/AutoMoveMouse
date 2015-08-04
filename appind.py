#!/usr/bin/env python

import os
import os.path
import pygtk
pygtk.require('2.0')
import gtk
import time
import subprocess
import threading
import atexit
import commands
import appindicator
from Xlib import display

MaxIdle = 10
lockFile = "/tmp/automouse.lck"
appFile = "/tmp/appfile.lck"

# Touch the signal file on script startup
open(appFile, 'a').close()

class AppIndicatorMouse:
  def __init__(self):
    self.ind = appindicator.Indicator ("AutoMouseMove-Indicator", "indicator-messages", appindicator.CATEGORY_APPLICATION_STATUS)
    self.ind.set_status (appindicator.STATUS_ACTIVE)
    self.ind.set_attention_icon ("indicator-messages-new")
    self.ind.set_icon("distributor-logo")

    self.start = True
    self.timer = None
    self.timer_text = ""

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

    button = gtk.MenuItem(label="Timer")
    button.connect("activate", self.TimerpopUp)
    button.show()
    self.menu.append(button)

    image = gtk.ImageMenuItem(gtk.STOCK_QUIT)
    image.connect("activate", self.quit)
    image.show()
    self.menu.append(image)
                
    self.menu.show()

    self.ind.set_menu(self.menu)

    self.thread = threading.Thread(target=self.StartbashScript)
    self.thread.daemon = True      
    self.thread.start()
    # self.thread.join()

  def quit(self, widget, data=None):
    # print self.thread
    try:
      self._bash.kill()
    except:
      pass  
    gtk.main_quit()

  def start_btn_pressed(self, widget):
    print "Start button clicked."
    try:
      os.remove(appFile)
    except:
      print "Unable to remove appFile"  

  def stop_btn_pressed(self, widget):
    print "Stop clicked."
    open(appFile, 'a').close()
    # self.ind.set_label("Stopped")

  def StartbashScript(self):
    self._bash = None
    self.thread1 = None
    prev_pos = None
    count = 0
    # self.timer = 30
    while True:
      if self.timer is not None:
        count = count + 1
        if int(count) >= int(self.timer) and not os.path.isfile(lockFile):
          try:
            print "Timer reached"
            count = 0
            self.timer = None
            open(appFile, 'a').close()
          except:
            print "Timer encountered an error!!"
            pass
      else:
        count = 0  
      if os.path.isfile(appFile):
        print "App is on stop mode!!"
        time.sleep(1)
        continue
      else:
        if not os.path.isfile(lockFile):
          self._bash = None
          prev_pos = None
        idle = commands.getstatusoutput('expr $(xprintidle) / 1000')[1]
        if (int(idle) > MaxIdle):
          if self._bash is None:
            print "system goes idle..!"
            self.thread1 = threading.Thread(target=self.AutoMouseMove)
            self.thread1.daemon = True
            self.thread1.start()
            self.thread1.join()
        else:
          print str(idle) + str(" : system active")
          if self._bash is not None:
            # print("The mouse position on the screen is {0}".format(self.mousepos()))
            cur_pos = self.mousepos()
            print "Current postion" + str(cur_pos)
            if prev_pos is not None and cur_pos != prev_pos:
              subprocess.Popen("exec " + "xte 'keyup Control_L' && xte 'keyup Alt_L'", shell=True, stdout=subprocess.PIPE)
              print "System activated by user input"
              self._bash.terminate()
              self._bash = None
              print "Lock file removed!"
              os.remove(lockFile)
            prev_pos = cur_pos
      FirstRun = False  
      time.sleep(1)


  def mousepos(self):
    """mousepos() --> (x, y) get the mouse coordinates on the screen (linux, Xlib)."""
    data = display.Display().screen().root.query_pointer()._data
    return data["root_x"]

  def AutoMouseMove(self):
    open(lockFile, 'a').close()
    self._bash = subprocess.Popen("exec " + "./start-mouse.sh", shell=True, stdout=subprocess.PIPE)
    print self._bash.pid

  def TimerpopUp(self,btn):
    #base this on a message dialog
    dialog = gtk.MessageDialog(
        None,
        gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
        gtk.MESSAGE_QUESTION,
        gtk.BUTTONS_OK,
        None)
    dialog.set_markup('Please set the <b>timer</b>:')
    #create the text input field
    entry = gtk.Entry()
    entry.set_text(self.timer_text)
    #allow the user to press enter to do ok
    entry.connect("activate", self.responseToDialog, dialog, gtk.RESPONSE_OK)
    entry.connect('changed', self.on_changed)
    #create a horizontal box to pack the entry and a label
    hbox = gtk.HBox()
    hbox.pack_start(gtk.Label("Timer (min):"), False, 5, 5)
    hbox.pack_end(entry)
    #some secondary text
    # dialog.format_secondary_markup("This will be used for <i>identification</i> purposes")
    #add it and show it
    dialog.vbox.pack_end(hbox, True, True, 0)
    dialog.show_all()
    #go go go
    dialog.run()
    text = entry.get_text()
    dialog.destroy()
    if text == '':
      self.timer_text = ""
      self.timer = None
    else:  
      self.timer_text = text
      self.timer = int(text) * 60
    print self.timer_text
    print "Automation will be active for next " + str(self.timer_text) + str(" mins")

  def on_changed(self, entry):
    text = entry.get_text().strip()
    entry.set_text(''.join([i for i in text if i in '123456789']))

  def responseToDialog(entry, dialog, response):
    dialog.response(response)

if __name__ == "__main__":
  gtk.gdk.threads_init()
  # test = Test1()
  indicator = AppIndicatorMouse()
  gtk.main()
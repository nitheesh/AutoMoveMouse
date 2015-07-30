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
# Browsers = "Firefox | Google-chrome-stable | Google-chrome | Google-chrome-unstable | Google-chrome-beta"
# gedit = "Gedit"
# sublm = "Sublime_text"

class AppIndicatorMouse:
  def __init__(self):
    self.ind = appindicator.Indicator ("AutoMouseMove-Indicator", "indicator-messages", appindicator.CATEGORY_APPLICATION_STATUS)
    self.ind.set_status (appindicator.STATUS_ACTIVE)
    self.ind.set_attention_icon ("indicator-messages-new")
    self.ind.set_icon("distributor-logo")

    self.thread = threading.Thread(target=self.StartBashScript)
    self.thread.daemon = True

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
    # print self.thread
    self._bash.kill()
    gtk.main_quit()

  def start_btn_pressed(self, widget):
    # self.ind.set_label("Running")
    try:
      os.remove('/tmp/automove-stopped.do')
    except:
      print "Unable to remove file"  
    try:  
      self.thread.start()
      self.thread.join()
    except:
      print "thread RuntimeError!"  
    print "Start clicked."

  def stop_btn_pressed(self, widget):
    # self.ind.set_label("Stopped")
    open('/tmp/automove-stopped.do', 'a').close()
    print "Stop clicked."

  def StartBashScript(self):
    #stdout=subprocess.PIPE
    self._bash = subprocess.Popen("exec " + "./start-mouse.sh", shell=True)
    print self._bash.pid

class Test():
  def __init__(self):
    self._bash = None
    FirstRun = True
    while True:
      idle = commands.getstatusoutput('expr $(xprintidle) / 1000')[1]
      if self._bash is None:
        idle = idle
      elif (int(idle) == 0) and (not FirstRun) and (self._bash is not None):
        idle = None

      if not os.path.isfile(lockFile):
        self._bash = None
      print os.path.isfile(lockFile)
      print idle
      if (idle is not None) and (int(idle) > MaxIdle):
        if self._bash is not None:
          print "debug1"
          try:
            out, err = self._bash.communicate()
            print out
          except:
            pass
        elif not os.path.isfile(lockFile):
          print "debug2"
          print str(idle) + str(" : system goes idle")
          # self.AutoMouseMove()
          self.thread = threading.Thread(target=self.AutoMouseMove)
          self.thread.daemon = True
          self.thread.start()
          self.thread.join()
        else:
          print "debug3"  
      else:
        print str(idle) + str(" : system active")
      FirstRun = False
      time.sleep(1)

  def monitor(self):
    f = open(r'/dev/input/mice', 'r')
    line = f.readline()
    if line:
      print 'Mouse moved',
      self._bash.terminate()
      print "Releasing the lock file from python script.."
      try:
        os.remove(lockFile)
      except:
        pass  
    else:
      print "no movement...."


  def AutoMouseMove(self):
    open(lockFile, 'a').close()
    self._bash = subprocess.Popen("exec " + "./start-mouse.sh", shell=True, stdout=subprocess.PIPE)
    print self._bash.pid

class Test1():
  def __init__(self):
    self._bash = None
    self.thread = None
    print os.path.isfile(lockFile)
    prev_pos = None
    while True:
      if not os.path.isfile(lockFile):
        self._bash = None
        prev_pos = None
      # print "main func running"
      idle = commands.getstatusoutput('expr $(xprintidle) / 1000')[1]
      if (int(idle) > MaxIdle):
        if self._bash is None:
          print "system goes idle..!"
          self.thread = threading.Thread(target=self.AutoMouseMove)
          self.thread.daemon = True
          self.thread.start()
          self.thread.join()
      else:
        print str(idle) + str(" : system active")
        if self._bash is not None:
          # print("The mouse position on the screen is {0}".format(self.mousepos()))
          cur_pos = self.mousepos()
          print "Current postion" + str(cur_pos)
          if prev_pos is not None and cur_pos != prev_pos:
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

if __name__ == "__main__":
    # Test = Test1()
    indicator = AppIndicatorMouse()
    gtk.main()
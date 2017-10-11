import threading
from threading import Thread
from main import Main
from interface import Interface
from reading import *

if __name__ == '__main__':
  ##Thread(target = Main).start()
  Thread(target = Reading().isActive).start()
  Thread(target = Main).start()
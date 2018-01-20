
import sys
from PyQt4 import QtGui


class ShowWindows(QtGui.QWidget):
	
	def __init__(self):
		
		super(ShowWindows,self).__init__()
		self.initGUI()

	def initGUI(self):

		self.setGeometry(300, 200, 700, 500)
		self.setWindowTitle('Text')
		self.setWindowIcon(QtGui.QIcon('./chicken.png'))		
		self.show()

def main():

	app = QtGui.QApplication(sys.argv)
	Windows = ShowWindows()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
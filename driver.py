import sys
from PyQt5.QtWidgets import QWidget, QGridLayout, QLineEdit, QPushButton, QLabel, QListWidget, QListWidgetItem, \
    QApplication
from PyQt5 import QtGui


class fileHunterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWidgets()

    def setWidgets(self):
        layout = QGridLayout()
        self.setLayout(layout)
        self.setWindowTitle("FileHunter")

        # create widgets
        self.searchBox = QLineEdit("Enter a keyword")
        searchButton = QPushButton('Search')
        keywordLabel = QLabel("Keyword:")
        outputLabel = QLabel("Output:")
        self.listView = QListWidget()
        openButton = QPushButton("Open")
        exitButton = QPushButton("Exit")

        # set icons
        self.word_icon = QtGui.QIcon('word.png')
        self.ppt_icon = QtGui.QIcon('ppt.png')
        self.excel_icon = QtGui.QIcon('excel.png')
        self.txt_icon = QtGui.QIcon('txt.png')
        open_icon = QtGui.QIcon('open.png')
        search_icon = QtGui.QIcon('search.png')

        # edit widgets
        openButton.setIcon(open_icon)
        searchButton.setIcon(search_icon)
        self.searchBox.selectAll()  # highlights the default text

        # add widgets to layout
        layout.addWidget(keywordLabel, 0, 0)
        layout.addWidget(self.searchBox, 1, 0, 1, 5)  # searchBox at row1 col0, rowSpan = 1, colSpan = 5
        layout.addWidget(searchButton, 1, 5)
        layout.addWidget(outputLabel, 2, 0)
        layout.addWidget(self.listView, 3, 0, 1, 6)  # outputList at row3 col0, rowSpan = 1, colSpan = 6
        layout.addWidget(openButton, 6, 4)
        layout.addWidget(exitButton, 6, 5)

        self.show()

        # add clicked functions
        searchButton.clicked.connect(self.searchClicked)
        openButton.clicked.connect(self.openClicked)
        exitButton.clicked.connect(self.exitClicked)
        self.listView.itemClicked.connect(self.listClicked)

    # backend stuff here
    def searchClicked(self):  # put target string from text box into a variable to run search function
        message = self.searchBox.text()
        print(message)
        #  create test list items
        self.listView.clear() # clear the list when a new search is made
        for x in range(0, 2):
            item = QListWidgetItem(self.word_icon, ("A Test Word File " + str(x + 1)))
            self.listView.addItem(item)
            item = QListWidgetItem(self.ppt_icon, ("A Test PowerPoint File " + str(x + 1)))
            self.listView.addItem(item)
            item = QListWidgetItem(self.excel_icon, ("A Test Excel File " + str(x + 1)))
            self.listView.addItem(item)
            item = QListWidgetItem(self.txt_icon, ("A Test Text File " + str(x + 1)))
            self.listView.addItem(item)

    def openClicked(self):
        print("Open Button clicked")

    def listClicked(self, item):
        listText = item.text() # add open function code in here
        print(listText)

    def exitClicked(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = fileHunterWindow()
    sys.exit(app.exec_())

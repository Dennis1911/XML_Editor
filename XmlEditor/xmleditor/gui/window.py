import sys
from xmleditor.xml import XMLTree
from PyQt5 import QtWidgets, QtGui, QtCore

class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super(Window, self).__init__() 
        self.setGeometry(50, 50, 600, 680)
        self.setWindowTitle("XML_File Editor")
        self.setWindowIcon(QtGui.QIcon('sap.png'))

#schließen
        extractAction = QtWidgets.QAction("&Quit", self)
        extractAction.setShortcut("Ctrl+Q")
        extractAction.setStatusTip("Leave The App")
        extractAction.triggered.connect(self.close_application)

#speichern
        saveFile = QtWidgets.QAction("&Save it", self)
        saveFile.setShortcut("Ctrl+S")
        saveFile.setStatusTip("Save your File")
        saveFile.triggered.connect(self.file_save)

        self.editor()

#FileOpener
        openFile = QtWidgets.QAction('&Open File',self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open File')
        openFile.triggered.connect(self.file_open)
        
        self.statusBar()
#MenüBar        
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("&File")

        fileMenu.addAction(openFile)
        
        fileMenu.addAction(saveFile)
        fileMenu.addSeparator()
        fileMenu.addAction(extractAction)

        self.home()
        self.show()
        
    #Nachfrage ob ich schließen darf
    def file_open(self):
        name,typ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File",'',"*.xml")
        if name:           
            self.xtree = XMLTree(name)
            self.refresh_combobox()
            self.comboBox.setDisabled(False)
            self.Checkitem(index = 0)
    #Funktion der pre_save Taste
            
    def pre_save(self):
        text = self.textEdit.toPlainText()
        index = self.item_index
        self.xtree.edit_checkitem(index, text)
        
    #speicher Funktion
    def file_save(self):
        name, typ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File")
        if name:
            self.xtree.write(name)

    def closeEvent(self, event):
        event.ignore()
        self.close_application()

    
    def home(self):
        #popUp-Add Taste
        btn = QtWidgets.QPushButton("Add+", self)
        btn.clicked.connect(self.popupex)
        btn.move(410,50)

        #Save Checkitem Taste
        save_btn = QtWidgets.QPushButton("Pre-Save Changes", self)
        save_btn.clicked.connect(self.pre_save)
        save_btn.setGeometry(50, 620, 150, 35)

        #Delete Checkitem Taste
        delete_btn = QtWidgets.QPushButton("Delete Checkitem", self)
        delete_btn.clicked.connect(self.delete_checkitem)
        delete_btn.setGeometry(220, 620, 150, 35)

        #checkitem_list =[]

        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.setGeometry(50, 50, 350, 30)
        self.comboBox.activated.connect(self.Checkitem)
        self.comboBox.setDisabled(True)

        #PopUp 
    def add_funktion(self, desc_field, item_id_field):
        desc = desc_field.text()
        item_id = item_id_field.text()
        self.xtree.add_checkitem(desc, item_id)
        self.refresh_combobox()
        self.comboBox.setCurrentIndex(-1)
        
    def delete_checkitem(self):
        self.xtree.del_checkitem(self.item_index)
        self.refresh_combobox()
        self.Checkitem(index = 0)
        
    def refresh_combobox(self):
        self.comboBox.clear()
        for item in self.xtree.list_checkitems():
            self.comboBox.addItem(",".join([item.get("desc"), item.get("id")]))
               
        #----------------------------------------------
        
    def Checkitem(self, index):
        text = self.xtree.to_string(self.xtree.list_checkitems()[index])
        self.textEdit.setText(text)
        self.item_index = index 

    def editor(self):
        self.textEdit = QtWidgets.QTextEdit(self)
        #self.setCentralWidget(self.textEdit)
        self.textEdit.setGeometry(50, 100, 500, 500)
        self.textEdit.show()
        
    def close_application(self):
        #(Wirklich schließen, ja oder nein?
        choice = QtWidgets.QMessageBox.question(self, "Quit!",
                                                "Escape?",
                                                 QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if choice == QtWidgets.QMessageBox.Yes:
            print("Goodbye")
            sys.exit()
        else:
            pass
        #sys.exit()
    def popupex(self):
        #Pop Up Fenster
        window = QtWidgets.QDialog()
        window.setGeometry(0, 0, 500, 250)
        window.setWindowTitle("Checkitem hinzufügen!")
        window.setWindowIcon(QtGui.QIcon('sap.png'))
        #ID:/ Desc: beim Popup
        id_field = QtWidgets.QLabel("id:", window)
        id_field.setGeometry(20, 80, 100, 40)
        
        
        desc_field = QtWidgets.QLabel("desc:", window)
        desc_field.setGeometry(20, 20, 100, 40)
        
        #Einzeiliges Eingabefeld
        desc_input_field = QtWidgets.QLineEdit(window)
        desc_input_field.setGeometry(100, 20, 300, 40)

        id_input_field = QtWidgets.QLineEdit(window)
        id_input_field.setGeometry(100, 80, 300, 40)

        #Okay Taste(w/ Text in das eigentliche Feld und danach schließen)
        butn = QtWidgets.QPushButton("Okay", window)
        butn.clicked.connect(lambda i, desc_field=desc_input_field, id_field=id_input_field: self.add_funktion(desc_field, id_field))
        butn.clicked.connect(window.close)
        butn.move(250,150)

        #Schließen
        butncancel = QtWidgets.QPushButton("Cancel", window)
        butncancel.clicked.connect(window.close)
        butncancel.move(150,150)

        

        window.exec() #Fenster wird angezeigt

def run():

    app = QtWidgets.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run()


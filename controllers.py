from Template.GUI import *
from WebScraping import *
scrap_dict = {}
RestructuredData_dictionary = {}

cambridgedict_url = "https://dictionary.cambridge.org/dictionary/english/"
class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.pushButton_SearchWord.clicked.connect(self.onClicked_pushButton_SearchWord)
        self.ui.listWidget_DefinitionList.itemActivated.connect(self.updatefield)
        self.show()

    def onClicked_pushButton_SearchWord(self):
        #Need a exception, check if field empty
        wordsearch_link = cambridgedict_url + self.ui.lineEdit_SearchWord.text()
        global RestructuredData_dictionary 
        RestructuredData_dictionary = WordData_dict(wordsearch_link, scrap_dict)
        self.ui.listWidget_DefinitionList.clear()
        for singleData in RestructuredData_dictionary:
            self.ui.listWidget_DefinitionList.addItem(str(singleData) + "." + RestructuredData_dictionary[singleData]["Definition"])

    def updatefield(self):
        #Clear all items first
        self.ui.lineEdit_WordEdit.clear()
        self.ui.lineEdit_PartofSpeech.clear()
        self.ui.lineEdit_PhoneticSymbolUK.clear()
        self.ui.lineEdit_PhoneticSymbolUS.clear()
        self.ui.plainTextEdit_DefinitionSingle.clear()
        self.ui.plainTextEdit_example.clear()
        self.ui.plainTextEdit_synonym.clear()
        #Get number ID of definition
        item_Selected = self.ui.listWidget_DefinitionList.selectedItems()
        item_IDSelected = []
        for i in item_Selected:
            item_IDSelected.append(str(i.text()))
            item_IDSelected = item_IDSelected[0].split('.')
            item_IDSelected = str(item_IDSelected[0])
            print(str(item_IDSelected))
        #Input all fields to GUI
        self.ui.lineEdit_WordEdit.setText(RestructuredData_dictionary[int(item_IDSelected)]['Word'])
        self.ui.lineEdit_PartofSpeech.setText(RestructuredData_dictionary[int(item_IDSelected)]['PartsOfSpeech'])
        if "PhoneticSymbol_UK" in RestructuredData_dictionary[int(item_IDSelected)]:
            self.ui.lineEdit_PhoneticSymbolUK.setText(RestructuredData_dictionary[int(item_IDSelected)]["PhoneticSymbol_UK"])
        if "PhoneticSymbol_US" in RestructuredData_dictionary[int(item_IDSelected)]:
            self.ui.lineEdit_PhoneticSymbolUS.setText(RestructuredData_dictionary[int(item_IDSelected)]["PhoneticSymbol_US"])    
        self.ui.plainTextEdit_DefinitionSingle.setPlainText(RestructuredData_dictionary[int(item_IDSelected)]['Definition'])
        if "Example" in RestructuredData_dictionary[int(item_IDSelected)]:
            for Example_singleItem in RestructuredData_dictionary[int(item_IDSelected)]["Example"]:
                self.ui.plainTextEdit_example.appendPlainText(Example_singleItem) 
        if "Synonym" in RestructuredData_dictionary[int(item_IDSelected)]:
            self.ui.plainTextEdit_synonym.appendPlainText(RestructuredData_dictionary[int(item_IDSelected)]["Synonym"])
        Extraword_list = ""    
        if "Extra words" in RestructuredData_dictionary[int(item_IDSelected)]:
            for extraword_singleitem in RestructuredData_dictionary[int(item_IDSelected)]["Extra words"]:
                Extraword_list = Extraword_list + extraword_singleitem + " , "
        self.ui.plainTextEdit_synonym.appendPlainText(Extraword_list)    
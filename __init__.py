from controllers import *

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    # Dialog = QtWidgets.QDialog()
    w = MyWindow()
    w.show()
    # ui = Ui_Dialog()
    # ui.setupUi(Dialog)
    # Dialog.show()
    sys.exit(app.exec_())
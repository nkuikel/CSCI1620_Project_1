import sys
from PyQt6.QtWidgets import QApplication
from gui import BankApp

def main() -> None:
    '''This is the entry point for the account manager application. 
    It initializes the Qt application, displays the main window, and starts the event loop.'''
    app = QApplication(sys.argv)
    window = BankApp()
    window.show()
    sys.exit(app.exec())

#this block below runs the main function.
if __name__ == '__main__':
    main()
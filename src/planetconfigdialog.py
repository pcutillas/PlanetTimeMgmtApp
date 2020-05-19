from gui.ui_planetConfigDialog import Ui_Dialog
from PySide2.QtWidgets import QDialog, QMessageBox
from PySide2.QtGui import QPalette, QColor
from PySide2.QtCore import Qt


class PlanetConfigDialog(QDialog):

    def __init__(self, mainWindow):
        QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setModal(True)
        self.setWindowTitle("Planet Configuration")

        self.mainWindow = mainWindow
        self.initializeContent()

    def initializeContent(self):
        """
        Connects button signals and initializes spin boxes
        Fills in all the spin boxes with the current planets' enabled status and number of pieces
        NOT Static
        """
        for tabNum in range(1, 2):  # TODO: Change to 4 when done
            for planetNum in range(1, 6):
                planet = 'self.mainWindow.ui.pie' + str(planetNum) + 'series'
                spinBox = 'self.ui.planet' + str(planetNum) + 'Num'
                button = 'self.ui.planet' + str(planetNum) + 'Enable'
                if tabNum in (2, 3):
                    planet += '_' + str(tabNum)
                    spinBox += '_' + str(tabNum)
                    button += '_' + str(tabNum)

                codeList = [
                    button + '.toggled.connect(lambda checked, self=self: self.checkButton(checked, ' + button + ', ' + spinBox + '))',
                    spinBox + '.setMinimum(0)',
                    spinBox + '.setMaximum(500)',
                    'if ' + planet + '.enabled:',
                    '\tpieces = ' + planet + '.sum()',
                    '\t' + spinBox + '.setValue(pieces)',
                    '\t' + button + '.setChecked(True)'
                ]

                code = '\n'.join(codeList)
                exec(code)

    def checkButton(self, checked, button, spinBox):
        """
        If button is checked, turn green and enable spin box with minimum 1.
        else turn back to normal and disable spin box.
        """
        if checked:
            palette = QPalette()
            palette.setColor(QPalette.Button, Qt.darkGreen)
            palette.setColor(QPalette.ButtonText, Qt.white)
            button.setPalette(palette)
            spinBox.setPalette(palette)
            spinBox.setReadOnly(False)
            spinBox.setMinimum(1)
            button.setText('✓ Enabled')
        else:
            palette = QPalette()
            if self.mainWindow.theme is 0:
                palette.setColor(QPalette.Button, QColor(180, 180, 180))
                palette.setColor(QPalette.ButtonText, Qt.black)
            else:
                palette.setColor(QPalette.Button, QColor(53, 53, 53))
            button.setPalette(palette)
            spinBox.setPalette(palette)
            spinBox.setReadOnly(True)
            spinBox.setMinimum(0)
            button.setText('Enable')

    def accept(self):
        """
        Applies given information when the user clicks "OK"
        """
        warningShown = False

        for tabNum in range(1, 2):  # TODO: Change to 4 when done
            for planetNum in range(1, 6):
                planet = 'self.mainWindow.ui.pie' + str(planetNum) + 'series'
                spinBox = 'self.ui.planet' + str(planetNum) + 'Num'
                button = 'self.ui.planet' + str(planetNum) + 'Enable'
                if tabNum in (2, 3):
                    planet += '_' + str(tabNum)
                    spinBox += '_' + str(tabNum)
                    button += '_' + str(tabNum)

                exec('checked = ' + button + '.isChecked()', locals())
                exec('pE = ' + planet + '.enabled', locals())

                if locals()['checked']:
                    exec('pieces = ' + spinBox + '.value()', locals())
                    pcs = locals()['pieces']

                    exec('samePcNum = ' + planet + '.sum() == ' + str(pcs), locals())

                    if not locals()['pE']:
                        exec(planet + '.setEnabled(' + str(pcs) + ')')
                    elif not locals()['samePcNum']:
                        if not warningShown:
                            result = self.showChangeWarning()
                            warningShown = True
                            if result == QMessageBox.Cancel:
                                return

                        exec(planet + '.clear()')
                        exec(planet + '.setEnabled(' + str(pcs) + ')')
                    # Only other case is planet already being enabled with the same num of pcs, nothing to do.
                else:
                    if locals()['pE']:
                        if not warningShown:
                            result = self.showChangeWarning()
                            warningShown = True
                            if result == QMessageBox.Cancel:
                                return

                        toDelete = []
                        for wo in self.mainWindow.machines[tabNum-1].workOrders:
                            if wo.planetNum == planetNum:
                                toDelete.append(wo)
                        for wo in toDelete:
                            self.mainWindow.deleteWorkOrder(wo)
                        toDelete.clear()

                        exec(planet + '.setDisabled()')

        return QDialog.accept(self)

    def showChangeWarning(self):  # Could make this more user friendly, ie only clears when lowered or disabled
        title = "Warning"
        message = "Changing the number of pieces in a planet or disabling it will clear its work orders. Continue?"
        buttons = QMessageBox.Ok | QMessageBox.Cancel
        message = QMessageBox(QMessageBox.Warning, title, message, buttons=buttons, flags=Qt.Dialog)
        result = message.exec_()
        return result

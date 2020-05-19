from gui.ui_workOrderDialog import Ui_Dialog
from PySide2.QtWidgets import QDialog
from PySide2.QtGui import QPalette, QColor
import gui.ui_planetConfigDialog as planetCD


class WorkOrderDialog(QDialog):

    NUMBER_TRACKER = 1

    def __init__(self, mainWindow, workOrder, editing=False):
        QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setModal(True)  # Prevents other parts of main app from being interacted with
        self.setWindowTitle("Work Order Creation")

        palette = QPalette()
        palette.setColor(QPalette.WindowText, QColor(200, 0, 0))
        self.ui.errorSection.setPalette(palette)
        self.ui.errorSection.hide()

        self.ui.numPieces.setMinimum(1)
        self.ui.numPieces.setMaximum(500)
        self.ui.numPieces.editingFinished.connect(lambda: self.ui.yldBox.setMaximum(self.ui.numPieces.value()))

        self.ui.woNumber.setValue(WorkOrderDialog.NUMBER_TRACKER)
        self.ui.woNumber.setMinimum(WorkOrderDialog.NUMBER_TRACKER)
        self.ui.woNumber.setMaximum(500)

        self.ui.machineNum.addItems([
            'Machine 1', 'Machine 2', 'Machine 3'
        ])
        self.ui.planetNum.addItems([
            'Planet 1', 'Planet 2', 'Planet 3', 'Planet 4', 'Planet 5'
        ])

        self.workOrder = workOrder
        if workOrder.machineNum:
            self.ui.woNumber.setValue(int(workOrder.name[4:]))
            self.ui.numPieces.setValue(workOrder.pieces)
            self.ui.side.setCurrentText("Side " + str(workOrder.side))
            self.ui.machineNum.setCurrentText("Machine " + str(workOrder.machineNum))
            self.ui.planetNum.setCurrentText("Planet " + str(workOrder.planetNum))

        self.editing = editing
        if editing:
            self.ui.woNumber.setDisabled(True)
            self.ui.errorSection.setText("Warning: Editing Work Order #" + workOrder.name[4:])
            self.ui.errorSection.show()

        self.ui.yldBox.setMinimum(-1)
        self.ui.yldBox.setMaximum(self.ui.numPieces.value())
        self.ui.yldBox.setSpecialValueText("-")
        self.ui.yldBox.setValue(-1)

        self.ui.planetButton.clicked.connect(lambda: mainWindow.showPlanetConfigDialog())

        self.mainWindow = mainWindow

    def accept(self):
        """
        Executes before the "OK" functionality
        """
        wo = self.workOrder

        if not self.editing:
            errorList = []

            wos = [int(tmp.name[4:]) for machine in self.mainWindow.machines for tmp in machine.workOrders]
            if self.ui.woNumber.value() in wos:
                errorList.append('Work order with ID ' + str(self.ui.woNumber.value()) + ' already exists. ')
            else:
                if self.ui.woNumber.value() == WorkOrderDialog.NUMBER_TRACKER:
                    WorkOrderDialog.NUMBER_TRACKER += 1
                wo.name = "WO #" + str(self.ui.woNumber.value())

            if errorList:
                errors = "Please fix these errors:\n"
                errors += '\n'.join(errorList)
                self.ui.errorSection.setText(errors)
                self.ui.errorSection.show()
                return

            wo.pieces = self.ui.numPieces.value()
            wo.side = int(self.ui.side.currentText()[-1])
            wo.machineNum = int(self.ui.machineNum.currentText()[-1])
            wo.planetNum = int(self.ui.planetNum.currentText()[-1])
            if self.ui.yldBox.value() is not -1:
                wo.setYield(self.ui.yldBox.value())
        else:
            wo.pieces = self.ui.numPieces.value()
            wo.side = int(self.ui.side.currentText()[-1])
            wo.machineNum = int(self.ui.machineNum.currentText()[-1])
            wo.planetNum = int(self.ui.planetNum.currentText()[-1])
            if self.ui.yldBox.value() is not -1:
                wo.setYield(self.ui.yldBox.value())
            else:
                wo.yld = None
                wo.scrap = None

        return QDialog.accept(self)

from PySide2.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton, QDialog
from PySide2 import QtWidgets
from PySide2.QtGui import QColor, QPalette
from PySide2.QtCore import Qt, Signal, Slot, QTime
import src.workorder as wo
import src.workorderdialog as wod


class TableView(QTableWidget):

    fullRowSelected = Signal(wo.WorkOrder)

    def __init__(self, headers: list, window, *args):
        """
        Initializes table view with horizontal headers and no data
        """
        QTableWidget.__init__(self, *args)
        self.hHeaders = headers
        self.vHeaders = []
        self.window = window
        self.setHorizontalHeaderLabels(headers)
        self.firstInit = True
        self.disabledColumns = [2, 3, 4, 5, 6, 9]
        self.setEditTriggers(QTableWidget.NoEditTriggers)

        # Initialize mapping
        self.rowNumToWOMapping = {}

        # Connect cell selection signal
        self.cellClicked.connect(window.ensureSingleWorkOrder_r)

        # Set headers to split space well
        self.setHSpacing()

    def setColorToRow(self, rowIndex, color):
        """
        Sets color for a single row.
        """
        palette = QPalette()
        palette.setColor(QPalette.Button, color.darker(f=110))

        for j in range(self.columnCount()):
            try:
                wg = self.cellWidget(rowIndex, j)
                if wg:
                    wg.setPalette(palette)
                else:
                    self.item(rowIndex, j).setBackground(color)
            except:
                pass

    def setBG(self):
        """
        Sets table background to have alternating dark/lighter colors
        """
        if self.window.theme is 0:
            color1 = QColor(180, 180, 180)
            color2 = QColor(150, 150, 150)
        else:
            color1 = QColor(80, 80, 80)
            color2 = QColor(60, 60, 60)

        for i in range(self.rowCount()):
            if i % 2 is 0:
                self.setColorToRow(i, color1)
            else:
                self.setColorToRow(i, color2)

    def addRowFor(self, workOrder: 'WorkOrder'):
        """
        Adds row to results section for workOrder given. Then, associates row number to workOrder using mapping.
        Some data is calculated and filled in.
        """
        # Gets rid of weird graphics
        if self.firstInit:
            self.setHSpacing()
            self.firstInit = False

        self.vHeaders.append(workOrder.name)

        self.setRowCount(len(self.vHeaders))
        rowPos = self.rowCount() - 1
        self.insertRow(rowPos)
        workOrder.rowNum = rowPos
        self.rowNumToWOMapping[rowPos] = workOrder

        self.setVerticalHeaderLabels(self.vHeaders)

        for j in range(0, len(self.hHeaders)):

            if j is 0:  # Machine Number
                newItem = QTableWidgetItem("Machine " + str(workOrder.machineNum))
                newItem.setTextAlignment(Qt.AlignCenter)
                self.setItem(rowPos, j, newItem)

            elif j is 1:  # Planet Number
                newItem = QTableWidgetItem("Planet " + str(workOrder.planetNum))
                newItem.setTextAlignment(Qt.AlignCenter)
                self.setItem(rowPos, j, newItem)

            elif j is 2:  # Labor Hrs
                newItem = QTableWidgetItem(self.getLaborHrs(workOrder))
                newItem.setTextAlignment(Qt.AlignCenter)
                self.setItem(rowPos, j, newItem)

            elif j is 3:  # Machine Time
                newItem = QTableWidgetItem(self.getMachineTime(workOrder))
                newItem.setTextAlignment(Qt.AlignCenter)
                self.setItem(rowPos, j, newItem)

            elif j is 4:  # Setup Run
                newItem = QTableWidgetItem(self.getSetupRunTime(workOrder))
                newItem.setTextAlignment(Qt.AlignCenter)
                self.setItem(rowPos, j, newItem)

            elif j is 5:  # Test Run
                newItem = QTableWidgetItem(self.getTestRunTime(workOrder))
                newItem.setTextAlignment(Qt.AlignCenter)
                self.setItem(rowPos, j, newItem)

            elif j is 6:  # Coating Run
                newItem = QTableWidgetItem(self.getCoatingRunTime(workOrder))
                newItem.setTextAlignment(Qt.AlignCenter)
                self.setItem(rowPos, j, newItem)

            elif j is 7:  # Quantity
                newItem = QTableWidgetItem(str(workOrder.pieces) + " pieces")
                newItem.setTextAlignment(Qt.AlignCenter)
                self.setItem(rowPos, j, newItem)

            elif j is 8:  # Yield
                if workOrder.yld:
                    newItem = QTableWidgetItem(str(workOrder.yld) + ' pieces')
                else:
                    newItem = QTableWidgetItem('Not given')
                newItem.setTextAlignment(Qt.AlignCenter)
                self.setItem(rowPos, j, newItem)

            elif j is 9:  # Scrap
                if workOrder.scrap:
                    newItem = QTableWidgetItem(str(workOrder.scrap) + ' pieces')
                else:
                    newItem = QTableWidgetItem('Not given')
                newItem.setTextAlignment(Qt.AlignCenter)
                self.setItem(rowPos, j, newItem)

            elif j is 10:
                newItem = QPushButton()
                newItem.setText("...")
                newItem.clicked.connect(lambda: self.openEditWODialog(workOrder))
                self.setCellWidget(rowPos, j, newItem)
                self.updateButtons()

        self.window.updateResults(self.window.machines[workOrder.machineNum-1])
        self.removeRow(self.rowCount()-1)
        self.setBG()

    def updateButtons(self):
        """
        Fixes bug due to scrollbar appearing/disappearing
        """
        if self.rowCount() > 8:
            for rowNum in range(1, self.rowCount()):
                self.cellWidget(rowNum-1, 10).setFixedWidth(43)
        else:
            for rowNum in range(1, self.rowCount()):
                print(rowNum)
                self.cellWidget(rowNum-1, 10).setFixedWidth(69)  # ayyyy lmao. not intentional, actually the best value

    def openEditWODialog(self, workOrder):
        """
        Allows a user to edit a work order. Also, selects the relevant slice in the GUI
        """
        self.window.ensureSingleWorkOrder_r(workOrder.rowNum, 0)

        woDialog = wod.WorkOrderDialog(self.window, workOrder, editing=True)
        result = woDialog.exec_()

        if result == QDialog.Rejected:
            return
        else:
            self.window.updateWorkOrder(workOrder)

    def updateRowInfo(self, workOrder):
        """
        Updates the information in the workOrder's associated row.
        """
        rowPos = workOrder.rowNum
        for j in range(0, len(self.hHeaders)):

            if j is 0:  # Machine Number
                self.item(rowPos, j).setText("Machine " + str(workOrder.machineNum))

            elif j is 1:  # Planet Number
                self.item(rowPos, j).setText("Planet " + str(workOrder.planetNum))

            elif j is 2:  # Labor Hrs
                self.item(rowPos, j).setText(self.getLaborHrs(workOrder))

            elif j is 3:  # Machine Time
                self.item(rowPos, j).setText(self.getMachineTime(workOrder))

            elif j is 4:  # Setup Run
                self.item(rowPos, j).setText(self.getSetupRunTime(workOrder))

            elif j is 5:  # Test Run
                self.item(rowPos, j).setText(self.getTestRunTime(workOrder))

            elif j is 6:  # Coating Run
                self.item(rowPos, j).setText(self.getCoatingRunTime(workOrder))

            elif j is 7:  # Quantity
                self.item(rowPos, j).setText(str(workOrder.pieces) + " pieces")

            elif j is 8:  # Yield
                if workOrder.yld:
                    self.item(rowPos, j).setText(str(workOrder.yld) + ' pieces')
                else:
                    self.item(rowPos, j).setText('Not given')

            elif j is 9:  # Scrap
                if workOrder.scrap:
                    self.item(rowPos, j).setText(str(workOrder.scrap) + ' pieces')
                else:
                    self.item(rowPos, j).setText('Not given')

    def getLaborHrs(self, workOrder):
        """
        Calculates the labor hours for the workOrder and returns it as a string. If none, returns placeholder text.
        """
        return 'Waiting...'

    def getMachineTime(self, workOrder):
        """
        Calculates the machine time for the workOrder and returns it as a string. If none, returns placeholder text.
        """
        machine = self.window.machines[workOrder.machineNum-1]
        if machine.startTime and machine.endTime:
            try:
                totPcs = 0
                for tmpWO in machine.workOrders:
                    totPcs += tmpWO.pieces

                totTime = QTime().fromString(machine.startTime).secsTo(QTime().fromString(machine.endTime)) / 3600
                time = totTime * workOrder.pieces / totPcs

                return '{:.3f} hours'.format(time)
            except:
                return 'Not set...'
        else:
            return 'Not set...'

    def getSetupRunTime(self, workOrder):
        """
        Calculates the setup run time for the workOrder and returns it as a string. If none, returns placeholder text.
        """
        return 'Not set...'

    def getTestRunTime(self, workOrder):
        """
        Calculates the test run time for the workOrder and returns it as a string. If none, returns placeholder text.
        """
        return 'Not set...'

    def getCoatingRunTime(self, workOrder):
        """
        Calculates the coating run time for the workOrder and returns it as a string. If none, returns placeholder text.
        """
        return 'Not set...'

    def setHSpacing(self):
        """
        Ensures that all horizontal headers will share space evenly
        """
        header = self.horizontalHeader()  # TODO: Setup better spacing
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Interactive)  # Machine
        header.resizeSection(0, 95)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Interactive)  # Planet
        header.resizeSection(1, 95)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Interactive)  # Labor
        header.resizeSection(2, 95)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Interactive)  # Machine time
        header.resizeSection(3, 150)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Interactive)  # setup
        header.resizeSection(4, 118)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.Interactive)  # test run
        header.resizeSection(5, 118)
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.Interactive)  # coating
        header.resizeSection(6, 118)
        header.setSectionResizeMode(7, QtWidgets.QHeaderView.Interactive)  # qty
        header.resizeSection(7, 118)
        header.setSectionResizeMode(8, QtWidgets.QHeaderView.Interactive)  # yield
        header.resizeSection(8, 118)
        header.setSectionResizeMode(9, QtWidgets.QHeaderView.Interactive)  # scrap
        header.resizeSection(9, 117)
        header.setSectionResizeMode(10, QtWidgets.QHeaderView.Interactive)  # buttons
        header.resizeSection(10, 5)
        header.setStretchLastSection(True)

    def updateRowsFrom(self, row: int):
        """
        Gets workorders for row "row" onwards, and updates them with their new row number. updates mapping too.
        """

        if row <= self.rowCount():
            oldWo = self.rowNumToWOMapping[row]

            for newRow in range(row, self.rowCount()):
                wo = self.rowNumToWOMapping[newRow+1]
                self.rowNumToWOMapping[newRow] = wo
                wo.rowNum = newRow

            self.rowNumToWOMapping.pop(self.rowCount())
            self.vHeaders.pop(self.vHeaders.index(oldWo.name))
            self.updateButtons()

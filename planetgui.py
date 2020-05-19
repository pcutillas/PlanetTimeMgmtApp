# ---- NOTE: Keep "unused" imports: they are used by custom code that is only seen as a string. ---- #

# From installed packages
from PySide2.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QFileDialog, QMessageBox, QDialog
from PySide2.QtGui import QPalette, QColor, Qt, QPainter
from PySide2.QtCore import Slot, QTime, Signal
from PySide2.QtCharts import QtCharts
from collections import OrderedDict
from random import randrange
import pickle
import sys, os

# From local project
from src.planetconfigdialog import PlanetConfigDialog
from src.workorderdialog import WorkOrderDialog
from gui.ui_mainwindow import Ui_MainWindow
from src.workorder import WorkOrder
from src.tableview import TableView
from src.machine import Machine
from src.planet import Planet

# ---- NOTE: Keep "unused" imports: they are used by custom code that is only seen as a string. ---- #


class MainWindow(QMainWindow):

    themeChanged = Signal(int)

    def __init__(self):

        # Initializing window and UI
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Time Calculation App")

        # Initializing layout for custom titlebar
        # self.layout = QVBoxLayout()
        # self.layout.addWidget(MyBar(self))
        # self.setLayout(self.layout)
        # self.layout.setContentsMargins(0, 0, 0, 0)
        # self.layout.addStretch(-1)
        # self.setMinimumSize(800, 400)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        # self.pressing = False

        # Initializing Results Section
        headers = ['Machine', 'Planet', 'Labor (Hrs)', 'Machine Time (Hrs)', 'Setup (Hrs)', 'Test Run (Hrs)',
                   'Coating (Hrs)', 'Quantity', 'Yield', 'Scrap', '']
        self.results = TableView(headers, self, 0, len(headers))
        self.results.setParent(self.ui.resultsContainer)
        # self.results.setFixedWidth(1265)
        self.results.setFixedWidth(self.ui.resultsContainer.width())
        self.results.setFixedHeight(self.ui.resultsContainer.height())

        # Initialize variables needed
        self.machines = [Machine(), Machine(), Machine()]  # TODO: restructure to have planets w workorders in machines
        self.techID = None
        self.theme = 0

        # Initialize pie chart widgets
        self.initPieCharts()

        # Connect Signals and Slots
        self.ui.addWorkOrderButton.clicked.connect(lambda: self.showWOInitDialog())
        self.ui.planetConfigButton.clicked.connect(lambda: self.showPlanetConfigDialog())
        self.ui.randomButton.clicked.connect(lambda: self.loadRandomWorkOrders())
        self.ui.clearButton.clicked.connect(lambda: self.reInit())
        self.ui.themeButton.clicked.connect(lambda: self.toggleTheme())
        self.themeChanged.connect(lambda: self.results.setBG())
        self.ui.actionSave.triggered.connect(self.browseForFile_save)
        self.ui.actionLoad.triggered.connect(self.browseForFile_load)
        self.ui.techIDbutton.toggled.connect(self.setTechID)
        self.connectMachineSignals()

    @Slot(bool)
    def setTechID(self, checked):
        """
        If checked, sets the techID if valid and disables text field.
        Otherwise, re-enable the text field.
        """
        txtField = self.ui.techID
        if checked:
            txt = txtField.text()
            try:
                self.techID = int(txt)
                txtField.setReadOnly(True)
                palette = QPalette()
                palette.setColor(QPalette.Button, Qt.darkGreen)
                palette.setColor(QPalette.ButtonText, Qt.white)
                palette.setColor(QPalette.Base, QColor(100, 143, 100))
                txtField.setPalette(palette)
                self.ui.techIDbutton.setPalette(palette)
            except:
                title = "Error"
                message = "Technician ID must be an integer number."
                buttons = QMessageBox.Ok
                message = QMessageBox(QMessageBox.Warning, title, message, buttons=buttons, flags=Qt.Dialog)
                message.exec_()
                self.ui.techIDbutton.setChecked(False)
                self.techID = None
                return
        else:
            self.techID = None
            txtField.setReadOnly(False)
            palette = QPalette()
            if self.theme is 0:
                palette.setColor(QPalette.Button, QColor(180,180,180))
                palette.setColor(QPalette.ButtonText, Qt.black)
                palette.setColor(QPalette.Base, QColor(140,140,140))
            else:
                palette.setColor(QPalette.Button, QColor(53, 53, 53))
                palette.setColor(QPalette.Base, QColor(25, 25, 25))
            txtField.setPalette(palette)
            self.ui.techIDbutton.setPalette(palette)

    def initPieCharts(self):
        """
        Initializes pie chart widgets in 3 tabs.

        Not static: needs the self variable, but it is hidden as a string.
        Uses QtCharts, Planet, and QPainter imports.
        """
        for i in range(1, 2):  # Tab number: i
            for j in range(1, 6):  # Planet number: j

                # Generate the necessary widgets' names
                pieNum = "pie" + str(j)
                infoSect = "self.ui.infoP" + str(j)
                planetBox = "self.ui.planet" + str(j) + "Box"
                widName = pieNum + "Container"
                selfSeries = "self.ui." + pieNum + "series"
                if i in [2, 3]:
                    selfSeries += "_" + str(i)
                    widName += "_" + str(i)
                    infoSect += "_" + str(i)
                    planetBox += "_" + str(i)

                # Initialize commonly used custom strs
                selfChart = "self.ui." + pieNum + "chart"
                selfChartView = selfChart + "View"

                # Store custom lines to execute (a list is easier to maintain and edit)
                codeList = [selfChart + " = QtCharts.QChart()",
                            selfChart + ".setTheme(QtCharts.QChart.ChartThemeLight)",
                            selfSeries + " = Planet(" + selfChart + ", self, " + infoSect + ", " + planetBox + ")",
                            selfSeries + ".planetEnabled.connect(self.checkPlanetStatuses)",
                            'self.themeChanged.connect(lambda theme, self=self: ' + selfSeries + '.changeTheme(theme))',
                            selfSeries + ".notEnoughSpaceForWO.connect(self.noSpaceLeftFor)",
                            selfChart + ".addSeries(" + selfSeries + ")",
                            selfChart + ".setBackgroundVisible(False)",
                            selfChart + ".legend().hide()",
                            selfChartView + " = QtCharts.QChartView(" + selfChart + ")",
                            selfChartView + ".setRenderHint(QPainter.Antialiasing)",
                            selfChartView + ".setParent(self.ui." + widName + ")",
                            selfChartView + ".resize(340, 340)",
                            selfChartView + ".move(-52, -52)"]

                # Convert list to string, placing newlines between each command
                code = '\n'.join(codeList)

                # Execute custom code
                exec(code)

    @Slot(WorkOrder)
    def noSpaceLeftFor(self, workOrder: WorkOrder):
        """
        Gives user the option to change workorder's planet, or discard the order.
        """
        title = "Error: No Space Left On Planet"
        message = "There isn't enough space left on the selected planet to add this order.\n" \
                  "An option could be placed here to change the work order's planet, but this hasn't been implemented "\
                  "yet, so the only option at the moment is to discard it. If this is necessary functionality and " \
                  "needs to be implemented, please let me know."
        buttons = QMessageBox.Discard
        message = QMessageBox(QMessageBox.Warning, title, message, buttons=buttons, flags=Qt.Dialog)
        message.exec_()
        self.deleteWorkOrder(workOrder)

    def deleteWorkOrder(self, workOrder):
        """
        Pretty self-explanatory name lol
        """
        self.results.removeRow(workOrder.rowNum)
        self.results.updateRowsFrom(workOrder.rowNum)
        exec("self.ui.pie" + str(workOrder.planetNum) + "series.deleteSlice(workOrder.slice)")

    @Slot(QtCharts.QPieSlice)
    def ensureSingleWorkOrder_p(self, mySlice):
        """
        For signals coming from planets, when a slice was just selected.
        Ensures there is only one Work Order selected per machine: the one given.
        Then selects the Work Order's row in the results section.
        """
        wo = mySlice.order
        if not mySlice.selected:
            self.deselectAllSlicesInTab(wo.machineNum, mySlice=mySlice, planetNum=wo.planetNum)
            rowPos = wo.rowNum
            self.results.selectRow(rowPos)
        else:
            pie = "self.ui.pie" + str(wo.planetNum) + "series"
            exec(pie + ".clickSlice(mySlice)")

    @Slot(int, int)
    def ensureSingleWorkOrder_r(self, row, col):
        """
        For signals coming from the results section, when a cell of a row is selected.
        Ensures there is only one Work Order selected per machine: the one given.
        Then selects the corresponding slice in the pie charts
        """
        wo = self.results.rowNumToWOMapping[row]
        self.deselectAllSlicesInTab(wo.machineNum, mySlice=wo.slice, planetNum=wo.planetNum)

    def deselectAllSlicesInTab(self, tab, mySlice=None, planetNum=None):
        """
        Optional param is the one slice you do want selected.
        Note: Not static. Uses self, but it is hidden as string.
        """
        for j in range(1, 6):  # Planet number: j
            pie = "self.ui.pie" + str(j) + "series"

            if tab in [2, 3]:
                pie += "_" + str(tab)

            exec(pie + ".deselectAll()")

            if mySlice and j == planetNum:
                exec(pie + ".clickSlice(mySlice)")

    @Slot()
    def browseForFile_save(self) -> None:
        """
        Opens a file dialog when the user clicks on the "Save As..." option to choose a file to save to.
        """
        if self.techID:
            fileDialog = QFileDialog()
            fileDialog.setFileMode(QFileDialog.AnyFile)
            fileDialog.setDirectory(os.getcwd())
            fileDialog.setDefaultSuffix(".proj")
            fileDialog.setNameFilter("Project (*.proj)")
            fileDialog.fileSelected.connect(lambda url: self.saveFile(url))
            fileDialog.exec_()
        else:
            title = "Error"
            message = "Must set Technician ID to save project."
            buttons = QMessageBox.Ok
            message = QMessageBox(QMessageBox.Warning, title, message, buttons=buttons, flags=Qt.Dialog)
            message.exec_()

    @Slot()
    def browseForFile_load(self) -> None:
        """
        Opens a file dialog when the user clicks on the "Save As..." option to choose a file to save to.
        """

        fileDialog = QFileDialog()
        fileDialog.setFileMode(QFileDialog.ExistingFile)
        fileDialog.setDirectory(os.getcwd())
        fileDialog.setNameFilter("Project (*.proj)")
        fileDialog.fileSelected.connect(lambda url: self.loadFile(url))
        fileDialog.exec_()

    def saveFile(self, path):
        """
        Saves data to file, at location "path".
        """
        # Create dictionary first. All we really care about is the work orders, so we'll just save the list of them.
        d = {'techID': self.techID}
        for tab, machine in enumerate(self.machines):
            if tab == 0:  # TODO: change
                d[tab] = {}
                d[tab]['workOrders'] = {}
                for wo in machine.workOrders:
                    d[tab]['workOrders'][wo.name] = [wo.pieces, wo.side, wo.planetNum, wo.yld]
                d[tab]['startTime'] = machine.startTime
                d[tab]['endTime'] = machine.endTime
                d[tab]['loadTime'] = machine.loadTime
                d[tab]['unloadTime'] = machine.unloadTime
                d[tab]['cdn'] = machine.cdn
                d[tab]['testRun'] = machine.testRun
                d[tab]['coatingRun'] = machine.coatingRun
                d[tab]['loadingRun'] = machine.loadingRun
                d[tab]['setupRun'] = machine.setupRun

                # Storing planets' sum values.
                d[tab]['planets'] = {}

                for planet in range(1, 6):
                    pie = 'self.ui.pie' + str(planet) + 'series'
                    if tab in (1, 2):
                        pie += '_' + str(tab+1)
                    exec('tmp = ' + pie + '.enabled', locals())
                    if locals()['tmp']:
                        exec('sum = ' + pie + '.sum()', locals())
                        d[tab]['planets'][planet] = locals()['sum']
                    else:
                        d[tab]['planets'][planet] = None

        # Now save to file.
        with open(path, 'wb') as f:
            pickle.dump(d, f)

    def loadFile(self, path):
        """
         Attempts to load the file at path
        """
        error = False
        if path[-5:] == '.proj':
            try:
                # Load dictionary from file
                with open(path, 'rb') as f:
                    p = pickle.Unpickler(f)
                    d = p.load()

                if not p:
                    # file is empty
                    error = True  # Checks if file is empty

                else:
                    self.techID = d['techID']
                    self.ui.techID.setText(str(self.techID))
                    self.ui.techIDbutton.setChecked(True)

                    for tab in range(0, 1):  # TODO: Change
                        machine = self.machines[tab]

                        # Load all values
                        startTime = d[tab]['startTime']
                        endTime = d[tab]['endTime']
                        loadTime = d[tab]['loadTime']
                        unloadTime = d[tab]['unloadTime']
                        cdn = d[tab]['cdn']
                        testRun = d[tab]['testRun']
                        coatingRun = d[tab]['coatingRun']
                        loadingRun = d[tab]['loadingRun']
                        setupRun = d[tab]['setupRun']

                        # Check if they exist
                        if startTime:
                            machine.startTime = startTime

                            time = QTime().fromString(startTime)
                            tmp = 'self.ui.startTime'
                            but = 'self.ui.stButton'
                            if tab in (1, 2):
                                tmp += '_' + str(tab+1)
                                but += '_' + str(tab+1)
                            exec(tmp + '.setTime(time)')
                            exec(but + '.setChecked(True)')

                        if endTime:
                            machine.endTime = endTime

                            time = QTime().fromString(endTime)
                            tmp = 'self.ui.endTime'
                            but = 'self.ui.etButton'
                            if tab in (1, 2):
                                tmp += '_' + str(tab+1)
                                but += '_' + str(tab+1)
                            exec(tmp + '.setTime(time)')
                            exec(but + '.setChecked(True)')

                        if loadTime:
                            machine.loadTime = loadTime

                            time = QTime().fromString(loadTime)
                            tmp = 'self.ui.loadTime'
                            but = 'self.ui.ltButton'
                            if tab in (1, 2):
                                tmp += '_' + str(tab+1)
                                but += '_' + str(tab+1)
                            exec(tmp + '.setTime(time)')
                            exec(but + '.setChecked(True)')

                        if unloadTime:
                            machine.unloadTime = unloadTime

                            time = QTime().fromString(unloadTime)
                            tmp = 'self.ui.unloadTime'
                            but = 'self.ui.utButton'
                            if tab in (1, 2):
                                tmp += '_' + str(tab+1)
                                but += '_' + str(tab+1)
                            exec(tmp + '.setTime(time)')
                            exec(but + '.setChecked(True)')

                        if cdn:  # If there's the cdn, the other 4 are there too
                            machine.cdn = cdn
                            machine.testRun = testRun
                            machine.coatingRun = coatingRun
                            machine.loadingRun = loadingRun
                            machine.setupRun = setupRun

                            cdnBox = 'self.ui.cdn'
                            testBox = 'self.ui.testRun'
                            coatBox = 'self.ui.coatRun'
                            loadBox = 'self.ui.loadingRun'
                            setupBox = 'self.ui.setupTestRun'
                            vButton = 'self.ui.validateButton'

                            if tab in (1, 2):
                                cdnBox += '_' + str(tab+1)
                                testBox += '_' + str(tab+1)
                                coatBox += '_' + str(tab+1)
                                loadBox += '_' + str(tab+1)
                                setupBox += '_' + str(tab+1)
                                vButton += '_' + str(tab+1)

                            codeList = [
                                cdnBox + '.setText(str(cdn))',
                                testBox + '.setText(str(testRun))',
                                coatBox + '.setText(str(coatingRun))',
                                loadBox + '.setText(str(loadingRun))',
                                setupBox + '.setText(str(setupRun))',
                                vButton + '.setChecked(True)'
                            ]

                            code = '\n'.join(codeList)
                            exec(code)

                        # Initialize planets
                        for planetNum in d[tab]['planets']:
                            sum = d[tab]['planets'][planetNum]
                            if sum:
                                pie = 'self.ui.pie' + str(planetNum) + 'series'
                                if tab in (1, 2):
                                    pie += '_' + str(tab + 1)
                                exec(pie + '.setEnabled(sum)')

                        sortedWOList = []
                        for woName in d[tab]['workOrders']:
                            params = d[tab]['workOrders'][woName]

                            wo = WorkOrder()
                            wo.name = woName
                            wo.machineNum = tab + 1
                            wo.pieces = params[0]
                            wo.side = params[1]
                            wo.planetNum = params[2]
                            if params[3]:
                                wo.setYield(params[3])

                            sortedWOList.append(wo)
                        sortedWOList.sort(key=lambda workOrder: int(workOrder.name[4:]))

                        unsuccessful = []
                        for wo in sortedWOList:
                            success = self.addToPlanets(wo)
                            if success:
                                self.results.addRowFor(wo)
                                self.machines[wo.machineNum - 1].workOrders.append(wo)
                            else:
                                unsuccessful.append(wo)
                        if unsuccessful:
                            for wo in unsuccessful:
                                print(wo.name)
            except Exception as e:
                raise e
        else:
            # not a proj file
            error = True

        if error:
            title = "Error Loading Project"
            message = "Could not load the selected file successfully."
            buttons = QMessageBox.Ok
            message = QMessageBox(QMessageBox.Warning, title, message, buttons=buttons, flags=Qt.Dialog)
            message.exec_()

    @Slot(bool)
    def checkPlanetStatuses(self, enabled):
        """
        If a planet is switched to enabled, this unlocks the save as button.
        Otherwise if a planet is switched to disabled, this does a application-wide check to see
        if any other planets are currently enabled. If not, disables the save as button.
        """
        if enabled:
            if not self.ui.actionSave.isEnabled():
                self.ui.actionSave.setEnabled(True)
        else:
            if self.ui.actionSave.isEnabled():
                atLeastOneEnabled = False
                for machine in range(1, 2):  # 3 tabs TODO: Change 1 to 3 when other tabs are implemented
                    for planet in range(1, 6):  # 5 planets
                        pie = "self.ui.pie" + str(planet) + "series"
                        if machine in [2, 3]:
                            pie += "_" + str(machine)
                        if exec(pie + '.enabled'):
                            atLeastOneEnabled = True
                            break
                    if atLeastOneEnabled:
                        break
                if not atLeastOneEnabled:
                    self.ui.actionSave.setEnabled(False)

    def startTimeCheck(self, checked, machine, timeBox, button):
        """
        If the button next to the time is clicked (checked), this handles what to do with the data and gui.
        If it is unchecked, the data is deleted and the timeObject is enabled.
        """
        if checked:
            machine.startTime = timeBox.time().toString()
            timeBox.setReadOnly(True)
            palette = QPalette()
            palette.setColor(QPalette.Button, Qt.darkGreen)
            palette.setColor(QPalette.ButtonText, Qt.white)
            button.setPalette(palette)
            timeBox.setPalette(palette)

        else:
            machine.startTime = None
            timeBox.setReadOnly(False)
            palette = QPalette()
            if self.theme is 0:
                palette.setColor(QPalette.Button, QColor(180,180,180))
                palette.setColor(QPalette.ButtonText, Qt.black)
            else:
                palette.setColor(QPalette.Button, QColor(53, 53, 53))
            button.setPalette(palette)
            timeBox.setPalette(palette)

        self.updateResults(machine)

    def endTimeCheck(self, checked, machine, timeBox, button):
        """
        If the button next to the time is clicked (checked), this handles what to do with the data and gui.
        If it is unchecked, the data is deleted and the timeObject is enabled.
        """
        if checked:
            machine.endTime = timeBox.time().toString()
            timeBox.setReadOnly(True)
            palette = QPalette()
            palette.setColor(QPalette.Button, Qt.darkGreen)
            palette.setColor(QPalette.ButtonText, Qt.white)
            button.setPalette(palette)
            timeBox.setPalette(palette)
        else:
            machine.endTime = None
            timeBox.setReadOnly(False)
            palette = QPalette()
            if self.theme is 0:
                palette.setColor(QPalette.Button, QColor(180, 180, 180))
                palette.setColor(QPalette.ButtonText, Qt.black)
            else:
                palette.setColor(QPalette.Button, QColor(53, 53, 53))
            button.setPalette(palette)
            timeBox.setPalette(palette)

        self.updateResults(machine)

    def loadTimeCheck(self, checked, machine, timeBox, button):
        """
        If the button next to the time is clicked (checked), this handles what to do with the data and gui.
        If it is unchecked, the data is deleted and the timeObject is enabled.
        """
        if checked:
            machine.loadTime = timeBox.time().toString()
            timeBox.setReadOnly(True)
            palette = QPalette()
            palette.setColor(QPalette.Button, Qt.darkGreen)
            palette.setColor(QPalette.ButtonText, Qt.white)
            button.setPalette(palette)
            timeBox.setPalette(palette)
        else:
            machine.loadTime = None
            timeBox.setReadOnly(False)
            palette = QPalette()
            if self.theme is 0:
                palette.setColor(QPalette.Button, QColor(180, 180, 180))
                palette.setColor(QPalette.ButtonText, Qt.black)
            else:
                palette.setColor(QPalette.Button, QColor(53, 53, 53))
            button.setPalette(palette)
            timeBox.setPalette(palette)

        self.updateResults(machine)

    def unloadTimeCheck(self, checked, machine, timeBox, button):
        """
        If the button next to the time is clicked (checked), this handles what to do with the data and gui.
        If it is unchecked, the data is deleted and the timeObject is enabled.
        """
        if checked:
            machine.unloadTime = timeBox.time().toString()
            timeBox.setReadOnly(True)
            palette = QPalette()
            palette.setColor(QPalette.Button, Qt.darkGreen)
            palette.setColor(QPalette.ButtonText, Qt.white)
            button.setPalette(palette)
            timeBox.setPalette(palette)
        else:
            machine.unloadTime = None
            timeBox.setReadOnly(False)
            palette = QPalette()
            if self.theme is 0:
                palette.setColor(QPalette.Button, QColor(180, 180, 180))
                palette.setColor(QPalette.ButtonText, Qt.black)
            else:
                palette.setColor(QPalette.Button, QColor(53, 53, 53))
            button.setPalette(palette)
            timeBox.setPalette(palette)

        self.updateResults(machine)

    def validateData(self, checked, tab):
        """
        If checked, loads data from all text fields around validate button, and disables them. Also changes button text.
        Otherwise, enables all fields, clears data, and changes button text back.
        """
        cdnBox = "self.ui.cdn"
        testBox = "self.ui.testRun"
        coatBox = "self.ui.coatRun"
        loadBox = "self.ui.loadingRun"
        setupBox = "self.ui.setupTestRun"
        vButton = "self.ui.validateButton"
        machine = "self.machines[" + str(tab-1) + "]"
        if tab in (2, 3):
            cdnBox += "_" + str(tab)
            testBox += "_" + str(tab)
            coatBox += "_" + str(tab)
            loadBox += "_" + str(tab)
            setupBox += "_" + str(tab)
            vButton += "_" + str(tab)

        if checked:
            codeList = [
                'cdn = ' + cdnBox + '.text()',
                'testRun = ' + testBox + '.text()',
                'coatingRun = ' + coatBox + '.text()',
                'loadingRun = ' + loadBox + '.text()',
                'setupRun = ' + setupBox + '.text()',
                'locals()["valid"] = self.checkValidity(cdn, testRun, coatingRun, loadingRun, setupRun)'
            ]
            code = '\n'.join(codeList)
            exec(code)

            if locals()["valid"]:
                codeList = [
                    machine + '.cdn = int(' + cdnBox + '.text())',
                    machine + '.testRun = float(' + testBox + '.text())',
                    machine + '.coatingRun = float(' + coatBox + '.text())',
                    machine + '.loadingRun = float(' + loadBox + '.text())',
                    machine + '.setupRun = float(' + setupBox + '.text())',
                    cdnBox + '.setReadOnly(True)',
                    testBox + '.setReadOnly(True)',
                    coatBox + '.setReadOnly(True)',
                    loadBox + '.setReadOnly(True)',
                    setupBox + '.setReadOnly(True)',
                    vButton + '.setText("Unlock")',
                    'palette = QPalette()',
                    'palette.setColor(QPalette.Button, Qt.darkGreen)',
                    'palette.setColor(QPalette.ButtonText, Qt.white)',
                    'palette.setColor(QPalette.Base, QColor(100, 143, 100))',
                    vButton + '.setPalette(palette)',
                    cdnBox + '.setPalette(palette)',
                    testBox + '.setPalette(palette)',
                    coatBox + '.setPalette(palette)',
                    loadBox + '.setPalette(palette)',
                    setupBox + '.setPalette(palette)'
                ]
            else:
                codeList = [
                    vButton + '.setChecked(False)'
                ]
        else:
            palette = QPalette()
            if self.theme is 0:
                palette.setColor(QPalette.Button, QColor(180,180,180))
                palette.setColor(QPalette.ButtonText, Qt.black)
                palette.setColor(QPalette.Base, QColor(140, 140, 140))
            else:
                palette.setColor(QPalette.Button, QColor(53, 53, 53))
                palette.setColor(QPalette.Base, QColor(25, 25, 25))

            codeList = [
                machine + '.cdn = None',
                machine + '.testRun = None',
                machine + '.coatingRun = None',
                machine + '.loadingRun = None',
                machine + '.setupRun = None',
                cdnBox + '.setReadOnly(False)',
                testBox + '.setReadOnly(False)',
                coatBox + '.setReadOnly(False)',
                loadBox + '.setReadOnly(False)',
                setupBox + '.setReadOnly(False)',
                vButton + '.setText("Lock")',
                vButton + '.setPalette(palette)',
                cdnBox + '.setPalette(palette)',
                testBox + '.setPalette(palette)',
                coatBox + '.setPalette(palette)',
                loadBox + '.setPalette(palette)',
                setupBox + '.setPalette(palette)'
            ]

        code = '\n'.join(codeList)
        exec(code)

        self.updateResults(self.machines[tab-1])

    def checkValidity(self, cdn, testRun, coatingRun, loadingRun, setupRun):
        """
        Checks if all inputs are valid types.
        """
        try:
            int(cdn)
            float(testRun)
            float(coatingRun)
            float(loadingRun)
            float(setupRun)
            return True
        except:
            title = "Error"
            message = "At least one of the text fields does not have a numerical entry."
            buttons = QMessageBox.Ok
            message = QMessageBox(QMessageBox.Warning, title, message, buttons=buttons, flags=Qt.Dialog)
            message.exec_()
            return False

    def updateResults(self, machine):
        """
        When a button is pressed in a machine, this function makes sure
        to update its work orders with the correct values.
        """
        for workOrder in machine.workOrders:
            self.results.updateRowInfo(workOrder)

    def connectMachineSignals(self):
        """
        Connects all time and textbox signals for each machine.
        Note: Not static. Uses self variable, but hidden as string.
        """
        for tab in range(1, 2):  # TODO: Change 2 to 4 when other tabs are implemented.
            # Instantiate button names
            stButton = "self.ui.stButton"
            stBox = "self.ui.startTime"
            etButton = "self.ui.etButton"
            etBox = "self.ui.endTime"
            ltButton = "self.ui.ltButton"
            ltBox = "self.ui.loadTime"
            utButton = "self.ui.utButton"
            utBox = "self.ui.unloadTime"
            vButton = "self.ui.validateButton"
            machine = "self.machines[" + str(tab - 1) + "]"
            if tab in (2, 3):
                stButton += "_" + str(tab)
                etButton += "_" + str(tab)
                ltButton += "_" + str(tab)
                utButton += "_" + str(tab)
                vButton += "_" + str(tab)

            # List of code to run
            codeList = [
                stButton + ".toggled.connect(lambda checked, self=self: self.startTimeCheck(checked, " + machine + ", " + stBox + ", " + stButton + "))",
                etButton + ".toggled.connect(lambda checked, self=self: self.endTimeCheck(checked, " + machine + ", " + etBox + ", " + etButton + "))",
                ltButton + ".toggled.connect(lambda checked, self=self: self.loadTimeCheck(checked, " + machine + ", " + ltBox + ", " + ltButton + "))",
                utButton + ".toggled.connect(lambda checked, self=self: self.unloadTimeCheck(checked, " + machine + ", " + utBox + ", " + utButton + "))",
                vButton + ".toggled.connect(lambda checked, self=self: self.validateData(checked, " + str(tab) + "))"
            ]

            code = '\n'.join(codeList)
            exec(code)

    def showWOInitDialog(self, wo=None):
        """
        Shows the Work Order Dialog and does some extra action handling
        """
        if not wo:
            wo = WorkOrder()
        woDialog = WorkOrderDialog(self, wo)
        result = woDialog.exec_()
        if result == QDialog.Rejected:
            return
        else:
            success = self.addToPlanets(wo)
            if not success:
                self.showWOInitDialog(wo)
                return
            self.results.addRowFor(wo)
            self.machines[wo.machineNum-1].workOrders.append(wo)

    def updateWorkOrder(self, workOrder: WorkOrder):
        """
        Updates visual information about workOrder.
        """
        workOrder.slice.setValue(workOrder.pieces)
        workOrder.slice.parent().updateHeader()
        if workOrder.slice.selected:
            workOrder.slice.parent().clickSlice(workOrder.slice)
            workOrder.slice.parent().clickSlice(workOrder.slice)
        self.results.updateRowInfo(workOrder)

    def addToPlanets(self, workOrder: WorkOrder):
        """
        Adds a new work order to its planet
        """
        pie = "self.ui.pie" + str(workOrder.planetNum) + "series"
        if workOrder.machineNum in (2, 3):
            pie += "_" + str(workOrder.machineNum)
        exec('success = ' + pie + '.addSlice(workOrder)', locals())
        return locals()['success']

    def showPlanetConfigDialog(self):
        """
        Shows the planet configuration dialog
        """
        pcd = PlanetConfigDialog(self)
        pcd.exec_()

    def reInit(self, alreadyWarned=False):
        """
        Clears all info
        """
        result = None
        if not alreadyWarned:
            title = "Warning"
            message = "This will clear all work orders, and cannot be undone. Continue?"
            buttons = QMessageBox.Ok | QMessageBox.Cancel
            message = QMessageBox(QMessageBox.Warning, title, message, buttons=buttons, flags=Qt.Dialog)
            result = message.exec_()

        if alreadyWarned or result == QMessageBox.Ok:
            for num, machine in enumerate(self.machines):
                for workOrder in machine.workOrders:
                    self.deleteWorkOrder(workOrder)
                if num is 0:  # TODO: Remove when other tabs are implemented
                    for planetNum in range(1, 6):
                        planet = 'self.ui.pie' + str(planetNum) + 'series'
                        if num in (1, 2):
                            planet += '_' + str(num+1)
                        exec(planet + '.setDisabled()')
                machine.workOrders.clear()

    def toggleTheme(self):
        """
        Changes between light and dark theme. 0 is light, 1 is dark
        """
        qApp = QApplication.instance()
        if self.theme is 0:
            qApp.setStyle("Fusion")

            dark_palette = QPalette()
            dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
            dark_palette.setColor(QPalette.WindowText, Qt.white)
            dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
            dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
            dark_palette.setColor(QPalette.ToolTipText, Qt.white)
            dark_palette.setColor(QPalette.Text, Qt.white)
            dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
            dark_palette.setColor(QPalette.ButtonText, Qt.white)
            dark_palette.setColor(QPalette.BrightText, Qt.red)
            dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
            dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            dark_palette.setColor(QPalette.HighlightedText, Qt.black)
            dark_palette.setColor(QPalette.Disabled, QPalette.Text, QColor(190, 190, 190))
            dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, Qt.darkGray)
            qApp.setPalette(dark_palette)
            qApp.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
            self.theme = 1
            self.ui.themeButton.setText("Dark Mode")
            self.themeChanged.emit(self.theme)
        else:
            qApp.setStyle("Fusion")

            dark_palette = QPalette()
            dark_palette.setColor(QPalette.Window, QColor(180, 180, 180))
            dark_palette.setColor(QPalette.WindowText, Qt.black)
            dark_palette.setColor(QPalette.Base, QColor(140, 140, 140))
            dark_palette.setColor(QPalette.AlternateBase, QColor(180, 180, 180))
            dark_palette.setColor(QPalette.ToolTipBase, Qt.black)
            dark_palette.setColor(QPalette.ToolTipText, Qt.black)
            dark_palette.setColor(QPalette.Text, Qt.black)
            dark_palette.setColor(QPalette.Button, QColor(180, 180, 180))
            dark_palette.setColor(QPalette.ButtonText, Qt.black)
            dark_palette.setColor(QPalette.BrightText, Qt.red)
            dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
            dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            dark_palette.setColor(QPalette.HighlightedText, Qt.white)
            dark_palette.setColor(QPalette.Disabled, QPalette.Text, QColor(60, 60, 60))
            dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, Qt.darkGray)
            qApp.setPalette(dark_palette)
            qApp.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
            self.theme = 0
            self.ui.themeButton.setText("Light Mode")
            self.themeChanged.emit(self.theme)

    def loadRandomWorkOrders(self):
        """
        Iteratively creates random work orders. Loads data into
        planets 1-4 and the table at the bottom, ***only in Tab 1***.

        Not static: needs the self variable, but it is hidden as a string.
        """
        title = "Warning"
        message = "Running the demo will clear all current work orders. Continue?"
        buttons = QMessageBox.Ok | QMessageBox.Cancel
        message = QMessageBox(QMessageBox.Warning, title, message, buttons=buttons, flags=Qt.Dialog)
        result = message.exec_()

        if result == QMessageBox.Ok:
            self.reInit(True)
            c = 1
            for i in range(1, 5):  # The first 4 planets
                # Get current pie's name, initialize that pieSeries
                curPie = "self.ui.pie" + str(i) + "series"
                exec(curPie + ".setEnabled(100)")

                # Randomly generate some WorkOrders for this pie, add them
                # as slices to pie, and add data to results.
                for j in range(1, 5):
                    # Random num of pcs and side choice
                    numPcs = randrange(1, 26)
                    side = randrange(1, 3)

                    # Set name, create WorkOrder
                    name = "WO #" + str(c)
                    c += 1

                    tmpWO = WorkOrder()
                    tmpWO.name = name
                    tmpWO.pieces = numPcs
                    tmpWO.side = side
                    tmpWO.planetNum = i
                    tmpWO.machineNum = 1

                    # Create slice for WorkOrder, add it to mapping, add it to results
                    exec(curPie + ".addSlice(tmpWO)")
                    self.results.addRowFor(tmpWO)
                    self.machines[0].workOrders.append(tmpWO)


if __name__ == '__main__':
    def stylize(qApp):
        """
        Light grey theme.
        """
        qApp.setStyle("Fusion")

        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(180,180,180))
        dark_palette.setColor(QPalette.WindowText, Qt.black)
        dark_palette.setColor(QPalette.Base, QColor(140, 140, 140))
        dark_palette.setColor(QPalette.AlternateBase, QColor(180,180,180))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.black)
        dark_palette.setColor(QPalette.ToolTipText, Qt.black)
        dark_palette.setColor(QPalette.Text, Qt.black)
        dark_palette.setColor(QPalette.Button, QColor(180,180,180))
        dark_palette.setColor(QPalette.ButtonText, Qt.black)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.white)
        dark_palette.setColor(QPalette.Disabled, QPalette.Text, QColor(60, 60, 60))
        dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, Qt.darkGray)
        qApp.setPalette(dark_palette)
        qApp.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")

    app = QApplication(sys.argv)
    mainWindow = MainWindow()

    stylize(app)

    mainWindow.show()
    sys.exit(app.exec_())

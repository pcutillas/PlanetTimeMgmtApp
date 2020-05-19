import sys
from PySide2.QtCore import Qt, Slot, Signal
from PySide2.QtGui import QPainter, QPen, QColor
from PySide2.QtWidgets import QMainWindow, QApplication, QMessageBox
from PySide2.QtCharts import QtCharts
import src.workorder as wo


class Planet(QtCharts.QPieSeries):

    planetEnabled = Signal(bool)
    notEnoughSpaceForWO = Signal(wo.WorkOrder)

    def __init__(self, parent: QtCharts.QChart, window, infoSection, planetBox):
        QtCharts.QPieSeries.__init__(self)
        self.setParent(parent)
        self.setHoleSize(.35)

        # Initialize variables needed
        self.spacesLeft = 0
        self.window = window
        self.infoSection = infoSection
        self.planetBox = planetBox
        self.planetName = planetBox.title()
        self.enabled = True
        self.emptySlice: QtCharts.QPieSlice = None

        # Initialize to "disabled" appearance
        self.setDisabled()

    def setDisabled(self):
        """
        Gives the disabled look of the item, and disables interactivity via its parent.
        """
        if self.enabled:
            self.clear()
            self.append('Empty', 1)
            self.append('Empty', 3)
            if self.window.theme is 0:
                self.slices()[0].setBrush(QColor(120, 120, 120))
                self.slices()[1].setBrush(QColor(120, 120, 120))
            else:
                self.slices()[0].setBrush(QColor(45, 45, 45))
                self.slices()[1].setBrush(QColor(45, 45, 45))
            self.slices()[0].setPen(QPen(QColor(90, 90, 90), 2))
            self.slices()[0].setExploded()
            self.slices()[1].setPen(QPen(QColor(90, 90, 90), 2))
            self.infoSection.hide()
            self.planetBox.setTitle(self.planetName)
            self.emptySlice = None
            self.enabled = False
            self.planetEnabled.emit(False)

    def setEnabled(self, pieces):
        """
        Enables this pie chart. Stores the total number of pieces allowed in the planet, and enforces it.
        """
        if not self.enabled:
            # Initialize empty slice with number of slices in planet, set necessary attributes
            self.clear()
            self.emptySlice = self.append('Empty', pieces)
            if self.window.theme == 0:
                self.emptySlice.setBrush(QColor(120, 120, 120))
            else:
                self.emptySlice.setBrush(QColor(50, 50, 50))
            self.emptySlice.setPen(QPen(QColor(90, 90, 90), 2))
            self.emptySlice.selected = False

            # Connect to slot
            self.emptySlice.clicked.connect(lambda: self.emptySliceClicked())

            # Initialize needed variables and show text area for planet box
            self.spacesLeft = pieces
            self.enabled = True
            self.infoSection.setText('Select a Work Order below.')
            self.infoSection.show()

            # Update Planet Header
            self.updateHeader()

            # Notify app that planet was updated
            self.planetEnabled.emit(True)

    def addSlice(self, workOrder):
        """
        Adds a slice, deducting the value from spacesLeft. Connects signals as needed
        """
        # Get values from workOrder
        value = workOrder.pieces
        label = workOrder.name

        # If no space left, check with user if they still want to add it
        if self.spacesLeft is 0:
            confirmed = self.updateSpaces(workOrder)
        else:
            confirmed = True

        if confirmed:
            if not self.enabled:
                self.setEnabled(workOrder.pieces)

            # Initialize new slice, associate it to the workOrder, and remove value from space left
            newSlice = self.append(label, value)
            self.spacesLeft -= value
            if self.emptySlice:
                self.emptySlice.setValue(self.spacesLeft)

            # Add new properties to the slice
            newSlice.selected = False
            newSlice.order = workOrder
            workOrder.slice = newSlice
            newSlice.selectedColor = Qt.green
            newSlice.selectedPen = QPen(Qt.darkGreen, 2)
            newSlice.normalPen = QPen(QColor(90, 90, 90), 2)
            newSlice.setExplodeDistanceFactor(.06)

            # Update all slice colors (they all start with the same color otherwise)
            for slc in self.slices():
                slc.hoveredColor = slc.brush().color().lighter(f=120)
                slc.normalColor = slc.brush().color()

            # Set pen (so it's not white)
            newSlice.setPen(newSlice.normalPen)

            # Connect slice signals to slots
            newSlice.hovered.connect(lambda: self.hoverSlice(newSlice))
            newSlice.clicked.connect(lambda: self.window.ensureSingleWorkOrder_p(newSlice))

            self.showPlanetStatus()
            self.updateHeader()
            return True
        else:
            return False

    def updateSpaces(self, workOrder):
        """
        Increases spacesLeft by workOrder and does necessary adjustments
        """
        confirmed = False
        if self.enabled:
            if self.emptySlice:
                self.remove(self.emptySlice)
                self.emptySlice = None

            title = "Warning"
            message = "Adding work order will increase the planet size from " + str(int(self.sum())) + \
                      " to " + str(int(self.sum() + workOrder.pieces)) + " pieces total. Continue?"
            buttons = QMessageBox.Ok | QMessageBox.Cancel
            message = QMessageBox(QMessageBox.Warning, title, message, buttons=buttons, flags=Qt.Dialog)
            result = message.exec_()
            if result == QMessageBox.Ok:
                confirmed = True
        else:
            confirmed = True

        if confirmed:
            self.spacesLeft += workOrder.pieces
            self.updateHeader()
            return True
        else:
            return False

    def updateHeader(self):
        """
        Updates the groupbox header
        """
        self.planetBox.setTitle(self.planetName + ":     " + str(int(self.sum())) + " pieces total")

    @Slot(bool)
    def hoverSlice(self, mySlice):
        """
        Gives slight explosion and color change of slice on hover.
        """
        if self.enabled:
            if not mySlice.selected:
                if not mySlice.isExploded():
                    mySlice.setBrush(mySlice.hoveredColor)
                    mySlice.setExploded()
                else:
                    mySlice.setExploded(False)
                    mySlice.setBrush(mySlice.normalColor)

    def clickSlice(self, mySlice):
        if self.enabled:
            if not mySlice.selected:
                self.deselectAll()
                mySlice.selected = True

                mySlice.setExplodeDistanceFactor(.12)
                mySlice.setExploded()
                mySlice.setPen(mySlice.selectedPen)
                mySlice.setBrush(mySlice.selectedColor)

                val = int(mySlice.value())
                order = mySlice.order
                if val > 1:
                    self.infoSection.setText(mySlice.label() + ":  " + str(val) + " pieces on side " + str(order.side))
                else:
                    self.infoSection.setText(mySlice.label() + ":  1 piece on side " + str(order.side))
            else:
                mySlice.selected = False
                mySlice.setExplodeDistanceFactor(.06)
                mySlice.setPen(mySlice.normalPen)
                mySlice.setBrush(mySlice.normalColor)
                self.showPlanetStatus()

    @Slot()
    def emptySliceClicked(self):
        """
        Only gets called if the empty slice is selected. Uses different graphics, hence the independent function.
        """
        if self.enabled:
            mySlice = self.emptySlice
            if not mySlice.selected:
                self.deselectAll()
                mySlice.selected = True

                self.showPlanetStatus()
            else:
                mySlice.selected = False

    def deselectAll(self):
        """
        Deselects all slices in self
        """
        if self.enabled:
            self.showPlanetStatus()
            for sl in self.slices():
                if sl.selected:
                    sl.selected = False

                    if sl.label() == "Empty":
                        sl.setBrush(QColor(120, 120, 120))
                    else:
                        sl.setExplodeDistanceFactor(.06)
                        sl.setExploded(False)
                        sl.setPen(sl.normalPen)
                        sl.setBrush(sl.normalColor)

    def showPlanetStatus(self):
        """
        Shows available number of spaces in planet
        """
        if self.emptySlice:
            taken = int(self.sum() - self.emptySlice.value())
            val = int(self.emptySlice.value())
            if val > 1:
                self.infoSection.setText(str(taken) + " pieces\n" + str(val) + " spaces available")
            elif val == 1:
                self.infoSection.setText(str(taken) + " pieces\n" + "1 space available")
            else:
                self.infoSection.setText(str(taken) + " pieces\n" + "No space left on planet")
        else:
            self.infoSection.setText("No space left on planet")

    def deleteSlice(self, mySlice):
        """
        Deletes slice from chart, and adds its value back to the empty space
        """
        if self.emptySlice:
            try:
                self.spacesLeft += mySlice.value()
                self.remove(mySlice)
                self.emptySlice.setValue(self.spacesLeft)
            except:
                pass

    def changeTheme(self, theme):
        """
        changes theme (i.e. empty slice color and disabled color). 0 is light, 1 is dark
        """
        if self.enabled and self.emptySlice:
            if theme is 0:
                self.emptySlice.setBrush(QColor(120, 120, 120))
            else:
                self.emptySlice.setBrush(QColor(45, 45, 45))
        elif not self.enabled:
            if theme is 0:
                self.slices()[0].setBrush(QColor(120, 120, 120))
                self.slices()[1].setBrush(QColor(120, 120, 120))
            else:
                self.slices()[0].setBrush(QColor(45, 45, 45))
                self.slices()[1].setBrush(QColor(45, 45, 45))

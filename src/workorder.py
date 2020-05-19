
class WorkOrder:

    def __init__(self):
        """
        Instantiates a work order
        """
        self.name = None
        self.pieces = None
        self.side = None
        self.planetNum = None
        self.machineNum = None
        self.slice = None
        self.rowNum = None
        self.yld = None
        self.scrap = None

    def setYield(self, yld):
        self.yld = yld
        self.scrap = self.pieces - yld

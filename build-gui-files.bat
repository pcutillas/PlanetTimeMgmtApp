@echo OFF
@echo Building .py files from .ui files...
pyside2-uic gui/ui/mainwindow.ui > gui/ui_mainwindow.py
pyside2-uic gui/ui/workOrderDialog.ui > gui/ui_workOrderDialog.py
pyside2-uic gui/ui/planetConfigDialog.ui > gui/ui_planetConfigDialog.py
@echo Done.
pause

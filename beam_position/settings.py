# Created by matveyev at 01.02.2022

import logging
import PyTango

from PyQt5 import QtWidgets, QtCore

from beam_position.main_window import APP_NAME
from beam_position.gui.settings_ui import Ui_Settings

WIDGET_NAME = 'ProgramSetup'

logger = logging.getLogger(APP_NAME)


class ProgramSetup(QtWidgets.QDialog):

    # ----------------------------------------------------------------------
    def __init__(self, main_window):
        """
        """
        super(ProgramSetup, self).__init__()
        self._ui = Ui_Settings()
        self._ui.setupUi(self)

        self._ui.le_source.setText(main_window.source)

        self._ui.dsb_pos_x.setValue(main_window.reference['x'])
        self._ui.dsb_pos_y.setValue(main_window.reference['y'])

        self.new_settings = {'source': main_window.source,
                             'x': main_window.reference['x'],
                             'y': main_window.reference['y']
                             }

        self._main_window = main_window

        self._ui.le_source.editingFinished.connect(self._check_source)

    # ----------------------------------------------------------------------
    def _check_source(self):

        new_source = self._ui.le_source.text()

        try:
            dev = PyTango.DeviceProxy(new_source)
        except Exception as err:
            self._main_window.report_error('Cannot connect to {}'.format(new_source), repr(err))
            return

        for attr in ['com_x', 'com_y']:
            if not hasattr(dev, attr):
                self._main_window.report_error('{} does not have {} attribute!'.format(new_source, attr))

    # ----------------------------------------------------------------------
    def show(self):

        try:
            self.restoreGeometry(QtCore.QSettings(APP_NAME).value("{}/geometry".format(WIDGET_NAME)))
        except:
            pass

        super(ProgramSetup, self).show()

    # ----------------------------------------------------------------------
    def accept(self):

        self.new_settings = {'source': self._ui.le_source.text(),
                             'x': self._ui.dsb_pos_x.value(),
                             'y': self._ui.dsb_pos_y.value()
                             }

        QtCore.QSettings(APP_NAME).setValue("{}/geometry".format(WIDGET_NAME), self.saveGeometry())

        super(ProgramSetup, self).accept()

    # ----------------------------------------------------------------------
    def reject(self):

        QtCore.QSettings(APP_NAME).setValue("{}/geometry".format(WIDGET_NAME), self.saveGeometry())

        super(ProgramSetup, self).reject()

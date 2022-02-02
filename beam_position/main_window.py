# Created by matveyev at 15.02.2021
APP_NAME = "PETRA_Beam_Position"

import PyTango
import logging
import numpy as np

from PyQt5 import QtWidgets, QtCore

from beam_position.settings import ProgramSetup
from beam_position.gui.main_window_ui import Ui_BeamPosition

logger = logging.getLogger(APP_NAME)

STATUS_TICK = 1000
PRECISION = 3
CRITICAL_SHIFT = 50


class BeamPosition(QtWidgets.QMainWindow):
    """
    """

    # ----------------------------------------------------------------------
    def __init__(self, options):
        """
        """
        super(BeamPosition, self).__init__()
        self._ui = Ui_BeamPosition()
        self._ui.setupUi(self)

        self.beamline = str(options.beamline).lower()

        self.reference = {'x': 0.,
                          'y': 0.}

        self.source = ''

        if not self._load_ui_settings():
            if not self._set_settings():
                self.report_error('No start settings, exit')
                raise RuntimeError('No start settings, exit')

        self._ui.lb_source.setText(f'Source: {self.source}')

        self._ui.lb_source.doubleClicked.connect(self._set_settings)
        self._ui.lb_ref_x.doubleClicked.connect(self._set_settings)
        self._ui.lb_ref_y.doubleClicked.connect(self._set_settings)

        try:
            PyTango.DeviceProxy(self.source)
        except Exception as err:
            self.report_error('Cannot connect to {}'.format(self.source), repr(err))
            raise

        self._refresh_coordinates()

        self._status_timer = QtCore.QTimer(self)
        self._status_timer.timeout.connect(self._refresh_coordinates)
        self._status_timer.start(STATUS_TICK)

    # ----------------------------------------------------------------------
    def _set_settings(self):

        dialog = ProgramSetup(self)
        if dialog.exec_() == QtWidgets.QDialog.Rejected:
            return False

        self.source = dialog.new_settings['source']
        self.reference = {'x': dialog.new_settings['x'],
                          'y': dialog.new_settings['y']}

        self._save_settings()

        self._ui.lb_source.setText(f'Source: {self.source}')

        return True

    # ----------------------------------------------------------------------
    def _refresh_coordinates(self):

        arrows = {'x': [u'\u25C0', u'\u25B6'],
                  'y': [u'\u25BC', u'\u25B2']}

        for corr in ['x', 'y']:
            getattr(self._ui, f'lb_ref_{corr}').setText(f'{self.reference[corr]:.3f}')

            pos = getattr(PyTango.DeviceProxy(self.source), 'com_{}'.format(corr))
            getattr(self._ui, f'lb_act_{corr}').setText(f'{pos:.3f}')

            dlt = pos - self.reference[corr]
            getattr(self._ui, f'lb_dlt_{corr}').setText(f'{dlt:.3f}')
            r_color = min(255, 255*abs(dlt)/CRITICAL_SHIFT)
            getattr(self._ui, f'lb_dlt_{corr}').setStyleSheet("QLabel {color: rgb(" + str(r_color) + ", 25, 25);}")

            if dlt > np.power(10., -PRECISION):
                getattr(self._ui, f'lb_arr_{corr}').setText(arrows[corr][1])
            elif dlt < -np.power(10., -PRECISION):
                getattr(self._ui, f'lb_arr_{corr}').setText(arrows[corr][0])
            else:
                getattr(self._ui, f'lb_arr_{corr}').setText('')

            getattr(self._ui, f'lb_arr_{corr}').setStyleSheet("QLabel {color: rgb(" + str(r_color) + ", 25, 25);}")

    # ----------------------------------------------------------------------
    def report_error(self, text, informative_text='', detailed_text=''):

        logger.error("Error: {}, {}, {} ".format(text, informative_text, detailed_text))

        self.msg = QtWidgets.QMessageBox()
        self.msg.setModal(False)
        self.msg.setIcon(QtWidgets.QMessageBox.Critical)
        self.msg.setText(text)
        self.msg.setInformativeText(informative_text)
        if detailed_text != '':
            self.msg.setDetailedText(detailed_text)
        self.msg.setWindowTitle("Error")
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.msg.show()

    # ----------------------------------------------------------------------
    def _close_me(self):
        logger.info("Closing the app...")
        self._save_settings()
        self._save_ui_settings()

    # ----------------------------------------------------------------------
    def _exit(self):
        self._close_me()
        QtWidgets.QApplication.quit()

    # ----------------------------------------------------------------------
    def closeEvent(self, event):
        """
        """
        self._close_me()
        event.accept()

    # ----------------------------------------------------------------------
    def _save_settings(self):

        settings = QtCore.QSettings(APP_NAME)

        settings.setValue("{}/source".format(self.beamline), self.source)

        settings.setValue("{}/x".format(self.beamline), str(self.reference['x']))
        settings.setValue("{}/y".format(self.beamline), str(self.reference['y']))

    # ----------------------------------------------------------------------
    def _save_ui_settings(self):
        """Save basic GUI settings.
        """
        settings = QtCore.QSettings(APP_NAME)

        settings.setValue("MainWindow/geometry", self.saveGeometry())
        settings.setValue("MainWindow/state", self.saveState())

    # ----------------------------------------------------------------------
    def _load_ui_settings(self):
        """Load basic GUI settings.
        """
        settings = QtCore.QSettings(APP_NAME)

        try:
            self.restoreGeometry(settings.value("MainWindow/geometry"))
        except:
            pass

        try:
            self.restoreState(settings.value("MainWindow/state"))
        except:
            pass

        try:
            self.source = settings.value("{}/source".format(self.beamline))
        except:
            return False

        if self.source is None:
            return False

        try:
            self.reference['x'] = float(settings.value("{}/x".format(self.beamline)))
        except:
            return False

        try:
            self.reference['y'] = float(settings.value("{}/y".format(self.beamline)))
        except:
            return False

        return True

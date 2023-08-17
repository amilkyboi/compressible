# module app
'''
Main GUI for the compressible flow application.
'''

import sys
import math

from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QComboBox, \
                            QPushButton, QLabel, QLineEdit, QApplication, QMessageBox

import isentropic as isen
import inverse as inv

# Prandtl-Meyer angle limit in [deg]
PM_ANGLE_LIMIT = 130.454076

class CompressibleApp(QMainWindow):
    '''
    Calculator.
    '''

    def __init__(self):
        super().__init__()

        # WINDOW -----------------------------------------------------------------------------------

        self.setWindowTitle('Compressible Flow Calculator')
        self.setGeometry(100, 100, 500, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout() # type: ignore

        # GAMMA ------------------------------------------------------------------------------------

        self.gamma_layout = QHBoxLayout()

        self.gamma_ledit = QLineEdit()
        self.gamma_layout.addWidget(QLabel('Gamma:'))
        self.gamma_layout.addWidget(self.gamma_ledit)

        self.layout.addLayout(self.gamma_layout)

        # DROPDOWN ---------------------------------------------------------------------------------

        self.dropdown = QComboBox()

        quantities = ['Mach number', 'T/T0', 'p/p0', 'rho/rho0', 'A/A* (subsonic)', \
                      'A/A* (supersonic)', 'Mach angle (deg)', 'P-M angle (deg)']

        self.dropdown.addItems(quantities)

        self.layout.addWidget(self.dropdown)

        # INPUT ------------------------------------------------------------------------------------

        self.input_layout = QHBoxLayout()

        self.input_ledit = QLineEdit()
        self.input_layout.addWidget(QLabel('Input:'))
        self.input_layout.addWidget(self.input_ledit)

        self.layout.addLayout(self.input_layout)

        # CALCULATION BUTTON -----------------------------------------------------------------------

        self.calculate_button = QPushButton('Calculate')
        self.calculate_button.clicked.connect(self.calculate)

        self.layout.addWidget(self.calculate_button)

        # RESULTS ----------------------------------------------------------------------------------

        # Support for multiple returns
        self.result_labels = []
        self.result_ledits = []

        for operation in ['Mach number', 'Mach angle (deg)', 'P-M angle (deg)', 'p/p0', \
                          'rho/rho0', 'T/T0', 'p/p*', 'rho/rho*', 'T/T*', 'A/A*']:
            result_label = QLabel(f'{operation}:')
            result_ledit = QLineEdit()
            result_ledit.setReadOnly(True)

            self.result_labels.append(result_label)
            self.result_ledits.append(result_ledit)

            self.layout.addWidget(result_label)
            self.layout.addWidget(result_ledit)

        self.central_widget.setLayout(self.layout)

    # CALL CALCULATION FUNCTIONS -------------------------------------------------------------------

    def calculate(self):
        '''
        Calls functions.
        '''

        gamma, mach_num, flow_type = self.get_mach_num()

        if mach_num is None or gamma is None:
            pass

        else:
            self.result_ledits[0].setText(str(mach_num))
            if flow_type == 'subsonic':
                self.result_ledits[1].setText('subsonic flow')
                self.result_ledits[2].setText('subsonic flow')
            else:
                try:
                    self.result_ledits[1].setText(str(math.degrees(isen.ang(mach_num))))
                    self.result_ledits[2].setText(str(math.degrees(isen.pma(gamma, mach_num))))
                except ValueError:
                    self.result_ledits[1].setText('approached domain limit')
                    self.result_ledits[2].setText('approached domain limit')
            try:
                self.result_ledits[3].setText(str(isen.pp0(gamma, mach_num)))
                self.result_ledits[4].setText(str(isen.rr0(gamma, mach_num)))
                self.result_ledits[5].setText(str(isen.tt0(gamma, mach_num)))
                self.result_ledits[6].setText(str(isen.pps(gamma, mach_num)))
                self.result_ledits[7].setText(str(isen.rrs(gamma, mach_num)))
                self.result_ledits[8].setText(str(isen.tts(gamma, mach_num)))
                self.result_ledits[9].setText(str(isen.aas(gamma, mach_num)))
            except OverflowError:
                self.show_error_popup('congrats. now lower the input')

    def get_mach_num(self):
        '''
        Gets the Mach number in the cases where the input is something else.
        '''

        # Default entry is None to indicate if an error is found
        mach_num = None

        # Flow type switch for subsonic area ratio
        flow_type = 'supersonic'

        input_name = self.dropdown.currentText()

        try:
            gamma = float(self.gamma_ledit.text())
        except ValueError:
            gamma = None
            self.show_error_popup('Invalid entry for gamma')

            return gamma, mach_num, flow_type

        try:
            input_var = float(self.input_ledit.text())
        except ValueError:
            input_var = None
            self.show_error_popup(f'Invalid entry for {input_name}')

            return gamma, mach_num, flow_type

        try:
            if input_name == 'Mach number':
                mach_num = input_var

            elif input_name == 'T/T0':
                if 0 < input_var < 1:
                    mach_num = inv.inv_stag_temp(gamma, input_var)
                else:
                    self.show_error_popup(f'Invalid entry: 0 < {input_name} < 1')

            elif input_name == 'p/p0':
                if 0 < input_var < 1:
                    mach_num = inv.inv_stag_pres(gamma, input_var)
                else:
                    self.show_error_popup(f'Invalid entry: 0 < {input_name} < 1')

            elif input_name == 'rho/rho0':
                if 0 < input_var < 1:
                    mach_num = inv.inv_stag_dens(gamma, input_var)
                else:
                    self.show_error_popup(f'Invalid entry: 0 < {input_name} < 1')

            elif input_name == 'A/A* (subsonic)':
                flow_type = 'subsonic'

                if input_var > 1:
                    mach_num = inv.inv_area_ratio(gamma, input_var, flow_type)
                else:
                    self.show_error_popup(f'Invalid entry: {input_name} > 1')

            elif input_name == 'A/A* (supersonic)':
                if input_var > 1:
                    mach_num = inv.inv_area_ratio(gamma, input_var, flow_type)
                else:
                    self.show_error_popup(f'Invalid entry: {input_name} > 1')

            elif input_name == 'Mach angle (deg)':
                if 0 < input_var < 90:
                    mach_num = inv.inv_mach_angl(math.radians(input_var))
                else:
                    self.show_error_popup(f'Invalid entry: 0 < {input_name} < 90')

            elif input_name == 'P-M angle (deg)':
                # Approximate limit of the P-M angle (i.e. after this Mach number -> infinity)
                if 0 < input_var < PM_ANGLE_LIMIT:
                    mach_num = inv.inv_pran_angl(gamma, math.radians(input_var), 'newton')
                else:
                    self.show_error_popup(f'Invalid entry: 0 < {input_name} < {PM_ANGLE_LIMIT}')

        except OverflowError:
            self.show_error_popup('congrats. now lower the input')

        return gamma, mach_num, flow_type

    # ERROR POPUP ----------------------------------------------------------------------------------

    def show_error_popup(self, err_msg):
        '''
        _summary_

        Args:
            err_msg (_type_): _description_
        '''

        error_popup = QMessageBox()
        error_popup.setIcon(QMessageBox.Icon.Warning)
        error_popup.setWindowTitle('Error')
        error_popup.setText(err_msg)
        error_popup.setStandardButtons(QMessageBox.StandardButton.Ok)
        error_popup.exec()

def main():
    '''
    _summary_
    '''

    app    = QApplication(sys.argv)
    window = CompressibleApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

# module app
'''
Main GUI for the compressible flow application.
'''

import sys
import math

from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QComboBox, \
                            QPushButton, QLabel, QLineEdit, QApplication

import isentropic as isen
import inverse as inv

class CompressibleApp(QMainWindow):
    '''
    Calculator.
    '''

    def __init__(self):
        super().__init__()

        # WINDOW -----------------------------------------------------------------------------------

        self.setWindowTitle('Compressible Flow Calculator')
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout() # type: ignore

        # INPUT 1 ----------------------------------------------------------------------------------

        self.gamma_layout = QHBoxLayout()

        self.gamma_label = QLabel('Gamma:')
        self.gamma_ledit = QLineEdit()
        self.gamma_layout.addWidget(self.gamma_label)
        self.gamma_layout.addWidget(self.gamma_ledit)

        self.layout.addLayout(self.gamma_layout)

        # DROPDOWN ---------------------------------------------------------------------------------

        self.dropdown = QComboBox()
        self.dropdown.addItem('Mach number')
        self.dropdown.addItem('T/T0')
        self.dropdown.addItem('p/p0')
        self.dropdown.addItem('rho/rho0')
        self.dropdown.addItem('Mach angle (deg)')
        self.dropdown.addItem('P-M angle (deg)')

        self.layout.addWidget(self.dropdown)

        # INPUT 2 ----------------------------------------------------------------------------------

        self.input_layout = QHBoxLayout()

        self.input_label = QLabel('Input:')
        self.input_ledit = QLineEdit()
        self.input_layout.addWidget(self.input_label)
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

        gamma, mach_num = self.get_mach_num()

        self.result_ledits[0].setText(str(mach_num))
        self.result_ledits[1].setText(str(math.degrees(isen.ang(mach_num))))
        self.result_ledits[2].setText(str(math.degrees(isen.pma(gamma, mach_num))))
        self.result_ledits[3].setText(str(isen.pp0(gamma, mach_num)))
        self.result_ledits[4].setText(str(isen.rr0(gamma, mach_num)))
        self.result_ledits[5].setText(str(isen.tt0(gamma, mach_num)))
        self.result_ledits[6].setText(str(isen.pps(gamma, mach_num)))
        self.result_ledits[7].setText(str(isen.rrs(gamma, mach_num)))
        self.result_ledits[8].setText(str(isen.tts(gamma, mach_num)))
        self.result_ledits[9].setText(str(isen.aas(gamma, mach_num)))

    def get_mach_num(self):
        '''
        Gets the Mach number in the cases where the input is something else.
        '''

        gamma      = float(self.gamma_ledit.text())
        input_var  = float(self.input_ledit.text())

        input_name = self.dropdown.currentText()

        # Default entry is the Mach number
        mach_num = input_var

        if input_name == 'T/T0':
            mach_num = inv.inv_stag_temp(gamma, input_var)
        elif input_name == 'p/p0':
            mach_num = inv.inv_stag_pres(gamma, input_var)
        elif input_name == 'rho/rho0':
            mach_num = inv.inv_stag_dens(gamma, input_var)
        elif input_name == 'Mach angle (deg)':
            mach_num = inv.inv_mach_angl(input_var)
        elif input_name == 'P-M angle (deg)':
            mach_num = inv.inv_pran_angl(gamma, input_var)

        return gamma, mach_num

if __name__ == '__main__':
    app    = QApplication(sys.argv)
    window = CompressibleApp()
    window.show()
    app.exec()

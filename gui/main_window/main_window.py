from PyQt6.QtCore import QSize, Qt, QRect
from PyQt6.QtGui import QAction, QFont, QPalette, QValidator, QIntValidator, QIcon
from PyQt6.QtWidgets import QMainWindow, QSizePolicy, QWidget, QFrame, QGridLayout, QSpacerItem, QLabel, QVBoxLayout, \
    QPushButton, QListView, QTableWidget, QAbstractScrollArea, QMenuBar, QMenu, QDialog, QLineEdit, QSpinBox, QComboBox

from gui.dialogs.add_section_dialog import AddSectionDialog, EXIST_SECTION_INDEX
import Globals
from gui.section.section import Section
from gui.section.section_certification import SectionCertification
from gui.section.section_dcpn import SectionDcpn
from gui.section.section_redmine import SectionRedmine
from outlook.outlook import Outlook


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        # Main Window Configuration
        self.setFixedSize(1000, 680)
        self.setWindowTitle('Nvidia Weekly Report')

        self.setIconSize(QSize(100,20))
        # Top Frame ( Title and Buttons )
        #   Frame Configuration
        self.top_frame = QFrame(self)
        self.top_frame.setFixedSize(1000, 200)
        self.top_grid_layout = QGridLayout()
        self.top_frame.setLayout(self.top_grid_layout)
        #   Title
        self.title = QLabel('Weekly Report Generator')
        font = QFont()
        font.setPointSize(20)
        self.title.setFont(font)
        self.top_grid_layout.addWidget(self.title, 0, 1, 1, 2, Qt.AlignmentFlag.AlignLeft)
        #   Buttons
        #       Content Configuration
        self.buttons_frame = QFrame(self.top_frame)
        self.top_grid_layout.addWidget(self.buttons_frame, 1, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        self.buttons_layout = QVBoxLayout()
        self.buttons_frame.setLayout(self.buttons_layout)
        horizontal_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.buttons_layout.addItem(horizontal_spacer)
        #       Add Section Button
        self.add_section_btn = QPushButton('Add Section')
        self.add_section_btn.clicked.connect(self.add_section)
        self.buttons_layout.addWidget(self.add_section_btn)
        # Bottom Frame ( Report Sections )
        #   Frame Configuration
        self.bottom_frame = QFrame(self)
        self.bottom_frame.setGeometry(QRect(0, 200, 1000, 480))
        self.bottom_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.bottom_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.section_lay = QVBoxLayout()
        self.bottom_frame.setLayout(self.section_lay)
        # Menu Bar
        self.menu_bar = self.menuBar().addMenu('Options')
        self.action_send_mail = QAction('&Send Mail')
        self.action_get_last_report = QAction('&Get Last Report')
        self.menu_bar.addAction(self.action_get_last_report)
        self.menu_bar.addAction(self.action_send_mail)


        self.show()
        self.report_info = {}

        outlook = Outlook()
        #last_status = outlook.get_last_mail(filter_subject='Weekly Status')

    def add_section(self):
        w = AddSectionDialog()

        if w.exec() == QDialog.DialogCode.Accepted:
            section = None
            if w.radio_btn_group.checkedId() == EXIST_SECTION_INDEX:
                section_name = w.output_variables_list[0]
                if section_name == 'RedMine':
                    section = SectionRedmine(section_name)
                elif section_name == 'DCPN':
                    section = SectionDcpn(section_name)
                elif section_name == 'Certification':
                    section = SectionCertification(section_name)
                elif section_name == 'QA Runs':
                    section = SectionCertification(section_name)
            else:
                section_name, status_desc = w.output_variables_list
                section = Section(section_name, status_desc)
            if section:
                self.section_lay.addWidget(section)



import datetime
import os
import pickle

from dateutil.relativedelta import relativedelta
from PyQt6.QtCore import Qt, QRect, pyqtSlot
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QMainWindow, QSizePolicy, QFrame, QGridLayout, QSpacerItem, QLabel, QVBoxLayout, \
    QPushButton, QDialog, QComboBox, QMessageBox, QWidget

from gui.dialogs.add_section_dialog import AddSectionDialog, EXIST_SECTION_INDEX
import Globals
from gui.dialogs.select_time_dialog import SelectTimeDialog
from gui.dialogs.send_mail_dialog import SendMailDialog
from gui.section.section import Section
from gui.section.section_automation import SectionAutomation
from gui.section.section_certification import SectionCertification
from gui.section.section_dcpn import SectionDcpn
from gui.section.section_redmine import SectionRedmine
from message_handler.message_builder import MessageBuilder
from message_handler.message_parser import MessageParser
from outlook.outlook import Outlook


class MainWindow(QMainWindow):

    def __init__(self, app_path):
        super().__init__()
        self.app_path = app_path
        # Main Window Configuration
        self.setFixedSize(1000, 680)
        self.setWindowTitle('Nvidia Weekly Report')
        self.setWindowIcon(QIcon(os.path.join(self.app_path, 'Images\\logo.png')))
        # Top Frame ( Title and Buttons )
        #   Frame Configuration
        self.top_frame = QFrame(self)
        self.top_frame.setFixedSize(1000, 200)
        self.top_grid_layout = QGridLayout()
        self.top_frame.setLayout(self.top_grid_layout)
        #   Title
        self.title = QLabel('<h1>Weekly Report Generator</h1>')
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
        self.file_menu = self.menuBar().addMenu('File')
        self.options_menu = self.menuBar().addMenu('Options')
        self.get_reports = self.options_menu.addMenu('Get Reports From Mail')
        self.view_mail = QAction('View Report as Mail')
        self.view_mail.triggered.connect(self.view_report)
        self.action_send_mail = QAction('Send Report on Mail')
        self.action_send_mail.triggered.connect(self.send_mail)
        self.action_get_last_report = QAction('Last Report')
        self.get_reports_from_period = QAction('View Reports From Period')
        self.action_get_last_report.triggered.connect(self.get_last_report)
        self.get_reports_from_period.triggered.connect(self.view_reports)
        self.save_file = QAction('Save')
        self.save_file.triggered.connect(self.save_content)
        self.load_file = QAction('Load')
        self.load_file.triggered.connect(self.load_content)
        self.get_reports.addAction(self.action_get_last_report)
        self.get_reports.addAction(self.get_reports_from_period)
        self.options_menu.addSeparator()
        self.options_menu.addAction(self.view_mail)
        self.options_menu.addAction(self.action_send_mail)
        self.file_menu.addAction(self.save_file)
        self.file_menu.addAction(self.load_file)
        # Show Window
        self.show()
        # Additional class variables
        self.report_info = {}
        self.outlook = Outlook()
        self.msg_builder = MessageBuilder(self.app_path)
        self.msg_parser = MessageParser()
        self.sections = []

    def send_mail(self):
        if self.sections:
            self.msg_builder.build_message(self.sections)
            answer = QMessageBox.question(self, 'Sending mail', 'Are you sure you want to send mail?',
                                          QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if answer == QMessageBox.StandardButton.Yes:
                w = SendMailDialog()
                if w.exec() == QDialog.DialogCode.Accepted:
                    if not w.to.text():
                        QMessageBox.warning(self, 'Sending mail',
                                            "You didn't fill the people you want to send the mail."
                                            " Cancelling mail send...")
                        return
                    self.msg_builder.build_message(self.sections)
                    self.outlook.send_html_mail(html_text=self.msg_builder.msg,
                                                subject=f"Weekly Status ({self.msg_builder.get_today_date()})",
                                                to=w.to.text(),
                                                cc=w.cc.text())

    def view_report(self):
        if self.sections:
            self.msg_builder.build_message(self.sections)
            self.msg_builder.view_msg_as_html()

    def view_reports(self):

        w = SelectTimeDialog()
        if w.exec() == QDialog.DialogCode.Accepted:
            str_num, date = w.choice.split(' ')
            num = int(str_num)
            if date == 'years':
                min_time = datetime.date.today() - relativedelta(years=num)
            elif date == 'months':
                min_time = datetime.date.today() - relativedelta(months=num)
            elif date == 'weeks':
                min_time = datetime.date.today() - relativedelta(weeks=num)
            elif date == 'days':
                min_time = datetime.date.today() - relativedelta(days=num)
            else:
                QMessageBox.critical(self, 'Get Last Mails', f'invalid date {date}')
                return
            messages = self.outlook.get_last_mails(filter_subject='Weekly Status', start_time=min_time)
            self.msg_builder.merge_messages(messages)
            self.msg_builder.view_msg_as_html()

    def get_last_report(self):
        last_status = self.outlook.get_last_mail(filter_subject='Weekly Status')
        html_txt = last_status.HTMLBody
        sections = self.msg_parser.parse_html(html_txt)
        self.add_sections_from_dict(sections)

    def get_sections_info(self):
        sections_info = {}
        for section in self.sections:
            sections_info[section.section_name] = section.get_all_lines_info()
        return sections_info

    def save_content(self):
        if self.sections:
            username = os.getlogin().replace(' ', '_')
            save_dict = self.get_sections_info()
            with open(os.path.join(self.app_path, f"saved_files\\{username}.pcl"), 'wb') as f:
                pickle.dump(save_dict, f)

    def load_content(self):
        self.remove_all_sections()
        username = os.getlogin().replace(' ', '_')
        try:
            with open(os.path.join(self.app_path, f"saved_files\\{username}.pcl"), 'rb') as f:
                load_content = pickle.load(f)
        except Exception:
            return
        self.add_sections_from_dict(load_content)

    def add_sections_from_dict(self, content_dict):
        for section_name in content_dict:
            if section_name == 'RedMine':
                section = SectionRedmine(section_name)
            elif section_name == 'DCPN':
                section = SectionDcpn(section_name)
            elif section_name == 'Certification':
                section = SectionCertification(section_name)
            elif section_name == 'QA Runs':
                section = SectionCertification(section_name)
            elif section_name == 'Automation':
                section = SectionAutomation(section_name)
            else:
                if isinstance(content_dict[section_name][1]['Status'], QComboBox):
                    status_type = Globals.DescriptionType.STATUS
                else:
                    status_type = Globals.DescriptionType.PERCENTAGE
                section = Section(section_name, status_type)
            for idx in content_dict[section_name]:
                section.set_line(idx, content_dict[section_name][idx])
            section.section_deleted.connect(self.remove_section_from_list)
            self.section_lay.addWidget(section)
            self.sections.append(section)

    def remove_all_sections(self):
        for section in self.sections:
            self.sections.remove(section)
            section.destroy_section()

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
                elif section_name == 'Automation':
                    section = SectionAutomation(section_name)
            else:
                section_name, status_desc = w.output_variables_list
                section = Section(section_name, status_desc)
            if section:
                section.section_deleted.connect(self.remove_section_from_list)
                self.sections.append(section)
                self.section_lay.addWidget(section)

    @pyqtSlot(QWidget)
    def remove_section_from_list(self, section):
        self.sections.remove(section)

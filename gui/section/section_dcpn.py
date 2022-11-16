from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QLineEdit, QComboBox

import Globals
from gui.section.section import Section


class SectionDcpn(Section):

    link_prefix = 'https://techpartnerhub.vmware.com/support/my-cases/'

    def add_content(self):
        task_edit = QLineEdit()
        task_edit.setPlaceholderText('Enter RM ticket...')
        task_edit.setValidator(QIntValidator())
        status = QComboBox()
        status.addItems(Globals.dcpn_status_items)
        comments_edit = QLineEdit()
        comments_edit.setPlaceholderText('Enter your comment here...')
        self.content_lay.addWidget(task_edit, self.content_current_row, 0)
        self.content_lay.addWidget(status, self.content_current_row, 1)
        self.content_lay.addWidget(comments_edit, self.content_current_row, 2)
        self.content_current_row += 1



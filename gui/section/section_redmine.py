from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QLineEdit, QComboBox

import Globals
from gui.section.section import Section


class SectionRedmine(Section):

    link_prefix = 'https://redmine.mellanox.com/issues/'

    def add_content(self):
        task_edit = QLineEdit()
        task_edit.setPlaceholderText('Enter RM ticket...')
        task_edit.setValidator(QIntValidator())
        status = QComboBox()
        status.addItems(Globals.rm_status_items)
        comments_edit = QLineEdit()
        comments_edit.setPlaceholderText('Enter your comment here...')
        self.content_lay.addWidget(task_edit, len(self.content_list), 0)
        self.content_lay.addWidget(status, len(self.content_list), 1)
        self.content_lay.addWidget(comments_edit, len(self.content_list), 2)
        self.content_list.append([task_edit, status, comments_edit])

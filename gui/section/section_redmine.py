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

    def set_line(self, line_num, content_dict):
        while len(self.content_list) <= line_num:
            self.add_content()
        self._set_task(line_num, content_dict['Ticket'])
        self._set_status_description(line_num, content_dict['Status'])
        self._set_comment(line_num, content_dict['Comment'])

    def _set_status_description(self, row, status: str):
        self.content_list[row][1].setCurrentIndex(Globals.rm_status_items.index(status))

    def get_line_info(self, line_num):
        content = {'Ticket': self.get_task(line_num), 'Status': self.get_status_description(line_num),
                   'Comment': self.get_comment(line_num)}
        return content

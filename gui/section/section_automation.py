from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QLineEdit, QComboBox

import Globals
from gui.section.section_redmine import SectionRedmine


class SectionAutomation(SectionRedmine):

    link_prefix = 'http://l-gerrit.mtl.labs.mlnx:8080/c/PLACEHOLDER/+'

    def add_content(self):
        task_edit = QLineEdit()
        task_edit.setPlaceholderText('Enter gerrit number...')
        task_edit.setValidator(QIntValidator())
        repo = QComboBox()
        repo.addItems(Globals.repositories)
        status = QComboBox()
        status.addItems(Globals.automation_items)
        comments_edit = QLineEdit()
        comments_edit.setPlaceholderText('Enter your comment here...')
        self.content_lay.addWidget(task_edit, len(self.content_list), 0)
        self.content_lay.addWidget(repo, len(self.content_list), 1)
        self.content_lay.addWidget(status, len(self.content_list), 2)
        self.content_lay.addWidget(comments_edit, len(self.content_list), 3)
        self.content_list.append([task_edit, repo, status, comments_edit])

    def set_line(self, line_num, content_dict):
        while len(self.content_list) <= line_num:
            self.add_content()
        self._set_task(line_num, content_dict['Ticket'])
        self._set_repository(line_num, content_dict['Repo'])
        self._set_status_description(line_num, content_dict['Status'])
        self._set_comment(line_num, content_dict['Comment'])

    def get_line_info(self, line_num):
        content = {'Ticket': self.get_task(line_num),
                   'Repo': self.get_repository(line_num),
                   'Status': self.get_status_description(line_num),
                   'Comment': self.get_comment(line_num)}
        return content

    def _set_repository(self, row, repo):
        self.content_list[row][1].setCurrentIndex(Globals.repositories.index(repo))

    def get_repository(self, row):
        return self.content_list[row][1].currentText()

    def _set_status_description(self, row, status: str):
        self.content_list[row][2].setCurrentIndex(Globals.automation_items.index(status))

    def get_status_description(self, row):
        return self.content_list[row][2].currentText()

    def _set_comment(self, row, text):
        self.content_list[row][3].setText(text)

    def get_comment(self, row):
        return self.content_list[row][3].text()



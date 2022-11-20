from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QCursor
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QLineEdit, QSpinBox, QComboBox, QLabel, \
    QMenu, QLayoutItem

import Globals


class Section(QWidget):
    num_of_columns = 3

    def __init__(self, section_name, description_type: Globals.DescriptionType = None, parent=None):
        super().__init__(parent)
        # Main Layout
        self.lay = QHBoxLayout()
        self.lay.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setLayout(self.lay)

        # Section Name Layout
        self.section_name_lay = QVBoxLayout()
        self.section_name_lay.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.lay.addLayout(self.section_name_lay)
        self.lbl = QLabel(section_name)
        self.section_name_lay.addWidget(self.lbl)

        # Content Layout
        self.content_lay = QGridLayout()
        self.content_lay.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.lay.addLayout(self.content_lay)
        place_holder = QWidget()
        self.content_lay.addWidget(place_holder, 0, 0)
        self.content_lay.setRowMinimumHeight(0, 30)
        self.content_lay.setColumnMinimumWidth(0, 75)
        self.content_list = [[place_holder]]

        self.description_type = description_type
        self.section_name = section_name
        self.add_content()

        # Context menu
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.open_menu)

    def open_menu(self):
        context_menu = QMenu()
        add_line = context_menu.addAction('Add line')
        add_line.triggered.connect(self.add_content)
        line_to_remove = context_menu.addMenu('Remove content line')
        for row in range(1, len(self.content_list)):
            line_to_remove.addAction(f'line {row}').triggered.connect(
                lambda x, chosen_row=row: self.remove_line(chosen_row))
        context_menu.addSeparator()
        delete_section = context_menu.addAction('Delete section')
        delete_section.triggered.connect(self.destroy_section)

        cursor = QCursor()
        context_menu.exec(cursor.pos())

    def add_content(self):
        task_edit = QLineEdit()
        task_edit.setPlaceholderText('Enter task summary here...')
        if self.description_type == Globals.DescriptionType.PERCENTAGE:
            status = QSpinBox()
            status.setRange(0, 100)
            status.setSuffix('%')
            status.setSingleStep(10)
        else:
            status = QComboBox()
            status.addItems(Globals.description_status_items)
        comments_edit = QLineEdit()
        comments_edit.setPlaceholderText('Enter your comment here...')
        self.content_lay.addWidget(task_edit, len(self.content_list), 0)
        self.content_lay.addWidget(status, len(self.content_list), 1)
        self.content_lay.addWidget(comments_edit, len(self.content_list), 2)
        self.content_list.append([task_edit, status, comments_edit])

    def _set_task(self, row, text: str):
        self.content_list[row][0].setText(text)

    def get_task(self, row):
        return self.content_list[row][0].text()

    def _set_percentage(self, row, num: int):
        self.content_list[row][1].setValue(num)

    def get_percentage(self, row):
        return self.content_list[row][1].value()

    def _set_status_description(self, row, status: str):
        self.content_list[row][1].setCurrentIndex(Globals.description_status_items.index(status))

    def get_status_description(self, row):
        return self.content_list[row][1].currentText()

    def _set_comment(self, row, text):
        self.content_list[row][2].setText(text)

    def get_comment(self, row):
        return self.content_list[row][2].text()

    def set_line(self, line_num, content_dict):
        while len(self.content_list) < line_num:
            self.add_content()
        self._set_task(line_num, content_dict['Task'])
        if self.description_type == Globals.DescriptionType.PERCENTAGE:
            self._set_percentage(line_num, int(content_dict['Status']))
        else:
            self._set_status_description(line_num, content_dict['Status'])
        self._set_comment(line_num, content_dict['Comment'])

    def get_line_info(self, line_num):
        status = self.get_percentage(line_num) if self.description_type == Globals.DescriptionType.PERCENTAGE\
            else self.get_status_description(line_num)
        content = {'Task': self.get_task(line_num), 'Status': status,
                   'Comment': self.get_comment(line_num)}

        return content

    def get_all_lines_info(self):
        all_content = {}
        for idx in range(1, len(self.content_list)):
            all_content[idx] = self.get_line_info(idx)
        return all_content

    def remove_line(self, row):
        if self.content_lay.rowCount() > 2:
            self.content_list.pop(row)
            self.update_grid(row)

    def update_grid(self, row):
        for col in range(self.content_lay.columnCount()):
            item = self.content_lay.itemAtPosition(row, col)
            self.content_lay.removeItem(item)
            item_content = item.widget()
            item_content.setParent(None)
            item_content.deleteLater()
            del item

        for row in range(len(self.content_list)):
            for col in range(len(self.content_list[row])):
                if isinstance(self.content_list[row][col], QWidget):
                    self.content_lay.addWidget(self.content_list[row][col], row, col)
                else:
                    self.content_lay.addLayout(self.content_list[row][col], row, col)

    def destroy_section(self):
        # destroying content
        for row in range(len(self.content_list)):
            for col in range(self.content_lay.columnCount()):
                item = self.content_lay.itemAtPosition(row, col)
                self.content_lay.removeItem(item)
                if item:
                    item_content = item.widget()
                    if item_content:
                        item_content.setParent(None)
                        item_content.deleteLater()
                    del item
        self.section_name_lay.removeWidget(self.lbl)
        self.lbl.setParent(None)
        self.lbl.deleteLater()
        self.deleteLater()

from PyQt6.QtWidgets import QGridLayout, QLineEdit, QSpinBox, QComboBox, QLabel, \
    QCheckBox, QFrame

import Globals
from gui.section.section import Section


class SectionCertification(Section):

    def add_content(self):
        component = QComboBox()
        component.addItems(Globals.tested_components_items)
        lbl = QLabel('-')
        task_edit = QLineEdit()
        task_edit.setPlaceholderText('Enter component version here...')
        check_boxes = []
        for cert in Globals.certification_suites_items:
            check_boxes.append(QCheckBox(cert))
        boxes_lay = QGridLayout()
        max_in_row = 4
        current_row = 0
        current_col = 0
        for box in check_boxes:
            boxes_lay.addWidget(box, current_row, current_col)
            current_col += 1
            if current_col == max_in_row:
                current_col = 1
                current_row += 1
        boxes_frame = QFrame()
        boxes_frame.setLayout(boxes_lay)
        boxes_frame.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        nics = QComboBox()
        nics.addItems(Globals.tested_nics_item)
        status = QSpinBox()
        status.setRange(0, 100)
        status.setSuffix('%')
        status.setSingleStep(10)
        comments_edit = QLineEdit()
        comments_edit.setPlaceholderText('Enter your comment here...')
        self.content_lay.addWidget(component, len(self.content_list), 0)
        self.content_lay.addWidget(lbl, len(self.content_list), 1)
        self.content_lay.addWidget(task_edit, len(self.content_list), 2)
        self.content_lay.addWidget(boxes_frame, len(self.content_list), 3)
        self.content_lay.addWidget(nics, len(self.content_list), 4)
        self.content_lay.addWidget(status, len(self.content_list), 5)
        self.content_lay.addWidget(comments_edit, len(self.content_list), 6)
        self.content_list.append([component, lbl, task_edit, boxes_frame, nics, status, comments_edit])

    def set_line(self, line_num: int, content_dict: dict):
        while len(self.content_list) <= line_num:
            self.add_content()
        self._set_component(line_num, content_dict['Component'])
        self._set_task(line_num, content_dict['Task'])
        self._set_box_checks(line_num, content_dict['Types'])
        self._set_nic(line_num, content_dict['Nic'])
        self._set_percentage(line_num, int(content_dict['Status']))
        self._set_comment(line_num, content_dict['Comment'])

    def get_line_info(self, line_num):
        content = {'Component': self.get_component(line_num),
                   'Task': self.get_task(line_num),
                   'Types': self.get_box_checks(line_num),
                   'Nic': self.get_nic(line_num),
                   'Status': self.get_percentage(line_num),
                   'Comment': self.get_comment(line_num)}
        return content

    def _set_component(self, row: int, component: str):
        self.content_list[row][0].setCurrentIndex(Globals.tested_components_items.index(component))

    def get_component(self, row: int):
        return self.content_list[row][0].currentText()

    def _set_task(self, row, text: str):
        self.content_list[row][2].setText(text)

    def get_task(self, row):
        return self.content_list[row][2].text()

    def _set_percentage(self, row, num: int):
        self.content_list[row][5].setValue(num)

    def get_percentage(self, row):
        return self.content_list[row][5].value()

    def _set_box_checks(self, row, checked_boxes: list):
        for child in self.content_list[row][3].children():
            if isinstance(child, QCheckBox) and child.text() in checked_boxes:
                child.setChecked(True)

    def get_box_checks(self, row):
        checked_boxes = []
        for child in self.content_list[row][3].children():
            if isinstance(child, QCheckBox) and child.isChecked():
                checked_boxes.append(child.text())
        return checked_boxes

    def _set_nic(self, row: int, nic: str):
        self.content_list[row][4].setCurrentIndex(Globals.tested_nics_item.index(nic))

    def get_nic(self, row: int):
        return self.content_list[row][4].currentText()

    def _set_comment(self, row, text):
        self.content_list[row][6].setText(text)

    def get_comment(self, row):
        return self.content_list[row][6].text()

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



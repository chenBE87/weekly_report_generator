from PyQt6.QtWidgets import QGridLayout, QLineEdit, QSpinBox, QComboBox, QLabel, \
    QCheckBox, QFrame

import Globals
from gui.section.section_certification import SectionCertification


class SectionQaRuns(SectionCertification):

    check_boxes = []

    def add_content(self):
        component = QComboBox()
        component.addItems(Globals.tested_components_items)
        lbl = QLabel('-')
        task_edit = QLineEdit()
        task_edit.setPlaceholderText('Enter component version here...')

        for cert in Globals.certification_suites_items:
            self.check_boxes.append(QCheckBox(cert))
        boxes_lay = QGridLayout()
        max_in_row = 4
        current_row = 0
        current_col = 0
        for box in self.check_boxes:
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
        self.content_lay.addWidget(component, self.content_current_row, 0)
        self.content_lay.addWidget(lbl, self.content_current_row, 1)
        self.content_lay.addWidget(task_edit, self.content_current_row, 2)
        self.content_lay.addWidget(boxes_frame, self.content_current_row, 3)
        self.content_lay.addWidget(nics, self.content_current_row, 4)
        self.content_lay.addWidget(status, self.content_current_row, 5)
        self.content_lay.addWidget(comments_edit, self.content_current_row, 6)
        self.content_current_row += 1



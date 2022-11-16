from PyQt6.QtCore import Qt, QStringListModel
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QRadioButton, QHBoxLayout, QDialogButtonBox, QMessageBox, QLineEdit, \
    QLabel, QButtonGroup, QFormLayout, QComboBox, QListView

import Globals
from Globals import template_sections

NEW_SECTION_INDEX = 1
EXIST_SECTION_INDEX = 0


class AddSectionDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Initiate main layout and variables.
        self.output_variables_list = None
        self.default_btns = {}
        self.section_lbl = QLabel('')
        lay = QVBoxLayout(self)
        lay.setAlignment(Qt.AlignmentFlag.AlignTop)
        # Create Radio Buttons
        #       Create the radio buttons. set "Checked" the first button.
        self.radio_btn_exist = QRadioButton("Select exists template")
        self.radio_btn_exist.setChecked(True)
        self.radio_btn_new = QRadioButton("Select General")

        #       Set the radio buttons group.
        self.radio_btn_layout = QHBoxLayout()
        self.radio_btn_layout.addWidget(self.radio_btn_exist)
        self.radio_btn_layout.addWidget(self.radio_btn_new)

        #       Set the radio buttons group.
        self.radio_btn_group = QButtonGroup(self)
        self.radio_btn_group.addButton(self.radio_btn_exist, EXIST_SECTION_INDEX)
        self.radio_btn_group.addButton(self.radio_btn_new, NEW_SECTION_INDEX)
        self.radio_btn_group.buttonClicked.connect(self.radio_btn_selected)

        # Set the widgets for the "Select from exist" option.
        #       Set the widgets for the "Select from exist template" option.
        self.exists_section_lay = QVBoxLayout()
        self.exists_section_lay.setAlignment(Qt.AlignmentFlag.AlignTop)
        existing_list = QStringListModel()
        existing_list.setStringList(template_sections)
        self.exist_template_list_view = QListView()
        self.exist_template_list_view.setModel(existing_list)
        self.exist_template_list_view.setFixedSize(200, 200)
        self.exists_section_lay.addWidget(self.exist_template_list_view)

        # Set the widgets for the "Select from new" option.

        self.new_section_lay = QFormLayout()
        self.new_section_lay.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.FieldsStayAtSizeHint)

        #       Section name row
        self.new_section_name_lbl = QLabel('Section name: ')
        self.new_section_name_input = QLineEdit('')
        self.new_section_lay.addRow(self.new_section_name_lbl, self.new_section_name_input)

        #       Section status presentation
        self.new_section_status_lbl = QLabel('Status update format: ')
        self.new_section_status_cb = QComboBox()
        self.new_section_status_cb.addItems([name.value for name in Globals.DescriptionType])
        self.new_section_lay.addRow(self.new_section_status_lbl, self.new_section_status_cb)

        # Set the Dialog window's buttons.
        dialog_button = QDialogButtonBox()
        dialog_button.setOrientation(Qt.Orientation.Horizontal)
        dialog_button.setStandardButtons(QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok)

        # Organize the widget in the window.
        lay.addLayout(self.radio_btn_layout)
        lay.addWidget(self.section_lbl)
        lay.addLayout(self.exists_section_lay)
        lay.addLayout(self.new_section_lay)
        lay.addStretch()
        lay.addWidget(dialog_button)

        # Display the "Select from exist" widgets.
        self.set_new_section_visible_status(False)
        self.section_lbl.setText('<u><h2>Select From Built-in Sections:<h2></u>')

        # Set window's style ( GUI representation ).
        self.resize(self.width() + 50, self.height())
        self.setWindowTitle("Add New Report Section")

        # Connect dialog buttons to method.
        dialog_button.accepted.connect(self.accept)
        dialog_button.rejected.connect(self.reject)

    """
    Function - accept ( Override )

    Brief - Callback for the "accept" button. The accept will send the variables for creating the new button.

    Description - 
                    1. If the user is in the "Select from exist" option:
                        1.1. if the user didn't choose button from list, a warning message will be displayed.
                        1.2. Else, list of variables will be sent 
                             ( list = [selected_radio_button_index, new_button_name, 
                                       new_button_procedure, new_button_description]
                             ).
                    2. Else:
                        2.1. If one of the string field, that uer needs to 
                             fill, is empty, a warning message will be displayed.
                        2.2. Else, list of variables will be sent 
                             ( list = [selected_radio_button_index, new_button_name, 
                                       new_button_procedure, new_button_description]
                             ).
    """

    def accept(self):
        if self.radio_btn_group.checkedId() == EXIST_SECTION_INDEX:
            if len(self.exist_template_list_view.selectedIndexes()) == 0:
                QMessageBox.warning(self, 'Section not selected', 'No Section template has been selected !')
            else:
                section = self.exist_template_list_view.selectedIndexes()[0].data()
                self.output_variables_list = [section]
        else:
            if self.new_section_name_input.text() == '' or self.new_section_status_cb.currentText() == '':
                QMessageBox.warning(self, 'Section not selected', 'Please fill all fields for creating new section !')
            else:
                self.output_variables_list = [self.new_section_name_input.text(),
                                              Globals.DescriptionType(self.new_section_status_cb.currentText())]
        super().accept()  # <-- call parent method

    """
    Function - radio_btn_selected

    Brief - Callback that is invoked when radio button has been selected.

    Parameters  -  
                    btn_id: int - selected button ID

    Description - 
                    1. The method will switch between window's options, according to the input button id:
                        1.1. "Select from exist" option.
                        1.2. "Select from new" option.
    """

    def radio_btn_selected(self):
        set_new_visible = True
        checked_btn = self.radio_btn_group.checkedId()
        if checked_btn != NEW_SECTION_INDEX:
            set_new_visible = False
        self.set_new_section_visible_status(set_new_visible)
        self.set_builtin_section_visible_status(not set_new_visible)

    """
    Function - set_new_btn_visible_status

    Brief - Set visible attribute for "Select from new" option widget 

    Parameters  -  
                    status: bool - value to assign tp the setVisible method

    """

    def set_new_section_visible_status(self, status):
        if status:
            self.section_lbl.setText('<u><h2>Create new Section:<h2></u>')
        self.new_section_name_lbl.setVisible(status)
        self.new_section_name_input.setVisible(status)
        self.new_section_status_lbl.setVisible(status)
        self.new_section_status_cb.setVisible(status)

    """
    Function - set_existing_btn_visible_status

    Brief - Set visible attribute for "Select from exist" option widget 

    Parameters  -  
                    status: bool - value to assign tp the setVisible method

    """

    def set_builtin_section_visible_status(self, status):
        if status:
            self.section_lbl.setText('<u><h2>Select From Built-in Sections:<h2></u>')
        self.exist_template_list_view.setVisible(status)

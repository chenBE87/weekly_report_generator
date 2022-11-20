
import Globals
from gui.section.section_redmine import SectionRedmine


class SectionDcpn(SectionRedmine):

    link_prefix = 'https://techpartnerhub.vmware.com/support/my-cases/'

    def add_content(self):
        super().add_content()
        self.content_list[-1][0].setPlaceholderText('Enter DCPN ticket...')
        self.content_list[-1][1].clear()
        self.content_list[-1][1].addItems(Globals.dcpn_status_items)

    def _set_status_description(self, row, status: str):
        self.content_list[row][1].setCurrentIndex(Globals.dcpn_status_items.index(status))



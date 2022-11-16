from enum import Enum


class DescriptionType(Enum):
    PERCENTAGE = 'By %'
    STATUS = 'By Description'


description_status_items = ['TBD', 'Future Task', 'WIP', 'Blocked', 'On Hold', 'Done']
rm_status_items = ['New', 'In Progress', 'Fixed', 'Need Fix Verify', 'Closed', 'External',
                   'Rejected', 'Close (Rejected)']
dcpn_status_items = ['Waiting for vmware', 'Waiting for partner', 'Fixed', 'Won\'t fix', 'Waiver']
tested_nics_item = ['ConnectX5', 'ConnectX6', 'ConnectX7', 'BlueFiled2']
tested_components_items = ['FW', 'Driver']
certification_suites_items = ['IOVP', 'ENS', 'RDMA']
template_sections = ['RedMine', 'DCPN', 'Certification', 'QA Runs']

import re

from bs4 import BeautifulSoup

import Globals


class MessageParser:


    def parse_html(self, html_txt: str):
        sections = {}
        data = BeautifulSoup(html_txt, 'html.parser')
        #data1 = data.find_all('ul')
        content = data.find_all("li")
        while content:
            section_name = content.pop(0).text
            section_name = section_name.strip()
            section_bullets = []
            if content:
                section_content = content[0]
                if 'level1' not in section_content['style']:
                    while content and 'level1' not in content[0]['style']:
                        section_bullets.append(content.pop(0))
            if section_name.lower() == 'RedMine'.lower():
                section_name = 'RedMine'
                section_info = self._parse_redmine_section(section_bullets)
            elif section_name == 'DCPN':
                section_info = self._parse_dcpn_section(section_bullets)
            elif section_name == 'Certification':
                section_info = self._parse_certification_section(section_bullets)
            elif section_name == 'QA Runs':
                section_info = self._parse_qa_runs_section(section_bullets)
            else:
                section_info = None
            sections[section_name] = section_info
        return sections
                # self._add_generic_section(section)
        # for li in data1.find_all("li"):
        #     li.name
        #     print(li.text, end=" ")

    def _parse_qa_runs_section(self, section_bullets: list):
        return self._parse_certification_section(section_bullets)

    def _parse_certification_section(self, section_bullets: list):
        cert_section = {}
        is_first_bullet = True
        idx = 1
        info_dict = {}
        for bullet in section_bullets:
            if 'level2' in bullet['style']:
                if not is_first_bullet:
                    cert_section[idx] = {info_dict}
                    info_dict = {}
                    idx += 1
                info_dict = {}
                txt = bullet.text
                if ' - ' in txt or f' {chr(8211)} ' in txt:
                    minus_char = '-' if ' - ' in txt else chr(8211)
                    component, task = txt.split(f' {minus_char} ')
                    if component not in Globals.tested_components_items:
                        task = component
                        component = 'Driver'
                else:
                    component = 'Driver'
                    task = txt
                info_dict['Component'] = component
                info_dict['Task'] = task
            elif 'level3' in bullet['style']:
                types: str = bullet.text
                valid_txt = [i for i in types.split(', ') if i in Globals.certification_suites_items]
                types = ', '.join(valid_txt)
                info_dict['Types'] = types
            elif 'level4' in bullet['style']:
                txt = bullet.text
                if ' - ' in txt or f' {chr(8211)} ' in txt:
                    minus_char = '-' if ' - ' in txt else chr(8211)
                    nic, stat_and_comm = txt.split(f' {minus_char} ')
                    nic.replace('-', '')
                    if nic not in Globals.tested_nics_item:
                        for saved_nic in Globals.tested_nics_item:
                            if nic.lower() == saved_nic.lower():
                                nic = saved_nic
                                break
                        else:
                            nic = Globals.tested_nics_item[0]
                    info_dict['Nic'] = nic
                    match = re.search(r'\(.*\)', stat_and_comm)
                    if match:
                        comment = match.group(0).replace('(', '').replace(')', '').strip()
                    else:
                        comment = ''
                    match = re.search(r'\d+% Done', stat_and_comm)
                    if match:
                        status = match.group(0).split('%')[0].strip()
                    else:
                        status = '0'
                    info_dict['Status'] = status
                    info_dict['Comment'] = comment

                else:
                    status = '0'
                    comment = ''
                info_dict['Status'] = status
                info_dict['Comment'] = comment
        cert_section[idx] = info_dict
        return cert_section

    def _parse_redmine_section(self, section_bullets: list):
        rm_section = {}
        idx = 1
        for bullet in section_bullets:
            info_dict = {}
            txt = bullet.text
            ticket = ''
            status = ''
            comment = ''
            if ' - ' in txt or f' {chr(8211)} ' in txt:
                minus_char = '-' if ' - ' in txt else chr(8211)
                ticket, stat_and_comm = txt.split(f' {minus_char} ')
                match = re.search(r'\(.*\)', stat_and_comm)
                if match:
                    comment = match.group(0).replace('(', '').replace(')', '').strip()
                status = stat_and_comm.split(' (')[0].strip()
            info_dict['Ticket'] = ticket
            info_dict['Status'] = status
            info_dict['Comment'] = comment
            rm_section[idx] = info_dict
            idx += 1


        return rm_section

    def _parse_dcpn_section(self, section_bullets: list):
        return self._parse_redmine_section(section_bullets)

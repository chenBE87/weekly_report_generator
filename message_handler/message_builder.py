import datetime
import os
import re
import webbrowser
import Globals


class MessageBuilder:

    def __init__(self, saved_files_full_dir):
        self.output_file = f'{saved_files_full_dir}\\saved_files\\msg_builder_html.html'
        self.msg = ''

    def build_message(self, sections: list):
        self.msg = '<!DOCTYPE html><html><body lang=en-IL link=\"#0563C1\" vlink=\"#954F72\"' \
                   " style='word-wrap:break-word'><div>"
        self._add_title()
        for section in sections:
            if section.section_name == 'RedMine':
                self._add_rm_section(section)
            elif section.section_name == 'DCPN':
                self._add_rm_section(section)
            elif section.section_name == 'Certification':
                self._add_certification_section(section)
            elif section.section_name == 'QA Runs':
                self._add_qa_runs_section(section)
            elif section.section_name == 'Automation':
                self._add_automation_line(section)
            else:
                self._add_generic_section(section)
        self._add_message_suffix()
        with open(self.output_file, 'w') as f:
            f.write(self.msg)

    def view_msg_as_html(self):
        url = f'file://{os.path.realpath(self.output_file)}'
        webbrowser.open(url)

    def _add_qa_runs_section(self, section):
        self._add_certification_section(section)

    def _add_certification_section(self, section):
        self._open_bullet()
        self._add_bullet_line(1, section.section_name)
        section_content = section.get_all_lines_info()
        for component_name in self.get_certification_components(section_content):
            self._open_bullet()
            self._add_bullet_line(2, component_name)
            for cert_types in self.get_cert_component_test_types(component_name, section_content):
                self._open_bullet()
                self._add_bullet_line(3, cert_types)
                for section_line in self.get_section_lines_by_cert_types(cert_types, section_content):
                    self._open_bullet()
                    nic = section_line['Nic']
                    status = section_line['Status']
                    txt = f'{nic} - {self.get_percentage_text(int(status))}'
                    comment = section_line['Comment']
                    if comment:
                        txt += f' ( {comment} )'
                    self._add_bullet_line(4, txt)
                    self._close_bullet()
                self._close_bullet()
            self._close_bullet()
        self._close_bullet()

    def _add_generic_section(self, section):
        self._open_bullet()
        self._add_bullet_line(1, section.section_name)
        section_content = section.get_all_lines_info()
        for idx in section:
            task = section_content[idx]['Task']
            status = section_content[idx]['Status']
            comment = section_content[idx]['Comment']
            if section.description_type == Globals.DescriptionType.PERCENTAGE:
                status_txt = self.get_percentage_text(int(status))
            else:
                status_txt = status
            txt = f'{task} - {status_txt}'
            if comment:
                txt += f' ( {comment} )'
            self._open_bullet()
            self._add_bullet_line(2, txt)
            self._close_bullet()
        self._close_bullet()

    @staticmethod
    def get_certification_components(section):
        comp_versions = set()
        for idx in section:
            component = section[idx]['Component']
            component_name = section[idx]['Task']
            comp_versions.add(f'{component} - {component_name}')
        return comp_versions

    @staticmethod
    def get_cert_component_test_types(component_name, section):
        types = set()
        for idx in section:
            component = section[idx]['Component']
            name = section[idx]['Task']
            current_component = f'{component} - {name}'
            if current_component == component_name:
                types.add(", ".join(section[idx]['Types']))
        return types

    @staticmethod
    def get_section_lines_by_cert_types(types, section):
        section_lines = []
        for idx in section:
            current_types = ", ".join(section[idx]['Types'])
            if current_types == types:
                section_lines.append(section[idx])
        return section_lines

    def _add_rm_section(self, section):
        self._open_bullet()
        self._add_bullet_line(1, section.section_name)
        section_content = section.get_all_lines_info()
        for idx in section_content:
            self._open_bullet()
            ticket = section_content[idx]['Ticket']
            link = f'{section.link_prefix}/{ticket}'
            ticket_link_txt = self.create_href(link, ticket)
            status = section_content[idx]['Status']
            comment = section_content[idx]['Comment']
            txt = f'{ticket_link_txt} - {status}'
            if comment:
                txt += f' ( {comment} )'
            self._add_bullet_line(2, txt)
            self._close_bullet()
        self._close_bullet()

    def _add_dcpn_line(self, section):
        self._add_rm_section(section)

    def _add_automation_line(self, section):
        self._open_bullet()
        self._add_bullet_line(1, section.section_name)
        section_content = section.get_all_lines_info()
        for idx in section_content:
            self._open_bullet()
            ticket = section_content[idx]['Ticket']
            repo = section_content[idx]['Repo']
            link = f'{section.link_prefix.replace("PLACEHOLDER", repo)}/{ticket}'
            ticket_link_txt = self.create_href(link, ticket)
            status = section_content[idx]['Status']
            comment = section_content[idx]['Comment']
            txt = f'{ticket_link_txt} - {status}'
            if comment:
                txt += f' ( {comment} )'
            self._add_bullet_line(2, txt)
            self._close_bullet()
        self._close_bullet()

    def _add_title(self):
        html_title = "<p class=MsoNormal><b><span lang=EN-US style='font-size:22.0pt'>" \
                     f"Weekly Status ({self.get_today_date()})<o:p></o:p></span></b></p></br></br>"
        self.msg += html_title

    @staticmethod
    def get_today_date():
        return datetime.date.today().strftime('%d.%m.%Y')

    def _add_new_line(self):
        new_line = '<p class=MsoNormal><span lang=EN-US><o:p>&nbsp;</o:p></span></p>'
        self.msg += new_line

    def _open_bullet(self):
        self.msg += f"<ul style='margin-top:0cm' type=disc>"

    def _add_bullet_line(self, level: int, text):
        self.msg += f"<li class=MsoListParagraph style='margin-left:0cm;mso-list:l1 level{str(level)} lfo3'>" \
                    f"<span lang=EN-US>{text}<o:p></o:p></span></li>"

    def get_percentage_text(self, percentage: int):
        color = self.get_percentage_color(percentage)
        txt = f"<span style='color:#{color}'>{str(percentage)}% Done</span>"
        return txt

    @staticmethod
    def get_percentage_color(percentage: int):
        if percentage == 0:
            return '0000B0'  # Blue
        if 0 < percentage <= 50:
            return 'CB4335'  # Red
        if 50 < percentage <= 80:
            return 'F5B041'  # Orange
        return '00B050'  # Green

    @staticmethod
    def create_href(link, text):
        href = f"<a href=\"{link}\"><span style='font-size:10.0pt;font-family:\"Arial\",sans-serif;color:#1D428A;" \
               f"background:white;text-decoration:none'>{text}</span></a>"
        return href

    def _close_bullet(self):
        self.msg += "</ul>"

    def _add_message_suffix(self):
        self.msg += '</div></body></html>'

    def merge_messages(self, messages):
        msg = '<!DOCTYPE html><html><body lang=en-IL link=\"#0563C1\" vlink=\"#954F72\"' \
                   " style='word-wrap:break-word'><div>"
        for message in messages:
            html_str: str = message.HTMLBody
            html_str = re.search(r'<div.*</div>', html_str).group(0)
            msg += html_str
        msg += '</body></html>'
        with open(self.output_file, 'w') as f:
            f.write(msg)

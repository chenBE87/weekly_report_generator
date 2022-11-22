import datetime

import win32com.client

INBOX_FOLDER = 6
SENT_FOLDER = 5


class Outlook:

    def __init__(self):
        self.outlook = win32com.client.Dispatch('outlook.application')
        self.mapi = self.outlook.GetNamespace("MAPI")
        self.sent_box = self.mapi.GetDefaultFolder(SENT_FOLDER)

    def get_last_mail(self, filter_subject):
        messages = self.sent_box.Items
        messages = messages.Restrict(f"@SQL=(urn:schemas:httpmail:subject LIKE '%{filter_subject}%')")
        if messages:
            messages.Sort("[ReceivedTime]", Descending=True)
            return messages[0]
        return []

    def get_last_mails(self, filter_subject: str, start_time: datetime.date):
        filtered_messages = []
        messages = self.sent_box.Items
        messages = messages.Restrict(f"@SQL=(urn:schemas:httpmail:subject LIKE '%{filter_subject}%')")
        if messages:
            messages.Sort("[ReceivedTime]", Descending=True)
            for message in messages:
                if message.SentOn.date() >= start_time:
                    filtered_messages.append(message)
        return filtered_messages

    def send_html_mail(self, subject, html_text, to, cc):
        new_mail = self.outlook.CreateItem(0)
        new_mail.Subject = subject
        new_mail.HTMLBody = html_text
        new_mail.To = to
        if cc:
            new_mail.cc = cc
        new_mail.Send()

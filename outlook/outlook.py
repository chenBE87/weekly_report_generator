import win32com.client
import os
from datetime import datetime, timedelta

INBOX_FOLDER = 6
SENT_FOLDER = 5


class Outlook:

    def __init__(self):
        outlook = win32com.client.Dispatch('outlook.application')
        mapi = outlook.GetNamespace("MAPI")
        self.inbox = mapi.GetDefaultFolder(SENT_FOLDER)

    def get_last_mail(self, filter_subject):
        messages = self.inbox.Items
        messages = messages.Restrict(f"@SQL=(urn:schemas:httpmail:subject LIKE '%{filter_subject}%')")
        if messages:
            messages.Sort("[ReceivedTime]", Descending=True)
            return messages[0]
        return None

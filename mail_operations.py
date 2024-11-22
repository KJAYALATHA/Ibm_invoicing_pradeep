import os

import win32com.client

import file_operations
from log_handler import custom_logger

log = custom_logger()

app_type = "Outlook.Application"
name_space = "MAPI"
err_msg = "Failed to read outlook email with error : {}"


def send_outlook_email(file_to_attach=None, add_sub=None):
    """
    method to send an outlook365 email for notification
    :param add_sub: additional subject line if user wishes to share status
    :param file_to_attach: full file path to attach
    :return: None if success, else error
    """
    config_path = os.path.join(os.getcwd(), "config.cfg")
    to_email = file_operations.load_config_file(config_path, str('Email'), "TO_EMAIL")
    subject = file_operations.load_config_file(config_path, str('Email'), "SUBJECT")
    try:
        html = """
                <html>
                    <head></head>
                        <body>
                            <h1>Hi """ + to_email + """ !</h1>
                                <p>
                                    This is an Automatic email triggered by the
                                    """ + subject + """ robot to notify user on the bot
                                    execution progress / status to you.
                                </p>
                                <p>Kind regards,<br>
                                    <em>Quess Corp </em>
                                </p>
                        </body>
                </html>
                """
        outlook = win32com.client.Dispatch(app_type)
        mail = outlook.CreateItem(0)
        #mail.To = to_email
        mail.To = 'jayalatha.k@quesscorp.com'
        mail.Subject = subject + add_sub
        # mail.Body = 'Message body'
        mail.HTMLBody = html  # this field is optional
        # To attach a file to the email (optional):
        if file_to_attach is not None:
            attachment = file_to_attach
            mail.Attachments.Add(attachment)
        mail.Send()
    except Exception as e:
        log.exception(err_msg.format(e))


def read_outlook_email_by_subject(subject):
    """
    method to read out look email based on subject
    :param subject:
    :return: body content if true, else null
    """
    try:
        outlook_emails = win32com.client.Dispatch(app_type).GetNamespace(name_space)
        # "6" refers to the index of a folder - in this case,
        # the inbox. You can change that number to reference
        # any other folder
        root_folder = outlook_emails.Folders.Item(1)
        inbox = root_folder.Folders['Inbox']
        messages = inbox.Items
        messages = messages.Restrict("[Subject] = '{}'".format(subject))
        message = messages.GetLast()
        body_content = message.body
        return body_content
    except Exception as e:
        log.exception(err_msg.format(e))
        return ""


def download_email_attachment_by_type(partial_file_name, sub_folder_name):
    """
    method to download an attachment matching partial file name
    :param sub_folder_name:
    :param partial_file_name:
    :return: true if successful, else false
    """
    bln_found = False
    try:
        file_operations.create_folder(os.path.join(os.getcwd(), "downloads"))
        file_operations.create_folder(os.path.join(os.getcwd(), "downloads", partial_file_name))
        outlook_emails = win32com.client.Dispatch(app_type).GetNamespace(name_space)
        # "6" refers to the index of a folder - in this case,
        # the inbox. You can change that number to reference
        # any other folder
        root_folder = outlook_emails.Folders.Item(1)
        inbox = root_folder.Folders['Inbox']
        type4 = inbox.Folders.item(sub_folder_name)
        messages = type4.Items
        for message in messages:
            if message.UnRead:
                attachments = message.Attachments
                if len(attachments) == 0:
                    continue
                for att in attachments:
                    attachment_name = att.FileName.lower()
                    if partial_file_name.lower() in attachment_name.lower():
                        att.SaveASFile(os.path.join(os.getcwd(), "downloads", partial_file_name, attachment_name))
                        log.info("Downloaded the file {} at location {}"
                                 .format(attachment_name, os.path.join(os.getcwd(), "downloads", partial_file_name)))
                        message.UnRead = False
                        bln_found = True
        if not bln_found:
            log.info("No Unread emails for {} to download".format(partial_file_name))
            bln_found = False
    except Exception as e:
        log.exception("Failed to download email attachment of type : {} with error {} ".format(partial_file_name, e))
        return False
    return bln_found


def download_email_attachment_by_extn(partial_file_name, sub_folder_name):
    """
    method to download an attachment matching partial file name
    :param sub_folder_name:
    :param partial_file_name:
    :return: true if successful, else false
    """
    bln_found = False
    try:
        file_operations.create_folder(os.path.join(os.getcwd(), "downloads"))
        file_operations.create_folder(os.path.join(os.getcwd(), "downloads", partial_file_name))
        outlook_emails = win32com.client.Dispatch(app_type).GetNamespace(name_space)
        # "6" refers to the index of a folder - in this case,
        # the inbox. You can change that number to reference
        # any other folder
        root_folder = outlook_emails.Folders.Item(1)
        inbox = root_folder.Folders['Inbox']
        type4 = inbox.Folders.item(sub_folder_name)
        messages = type4.Items
        for x, message in enumerate(messages):
            if message.UnRead:
                attachments = message.Attachments
                if len(attachments) == 0:
                    continue
                for att in attachments:
                    attachment_name = att.FileName.lower()
                    if partial_file_name.lower() == "." + attachment_name.lower().split(".")[1]:
                        att.SaveASFile(os.path.join(os.getcwd(), "downloads", partial_file_name, attachment_name))
                        log.info("Downloaded the file {} at location {}"
                                 .format(attachment_name, os.path.join(os.getcwd(), "downloads", partial_file_name)))
                        message.UnRead = False
                        bln_found = True
        if not bln_found:
            log.info("No Unread emails for {} to download".format(partial_file_name))
            bln_found = False
    except Exception as e:
        log.exception("Failed to download email attachment of type : {} with error {} ".format(partial_file_name, e))
        return False
    return bln_found

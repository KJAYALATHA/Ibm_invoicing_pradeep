import json
import os
from glob import glob
from pathlib import Path

import pandas as pd

import file_operations
from app_monitor_handler import monitor
from browser_handler import get_browser, close_all_browsers
from log_handler import custom_logger
from mail_operations import send_outlook_email
from pages.qpay_billing_days import QpayBillingDaysPage
from pages.qpay_home import QpayHomePage
from pages.qpay_login import QpayLoginPage
from prepare_billing_days_report import prepare_billing_days_report, \
    prepare_ss_allowance_days_report, prepare_mi_allowance_days_report

log = custom_logger()


# ----------------COMMENT THE BELOW LINE WHEN PACKAGING ---------------------------------------------------
# os.environ['QPAY_PORTAL_LOGIN_ID'] = '10002147'  # DEV
# os.environ['QPAY_PORTAL_PWD'] = 'Quess@123'  # DEV
# os.environ['QPAY_PORTAL_URL'] = 'https://azqpayroll.quesscorp.com/'
# os.environ['QPAY_PORTAL_LOGIN_ID'] = '10017890'  --- PROD
# os.environ['QPAY_PORTAL_PWD'] = 'Reurs4004*'  --- PROD
# os.environ['QPAY_PORTAL_URL'] = 'https://piqpayrollsim.quesscorp.com/'

# os.environ['HEADLESS_FLAG'] = "False"


# ----------------COMMENT THE ABOVE LINE WHEN PACKAGING ---------------------------------------------------


def create_env_json():
    """
    method to create json file for environment variables
    :return: json of environment variables
    """
    dict_json = None
    try:
        json_obj = json.dumps({**{}, **os.environ}, indent=4)
        dict_json = json.loads(json_obj)
    except SyntaxError as se:
        log.error(
            "{} error, environment variables parsing error, {}".format("Qpay Invoicing", create_env_json.__name__),
            se)
    return dict_json


def check_env_keys_loaded(json_str):
    """
    method to check if all required environment variables are loaded on the OS
    :param json_str:
    :return: true if success, else false
    """
    success = False
    try:
        keys = ['QPAY_PORTAL_LOGIN_ID', 'QPAY_PORTAL_PWD', 'INPUT_FILE_LOCATION', 'HEADLESS_FLAG',
                'NOTIFICATION_EMAIL', 'QPAY_PORTAL_URL', 'BROWSER_WAIT', 'ELEMENT_WAIT']
        missing_keys = [key for key in keys if key not in json_str]
        # checking for values if any of the required values is blank we terminate the run
        missing_values = [key for key, value in json_str.items() if key in keys and len(value) == 0 or value == " "]
        if len(missing_values) > 0:
            log.error("{}: Error in env keys, missing values for keys {}".format("Infosys Invoicing", missing_values))
            raise SystemExit()
        count = len(missing_keys)
        if count > 0:
            log.error(
                "{} error, {} number of env keys were missing, {}".format("Qpay Invoicing", count,
                                                                          create_env_json.__name__))
            return False
        else:
            success = True
    except SyntaxError as se:
        log.error(
            "{} error, required environment variables were not loaded, {} ".format("Qpay Invoicing",
                                                                                   create_env_json.__name__),
            se)
    return success


def qpay_invoicing(template_type):
    driver = None
    result = None
    try:
        # reading configurations
        qpay_url = file_operations.load_config_file(config_path, str('Qpay'), "QPAY_URL")
        qpay_user_id = file_operations.load_config_file(config_path, str('Qpay'), "QPAY_USER_ID")
        qpay_passwd = file_operations.load_config_file(config_path, str('Qpay'), "QPAY_PASSWORD")
        browser = file_operations.load_config_file(config_path, str('Browser'), "BROWSER_TYPE")
        # check the app status before stating the upload process
        # if monitor(qpay_url):
        # ------------------Launching driver and browser with application url--------------------------------
        driver = get_browser(browser, qpay_url)
        login = QpayLoginPage(driver)
        home = QpayHomePage(driver)
        bill = QpayBillingDaysPage(driver)
        # Login to qpay portal
        result = login.qpay_login(qpay_user_id, qpay_passwd)
        if not result:
            msg = "Failed to login to qpay portal"
            send_outlook_email(add_sub=msg)
            exit(-1)
        # navigate to qpay home page and select a report type
        print("login successs by jaya")
        result &= home.select_qpay_report_type()
        print(result,"jaya11111")
        if not result:
            msg = "Failed to select billing report from qpay home page"
            send_outlook_email(add_sub=msg)
            exit(-1)
        # navigate to qpay billing days page and select a import type
        result &= bill.download_template(template_type)
        print(result,"check sow")
        if not result:
            msg = "Failed to download report template {} from qpay billing days page".format(template_type)
            send_outlook_email(add_sub=msg)
            exit(-1)
        # prepare the billing days based on the template downloaded
        # ---------------------------------------------------------------------------------------------------
        result &= prepare_upload_file()

        if not result:
            print("comming in false result")

            msg = "Failed to generate upload report".format(template_type)
            send_outlook_email(add_sub=msg)
            exit(-1)
        print("line numbe4 130")



        # ---------------------------------------------------------------------------------------------------
        # navigate to qpay billing days page and upload an updated import type file
        up_flag = file_operations.load_config_file(config_path, str('Input'), "UPLOAD_FLAG")
        if up_flag == 'True':
            for fn in [f for f in list(Path(os.path.join(os.getcwd(), input_location)).glob('*_Upload.xlsx'))]:
                result &= bill.upload_file(fn)
                if not result:
                    msg = 'Failed to upload the file {} on the billing days page, due to incomplete file'.format(fn)
                    send_outlook_email(add_sub=msg)
                    exit(-1)
    # else:
    #     log.error('Qpay Portal is not accessible')

    except Exception as e:
        msg = "Error {} while downloading the qpay billing report".format(e)
        log.error(msg)
        result = False
    finally:
        log.info(
            "Uploading documents to qpay task finished, check email for success or failure message")
        driver.quit()
        close_all_browsers()
    return result


def qpay_invoicing_integration(type_of_template):
    # env_json = create_env_json()
    # if env_json is None:
    #     return False
    # flag = check_env_keys_loaded(env_json)
    # if not flag:
    #     return False
    # values are :  Billable Days | Arrear Billable Days | Billable Report
    qpay_invoicing(type_of_template)


def prepare_upload_file():
    claim_df = None
    inv_merge_df = None
    try:
        if os.path.exists(os.path.join(os.getcwd(), input_location,  "claim.xlsx")):
            claim_df = pd.read_excel(os.path.join(os.getcwd(), input_location, "claim.xlsx"), index_col=None)
            claim_df.drop(columns={'Remarks'}, inplace=True)
            claim_df.drop_duplicates(inplace=True)
        if os.path.exists(os.path.join(os.getcwd(), input_location, "invoice.xlsx")):
            invoice_df = pd.read_excel(os.path.join(os.getcwd(), input_location, "invoice.xlsx"), index_col=None)
            #jayalatha changed drop column names
            invoice_df.drop(
                columns={'TalentID', 'Total Amount', 'Total Invoicing Value', 'Remarks', 'Key_Invoice', 'Claim Year-Month',
                         'Claim Start Date', 'Claim End Date', 'Employee Name'}, inplace=True)
            inv_merge_df = pd.merge(claim_df, invoice_df, on='PO Number')
            inv_merge_df.drop_duplicates(inplace=True)
            # handle Total Invoicing hours as 0 if Total Hours is 0
            inv_merge_df['Total Invoicing Hours'] = inv_merge_df.apply(
                lambda x: x['Total Hours'] if x['Total Hours'] < 1 else x['Total Invoicing Hours'], axis=1)
            inv_merge_df = inv_merge_df[inv_merge_df['Total Hours'] > 0]
        extract_df = pd.read_excel(os.path.join(os.getcwd(), input_location, "extracted.xlsx"), index_col=None)
        # Need to Fix from here
        if os.path.exists(os.path.join(os.getcwd(), input_location, "claim.xlsx")) \
                & os.path.exists(os.path.join(os.getcwd(), input_location, "invoice.xlsx")):
            final_extract_inv_df = pd.concat([inv_merge_df, extract_df])
        else:
            final_extract_inv_df = extract_df
        final_extract_inv_df = final_extract_inv_df[~pd.isna(final_extract_inv_df['Total Hours'])]
        emp_master_df = pd.read_excel(os.path.join(os.getcwd(), "IBM Master Tracker.xlsx"), index_col=None)
        final_df = pd.merge(final_extract_inv_df, emp_master_df, left_on='TalentID', right_on='Client ID')
        final_df.to_excel(os.path.join(os.getcwd(), input_location, "timesheet_invoicing_final.xlsx"), index=False)
        prepare_billing_days_report(r'timesheet_invoicing_final.xlsx')
        # shift & standby allowance
        if os.path.exists(os.path.join(os.getcwd(), input_location, "invoice.xlsx")):
            invoice_df = pd.read_excel(os.path.join(os.getcwd(), input_location, "invoice.xlsx"), index_col=None)
            final_ss_all_df = pd.merge(invoice_df, emp_master_df, left_on='TalentID', right_on='Client ID')
            final_ss_all_df = final_ss_all_df[final_ss_all_df['Total Amount'] > 0]
            final_ss_all_df.to_excel(os.path.join(os.getcwd(), input_location, "final_ss_allowance.xlsx"), index=False)
            prepare_ss_allowance_days_report(r'final_ss_allowance.xlsx')
        else:
            final_df = final_df[final_df['Total Amount'] > 0]
            final_df.drop(columns=['Key'], inplace=True)
            final_df.rename(columns={'Key_Invoice': 'Key'}, inplace=True)
            final_df.to_excel(os.path.join(os.getcwd(), input_location, "final_ss_allowance.xlsx"), index=False)
            prepare_ss_allowance_days_report(r'final_ss_allowance.xlsx')
        # mobile and internet allowance
        if os.path.exists(os.path.join(os.getcwd(), input_location, "allowance.xlsx")):
            allowance_df = pd.read_excel(os.path.join(os.getcwd(), input_location, "allowance.xlsx"), index_col=None)
            allowance_df.drop(columns=['Claim Type'], inplace=True)
            allowance_df['Total Invoicing Value'] = allowance_df['Total Amount']
            new_all_df = allowance_df.groupby(
                ['Employee Name', 'TalentID', 'Claim Year-Month', 'Claim Start Date', 'Claim End Date', 'Total Amount',
                 'PO Number', 'Remarks', 'Key'], as_index=False)['Total Invoicing Value'].sum()
            final_mi_all_df = pd.merge(new_all_df, emp_master_df, left_on='TalentID', right_on='Client ID')
            final_mi_all_df.to_excel(os.path.join(os.getcwd(), input_location, "final_mi_allowance.xlsx"), index=False)
            prepare_mi_allowance_days_report(r'final_mi_allowance.xlsx')
        
        msg = 'Upload activity of IBM invoicing for GBS completed'
        print(msg,"succcessfull in jayalatha")
        #jayalatha commented
        #send_outlook_email(add_sub=msg)
        return True
    except (IndexError, AttributeError, ValueError):
        msg = 'Oops...something unexpected happened in upload activity of IBM invoicing for GBS'
        send_outlook_email(add_sub=msg)
        return False


if __name__ == '__main__':
    config_path = os.path.join(os.getcwd(), "config.cfg")
    temp_type = file_operations.load_config_file(config_path, str('Input'), "TEMPLATE_TYPE")
    input_location = file_operations.load_config_file(config_path, str('Input'), "INPUT_FILE_LOCATION")
    qpay_invoicing_integration(temp_type)
    prepare_upload_file()

import datetime
import os
from pathlib import Path

import pandas as pd

from db import read_qpay_employee_db
from log_handler import custom_logger

log = custom_logger()


def unique_id():
    """
    method to generate a unique id based on current time seconds and milliseconds
    :return:
    """
    return int(datetime.datetime.now().strftime("%S%f"))


def prepare_billing_days_report(ts_file):
    template_path = list(Path(os.path.join(os.getcwd(), "downloads")).glob('*BillingDays_Template.xlsx'))[0]
    ts_file_path = list(Path(os.path.join(os.getcwd(), "downloads")).glob('*{}'.format(ts_file)))[0]
    print(ts_file,"prepareee")

    try:
        emp_df = read_qpay_employee_db()
        print(len(emp_df),"check sowthri")
        temp_df = pd.read_excel(template_path, index_col=None)
        ts_df = pd.read_excel(ts_file_path, index_col=None, dtype=str)
        ts_df['EmpID'] = ts_df['EmpID'].apply(str)
        emp_df['radar_code'] = emp_df['radar_code'].apply(str)
        ts_df = ts_df.merge(emp_df, left_on='EmpID', right_on='radar_code')
        ts_df.to_excel("checkj.xlsx")
        for i in ts_df.index:
            input_num = unique_id()
            start_dt = ts_df.loc[i, 'Claim Start Date']
            end_dt = ts_df.loc[i, 'Claim End Date']
            temp_df.loc[i, 'EMPLOYEE_CODE'] = ts_df.loc[i, 'Qpay ID']
            cycle_date = ts_df.loc[i, 'Claim End Date']
            temp_df.loc[i, 'PAY_PERIOD'] = " ".join(
                [pd.to_datetime(cycle_date).strftime("%B"), pd.to_datetime(cycle_date).strftime("%Y")])
            temp_df.loc[i, 'BILLABLE_DAYS'] = ts_df.loc[i, 'Total Invoicing Hours']
            temp_df.loc[i, 'SERVICE_CHARGE_TYPE'] = 'BILL TO RATE'
            if i > 0:
                if ts_df.loc[i - 1, 'PO Number'] != ts_df.loc[i, 'PO Number']:
                    temp_df.loc[i, 'INPUT_NUMBER'] = input_num
                else:
                    
                    temp_df.loc[i, 'INPUT_NUMBER'] = temp_df.loc[i - 1, 'INPUT_NUMBER']
            else:
                temp_df.loc[i, 'INPUT_NUMBER'] = input_num
            temp_df.loc[i, 'MATERIALCODE'] = 4101  # <--- Is this fixed Material Code
            temp_df.loc[i, 'TS_START_DATE'] = pd.to_datetime(start_dt).strftime("%d.%m.%Y")
            temp_df.loc[i, 'TS_END_DATE'] = pd.to_datetime(end_dt).strftime("%d.%m.%Y")
            temp_df.loc[i, 'REMARK'] = ts_df.loc[i, 'Key']
            temp_df.loc[i, 'SHIPPING_PARTNER_CODE'] = ""
            temp_df.loc[i, 'BILLING_PARTNER_CODE'] = ""
            # temp_df.loc[i, 'ADDRESSCODE'] = ts_df.loc[i, 'addresscode']
            temp_df.loc[i, 'GST_GROUP_NAME'] = ts_df.loc[i, 'gstgroupname']
            temp_df.loc[i, 'LEAVE'] = ""
            temp_df.loc[i, 'MODE'] = 'ADD'
        temp_df.to_excel(r"downloads\Billing_Days_TS_Upload.xlsx", index=False)
    except (ValueError, IndexError, AttributeError, TypeError) as e:
        log.error("Function {} failed due to error {}".format(prepare_billing_days_report.__name__, e))


# prepare_billing_days_report('timesheet_handler_magic.xlsx')


def prepare_ss_allowance_days_report(ts_file):
    template_path = list(Path(os.path.join(os.getcwd(), "downloads")).glob('*BillingDays_Template.xlsx'))[0]
    ts_file_path = list(Path(os.path.join(os.getcwd(), "downloads")).glob('*{}'.format(ts_file)))[0]
    try:
        emp_df = read_qpay_employee_db()
        print(emp_df.columns)
        temp_df = pd.read_excel(template_path, index_col=None)
        ts_df = pd.read_excel(ts_file_path, index_col=None, dtype=str)
        
        ts_df['EmpID'] = ts_df['EmpID'].apply(str)
        emp_df['radar_code'] = emp_df['radar_code'].apply(str)
        ts_df = ts_df.merge(emp_df, left_on='EmpID', right_on='radar_code')
        print(len(ts_df),"check sowthrii")
        print(ts_df.head())
        for i in ts_df.index:
            input_num = unique_id()
            start_dt = ts_df.loc[i, 'Claim Start Date']
            end_dt = ts_df.loc[i, 'Claim End Date']
            temp_df.loc[i, 'EMPLOYEE_CODE'] = ts_df.loc[i, 'Qpay ID']
            cycle_date = ts_df.loc[i, 'Claim End Date']
            temp_df.loc[i, 'PAY_PERIOD'] = " ".join(
                [pd.to_datetime(cycle_date).strftime("%B"), pd.to_datetime(cycle_date).strftime("%Y")])
            temp_df.loc[i, 'BILLABLE_DAYS'] = 1
            temp_df.loc[i, 'SERVICE_CHARGE_TYPE'] = 'BILL TO RATE'
            if i > 0:
                if ts_df.loc[i - 1, 'PO Number'] != ts_df.loc[i, 'PO Number']:
                    temp_df.loc[i, 'INPUT_NUMBER'] = input_num
                else:
                    temp_df.loc[i, 'INPUT_NUMBER'] = temp_df.loc[i - 1, 'INPUT_NUMBER']
            else:
                temp_df.loc[i, 'INPUT_NUMBER'] = input_num
            print(temp_df.loc[i, 'EMPLOYEE_CODE'] ,"employee code by jaya")
            print(temp_df.loc[i, 'INPUT_NUMBER'],"check by jaya")
            temp_df.loc[i, 'OTHER_ALLOWANCE'] = ts_df.loc[i, 'Total Amount']
            temp_df.loc[i, 'MATERIALCODE'] = 4152  # <--- Is this fixed Material Code
            temp_df.loc[i, 'TS_START_DATE'] = pd.to_datetime(start_dt).strftime("%d.%m.%Y")
            temp_df.loc[i, 'TS_END_DATE'] = pd.to_datetime(end_dt).strftime("%d.%m.%Y")
            #jayalatha commented for testing
            #temp_df.loc[i, 'REMARK'] = "shift allowance-{}".format(ts_df.loc[i, 'Key'])
            #temp_df.loc[i, 'REMARK'] = "shift allowance-{}".format(ts_df.loc[i, 'Key'])
            temp_df.loc[i, 'SHIPPING_PARTNER_CODE'] = ""
            temp_df.loc[i, 'BILLING_PARTNER_CODE'] = ""
            # temp_df.loc[i, 'ADDRESSCODE'] = ts_df.loc[i, 'addresscode']
            temp_df.loc[i, 'GST_GROUP_NAME'] = ts_df.loc[i, 'gstgroupname']
            temp_df.loc[i, 'LEAVE'] = ""
            temp_df.loc[i, 'MODE'] = 'ADD'
        temp_df.to_excel(r"downloads\Billing_Days_SS_Upload.xlsx", index=False)
    except (ValueError, IndexError, AttributeError, TypeError) as e:
        log.error("Function {} failed due to error {}".format(prepare_billing_days_report.__name__, e))


def prepare_mi_allowance_days_report(ts_file):
    template_path = list(Path(os.path.join(os.getcwd(), "downloads")).glob('*BillingDays_Template.xlsx'))[0]
    ts_file_path = list(Path(os.path.join(os.getcwd(), "downloads")).glob('*{}'.format(ts_file)))[0]
    try:
        emp_df = read_qpay_employee_db()
        temp_df = pd.read_excel(template_path, index_col=None)
        ts_df = pd.read_excel(ts_file_path, index_col=None, dtype=str)
        ts_df['EmpID'] = ts_df['EmpID'].apply(str)
        emp_df['radar_code'] = emp_df['radar_code'].apply(str)
        ts_df = ts_df.merge(emp_df, left_on='EmpID', right_on='radar_code')
        for i in ts_df.index:
            input_num = unique_id()
            start_dt = ts_df.loc[i, 'Claim Start Date']
            end_dt = ts_df.loc[i, 'Claim End Date']
            temp_df.loc[i, 'EMPLOYEE_CODE'] = ts_df.loc[i, 'Qpay ID']
            cycle_date = ts_df.loc[i, 'Claim End Date']
            temp_df.loc[i, 'PAY_PERIOD'] = " ".join(
                [pd.to_datetime(cycle_date).strftime("%B"), pd.to_datetime(cycle_date).strftime("%Y")])
            temp_df.loc[i, 'BILLABLE_DAYS'] = 1
            temp_df.loc[i, 'SERVICE_CHARGE_TYPE'] = 'BILL TO RATE'
            if i > 0:
                if ts_df.loc[i - 1, 'PO Number'] != ts_df.loc[i, 'PO Number']:
                    temp_df.loc[i, 'INPUT_NUMBER'] = input_num
                else:
                    temp_df.loc[i, 'INPUT_NUMBER'] = temp_df.loc[i - 1, 'INPUT_NUMBER']
            else:
                temp_df.loc[i, 'INPUT_NUMBER'] = input_num
            temp_df.loc[i, 'OTHER_ALLOWANCE'] = ts_df.loc[i, 'Total Invoicing Value']
            temp_df.loc[i, 'MATERIALCODE'] = 4162  # <--- Is this fixed Material Code
            temp_df.loc[i, 'TS_START_DATE'] = pd.to_datetime(start_dt).strftime("%d.%m.%Y")
            temp_df.loc[i, 'TS_END_DATE'] = pd.to_datetime(end_dt).strftime("%d.%m.%Y")
            temp_df.loc[i, 'REMARK'] = "Internet Allowance-{}".format(ts_df.loc[i, 'Key'])
            temp_df.loc[i, 'SHIPPING_PARTNER_CODE'] = ""
            temp_df.loc[i, 'BILLING_PARTNER_CODE'] = ""
            # temp_df.loc[i, 'ADDRESSCODE'] = ts_df.loc[i, 'addresscode']
            temp_df.loc[i, 'GST_GROUP_NAME'] = ts_df.loc[i, 'gstgroupname']
            temp_df.loc[i, 'LEAVE'] = ""
            temp_df.loc[i, 'MODE'] = 'ADD'
        temp_df.to_excel(r"downloads\Billing_Days_MI_Upload.xlsx", index=False)
    except (ValueError, IndexError, AttributeError, TypeError) as e:
        log.error("Function {} failed due to error {}".format(prepare_billing_days_report.__name__, e))


def merge_with_emp_master_partial_search(read_df, read_col_name, src_file, src_sheet, src_col_name,
                                         generate_file_flag=False):
    try:
        src_df = pd.read_excel(src_file, sheet_name=src_sheet, index_col=None)
        for i in read_df.index:
            if i <= len(read_df):
                pattern = "|".join(read_df.loc[i, read_col_name].split(" "))
                mask = src_df[src_col_name].str.contains(pattern, case=False, na=False)
                if len(src_df[mask]) > 0:
                    read_df.loc[i, 'Employee Name'] = src_df.loc[mask, "EmpID"].values[0]
                    read_df.loc[i, 'DOJ'] = src_df.loc[mask, "DOJ"].values[0]
                    read_df.loc[i, 'LWD'] = src_df.loc[mask, "DOS"].values[0]
                    read_df.loc[i, 'Location'] = src_df.loc[mask, "Location"].values[0]
        if generate_file_flag:
            read_df.to_excel(r"downloads\{}.xlsx".format(merge_with_emp_master_partial_search.__name__),
                             index=False)
        return read_df
    except ValueError:
        log.error("Error in function {}".format(merge_with_emp_master_partial_search.__name__))
        return False


def find_emp_id_and_qpay_id(df, src_sheet, lst_merge_on_col, partial_match=False, generate_file_flag=False):
    emp_master_path = list(Path(os.path.join(os.getcwd())).glob('*IBM Master Tracker.xlsx'))[0]
    try:
        src_df = pd.read_excel(emp_master_path, sheet_name=src_sheet, index_col=None)
        if len(lst_merge_on_col) > 1:
            if not partial_match:
                merge_df = pd.merge(df, src_df, left_on=lst_merge_on_col[0], right_on=lst_merge_on_col[1])
            else:
                merge_df = merge_with_emp_master_partial_search(df, lst_merge_on_col[0], emp_master_path, src_sheet,
                                                                lst_merge_on_col[1])
        else:
            if not partial_match:
                merge_df = pd.merge(df, src_df, left_on=lst_merge_on_col[0], right_on=lst_merge_on_col[0])
            else:
                merge_df = merge_with_emp_master_partial_search(df, lst_merge_on_col[0], emp_master_path, src_sheet,
                                                                lst_merge_on_col[1])
        log.info("Number of records after merging with master was {}".format(len(merge_df)))
        if generate_file_flag:
            merge_df.to_excel(r"downloads\{}.xlsx".format(find_emp_id_and_qpay_id.__name__), index=False)
        return merge_df
    except ValueError:
        log.error("Error in function {}".format(find_emp_id_and_qpay_id.__name__))
    return None

#
# extract_df = pd.read_excel(os.path.join(os.getcwd(), "extracted.xlsx"), index_col=None)
# rename_df = pd.read_excel(os.path.join(os.getcwd(), "rename_date_columns.xlsx"), index_col=None)
# emp_master_df = pd.read_excel(os.path.join(os.getcwd(), "IBM Master Tracker.xlsx"), index_col=None)
# qpay_df = pd.merge(extract_df, rename_df, left_on='TalentID', right_on='UserID')
# final_df = pd.merge(qpay_df, emp_master_df, left_on='TalentID', right_on='Client ID')
# print(final_df)

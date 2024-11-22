import os

import pandas as pd
import pypyodbc
import warnings

import file_operations

# UserWarning: pandas only supports SQLAlchemy connectable
warnings.filterwarnings('ignore')


# def read_qpay_employee_db():
#     config_path = os.path.join(os.getcwd(), "config.cfg")
#     host = file_operations.load_config_file(config_path, str('DB'), "HOST")
#     db_name = file_operations.load_config_file(config_path, str('DB'), "DB_NAME")
#     uid = file_operations.load_config_file(config_path, str('DB'), "UID")
#     pwd = file_operations.load_config_file(config_path, str('DB'), "PWD")
#     try:
#         conn = pypyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
#                                 f"Server={host};"
#                                 f"Database={db_name};"
#                                 f"uid={uid};pwd={pwd}")
#         db_df = pd.read_sql_query(
#             """SELECT EMPLOYEE_CODE,Radar_Code,AddressCode,GstGroupName FROM TBL_QITS_EMPLOYEE WHERE AddressCode != ''""",
#             conn, index_col=None, dtype=str)
#         print("datbaseeee")
#         return db_df
#     #except pypyodbc.Error:
#     except Exception as e:
#         print(e,"error is in db")
#
#         return None


def read_qpay_employee_db():
    config_path = os.path.join(os.getcwd(), "config.cfg")
    host = file_operations.load_config_file(config_path, str('DB'), "HOST")
    db_name = file_operations.load_config_file(config_path, str('DB'), "DB_NAME")
    uid = file_operations.load_config_file(config_path, str('DB'), "UID")
    pwd = file_operations.load_config_file(config_path, str('DB'), "PWD")

    try:
        conn = pypyodbc.connect(
            "Driver={ODBC Driver 17 for SQL Server};"
            f"Server={host};"
            f"Database={db_name};"
            f"uid={uid};pwd={pwd}"
        )
        db_df = pd.read_sql_query(
            """SELECT EMPLOYEE_CODE, Radar_Code, AddressCode, GstGroupName 
            FROM TBL_QITS_EMPLOYEE WHERE AddressCode != ''""",
            conn, index_col=None, dtype=str
        )
        print("Database connection successful")
        return db_df
    except pypyodbc.Error as db_err:
        print(f"Database error: {db_err}")
    except Exception as e:
        print(f"General error: {e}")
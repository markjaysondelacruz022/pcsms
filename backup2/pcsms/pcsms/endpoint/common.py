import frappe
import base64

@frappe.whitelist(allow_guest=True)
def sendMail(recipients, msg, title, cc=None, attachments=None, delayed=None):
    frappe.sendmail(recipients=recipients,
                    cc=cc,
                    subject=title,
                    message=msg,
                    attachments=attachments,
                    delayed=delayed)
    
# @frappe.whitelist()
# def import_scholarship_application(file_name, file_data):
#     file_bytes = base64.b64decode(file_data)

#     import pandas as pd
#     df = pd.read_excel(file_bytes)



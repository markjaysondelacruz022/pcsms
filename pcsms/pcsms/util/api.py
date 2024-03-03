import frappe
from frappe import utils

@frappe.whitelist()
def save_application(email,first_name,last_name,type,mobile):
    doc = frappe.new_doc('Scholar Application')
    doc.email_address = email
    doc.first_name=first_name
    doc.last_name=last_name
    doc.status=type
    doc.mobile_number=mobile
    doc.application_date=utils.now()
    doc.save()
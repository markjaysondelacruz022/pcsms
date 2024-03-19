import frappe
from pcsms.endpoint.common import sendMail
from pcsms.utility.common  import populate_template_html

@frappe.whitelist(allow_guest = True)
def send_test_email():
    data = { 'first_name': 'MJ' }
    email_content = populate_template_html(template_path = 'pcsms/templates/notifications/test-notification.html', data=data)
    email_recipients = ['markjayson.delacruz022@gmail.com']
    result = sendMail(email_recipients, email_content, 'Teest', delayed=False)
    return result
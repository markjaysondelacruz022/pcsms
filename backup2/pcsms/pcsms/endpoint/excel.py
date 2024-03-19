import frappe
from frappe import _
import os
import glob
import base64
import pandas as pd
import time

@frappe.whitelist()
def list_json_files():
    directory_path = os.path.join(os.path.dirname(__file__))
    # Search for all Excel files in the directory
    excel_files = glob.glob(os.path.join(directory_path, '*.xls*'))
    filenames = [os.path.basename(file) for file in excel_files]
    return filenames

@frappe.whitelist()
def get_json_data(file_name):
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    
    if not os.path.exists(file_path):
        return {'error': 'File does not exist'}

    # Read the Excel file
    df = pd.read_excel(file_path)
    # Convert the DataFrame to JSON
    data = df.to_json(orient='records')
    return data



@frappe.whitelist()
def enqueue_import_scholar_application(file_name, file_data):
    frappe.enqueue('pcsms.endpoint.excel.import_scholar_application', file_name = file_name, file_data = file_data)
    return {'message': 'import scholar application process has been queued!'}

@frappe.whitelist()
def import_scholar_application(file_name, file_data):
    
    # frappe.publish_progress(0,
    #                         title = 'Importing scholar application',
    #                         description = 'Please wait...')
    frappe.publish_realtime('import_process',
                        {'message': 'Importing scholar application.', 'progress': 0 },
                        user=frappe.session.user)
    file_bytes = base64.b64decode(file_data)
    
    import io
    df = pd.read_excel(io.BytesIO(file_bytes))

    # Iterate over the DataFrame rows and insert into the database
    inserted_records = []
    error_messages = []

    row_count = sum(1 for _ in df.iterrows())
    for index, row in df.iterrows():
        frappe.db.savepoint('user')

        # TODO: Validation field block
        email = row.get('email_address', '').strip()  # Ensure email is a string and remove whitespace
        if not email:
            error_message = f"Row {index + 1}: Email Address is required."
            error_messages.append(error_message)
            continue  # Skip this row


        try:
            # Create a new document for Scholar Application
            doc = frappe.get_doc({
                'doctype': 'Scholar Application',
                # Corrected the key to match the Excel column name
                'email_address': email,
                'first_name': row.get('first_name', '').strip(),
                'last_name': row.get('last_name', '').strip()
                # match the fields from database, put here the remaining data.
            })
            
            doc.insert(ignore_permissions=True)
            inserted_records.append(doc.name)
        except Exception as e:
            error_message = f"Failed to insert record for row {index + 1}: {e}"
            error_messages.append(error_message)
            frappe.log_error(frappe.get_traceback(), 'insert_excel_data_to_db failed')
            frappe.db.rollback(save_point = 'user')
        
        frappe.publish_realtime('import_process',
                        {'message': _(f'Processing {index + 1} out of {row_count}'), 'progress': float(index + 1) / row_count * 100 },
                        user=frappe.session.user)
        
        # frappe.publish_progress(float(index + 1) / row_count * 100 ,
        #                 title = _('Importing scholar application'),
        #                 description = _(f'Please wait... ({index + 1} / {row_count})'))
        


    # if error_messages:
    #     frappe.throw('\n'.join(error_messages))
    #     frappe.db.rollback()
        
    inserted_records_count = len(inserted_records);

    post_insert_message = _(f'Saving records') if inserted_records_count > 0 else _(f'No record processed')
    time.sleep(1)
    
    frappe.publish_realtime('import_process',
                        {'message': post_insert_message, 'progress': 0 if inserted_records_count > 0 else 100, 'is_completed': inserted_records_count == 0 },
                        user=frappe.session.user)
    if len(inserted_records) != 0:
        frappe.db.commit()  # Commit changes to the database
        time.sleep(1)
        frappe.publish_realtime('import_process',
                        {'message': _(f'Saved {len(inserted_records)} records.'), 'progress': 100, 'is_completed': True },
                        user=frappe.session.user)
    # return frappe.msgprint(__(f'Successfully inserted {len(inserted_records)} records.'))
    return {'message': f'Successfully inserted {len(inserted_records)} records. \n Failed inserted {len(error_messages)} records'}

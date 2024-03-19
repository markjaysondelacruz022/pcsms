
from frappe.core.doctype.file.file import File
import shutil
import os

class CustomFile(File):
    def before_save(self):
        # Define new file path on the filesystem
        new_file_system_path = 'C:\\Users\\mj\\Documents\\xurpas\\project\\pcsms\\testFiles{}'.format(self.file_name)

        # Define new file URL for web access
        new_file_url = '/files/testFiles/{}'.format(self.file_name)

        # Check if directory exists, if not, create it
        os.makedirs(os.path.dirname(new_file_system_path), exist_ok=True)

        # Move the file from the old location to the new one
        shutil.move(self.get_full_path(), new_file_system_path)

        # Update the file_url field to the new web-accessible path
        self.file_url = new_file_url

# Now you need to tell Frappe to use this CustomFile class instead of the default File class
# Update the override_doctype_class in your hooks.py as shown below
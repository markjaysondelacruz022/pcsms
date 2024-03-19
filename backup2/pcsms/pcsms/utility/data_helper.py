import frappe

def populate_template_html(**args):
    try:
        template_path = args.get('template_path')
        if template_path:
            return frappe.render_template(template_path, args.get('data'))
        else:
            frappe.throw(_('No template path provided'))
    except Exception as e:
        frappe.throw(_(f'Error rendering the form html: {e}'))


# def distinct_group(message, group_key="group_name", academic_level_key="academic_level", level_key="level"):
#     distinct_groups = {}
#     for entry in message:
#         group_name = entry[group_key]
#         academic_level = entry[academic_level_key]
#         if group_name not in distinct_groups:
#             distinct_groups[group_name] = {group_key: group_name, academic_level_key: []}
#         distinct_groups[group_name][academic_level_key].append({level_key: academic_level.lower()})
#     return list(distinct_groups.values())

def nest_json_list(all_data, key_map, parents = [], owner_key = None, owner_id = None):
    if not key_map:
        return None
    # if owner_key and owner_id:
    #     if owner_key not in (p.get('key') for p in parents):
    #         parents.append({'key': owner_key, 'id': owner_id})
    #     else:
    #         for p in parents:
    #             if p.get('key') == owner_key:
    #                 p['id'] = owner_id
    #                 break
    field_divider = '__'
    field_key = key_map.get('key')
    type = key_map.get('type')
    build_data = [] if type == 'list' else {}
    for data in all_data:
        
        current_data_id = data.get(field_key + field_divider +'id')
        if not current_data_id:
            continue
        
        if isinstance(build_data, list) and len(build_data) > 0:
            if current_data_id in (d.get('id') for d in build_data):
                continue
        
        if len(parents) != 0:
            is_parent_match = False
            for parent in parents:
                key = parent.get('key')
                id = parent.get('id')
                if data.get(key + field_divider + 'id') and data.get(key + field_divider + 'id') == id:
                    is_parent_match = True
                else:
                    is_parent_match = False
                    break
            if not is_parent_match:    
                continue

        # if owner_key is not None and owner_id is not None:
        #     data_id = data.get(owner_key + field_divider + 'id')
        #     if (owner_id != data_id):
        #         continue

        new_data = {}
        for key in data.keys():
            if key.startswith(field_key + field_divider):
                new_content_key = key.replace(field_key + field_divider, '')
                new_data[new_content_key] = data.get(key)
    
        children_key_map = key_map.get('children', None)
        if children_key_map is not None and len(children_key_map) > 0:
            for child_map in children_key_map:
                child_key = child_map.get('key')
                child_type = child_map.get('type')
                if child_key not in new_data.keys():
                    new_data[child_key] = [] if child_type == 'list' else {}
                if field_key not in (p.get('key') for p in parents):
                    parents.append({'key': field_key, 'id': new_data.get('id')})
                else:
                    for p in parents:
                        if p.get('key') == field_key:
                            p['id'] = new_data.get('id')
                            break
                filter_data = all_data
                # for parent in parents:
                #     filter_data = [d for d in filter_data if d.get(parent.get('key') + field_divider + 'id') == parent.get('id')]
                # parent_key = ''+field_key
                new_data[child_key] = data_loader(new_data.get(child_key), nest_json_list(all_data, child_map, parents, field_key, new_data.get('id')))
                parents.pop()
                
        build_data = data_loader(build_data, new_data)
        # parents = parents[:-1]
    # if owner_key is not None:
    #     parents = [p for p in parents if p.get('key') != owner_key]
    #     test=True
    # parents = []
    return build_data

def data_loader(data_doc, data_built):
    if isinstance(data_doc, list):
        if isinstance(data_built, dict):
            data_doc.append(data_built)
        elif isinstance(data_built, list):
            data_doc.extend(data_built)
    else:
        data_doc = data_built
    return data_doc

# def build_data_list(data, key_map):
#     if not key_map:
#         return None
    
#     data_list = []
#     for item in data:
#         data_row = build_row_data(data, item, key_map)
#         data_list.append(data_row)

#     return data_list
   
# def save_file():
    # attachment_file_names = row.get('attachment_file_names')
    # existing_file_name = attachment_file_names
    # file_content = None
    # with open('/workspace/development/attachments_to_import/'+existing_file_name, 'r') as file:
    #     file_content = file.read()

    # if file_content is not None:
    #     file_doc = frappe.get_doc(
    #         {
    #         "doctype": "File",
    #         "file_name": existing_file_name, 
    #         "attached_to_doctype": None,
    #         "attached_to_name": None,
    #         "content": file_content,
    #         "is_private": 1
    #     })
    #     file_doc.save()
    
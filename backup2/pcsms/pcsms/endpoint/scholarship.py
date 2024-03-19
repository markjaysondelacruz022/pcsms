import frappe
from frappe.query_builder import DocType
from pcsms.utility.data_helper import nest_json_list



@frappe.whitelist(allow_guest = True)
def get_academic_level_group_details():
    
    # academic_level_group = frappe.get_all('Academic Level Group', fields = ('name', 'group_name', '`tabAcademic Level Group`.name'),)
    AcademicLevelType = DocType('Academic Level Type')
    AcademicLevel = DocType('Academic Level')
    
    query = (
        frappe.qb.from_(AcademicLevelType)
            .inner_join(AcademicLevel)
            .on(AcademicLevel.academic_level_type == AcademicLevelType.name)
            .select(AcademicLevelType.name.as_('academic_level_type__id'), AcademicLevelType.type_name.as_('academic_level_type__type'),
                    AcademicLevelType.has_courses.as_('academic_level_type__has_courses'),
                    AcademicLevel.name.as_('academic_grade_level__id'),
                    AcademicLevel.academic_level.as_('academic_grade_level__name'),
                    AcademicLevel.academic_level_type.as_('academic_grade_level__academic_level_type'),
                    AcademicLevel.active.as_('academic_grade_level__active'))
            )
    key_map = {'key' : 'academic_level_type', 
               'type': 'list',
               'children': [
                                {
                                    'key' : 'academic_grade_level',
                                    'type': 'list'
                                        
                                }
                            ]
                }
    result = query.run(as_dict = True)
    return nest_json_list(result, key_map)
    # return result

@frappe.whitelist(allow_guest = True)
def get_scholarship_programs():

    # academic_level_group = frappe.get_all('Academic Level Group', fields = ('name', 'group_name', '`tabAcademic Level Group`.name'),)
    ScholarshipProgram = DocType('Scholarship Program')
    AcademicLevelTypes = DocType('Academic Level Types')
    AcademicLevelType = DocType('Academic Level Type')
    AcademicLevel = DocType('Academic Level')
    AcademicLevels = DocType('Academic Levels')

    ApplicationTypes = DocType('Application Types')
    ApplicationType = DocType('Type of Application')
    
    query = (
        frappe.qb.from_(ScholarshipProgram)

            .inner_join(ApplicationTypes)
            .on((ApplicationTypes.parenttype == 'Scholarship Program') 
                & (ApplicationTypes.parent == ScholarshipProgram.name))
            .inner_join(ApplicationType)
            .on(ApplicationType.name == ApplicationTypes.application_type)

            .inner_join(AcademicLevelTypes)
            .on((AcademicLevelTypes.parenttype == 'Scholarship Program') 
                & (AcademicLevelTypes.parent == ScholarshipProgram.name))
            .inner_join(AcademicLevelType)
            .on(AcademicLevelType.name == AcademicLevelTypes.academic_level_type)

            .left_join(AcademicLevels)
            .on((AcademicLevels.parenttype == 'Scholarship Program') 
                & (AcademicLevels.parent == ScholarshipProgram.name))
            .left_join(AcademicLevel)
            .on((AcademicLevel.name == AcademicLevels.academic_level) 
                & (AcademicLevel.academic_level_type == AcademicLevelTypes.academic_level_type))
            
            .select(ScholarshipProgram.name.as_('scholarship_program__id'),
                    ScholarshipProgram.program_name.as_('scholarship_program__program_name'),
                    ScholarshipProgram.start_date.as_('scholarship_program__start_date'),
                    ScholarshipProgram.end_date.as_('scholarship_program__end_date'),

                    ApplicationType.name.as_('application_type_filters__id'),
                    ApplicationType.type_name.as_('application_type_filters__type_name'),

                    AcademicLevelType.name.as_('academic_level_type_filters__id'),
                    AcademicLevelType.type_name.as_('academic_level_type_filters__type_name'),

                    AcademicLevel.name.as_('academic_level_filters__id'),
                    AcademicLevel.academic_level.as_('academic_level_filters__academic_level'))
            .where(ScholarshipProgram.active == 1)
            )
    key_map = {
                    "key": "scholarship_program",
                    "type": "list",
                    "children": [
                        {
                            "key": "academic_level_type_filters",
                            "type": "list",
                            "children": [
                                {
                                    "key": "academic_level_filters",
                                    "type": "list"
                                }
                            ]
                        },
                        {
                            "key": "application_type_filters",
                            "type": "list"
                        }
                    ]
                }

    result = query.run(as_dict = True)
    return nest_json_list(result, key_map, [], None, None)
    # return result
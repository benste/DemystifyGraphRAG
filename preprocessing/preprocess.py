from datashaper import Workflow
from preprocessing import create_base_documents, create_base_text_units, create_final_documents, create_final_text_units

# workflows[0].name
# 'create_base_documents'
# workflows[1].name
# 'create_final_documents'
# workflows[2].name
# 'create_base_text_units'
# workflows[3].name
# 'join_text_units_to_entity_ids'
# workflows[4].name
# 'join_text_units_to_relationship_ids'
# workflows[5].name
# 'create_final_text_units'

def load_workflow(name, build_steps):
    return Workflow(
        schema={
            "name": name,
            "steps": build_steps,
        },
        validate=False,
    )
 
 
def test():   
    workflows_raw = [
        {'name': create_base_text_units.workflow_name, 'steps': create_base_text_units.build_steps()},
        {'name': create_base_documents.workflow_name, 'steps': create_base_documents.build_steps()},
        {'name': create_final_documents.workflow_name, 'steps': create_final_documents.build_steps()},
    ]
    workflows = [load_workflow(raw_flow['name'], raw_flow['steps']) for raw_flow in workflows_raw]
    1+1
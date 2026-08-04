from typing import TypedDict

class WorkflowState(TypedDict):
    project_name:str
    execution_id:str
    documents:list
    knowledge:dict|None
    process:dict|None
    gap:dict|None
    sme:dict|None
    sop:dict|None

def is_multiple_fabric(all_fabric_details_list:list[dict]) -> bool:
    return True if len(all_fabric_details_list) >1 else False


def mockup_data_annotation(fabric_name:str,stage:str) -> str:
    starting_text = "Mockup"
    return f"Stage: {stage} , {starting_text} of {fabric_name}"

def dying_data_annotation(fabric_name:str,stage:str,color:str)->str:
    starting_text = "Dying"
    return f"Stage: {stage} , {starting_text} of {fabric_name} , Color: {color}"

def printing_data_annotation(fabric_name:str,stage:str,printing_technique:str)->str:
    starting_text = "Strike Off"
    return f"Stage: {stage} , {starting_text} of {fabric_name} , Printing Technique: {printing_technique}"


def color_wise_dying_processor(fabric_name:str,color_name:str,stage:str, quantity:int):
    
    ...

    
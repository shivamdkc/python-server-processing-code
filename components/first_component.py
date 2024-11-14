def is_multiple_fabric(all_fabric_details_list:list[dict]) -> bool:
    return True if len(all_fabric_details_list) >1 else False


def description_annotator(process:str,fabric_name:str,stage:str,color_print_params:str=None)->str:
    if process == "Mockup":
        starting_text = "Mockup"
        return f"Stage: {stage} , {starting_text} of {fabric_name}"
    
    if process == "Dying":
        starting_text = "Dying"
        return f"Stage: {stage} , {starting_text} of {fabric_name} , Color: {color_print_params}"
    
    starting_text = "Strike Off"
    return f"Stage: {stage} , {starting_text} of {fabric_name} , Printing Technique: {color_print_params}"
                 

def color_wise_dying_processor(fabric_name:str,colors:list,stage:str):
    for color in colors:
        dying_data_annotation(fabric_name,stage,color) #Till now no use of this function.


def end_date_calculator(start_date, number_of_days):
    # Helper function to convert string to date
    def string_to_date(date_str):
        return datetime.strptime(date_str, '%Y-%m-%d').date()

    # Convert start_date to date if it's a string
    if isinstance(start_date, str):
        start_date = string_to_date(start_date)

    # Convert number_of_days to an integer if it's a string
    if isinstance(number_of_days, str):
        number_of_days = int(number_of_days)
    elif isinstance(number_of_days, timedelta):
        number_of_days = number_of_days.days

    # Calculate end date
    end_date = start_date + timedelta(days=number_of_days)

    return end_date
    


    

def total_quantity_calculator(quantity_dict: dict) -> int:
    result = 0
    for _, quantity in quantity_dict.items():
        result += int(quantity)
    return result


def get_fabric_usage(fabric_name: str, data: dict = user_input_data) -> int:
    for fabric in data['fabricDetails']:
        if fabric['name'] == fabric_name:
            return int(float(fabric['usage']['value']))
    return None  # or raise an error if fabric is not found

def material_quantity_calculator(fabric:str,quantity:int)->int:
    per_garment_quantity = get_fabric_usage(fabric)
    return quantity * per_garment_quantity



def get_submission_days(process:str) ->int: # This function will return the submission days for any process.
    process_data =  df_submission_days_supporter[df_submission_days_supporter['Process'] == process]
    return int(process_data["Minimum days"].iloc[0])



def dying_printing_handler_for_submission_stage(fabric_name:str,color_print_quantity_params:dict,stage:str,start_date:datetime,process:str):

    total_order_quantity = total_quantity_calculator(color_print_quantity_params)

    lowest_days_needed = get_submission_days(process)
    end_date = end_date_calculator(start_date,lowest_days_needed)

    for color_print,c_quantity in color_print_quantity_params.items():
        df_workflow_tracker = add_to_dataframe(
                df_workflow_tracker,
                stage=stage,
                fabric_name=fabric_name,
                process=process,
                description=description_annotator(fabric_name=fabric_name,stage=stage,color_print_params=color_print,process=process),
                quantity=c_quantity,
                color=color_print,
                start_date=start_date,
                lowest_days=lowest_days_needed,
                end_date=end_date)
        
def mockup_handler_for_submission_stage(fabric_name:str,color_print_quantity_params:dict,stage:str,start_date:datetime,process:str)-> None:

    
    total_order_quantity = total_quantity_calculator(color_print_quantity_params)

    lowest_days_needed = get_submission_days(process)
    end_date = end_date_calculator(start_date,lowest_days_needed)

    for color_print,c_quantity in color_print_quantity_params.items():
        df_workflow_tracker = add_to_dataframe(
                df_workflow_tracker,
                stage=stage,
                fabric_name=fabric_name,
                process=process,
                description=description_annotator(fabric_name=fabric_name,stage=stage,color_print_params=color_print,process=process),
                quantity=c_quantity,
                color=color_print,
                start_date=start_date,
                lowest_days=lowest_days_needed,
                end_date=end_date)    







        


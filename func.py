from typing import Tuple, Dict
import json

def format_task_response(dblist):
    """
    Convert database tuple to formatted JSON response
    
    Args:
        db_tuple: Tuple from database (id, name, description, additional_desc, location, price, ...)
        
    Returns:
        Dict: Formatted dictionary ready for JSON response
    """
    datalist = []
    print(dblist)
    for i in dblist:
        print(i)
    # Map the tuple values to dictionary
        formatted_response = {
            "id":i[0],
            "name": i[2],  # 'chris'
            "description": i[3],  # combining 'test' and 'test 2'
            "location": i[4],  # 'belfast' (stripped of whitespace)
            "price": i[5]  # 100.0
        }
        datalist.append(formatted_response)
    
    return datalist
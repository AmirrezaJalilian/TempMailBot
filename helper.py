

from config import OWNER_USERNAME,OWNER_ID
from db.db import DataBaseJson



class Permission:
    
    def is_owner(username=None,user_id=None):
        """check user is owner or not"""
        
        if user_id is not None:
            return bool(user_id == OWNER_ID)
        
        elif username is not None:
            return bool(username == OWNER_USERNAME)
        
        else:
            return None
        
    def have_access(user_id):
        """return user have access or not"""
        
        return bool(DataBaseJson.get_user_access(user_id))
    
    
    
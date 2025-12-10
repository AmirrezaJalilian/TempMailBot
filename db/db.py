
import json

data_file = "data/data.json"
utf_8 = "utf-8"

class DataBaseJson:
    
    @staticmethod
    def load():
        """return data of data_file"""
            
        with open(data_file,'r',encoding=utf_8) as file:
            return json.load(file)
    
    @staticmethod 
    def save(data):
        """save data into data_file"""
        
        with open(data_file,'w',encoding=utf_8) as file:
            json.dump(data,file,indent=4)
    
    @staticmethod       
    def get_users():
        """return users from data_file"""
        
        return DataBaseJson.load()['users']
    
    @staticmethod 
    def add_user(user_id):
        """add user into data_file"""
        
        data = DataBaseJson.load()
        
        user_data = {
            "access":True,
            "emails":{}
        }
        
        data["users"][str(user_id)] = user_data
        
        DataBaseJson.save(data)
    
    @staticmethod 
    def exist(user_id):
        """check user is in data_file"""
        
        return bool(str(user_id) in DataBaseJson.get_users())
    
    @staticmethod 
    def rem_user(user_id):
        """remove user from data_file"""
        
        data = DataBaseJson.load()
        
        del data['users'][str(user_id)]
        
        DataBaseJson.save(data)
    
    @staticmethod 
    def get_user(user_id):
        """return user from data_file"""
        
        data = DataBaseJson.load()
        
        return data['users'][str(user_id)]
    
    @staticmethod 
    def get_user_access(user_id):
        """return user access"""
        
        user = DataBaseJson.get_user(user_id)
        
        return user['access']
    
    @staticmethod 
    def get_user_emails(user_id):
        """return user emails from data_file"""
        
        user = DataBaseJson.get_user(user_id)
        
        return user['emails']
    
    @staticmethod 
    def set_user_access(user_id,access=True):
        """set user access"""

        data = DataBaseJson.load()
        
        data['users'][str(user_id)]['access'] = access
        
        DataBaseJson.save(data)
    
    @staticmethod 
    def add_user_email(user_id,email,email_token):
        """add email to user in data_file"""
        
        data = DataBaseJson.load()
        
        email_data = {
            "status":True,
            "token":email_token
        }
        
        data['users'][str(user_id)]['emails'][str(email)] = email_data
        
        DataBaseJson.save(data)
    
    @staticmethod
    def exist_email(user_id,email):
        """check email is in user emails from data_file"""
        
        return bool(email in DataBaseJson.get_user_emails(user_id))
    
    @staticmethod
    def get_user_email(user_id,email):
        """return user email from data_file"""
        
        user_emails = DataBaseJson.get_user_emails(user_id)
        
        return user_emails[str(email)]
    
    @staticmethod
    def rem_user_email(user_id,email):
        """remove user email from data_file"""
        
        data = DataBaseJson.load()
        
        del data['users'][str(user_id)]['emails'][str(email)]
        
        DataBaseJson.save(data)
    
    @staticmethod
    def get_user_email_status(user_id,email):
        """return user email status from data_file"""
        
        user_email = DataBaseJson.get_user_email(user_id,email)
        
        return user_email['status']
    
    @staticmethod
    def set_user_email_status(user_id,email,status=False):
        """set user email status from data_file"""
        
        data = DataBaseJson.load()
        
        data['users'][str(user_id)]['emails'][str(email)]['status'] = status
        
        DataBaseJson.save(data)
    
    @staticmethod
    def get_user_email_token(user_id,email):
        """return user email token from data_file"""
        
        user_email = DataBaseJson.load()['users'][str(user_id)]['emails'][str(email)]
        
        return user_email['token']
from .models import account

class auth:
    def authenticate(self,iam=None,alias=None,passwd=None):
        try:
            users_iam = [account.objects.get().iam]
            users_alias = [account.objects.get().alias]
            if(alias in users_alias):
                # print(account.objects.get(alias=alias).passwd,passwd)
                if(str(passwd) == str(account.objects.get(alias=alias).passwd)):
                    return True
                else:
                    return False
            else:
                return False
        except:
            return False
        
    def get_user(self,num):
        try:
            return account.objects.get(iam=num)
        except:
            return None

    

from licensing.models import *
from licensing.methods import Key, Helpers
import os

FLOATING_INTERVAL = 300

def verify():
    try:
        result = Key.activate(token=os.environ['ACCESS_TOKEN'],\
                        rsa_pub_key=os.environ['RSA_PUB_KEY'],\
                        product_id=os.environ["PRODUCT_ID"], \
                        key=os.environ['LICENSE_KEY'],\
                        floating_time_interval=FLOATING_INTERVAL + 30,
                        machine_code=Helpers.GetMachineCode(v=2))
        
        
        if result[0] == None or not Helpers.IsOnRightMachine(result[0],is_floating_license=True, v=2):
            return False
        else:
            return True
    except:
        return False


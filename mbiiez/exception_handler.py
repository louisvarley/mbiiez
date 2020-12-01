
import json

class exception_handler:

    instance = None

    def __init__(self, instance):
        self.instance = instance
            
    def log(self, ex):
        
        trace = []
        tb = ex.__traceback__
        while tb is not None:
            trace.append({
                "filename": tb.tb_frame.f_code.co_filename,
                "name": tb.tb_frame.f_code.co_name,
                "lineno": tb.tb_lineno
            })
            tb = tb.tb_next
            

        exception_message = (str({
            'type': type(ex).__name__,
            'message': str(ex),
            'trace': trace
        }))

        self.instance.log_handler.log("Exception Occured:{}".format(exception_message))
            
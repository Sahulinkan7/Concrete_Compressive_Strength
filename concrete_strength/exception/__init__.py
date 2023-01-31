import os,sys


class ConcreteException(Exception):
    def __init__(self,error_message: Exception,error_details:sys):
        super().__init__(Exception)
        self.error_message=ConcreteException.get_detailed_error_message(error_message=error_message,error_details=error_details)

    @staticmethod
    def get_detailed_error_message(error_message:Exception,error_details:sys):
        """
        error_message : an Exception object 
        error_details : object of sys module 
        """
        _,_ ,exec_tb=error_details.exc_info()
        exception_block_line_number=exec_tb.tb_frame.f_lineno
        try_block_line_number=exec_tb.tb_lineno
        file_name=exec_tb.tb_frame.f_code.co_filename

        error_message=f"""
        Error occured in script: [{file_name}] 
        at try block line number : [{try_block_line_number}]
        error_message : [{error_message}]
        """
        return error_message

    def __str__(self):
        return self.error_message

    def __repr__(self):
        return ConcreteException.__name__.str()
import logging


class LogHandler:
    log_format = '%(asctime)s:%(name)s:%(module)s:%(lineno)d:%(levelname)s:%(message)s'
    formatter = logging.Formatter(log_format)
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)

    def __init__(self, logger_name, log_level='INFO'):
        self.logger = logging.getLogger(logger_name)
        self.logger.addHandler(self.sh)
        self.logger.propagate = False
        self.__setlevel(log_level)

    def __setlevel(self, loglevel):
        self.logger.setLevel(loglevel)

"""
sample log:
date:session_id:module:filename:line#:Level:message
2019-04-19 18:03:13,720:cidr:test_logger:9:INFO:The sky is so blue
2019-04-19 18:03:13,720:cidr:test_logger:10:ERROR:Oh, its getting dark!
2019-04-19 18:03:13,720:cidr:test_logger:11:CRITICAL:Ohhh, no, the flood, the landslide!!!
"""
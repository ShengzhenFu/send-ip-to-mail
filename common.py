# !/usr/bin/env python
# -*- coding:utf-8 -*-
import logging
import logging.handlers

class Log(logging.Logger):
    def __init__(self):
        
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        log_path_config = 'D:\\code\\send-ip-to-mail-py\\send-mail.log'
        logHandler = logging.handlers.RotatingFileHandler(log_path_config, maxBytes=20000000, backupCount=10)
        logHandler.setLevel(logging.INFO)
        logHandler.setFormatter(formatter)

        self.logger.addHandler(logHandler)
        #logHandler.close()

    def info(self,msg):
	       return self.logger.info(msg)

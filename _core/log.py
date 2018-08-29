#!/usr/bin/python
# -*- coding: utf-8 -*-

class Log():

    enabled_info  = True
    log_path = None

    enable_error = True
    error_log_path = None

    @staticmethod
    def l(message):
        Log.log(message, Log.enabled_info, Log.log_path)

    @staticmethod
    def le(message):
        Log.log(message, Log.enable_error, Log.error_log_path)

    @staticmethod
    def log(message, enabled, log_path):
        if enabled:
            if log_path == None:
                print(message)
            else:
                with open(log_path, 'a') as f:
                    f.write(message + '\n')
                f.closed

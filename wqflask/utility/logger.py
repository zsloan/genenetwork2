# GeneNetwork logger
#
# The standard python logging module is very good. This logger adds a
# few facilities on top of that. Main one being that it picks up
# settings for log levels (global and by module) and (potentially)
# offers some fine grained log levels for the standard levels.
#
# All behaviour is defined here.  Global settings (defined in
# default_settings.py).
#
# To use logging and settings put this at the top of a module:
#
#   import utility.logger
#   logger = utility.logger.getLogger(__name__ )
#
# To override global behaviour set the LOG_LEVEL in default_settings.py
# or use an environment variable, e.g.
#
#    env LOG_LEVEL=INFO ./bin/genenetwork2
#
# To override log level for a module replace that with, for example,
#
#   import logging
#   import utility.logger
#   logger = utility.logger.getLogger(__name__,level=logging.DEBUG)
#
# We'll add more overrides soon.

import logging
import string
from inspect import isfunction
from utility.tools import LOG_LEVEL

class GNLogger:
    """A logger class with some additional functionality, such as
    multiple parameter logging, SQL logging, timing, colors, and lazy
    functions.

    """

    def __init__(self,name):
        self.logger = logging.getLogger(name)

    def setLevel(self,value):
        """Set the undelying log level"""
        self.logger.setLevel(value)

    def debug(self,*args):
        """Call logging.debug for multiple args"""
        self.collect(self.logger.debug,*args)

    def info(self,*args):
        """Call logging.info for multiple args"""
        self.collect(self.logger.info,*args)

    def warning(self,*args):
        """Call logging.warning for multiple args"""
        self.collect(self.logger.warning,*args)
        self.logger.warning(self.collect(*args))

    def error(self,*args):
        """Call logging.error for multiple args"""
        self.collect(self.logger.error,*args)

    def infof(self,*args):
        """Call logging.info for multiple args lazily"""
        # only evaluate function when logging
        if self.logger.getEffectiveLevel() < 30:
            self.collectf(self.logger.debug,*args)

    def debugf(self,*args):
        """Call logging.debug for multiple args lazily"""
        # only evaluate function when logging
        if self.logger.getEffectiveLevel() < 20:
            self.collectf(self.logger.debug,*args)

    def sql(self, description, sqlcommand, fun = None):
        """Log SQL command, optionally invoking a timed fun"""
        self.info(description,sqlcommand)
        if fun:
            self.info("Invoking function")
            return fun(sqlcommand)

    def collect(self,fun,*args):
        """Collect arguments and use fun to output one by one"""
        for a in args:
            fun(a)

    def collectf(self,fun,*args):
        """Collect arguments and use fun to output one by one"""
        for a in args:
            if isfunction(a):
                fun(a())
            else:
                fun(a)

# Get the module logger. You can override log levels at the
# module level
def getLogger(name, level = None):
    gnlogger = GNLogger(name)
    logger = gnlogger.logger

    if level:
        logger.setLevel(level)
    else:
        logger.setLevel(LOG_LEVEL)

    logger.info("Log level of "+name+" set to "+logging.getLevelName(logger.getEffectiveLevel()))
    return gnlogger

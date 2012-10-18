"""
InaSAFE Disaster risk assessment tool developed by AusAid and World Bank
- **Helpers, globals and general utilities for the realtime package**

Contact : ole.moller.nielsen@gmail.com

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'tim@linfiniti.com'
__version__ = '0.5.0'
__date__ = '19/07/2012'
__copyright__ = ('Copyright 2012, Australia Indonesia Facility for '
                 'Disaster Reduction')

import os
import shutil
import logging
import logging.handlers


def baseDataDir():
    """Create (if needed) and return the path to the base realtime data dir"""
    # TODO: support env var setting here too
    myBaseDataDir = '/tmp/inasafe/realtime'
    mkDir(myBaseDataDir)
    return myBaseDataDir


def dataDir():
    """Return the path to the standard data dir for e.g. geonames data"""
    myDir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                         'fixtures'))
    mkDir(myDir)
    return myDir


def shakemapZipDir():
    """Create (if needed) and return the path to the base shakemap zip dir"""
    myDir = os.path.join(baseDataDir(), 'shakemaps-zipped')
    mkDir(myDir)
    return myDir


def shakemapExtractDir():
    """Create (if needed) and return the path to the base shakemap extract dir
    """
    myDir = os.path.join(baseDataDir(), 'shakemaps-extracted')
    mkDir(myDir)
    return myDir


def shakemapDataDir():
    """Create (if needed) and return the path to the base shakemap post
    procesed (tifs and pickled events) data dir.
    """
    myDir = os.path.join(baseDataDir(), 'shakemaps-processed')
    mkDir(myDir)
    return myDir


def reportDataDir():
    """Create (if needed) and return the path to the base report data dir"""
    myDir = os.path.join(baseDataDir(), 'reports')
    mkDir(myDir)
    return myDir


def logDir():
    """Create (if needed) and return the path to the log directory"""
    myDir = os.path.join(baseDataDir(), 'logs')
    mkDir(myDir)
    return myDir


def mkDir(thePath):
    """Make a directory, making sure it is world writable"""
    if not os.path.exists(thePath):
        # Ensure that the dir is world writable
        # Umask sets the new mask and returns the old
        myOldMask = os.umask(0000)
        os.makedirs(thePath, 0777)
        # Resinstate the old mask for tmp
        os.umask(myOldMask)


def purgeWorkingData():
    """Get rid of the shakemaps-* directories - mainly intended for
    invocation from unit tests to ensure there is a clean slate before
    testing."""
    shutil.rmtree(shakemapExtractDir())
    shutil.rmtree(shakemapDataDir())
    shutil.rmtree(shakemapZipDir())


def setupLogger():
    """Run once when the module is loaded and enable logging
    Borrowed heavily from this:
    http://docs.python.org/howto/logging-cookbook.html
    """
    myLogger = logging.getLogger('InaSAFE-Realtime')
    myLogger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    myLogFile = os.path.join(logDir(), 'realtime.log')
    myFileHandler = logging.FileHandler(myLogFile)
    myFileHandler.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    myConsoleHandler = logging.StreamHandler()
    myConsoleHandler.setLevel(logging.ERROR)
    # Email handler for errors
    #myEmailServer = 'localhost'
    #myEmailServerPort = 25
    #mySenderAddress = 'realtime@inasafe.org'
    #myRecipientAddresses = ['tim@linfiniti.com']
    #mySubject = 'Error'
    #myEmailHandler = logging.handlers.SMTPHandler(
    #    (myEmailServer, myEmailServerPort),
    #    mySenderAddress,
    #    myRecipientAddresses,
    #    mySubject)
    #myEmailHandler.setLevel(logging.ERROR)

    # create formatter and add it to the handlers
    myFormatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    myFileHandler.setFormatter(myFormatter)
    myConsoleHandler.setFormatter(myFormatter)
    #myEmailHandler.setFormatter(myFormatter)
    # add the handlers to the logger
    myLogger.addHandler(myFileHandler)
    myLogger.addHandler(myConsoleHandler)
    #myLogger.addHandler(myEmailHandler)

    # Sentry handler - this is optional hence the localised import
    try:
        from raven.handlers.logging import SentryHandler
        from raven import Client

        myClient = Client('http://5aee75e47c6740af842b3ef138d3ad33:16160af'
                          'd794847b98a34e1fde0ed5a8d@sentry.linfiniti.com/'
                          '4')
        mySentryHandler = SentryHandler(myClient)
        mySentryHandler.setFormatter(myFormatter)
        mySentryHandler.setLevel(logging.ERROR)
        myLogger.addHandler(mySentryHandler)
        mySentryMessage = 'Sentry logging enabled'
    except:
        mySentryMessage = 'Sentry logging could not be enabled'

    myLogger.info('Realtime Module Loaded')
    myLogger.info('----------------------')
    myLogger.info('CWD: %s' % os.path.abspath(os.path.curdir))
    myLogger.info(mySentryMessage)

#!/usr/bin/env python
# coding=iso-8859-15
###############################################################################
#
# © Ericsson AB 2009 All rights reserved.
# The information in this document is the property of Ericsson.
# Except as specifically authorized in writing by Ericsson,
# the receiver of this document shall keep the information contained
# herein confidential and shall protect the same in whole or in partF
# from disclosure and dissemination to third parties.
# Disclosure and disseminations to the receivers employees shall only be made
# on a strict need to know basis.
#
###############################################################################

import sys


def importName( modulename, name ):
    """ Import a named object from a module in the context of this function,
        which means you should use fully qualified module paths.

        Return None on failure.
    """
    
    try:
        module = __import__(modulename, globals(), locals(), [name])
    except (ImportError, KeyError), e:
        print "importHandler importName error!"
        print modulename
        print e
        return None

    if name in vars(module).keys():
        return vars(module)[name]
    else:
        return None


if __name__ == "__main__":
    print importName(sys.argv[1] ,sys.argv[2] )
    

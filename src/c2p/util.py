class Impossible(Exception):
    '''
    This exception should never be caught, and thrown only in "impossible" code paths
    that should never get run into.
    '''

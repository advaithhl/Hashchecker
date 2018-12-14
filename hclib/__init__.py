from sys import version_info as v

if v.major < 3:
    err_msg = 'HashChecker needs Python 3. You have ' + \
        str(v.major) + '.' + str(v.minor) + '.' + str(v.micro)
    raise EnvironmentError(err_msg)

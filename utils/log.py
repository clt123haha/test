import logging

def log_testing():
    log_file = 'log.log'
    handler_test = logging.FileHandler(log_file)  # stdout to file
    handler_control = logging.StreamHandler()  # stdout to console
    handler_test.setLevel('ERROR')
    handler_control.setLevel('INFO')

    selfdef_fmt = '%(asctime)s - %(funcName)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(selfdef_fmt)
    handler_test.setFormatter(formatter)
    handler_control.setFormatter(formatter)

    logger = logging.getLogger('updateSecurity')
    logger.setLevel('DEBUG')

    logger.addHandler(handler_test)
    logger.addHandler(handler_control)
log_testing()
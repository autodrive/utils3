"""
This logger is based on following reference.
wapj2000, About Python Logging Module, Sep 02 2014, [Online] Available: http://gyus.me/?p=418 (Accessed May 02 2017).
16.6. logging — Logging facility for Python, 16. Generic Operating System Services, The Python Standard Library,
    Python Documentation, March 27 2017, [Online] Available: https://docs.python.org/3/library/logging.html
    (Accessed May 02 2017).
16.8. logging.handlers — Logging handlers, 16. Generic Operating System Services, The Python Standard Library,
    Python Documentation, March 27 2017, [Online] Available: https://docs.python.org/3/library/logging.handlers.html
    (Accessed May 02 2017).
"""
import logging
import logging.handlers


def initialize_logger(log_file_name, mode='a', logger_name='wapj_logger',
                      fmt='[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s',
                      level=logging.DEBUG):
    """

    :param str log_file_name:
    :param str mode: log file open mode. By default 'a'.
    :param str logger_name: identifies the logger. Hierarchical name possible (a.b)
    :param str fmt: by default [(level)|(script filename).py:(line number)] (date time) > (message)
    :param int|str level: one of {logging.INFO, logging.DEBUG, ...}
    :return:
    """
    # http://gyus.me/?p=418
    # https://docs.python.org/3/library/logging.html

    # make logger instance
    git_logger_under_construction = logging.getLogger(logger_name)

    # make log formatter
    # https://docs.python.org/3/library/logging.html#logging.Formatter
    formatter = logging.Formatter(fmt)

    # make handlers for stream and file
    file_handler = logging.FileHandler(log_file_name, mode=mode)
    stream_handler = logging.StreamHandler()

    # apply formatter to handlers
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    # add handlers to logger
    git_logger_under_construction.addHandler(file_handler)
    git_logger_under_construction.addHandler(stream_handler)

    # set logging level
    git_logger_under_construction.setLevel(level)

    return git_logger_under_construction

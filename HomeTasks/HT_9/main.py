import argparse
import logging
import os

import config as cfg

# init logging on top for logging inside class
logger = logging.getLogger(cfg.APP_NAME)
logger.setLevel(logging.INFO)


class Parser(object):
    """Parser for web-site"""
    category = []

    def __init__(self, category):
        if category.lower() == "all":
            self.category = cfg.CATEGORIES
        elif category.lower() in cfg.CATEGORIES:
            self.category.append(category)
        else:
            logger.error("{} is not valid category!".format(category))
            self.category = []


def main():
    # get command-line args
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-c", "--category", type=str,
                            default=cfg.DEFAULT_CATEGORY,
                            choices=cfg.CATEGORIES, help="name of category")
    cat_name = arg_parser.parse_args().category

    create_dir = False
    create_log_file = False

    # Check for existing directory and log-file
    if not os.path.isdir(cfg.OUT_DIR):
        os.mkdir(cfg.OUT_DIR)
        create_dir = True

    if not os.path.isfile(cfg.LOG_FILE):
        create_log_file = True

    # add handlers to logger
    fh = logging.FileHandler(cfg.LOG_FILE)
    fmt = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    # create console handler
    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    # logging all options for the possibility of changing their quantity
    logger.info("Program started with next options: {opt}".format(
        opt=arg_parser.parse_args()))
    if create_dir:
        logger.info("Create output directory '{dir_name}'.".format(
            dir_name=cfg.OUT_DIR))
    if create_log_file:
        logger.info("Create log-file '{log_file}'.".format(
            log_file=cfg.LOG_FILE))

if __name__ == '__main__':
    main()

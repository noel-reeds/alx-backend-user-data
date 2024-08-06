#!/usr/bin/python3
import logging
import mylib

logger = logging.getLogger(__name__)

def main():
    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    logger.info('started..')
    mylib.do_something()
    logger.info('..finished')

if __name__ == '__main__':
    main()

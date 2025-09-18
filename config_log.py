import os
import logging
from datetime import datetime

def timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]

if __name__ == 'config_log':
    if not os.path.exists('logs'):
        os.mkdir('logs')

    with open('logs/Rubic_cube_log.log', 'w') as f:
        f.write('Log file created at {}\n\n'.format(timestamp()))

    logging.basicConfig(
        filename='logs/Rubic_cube_log.log',
        level=logging.INFO,           
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

elif __name__ == '__main__':
    print(timestamp())
    print('This module is not meant to be run directly. Please import it in your main application.')
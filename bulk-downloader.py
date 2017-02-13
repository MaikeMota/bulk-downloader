import sys
import getopt
import os
import queue
import threading
from FileDownloader import FileDownloader

MAX_PARALLELS_DOWNLOAD = 2

LINKS_PATH = None
OUTPUT_DIR = None


def handle_arguments(sys_args):
    """
        Handle arguments
    """
    try:
        opts, args = getopt.getopt(sys_args, "hf:o:", ["file=", "outdir="])
    except getopt.GetoptError:
        print('usage: bulk-downloader.py -f <link.txt> -o <output_dir>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('usage: bulk-downloader.py -f <link.txt> -o <output_dir>')
            sys.exit()
        elif opt in ("-f", "--file"):
            global LINKS_PATH
            LINKS_PATH = arg
        elif opt in ("-o", "--outdir"):
            global OUTPUT_DIR
            OUTPUT_DIR = arg
        elif opt in ('-p', "--parallels"):
            global MAX_PARALLELS_DOWNLOAD
            MAX_PARALLELS_DOWNLOAD = int(arg)

    if LINKS_PATH is None:
        print('Missing links file parameter.')
        sys.exit(2)

    if OUTPUT_DIR is None:
        print('Missing outputdir parameter.')
        sys.exit(2)


def main():
    """
        Main application function.
    """
    downloaders = []
    handle_arguments(sys.argv[1:])
    print('Output dir: ' + OUTPUT_DIR)
    if not os.path.exists(LINKS_PATH):
        print(LINKS_PATH + " does not exists... exiting application")
        sys.exit(2)

    if not os.path.exists(OUTPUT_DIR):
        print(OUTPUT_DIR + " does not exists... creating...")
        os.makedirs(OUTPUT_DIR)
        print(OUTPUT_DIR + " created!")

    print('Opening ' + LINKS_PATH + "...")
    try:
        with open(LINKS_PATH) as links_file:
            url = links_file.readline()
            id = 0
            while url != None:
                if MAX_PARALLELS_DOWNLOAD > len(downloaders):
                    id = id + 1
                    downloader = FileDownloader(id,url, OUTPUT_DIR)
                    print('starting new thread')
                    downloaders.append(downloader)
                    downloader.start()
                else:     
                    while len(downloaders) > MAX_PARALLELS_DOWNLOAD:
                        for downloader in downloaders:
                            sys.stdout.write('%s ' % self.file_name)
                            if not downloader.is_alive():
                                print('thread removed')
                                downloaders.remove(downloader)
                            # sys.stdout.write(('\r\n')
                            # sys.stdout.write('\r%s[%s%s] %.2f Mb of %.2f Mb %.2f Mb/s ETA: %s' %
                            #                 (
                            #                     '\n' * self.id,
                            #                     '=' * done, ' ' * (25 - done),
                            #                     total_mb_downloaded,
                            #                     float(total_length_mb),
                            #                     speed,
                            #                     str(datetime.timedelta(
                            #                         seconds=int(remaining_size / speed)))
                            #                 ))
                            # sys.stdout.flush()
                            
                id = 0
                url = links_file.readline()

    except KeyboardInterrupt:
        for downloader in downloaders:
            downloader.stop()
        print('\nO Programa foi encerrado pelo usuário.')


if __name__ == "__main__":
    main()

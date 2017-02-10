import requests
import time
import os
import sys
import datetime
import threading

MB_SIZE = 1048576
CHUNK_SIZE = 1024


class FileDownloader(threading.Thread):
    """
        File Downloader
    """

    def __init__(self, id, url, destination):
        threading.Thread.__init__(self)
        self.id = id
        self.output_lock = threading.Lock()
        url = url.replace('\n', '')
        self.url = url
        last_slash_index = url.rindex('/')
        self.file_name = url[last_slash_index + 1: len(url)]
        self.destination = destination
        self.downloaded = 0
        self.total_length = 0

    def run(self):
        """
            Starts to download the file
        """
        threading.Thread.run(self)
        res = requests.get(self.url, stream=True)
        total_length = res.headers.get('content-length')
        self.total_length = int(total_length)
        loops = 0
        speeds = 0

        with open(self.destination + "/" + self.file_name, 'wb') as file:
            total_length_mb = self.total_length / MB_SIZE
            start_time = time.mktime(time.localtime())
            for chunk in res.iter_content(CHUNK_SIZE):
                file.write(chunk)
                elapsed_time = time.mktime(time.localtime()) - start_time

                if elapsed_time == 0:
                    elapsed_time = 1

                self.downloaded = self.downloaded + len(chunk)
                done = int(25 * self.downloaded / self.total_length)
                total_mb_downloaded = float(self.downloaded / MB_SIZE)
                remaining_size = total_length_mb - total_mb_downloaded
                speed = float(total_mb_downloaded / elapsed_time)
                speeds = speeds + speed
                loops = loops + 1
                
                #sys.stdout.write(('%s ' % (self.file_name))
                #sys.stdout.write(('\r\n')
                sys.stdout.write('\r%s[%s%s] %.2f Mb of %.2f Mb %.2f Mb/s ETA: %s' %
                                 (
                                     '\n' * self.id,
                                     '=' * done, ' ' * (25 - done),
                                     total_mb_downloaded,
                                     float(total_length_mb),
                                     speed,
                                     str(datetime.timedelta(
                                         seconds=int(remaining_size / speed)))
                                 ))
                sys.stdout.flush()

            #sys.stdout.write("\n")
            #sys.stdout.write("\n")
            #sys.stdout.flush()
       # print("Elapsed time: %s, Avg Speed: %.2f Mb/s" %
        #      (str(datetime.timedelta(seconds=elapsed_time)), float(speeds / loops)))
       # print(self.file_name + " saved to " + self.destination + " folder")

    def stop(self):
        """
            Stop current Thread
        """
        threading.Thread._stop(self)

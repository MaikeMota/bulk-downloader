import requests
import time
import os, sys
import datetime

MB_SIZE = 1048576
CHUNK_SIZE = 1024

class DownloadableFile(object):

    def __init__(self, url, destination): 
        url = url.replace('\n', '')
        self.url = url
        last_slash_index = url.rindex('/')
        self.fileName = url[last_slash_index + 1 : len(url)]
        self.destination = destination
        self.downloaded = 0
        self.totalLength = 0

    def startDownload(self): 
        res = requests.get(self.url, stream=True)
        total_length = res.headers.get('content-length')
        print("downloading " + self.fileName)
        self.totalLength = int(total_length)            
        loops = 0
        speeds = 0
        with open(self.destination + "/" +  self.fileName, 'wb') as file:
            total_length_mb = self.totalLength / MB_SIZE
            start_time = time.mktime(time.localtime())
            for chunk in res.iter_content(CHUNK_SIZE):
                file.write(chunk)
                elapsed_time  = time.mktime(time.localtime()) - start_time
                if elapsed_time == 0:
                    elapsed_time = 1 
                self.downloaded = self.downloaded + len(chunk)
                done = int(25 * self.downloaded / self.totalLength)
                total_mb_downloaded = float(self.downloaded / MB_SIZE)
                remaining_size = total_length_mb - total_mb_downloaded
                speed = float(total_mb_downloaded / elapsed_time)
                speeds = speeds + speed
                loops = loops + 1
                sys.stdout.write('\r[%s%s] %.2f Mb of %.2f Mb %.2f Mb/s ETA: %s' % 
                    (
                        '=' * done, ' ' * (25-done),
                        total_mb_downloaded,
                        float(total_length_mb),
                        speed,
                        str(datetime.timedelta(seconds=int(remaining_size/speed)))
                    )
                )
                sys.stdout.flush()  
            sys.stdout.write("\n")
            sys.stdout.write("\n")
            sys.stdout.flush()
        print("Elapsed time: %s, Avg Speed: %.2f Mb/s" % 
        (
            str(datetime.timedelta(seconds= elapsed_time)), float(speeds/loops))
        )
        print(self.fileName + " saved to " + self.destination + " folder")
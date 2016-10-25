import requests
import sys, getopt, os
import time
import datetime

CHUNK_SIZE = 1024
MB_SIZE = 1048576

links = None
outputdir = None

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hf:o:",["file=","outdir="])
    except getopt.GetoptError: 
        print('usage: bulk-downloader.py -f <link.txt> -o <output_dir>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('usage: bulk-downloader.py -f <link.txt> -o <output_dir>')
            sys.exit()
        elif opt in ("-f", "--file"):
             links = arg
        elif opt in ("-o", "--outdir"):
             outputdir = arg

    if links is None:
        print('Missing links.txt parameter.')
        sys.exit(2)
    if outputdir is None:
        print('Missing output_dir parameter.')
        sys.exit(2)
    print('Output dir: ' + outputdir + "\n")
    if not os.path.exists(outputdir):
        print(outputdir + " does not exists... creating...\n")
        os.makedirs(outputdir)
        print(outputdir + " created!\n")
    print('Opening ' + links + "...\n")
    with open(links) as links_file:
        for url in links_file.readlines():
            url = url.replace('\n', '')
            last_slash_index = url.rindex('/')
            file_name = url[last_slash_index+1 : len(url)]
            res = requests.get(url, stream=True)
            total_length = res.headers.get('content-length')
            print("downloading " + file_name)
            dl = 0
            total_length = int(total_length)            
            loops = 0
            speeds = 0
            with open(outputdir + "/" +  file_name, 'wb') as file:
                total_length_mb = total_length / MB_SIZE
                start_time = time.mktime(time.localtime())
                for chunk in res.iter_content(CHUNK_SIZE):
                    file.write(chunk)
                    elapsed_time  = time.mktime(time.localtime()) - start_time
                    if elapsed_time == 0:
                        elapsed_time = 1 
                    dl = dl + len(chunk)
                    done = int(25 * dl / total_length)
                    total_mb_downloaded = float(dl / MB_SIZE)
                    remaining_size = total_length_mb - total_mb_downloaded
                    speed = float(total_mb_downloaded / elapsed_time)
                    speeds = speeds + speed;
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
            print(file_name + " saved to " + outputdir + " folder")

if __name__ == "__main__":
    main()
    
    
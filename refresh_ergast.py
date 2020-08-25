import os 
import urllib.request
import zipfile

def refresh(path, url='http://ergast.com/downloads/f1db_csv.zip'):
    """download latest ergast data and replace data in datadir"""    
    zf_path = os.path.join(path, 'f1db_csv.zip')
    urllib.request.urlretrieve(url, zf_path)
    zf = zipfile.ZipFile(zf_path)
    zf.extractall(path)

refresh('/home/luke/projects/f1metrics/data/ergast')
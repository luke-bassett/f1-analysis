import os 
import urllib.request
import zipfile

def refresh(path='../data/ergast_data', url='http://ergast.com/downloads/f1db_csv.zip'):
    """download latest ergast data and replace data in datadir"""  
    if not os.path.exists(path):
        os.makedirs(path)
        print('created path', path)
    else:
        print('found path', path)
    zf_path = os.path.join(path, 'f1db_csv.zip')
    print('downloading ergast data')
    urllib.request.urlretrieve(url, zf_path)
    zf = zipfile.ZipFile(zf_path)
    print('extracting data from zip file')
    zf.extractall(path)
    print('complete')

if __name__ == '__main__':
    refresh('data/ergast_data')

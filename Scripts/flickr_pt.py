import datetime
import urllib.request as getURL
import xml.etree.ElementTree as ET
import os
import sys
import time
import pickle
from urllib.error import HTTPError, URLError
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

'''
A flicker class, that takes care of downloading photos through the flicker API and
saving the related info to a csv file. It takes three arguments as input photo_path which
is by default a folder named .Photos that the script will create if it has the proper 
permissions, the user api_key and the coordinates of the most extreme points of the box 
to download photos from.

The class has two internal methods:

    __get_photo_xml:
        builds a list with the xml of each of the photos retrieved from the flickr api
        that are present in the box provided. It uses the flickr.photos.search API method 
        and produces a list of all photos found in the area of interest.

        

    __run:
        calls __get_photo_xml to build the list of photos, goes through it and downloads 
        the photo and compiles the respective that in a file called results.csv
        
        It uses the flickr.photos.getInfo API method to get the data of interest and downloads
        the through the staticflickr. 


static methods:
    progress_bar:
        a simple progress bar to help users keep track of the work

        args: count(int), total(int)


'''


def progress_bar(count, total):

    p_bar_len = 50
    at_len = round(p_bar_len * (count / total if total > 1 else 1))
    percent = round((100 * (count / total if total > 1 else 1)))
    bar = "=" * at_len + "-" * (p_bar_len - at_len)
    sys.stdout.write('\r[%s]%s%s' % (bar, percent, '%'))


class Flickr(object):
    api_base = "https://www.flickr.com/services/rest/?method="
    methods = {'photo_search':'flickr.photos.search','photo_info':'flickr.photos.getInfo'}
    def __init__(self,key, bbox):
        self.photos = []
        self.key = key
        self.bbox = bbox
    def get_photo_xml_by_square(self,min_date_taken,max_date_taken,geo_context,bbox,photo_path=None):
        self.photos = []
        bboxs = []
        print('\n\nGathering photo list\n')
        # Make the squares
        logs = [bbox[0]-(-0.1038125)*i for i in range(33)]
        lats = [bbox[1]+(0.1629375)*i for i in range(33)]
        #print(logs)
        #print(lats)
        for i in range(len(logs[:-1])):
            for j in range(len(lats[:-1])):

                bboxs.append("%2C".join([str(x) for x in [logs[i],lats[j],logs[i+1],lats[j+1]]]))

                #bbox = [lft_log,bot_lat,rgt_log,top_lat]
            
        
        for box_n, i in enumerate(bboxs):
            print(f'Gathering photos for box number {box_n} of 1024')
            self.get_photo_xml(min_date_taken,max_date_taken,geo_context,i,photo_path)
            
        
        with open(photo_path+'photos_dataset.pk1','wb') as out:
            pickle.dump(self.photos,out)


    def get_photo_xml(self,min_date_taken,max_date_taken, geo_context, bbox, photo_path= None):
        #self.photos = []
      
        page = 1
        total = 1
        count = 0
        
        while page <= total:
            progress_bar(count, total)
            photo_url=rf"""{self.api_base}{self.methods['photo_search']}&api_key={self.key}&min_taken_date={min_date_taken}&max_taken_date={max_date_taken}&bbox={bbox}&geo_context={geo_context}&page={page}&sort=date-posted-asc"""
            #print(photo_url)
            #photo_url = "https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key="\
            #            + self.__key + "&bbox=" + ",".join([str(x) for x in self.__box])\
            #            + "&page=" + str(page) + "&sort= date-posted-asc"
            self.photo_url = photo_url
            xml_file = getURL.urlopen(photo_url)
            xml_data = xml_file.read().decode()
            xml_file.close()

            rsp = ET.fromstring(xml_data)
            #return rsp
            #photo_set = rsp.getchildren()[0]
            photo_set = list(rsp)[0]
            total = int(photo_set.get('pages'))

            photos = rsp.findall('*/photo')
            for photo in photos:
                self.photos.append(photo)
                   
            count += 1
            page += 1

        progress_bar(total, total)
        print("\n")


    def final_list_and_download(self,photo_path):
    
        downloaded_files=[x.split('.')[0] for x in os.listdir(photo_path)]
        with open(photo_path+'results.csv','a+') as out, open(photo_path+'debug.txt','a+') as debug:
            out.write("Photo_ID\tPhoto_secret\tLatitude\tLongitude\tdate_posted\tdate_taken\n")
            total = len(self.photos)
            for count,photo in enumerate(self.photos):
                progress_bar(count, total)
                p_id = photo.get("id")
                p_secret = photo.get("secret")
                p_farm = photo.get("farm")
                p_server = photo.get("server")
                count = 0
                if p_id in downloaded_files:
                    count +=1
                    print(count)
                    continue


                photo_info_url = rf"""{self.api_base}{self.methods['photo_info']}&api_key={self.key}&photo_id={p_id}"""
                
                #photo_info_url = "https://api.flickr.com/services/rest/?method=flickr.photos.getInfo&api_key="\
                #                    + self.__key + "&photo_id=" + str(p_id)

                photo_url = "https://farm" + p_farm + ".staticflickr.com/" + p_server + "/"\
                            + p_id + "_" + p_secret + ".jpg"
                try:
                    xml_file = getURL.urlopen(photo_info_url)
                    xml_data = xml_file.read().decode()
                    xml_file.close()
                except (HTTPError,URLError) as err:
                    photo_name = photo_path + p_id + ".jpg"
                    debug.write("XML\t"+photo_name+"\t"+photo_url+"\n")
                    time.sleep(30)
                    try:
                        xml_file = getURL.urlopen(photo_info_url)
                        xml_data = xml_file.read().decode()
                        xml_file.close()
                    except (HTTPError,URLError) as err:
                        debug.write("XML\t"+photo_name+"\t"+photo_url+"\t"+"\tfailed twice moving to next"+"\n")
                        continue
                    else:
                        debug.write('XML Previous entry succeed\n')

                rsp = ET.fromstring(xml_data)
                try:

                    if list(rsp)[0].find('location').find('country').text.lower()=='portugal':

                        for child in rsp[0]:

                            if child.tag == "location":
                                p_latitude = child.get('latitude')
                                p_longitude = child.get('longitude')

                            elif child.tag == "dates":
                                p_taken = child.get('taken')
                                p_posted = child.get('posted')

                        try:
                            photo_name = photo_path + p_id + ".jpg"
                        
                            getURL.urlretrieve(photo_url, photo_name)
                            out.write(str(p_id) + "\t" + str(p_secret) + "\t" + str(p_latitude) + "\t" + str(
                                      p_longitude) + "\t" + datetime.datetime.fromtimestamp(int(p_posted)).strftime(
                                      '%Y-%m-%d %H:%M:%S') + "\t" + str(p_taken) + "\n")

                        except (HTTPError,URLError) as err:
                            debug.write("Photo\t"+photo_name+"\t"+photo_url+"\n")
                            time.sleep(30)
                            try:
                                photo_name = photo_path + p_id + ".jpg"
                        
                                getURL.urlretrieve(photo_url, photo_name)
                                out.write(str(p_id) + "\t" + str(p_secret) + "\t" + str(p_latitude) + "\t" + str(
                                          p_longitude) + "\t" + datetime.datetime.fromtimestamp(int(p_posted)).strftime(
                                          '%Y-%m-%d %H:%M:%S') + "\t" + str(p_taken) + "\n")
                            except (HTTPError,URLError) as err:
                                debug.write("Photo\t"+photo_name+"\t"+photo_url+"\tfailed\n")
                                continue
                            else:
                                debug.write('Previous entry suceeded\n')
                        
                        time.sleep(1)
                    
                    else:
                         out.write(str(p_id) + "\t" + str(p_secret) + "\t" + str(p_latitude) + "\t" + str(
                                      p_longitude) + "\t" + datetime.datetime.fromtimestamp(int(p_posted)).strftime(
                                      '%Y-%m-%d %H:%M:%S') + "\t" + str(p_taken) + "\tnot downloaded_check if in Spain\n")
                except AttributeError:
                    pass
            
            progress_bar(total, total)
            print("\n\n")


    def do_by_year(self,path_to_results,years=[]):
        for year in years:
            min_taken_date = f'{year}-07-01 00:00:01' # limit content to the specific dates used
            max_taken_date = f'{year}-10-31 23:59:59' # limit content to the specific dates used
            min_taken_date = min_taken_date.replace(' ','+').replace(':','%3A') # make sure the syntax is correct for URL (escaped spaces and escaped :)
            max_taken_date = max_taken_date.replace(' ','+').replace(':','%3A') # make sure the syntax is correct for URL (escaped spaces and escaped :)
            year_results_path = rf'{path_to_results}/{year}/' 
            try:
                os.mkdir(year_results_path)
            except FileExistsError:
                pass

            if os.path.isfile(year_results_path+'photos_dataset.pk1'):
                with open(year_results_path+'photos_dataset.pk1','rb') as inp:
                    self.photos=pickle.load(inp)
                    print(f'There are {len(self.photos)} photos')
            else:
                self.get_photo_xml_by_square(min_date_taken=min_taken_date,max_date_taken=max_taken_date,geo_context=2,bbox=self.bbox,photo_path=year_results_path)
                print(f'There are {len(self.photos)} photos')
            self.final_list_and_download(year_results_path)


    # def get_photo_xml(self):
    #     print('\n\nGathering photo list\n')
    #     country_url=f'{self.api_base}{self.methods[1]}&api_key={self.__key}&query={self.__country}'
    #     print(country_url)
    #     xml_file = getURL.urlopen(country_url)
    #     xml_data = xml_file.read().decode()
    #     xml_file.close()

    #     rsp = ET.fromstring(xml_data)
    #     country_code = rsp.getchildren()[0].get('place_id')
            
if __name__ == "__main__":
    import sys
    api_key = '6b7bd8736e1a05537d4aab3b5e94626f'
    api_secret = 'f583fd7b0da312d7'
    portugal_woeid = 23424925 # Portugal unique identifier
    top_lat = 42.160
    bot_lat = 36.946
    lft_log = -9.501
    rgt_log = -6.179
    year = list(map(int,sys.argv[1:]))
    
    bbox = [lft_log,bot_lat,rgt_log,top_lat] #geo box from where photos are to be gathered
    #bbox = "%2C".join([str(x) for x in bbox])
    flickr = Flickr(api_key,bbox)
    flickr.do_by_year('./results',year)         # Altera os valores dos anos  
    # geo_context = 2 # only select outdoor photos
    
    # flickr = Flickr(key=api_key)
    # a = flickr.get_photo_xml(min_date_taken=min_taken_date,max_date_taken=max_taken_date,geo_context=geo_context,bbox=bbox)
    # b = flickr.final_list('./results/')

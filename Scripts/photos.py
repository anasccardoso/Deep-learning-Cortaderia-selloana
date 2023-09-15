class photo_instance():
    api_base = "https://www.flickr.com/services/rest/?method="
    methods = {'photo_search':'flickr.photos.search','photo_info':'flickr.photos.getInfo'}
    def __init__(self,photo):
        self.element = photo
        self.id = photo.get('id')
        self.secret = photo.get('secret')
        self.farm = photo.get('farm')
        self.server = photo.get('server')

    def generate_url(self):
        return rf'https://farm{self.farm}.staticflickr.com/{self.server}/{self.id}_{self.secret}.jpg'
        
    def get_id(self):
        return self.id

    def get_secret(self):
        return self.secret 

    def get_farm(self):
        return self.farm
    
    def get_server(self):
        return self.server

    def __str__(self):
        return f'Photo {self.id}'

    def __repr__(self):
        return self.__str__()
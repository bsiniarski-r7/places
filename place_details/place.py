class Place:
    place_id = ""
    types = []
    location = ""
    formatted_address = ""
    formatted_phone_number = ""
    international_phone_number = ""
    url = ""
    website = ""

    '''Setters'''

    def set_place_id(self, place_id):
        self.place_id = place_id

    def set_types(self, types):
        self.types = types

    def set_location(self,location):
        self.location = location

    def set_formatted_address(self, formatted_address):
        self.formatted_address = formatted_address

    def set_formatted_phone_number(self, formatted_phone_number):
        self.formatted_phone_number = formatted_phone_number

    def set_international_phone_number(self, international_phone_number):
        self.international_phone_number = international_phone_number

    def set_url(self, url):
        self.url = url

    def set_website(self, website):
        self.website = website

#  artist id name
from collections import OrderedDict
import json
class Kpop_artist:
    kpop_artists = OrderedDict()
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def set_kpop_list(self):
        Kpop_artist.kpop_artists[self.id] =self.name

    def get_kpop_list(self):
        return Kpop_artist.kpop_artists
    
    def __str__(self):
        return "{},{}".format(self.id, self.name)

class Kpop_artistSql:
    id = 0
    def __init__(self, info):
        
        name, sub_name, debut, sns, member_info, mv, artist_img=info
        
        Kpop_artistSql.id += 1
        self.id = Kpop_artistSql.id
        
        self.name = name
        self.sub_name = sub_name
        self.member_info = member_info
        self.artist_img = artist_img
        self.debut = debut
        self.mv = mv
        self.sns = sns

    def write_arr(self):
        return [self.id,self.name, self.sub_name, self.debut , self.sns, self.member_info, self.mv, self.artist_img]

    def __str__(self):
        return "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(self.id,self.name, self.sub_name, self.debut , self.sns, self.member_info, self.mv, self.artist_img)
    
    def to_tuple(self):
        return (self.name, self.sub_name, self.debut , self.sns, self.member_info, self.mv, self.artist_img,)

#  artist id name
class Kpop_artistSearch:
    def __init__(self, line):
        id, name, lower_name, group= line.split('\t')
        self.id = id.strip()
        self.name = name.strip()
        self.lower_name = lower_name.strip()
        self.group = group.strip()

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_lower_name(self):
        return self.lower_name

    def get_group(self):
        return self.group
    
    def __str__(self):
        return "{}".format(self.lower_name)
    
class Artist_notice:
    def __init__(self, info):
        artist_id, category, title, content, date = info
        self.artist_id = artist_id
        self.category = category
        self.title = title
        self.content = content
        self.date = date
        
    def to_tuple(self):
        return (self.artist_id, self.category, self.title, self.content, self.date)
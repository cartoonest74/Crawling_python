#artist product
class Artist_product:

    def __init__(self,info):
        id, title, category, price, option_size, option_ment, notice, main_img, sub_img = info
        self.id = id
        self.title = title
        self.category = category
        self.price = price
        self.option_size = option_size
        self.option_ment = option_ment
        self.notice = notice
        self.main_img = main_img
        self.sub_img = sub_img

    def to_tuple(self):
        return (self.id, self.title, self.category, self.price, self.option_size, self.option_ment, self.notice, self.main_img, self.sub_img)
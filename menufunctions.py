import easyocr # package to read data
import cv2 # package to load img object for overlaying
import matplotlib.pyplot as plt # package to plot data back to menu

class ReadObj:
    def __init__(self, rawtext, bbox):
        self.rawtext = rawtext
        self.bbox = bbox
        self.in_eng = None
        self.ingred = None
        self.allerg = None
        self.count = None
    def add_count(self, count):
        self.count = count
    def __str__(self):
        out = f"{self.rawtext}, {self.bbox}, {self.in_eng}, {self.ingred}, {self.allerg}"
        return out

def read_menu(imagename)->dict[str, ReadObj]:
    """_summary_
    Reads menu with OCR, creates dictionary object
    Dict type key = raw string
    Dict type value = ReadObj class instance
    """
    reader = easyocr.Reader(['ja'])
    result = reader.readtext(imagename)
    menudata = {}
    count = 0
    for (bbox, rawtext, prob) in result:
        # print(f'Text: {rawtext}, Loc: {bbox}')
        readtext = ReadObj(rawtext, bbox) # initialize
        ####### add count for optimized data parsing
        readtext.add_count(count)
        count += 1
        ######## =============================
        menudata[rawtext] = readtext
        print("raw text: ", rawtext)
    return menudata

def process_msg(msg, menudata):
    # manual data cleaning
    parsed_msg = msg.split('\n')
    print('parsed_msg: ', parsed_msg)
    for i in range(len(parsed_msg)):
        menu_item = parsed_msg[i].split(';')
        menu_item_key = menu_item[0]
        if menu_item_key in menudata:
            menudata[menu_item_key].in_eng = menu_item[1].strip()
            menudata[menu_item_key].ingred = menu_item[2].strip()
        
        else: # if the object is there but it has been cut ie: creme brule
            for menudatakey in menudata:
                if menudatakey in menu_item_key:
                    menudata[menudatakey].in_eng = menu_item[1].strip()
                    menudata[menudatakey].ingred = menu_item[2].strip()
                elif menudatakey[:4] == menu_item_key[:4]: # if first 4 letters the same
                    menudata[menudatakey].in_eng = menu_item[1].strip()
                    menudata[menudatakey].ingred = menu_item[2].strip()
    
    return menudata

def opt_process_msg(msg, menudata):
    # optimized manual data cleaning
    # assumes gpt answer follows the bounding box order
    # if this is slow, use a different data structure (menu) instead of a hash table
    parsed_msg = msg.split('\n')
    menudatalist = list(menudata.keys())
    print('parsed_msg: ', parsed_msg)
    for i in range(len(parsed_msg)):
        menu_item = parsed_msg[i].split(';')
        menu_item_key = menu_item[0]
        # loop to find in menudata
        for counter in range(len(menudatalist)): # per updating menudatalist
            item = menudatalist[counter]
            if menu_item_key[:3] == item[:3]:
                menudata[item].in_eng = menu_item[1].strip()
                menudata[item].ingred = menu_item[2].strip()
                menudatalist = menudatalist[counter+1:]
                print("new menudatalist: ", menudatalist)
                break # break if menuitem is found
            
            
    print("\nprocessed in gpt")
    # print("\nmenudata: ", menudata)
    return menudata

def draw_on_menu(image, singlemenudata):
    print("\nsinglemenudata: ", singlemenudata)
    textcood1 = tuple(map(int, singlemenudata.bbox[0]))
    textcood2 = (textcood1[0], textcood1[1]+15)
    
    if (singlemenudata.in_eng):
        cv2.rectangle(image, tuple(map(int, singlemenudata.bbox[0])), tuple(map(int, singlemenudata.bbox[2])), (255, 255, 200), -1)
        cv2.putText(image, singlemenudata.in_eng, textcood2, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 50), 1)
        # if (singlemenudata.allerg):
        cv2.putText(image, singlemenudata.ingred, textcood1, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 100), 1)

    return image

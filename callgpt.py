from openai import OpenAI 
from dotenv import load_dotenv
import os
import base64
# import replicate # to connect to llama3

load_dotenv()

def get_translation(image_path):
    example_output = """{
        japanese_name:xx, 
        english_name:yy, 
        desrpiption:zz,
        allergens: [allergen1, allergen2, allergen3]
        }"""
    
    api_key = os.getenv('OPENAI_API_KEY')   
    client = OpenAI(api_key=api_key) 
    
    with open(image_path, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode("utf-8")
         
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system", 
                "content": f"You are a translator proficient in various languages.\
                            First, translate a menu from Japanese to English.\
                            Then, generate a description of each dish in 30words.\
                            Finally, list the allergens for each dish.\
                            Return in JSON format. Example shown: {example_output}"
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url" : f"data:image/jpeg;base64,{image_base64},"
                        }
                    }
                ]
            }
        ],
        response_format={"type": "json_object"}
    )

    print(completion.choices[0].message.content)
    return completion.choices[0].message.content


def callllama(prompt):
    for event in replicate.stream(
        "meta/llama-2-70b-chat",
        input={
            "prompt": prompt,
            "max_new_tokens": 250
        },
    ):
        print(str(event), end="")
    
    print('completed')
    print(event)

def process_in_gpt(menudata): 
    """_summary_
    Uses prompt to translate and get allergens
    """
    #### Prompt Engineer GPT to produce the results I want.
    # preprompt = """Help me filter out all the dishes from the above menu that a person with allergies should know including allergies to milk, seafood, nuts, or pork and beef. The answer should appear comma separated like the format below - with the original japanese dish, the english name for the dish, and then the allergens
    # """
    preprompt = """メニユー,~‥,おへず,お欧み物,カレーライス,コーンボク,ジミスーフ,950,『,ビーフカレ,980,わかめスーフ,400 円,ボークカレ,90り,オレンジジュース,350  円,アキンクレー,さう,30 円,』,シーフードカレー,950 7,400,:かの】・,0.5,,40 円, ビーフスアーキ,2000,6,ハンバーグ,1500 円,》5ろ.,テサート,%,ビーフス・ー・とハンバーグレいこいかついい、_,ナボリクンスバグッティ,1のの,シュートケーキ,450 門,フードビろフ,890 川,アイスクリーム,山0 円,いこつ』 イトリベリー,,コレーい 

From the above list, get the ingredients for each dish

The answer should return in the below format:
"コーンボク; Corn Potage; Ingredients: Milk, Corn, Potato, butter
ビーフカレ;  Japanese Beef Curry; Ingredients: Beef, onions, carrots, potatoes, curry roux, rice" """
    # connect to gpt api
    menudatatext = ','.join(menudata.keys())
    print("menudatatext: ", menudatatext)
    prompt = "["+ menudatatext + "]" + preprompt
    # msg = callllama(prompt)
    msg = callgpt(prompt)
    print("completed msg: ", msg)

    return msg


### TEST CASES ####
# import easyocr # package to read data
# import cv2 # package to load img object for overlaying
# import matplotlib.pyplot as plt # package to plot data back to menu
# from menufunctions import read_menu, draw_on_menu

# imagename = 'image_13.png'
# menudata = read_menu(imagename)
# menudata = process_in_gpt(menudata)

# # draw on img and print
# image = cv2.imread(imagename)

# for key in menudata:
#     image = draw_on_menu(image, menudata[key])

# plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGBA))
# plt.show()

if __name__ == "__main__":
    test = get_translation('image_13.png')
    test2 = get_translation('image_12.jpg')
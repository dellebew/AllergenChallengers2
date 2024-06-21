from openai import OpenAI # to connect to GPT
# import replicate # to connect to llama3

###### CONNECT TO GPT #######
def callgpt(prompt):
    client = OpenAI(api_key="sk-proj-Mmo7oPaItEfPOgogjJMzT3BlbkFJURDOYY0HsOzD8mAIulE8") # defaults to getting the key using os.environ.get("OPENAI_API_KEY")
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            # {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
            # {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
            {"role": "user", "content": prompt}
        ]
    )
    print('completed')
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
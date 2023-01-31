import openai as ai
import json


def load_txt_script(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as f:
        text_acc = ''
        for each_text in iter(lambda: f.read(1024), ''):
            text_acc = text_acc + each_text
    return text_acc


def save_QA_append(data=[{'Question': '你們還有什麼服務可以享受?', 'Answer': '我們有83吋的大彩電,以及地下室2樓有3名按摩師,1名物理治療師可以幫你們放鬆旅途的疲勞'},
                         {'Question': '你們附近有什麼不錯的餐點?',
                          'Answer': '建議你沒吃過台灣的鼎泰豐,可以去旁邊吃一下,或者可以直接預約去我們飯店總裁Allen先生的拿手好菜以及手沖咖啡'}],
                   path='./Script_data/w_hotel/addition/Question_append.json'):
    with open(path, 'w') as f:
        json.dump(data, f)


class GPT3_start_up:
    def __init__(self, API_KEY , Azure_Mode = False):        
        self.completion = ai.Completion()        
        if Azure_Mode == True:
            ai.api_key = API_KEY #"af373b251ff341b080a34fc0c64dcd49"
            # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
            ai.api_base =  "https://openai-wistron.openai.azure.com/" 
            ai.api_type = 'azure'
            ai.api_version = '2022-06-01-preview' # this may change in the future
            self.model = deployment_id='hotel_1' #This will correspond to the custom name you chose for your deployment when you deployed a model. 
        elif Azure_Mode == False:
            ai.api_key = API_KEY
            self.model = "text-davinci-003"
            
    def chat(self, question, chat_log=None) -> str:
        global prompt
        if (chat_log == None):
            chat_log = start_chat_log
        prompt = f"{chat_log}Human: {question}\nAI:"
        try:
            response = self.completion.create(prompt=prompt, engine=self.model, temperature=0.1, top_p=1,
                                              frequency_penalty=0,
                                              presence_penalty=0.6, best_of=3, max_tokens=512, stop="\nHuman: ")
#             print('生成答案: ',response.choices)
        except:
            print('your tokens is over please check your prompt,https://beta.openai.com/tokenizer')
            raise
        return response.choices[0].text

    def modify_start_message(self, hat_log, question, answer) -> str:
        global chat_log
        if chat_log == None:
            chat_log = start_chat_log
        chat_log += f"Human: {question}\nAI: {answer}\n"
        return chat_log

    def crerat_standard_chart_log(self, script_path='./Script_data/w_hotel/w_hotel_route.txt',
                                  test_mode=(False, {
                                      'QA_path': './Script_data/w_hotel/addition/Question_append.json'})):  # test_mode = (True , _)
        chat_log = None

        start_chat_log = load_txt_script(script_path)  # w_hotel-room_price.txt / w_hotel_main.txt /w_hotel_route.txt
        if test_mode[0] == True:
            train = input("\nDo you want to train the openai chatbot (True/False): ")
            if (train == "True"):
                print("\n(To stop the training enter stop in the qestion)\n")
                while (True):
                    question = input("Question:")
                    if question == "stop":
                        break
                    answer = input("Answer: ")
                    start_chat_log = self.modify_start_message(start_chat_log, question, answer)
                    print("\n")
        elif test_mode[0] == False:
            with open(test_mode[1]['QA_path'], newline='') as jsonfile:
                data = json.load(jsonfile)
            for QA in data:
                start_chat_log += f"Human: {QA['Question']}\nAI: {QA['Answer']}\n"
        start_chat_log = start_chat_log + 'Human: 請務必之後我們對話服務以中文(chinese)模式對談\nAI: 好的,之後會以中文token做對話溝通,竭誠以中文回應您,中文是我們對話的基石,是無可動搖的\n'
        return start_chat_log

def GPT_emotional_level(prompt_Q  , API_KEY):
    ai.api_key = API_KEY
    completion = ai.Completion()
    prompt = f"{prompt_Q}Human: 請問這些話是開心的嗎? 請回答是開心,或不開心即可 \nAI:"
    response = completion.create(prompt=prompt, engine="text-davinci-001", temperature=0.1, top_p=1,
                                              frequency_penalty=0,
                                              presence_penalty=0.6, best_of=3, max_tokens=512, stop="\nHuman: ")
    return response.choices[0].text
    
if __name__ == "__main__":
    GPT = GPT3_start_up(API_KEY='abcd')  
    start_chat_log = GPT.crerat_standard_chart_log(script_path='../Script_data/w_hotel/w_hotel_route.txt',
                                                   test_mode=(False, {
                                                       'QA_path': '../Script_data/w_hotel/addition/Question_append.json'}))

    print("\nEnter the questions to openai (to quit type \"stop\")")
    while True:
        question = input("Question: ")
        if question == "stop":
            break
        print(f'=====question:{question}==============')
        print("AI: ", GPT.chat(question, start_chat_log))

import json
import os

def update_json(filepath, new_entries):
    if not os.path.exists(filepath):
        data = {}
    else:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    
    data.update(new_entries)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Missing words for G7 Up
g7_up_fix = {
    "a few": {"sentence": ["I have a few English books to read this weekend.", "这周末我有几本英语书要读。"]},
    "a little": {"sentence": ["There is a little milk in the glass on the table.", "桌子上的玻璃杯里有一点牛奶。"]},
    "a lot of": {"sentence": ["I have a lot of friends in my new middle school.", "在我的新中学里我有很多朋友。"]},
    "actor": {"sentence": ["My uncle is a famous actor and he works in Beijing.", "我叔叔是一位著名的演员，他在北京工作。"]},
    "also": {"sentence": ["She likes playing the piano and she also likes singing songs.", "她喜欢弹钢琴，也喜欢唱歌。"]},
    "an": {"sentence": ["I usually have an apple and an egg for my breakfast.", "我早餐通常吃一个苹果和一个鸡蛋。"]},
    "art": {"sentence": ["Art is an interesting subject and I like drawing very much.", "美术是一门有趣的学科，我非常喜欢画画。"]},
    "as well as": {"sentence": ["He likes playing basketball as well as football after school.", "放学后他喜欢打篮球，也喜欢踢足球。"]},
    "Asia": {"sentence": ["China is a great country located in the east of Asia.", "中国是一个位于亚洲东部的伟大国家。"]},
    "at the moment": {"sentence": ["Mother is cooking a delicious dinner in the kitchen at the moment.", "妈妈此刻正在厨房里做美味的晚饭。"]},
    "at weekends": {"sentence": ["We often go to the library to study at weekends.", "我们经常在周末去图书馆学习。"]},
    "at work": {"sentence": ["My father is at work now and he will be back soon.", "我父亲现在正在工作，他很快就会回来。"]},
    "aunt": {"sentence": ["My aunt is a friendly nurse in a big city hospital.", "我姨妈是一个大城市医院里一位友好的护士。"]},
    "be bad for": {"sentence": ["Eating too much sweet candy is bad for your teeth.", "吃太多甜糖对你的牙齿有害。"]},
    "be good for": {"sentence": ["Eating more vegetables and fruit is good for your health.", "多吃蔬菜和水果对你的健康有好处。"]},
    "bean": {"sentence": ["My mother often cooks delicious green bean soup in summer.", "我妈妈夏天经常做美味的绿豆汤。"]},
    "bed": {"sentence": ["I usually go to bed at nine o'clock every night.", "我通常每晚九点上床睡觉。"]},
    "begin": {"sentence": ["Our first English lesson will begin at eight o'clock tomorrow.", "明天早晨八点开始我们的第一节英语课。"]},
    "between": {"sentence": ["The new library is between the classroom and the playground.", "新图书馆在教室和操场之间。"]},
    "bit": {"sentence": ["The weather is a bit cold today, so wear your jacket.", "今天天气有点冷，所以穿上你的夹克吧。"]},
    "can't": {"sentence": ["I can't play the violin, but I can play the piano.", "我不会拉小提琴，但我会弹钢琴。"]},
    "card": {"sentence": ["He sent me a beautiful birthday card yesterday morning.", "昨天早晨他寄给我一张精美的生日卡。"]},
    "catch": {"sentence": ["Hurry up! We need to catch the early bus to school.", "快点！我们需要赶早班公交去上学。"]},
    "CD": {"sentence": ["I often listen to English songs on this old CD player.", "我经常用这个旧CD播放机听英语歌。"]},
    "child": {"sentence": ["The little child is playing with a toy car in the yard.", "那个小孩正在院子里玩玩具车。"]},
    "coat": {"sentence": ["Put on your warm coat because it is cold outside now.", "穿上你暖和的外套，因为现在外面很冷。"]},
    "come from": {"sentence": ["Where do these beautiful flowers come from? From the garden.", "这些漂亮的花来自哪里？来自花园。"]},
    "company": {"sentence": ["My father works very hard in a big computer company.", "我父亲在一家大型电脑公司工作非常努力。"]},
    "cut": {"sentence": ["Be careful not to cut your finger with the sharp knife.", "小心别用锋利的刀割到手指。"]},
    "cute": {"sentence": ["The small panda is very cute and everyone likes it.", "那只小熊猫非常可爱，每个人都喜欢它。"]},
    "difficult": {"sentence": ["The math problem is very difficult for the little boy.", "那道数学题对那个小男孩来说非常难。"]},
    "document": {"sentence": ["Please help me print this important document for the meeting.", "请帮我为会议打印这份重要的文档。"]},
    "dress": {"sentence": ["She is wearing a beautiful red dress for the school party.", "她穿着一件漂亮的红裙子去参加学校派对。"]},
    "England": {"sentence": ["London is the capital of England and a very big city.", "伦敦是英国的首都，也是一个非常大的城市。"]},
    "Europe": {"sentence": ["He visited many interesting countries in Europe last summer holiday.", "去年暑假期间他参观了欧洲许多有趣的国家。"]},
    "evening": {"sentence": ["I usually do my homework in the evening before dinner.", "我通常在晚上晚饭前做作业。"]},
    "farmer": {"sentence": ["The farmer is working hard on his large farm now.", "农场主现在正在他的大农场里努力工作。"]},
    "fifty": {"sentence": ["There are about fifty students in our school music club.", "我们学校音乐俱乐部大约有五十名学生。"]},
    "film": {"sentence": ["We went to the cinema to watch an exciting film yesterday.", "昨天我们去电影院看了一部精彩的电影。"]},
    "first name": {"sentence": ["What is your first name? My first name is Peter.", "你叫什么名字？我的名字是彼得。"]},
    "front": {"sentence": ["There is a tall tree in front of our classroom.", "我们教室前面有一棵高树。"]},
    "furniture": {"sentence": ["My parents bought some new furniture for our new house.", "我父母为我们的新房子买了一些新家具。"]},
    "get fat": {"sentence": ["If you eat too much chocolate, you might get fat.", "如果你吃太多巧克力，你可能会变胖。"]},
    "get off": {"sentence": ["Remember to get off the bus at the next station.", "记得在下一站下车。"]},
    "get ready for": {"sentence": ["Every student is getting ready for the school sports meet.", "每个学生都在为校运会做准备。"]},
    "get up": {"sentence": ["He usually gets up early to go for a run in the park.", "他通常起得很早去公园跑步。"]},
    "go back": {"sentence": ["I need to go back home to get my English book.", "我需要回家去拿我的英语书。"]},
    "go home": {"sentence": ["I usually go home immediately after the football match.", "足球赛结束后我通常立即回家。"]},
    "go shopping": {"sentence": ["My mother often goes shopping in the supermarket on Sundays.", "我妈妈经常在周日去超市购物。"]},
    "go to bed": {"sentence": ["It is a good habit to go to bed early every night.", "每天早睡是一个好习惯。"]},
    "go to school": {"sentence": ["I go to school by bike every morning to exercise.", "我每天早晨骑自行车上学以锻炼身体。"]},
    "go to sleep": {"sentence": ["The little baby usually goes to sleep at eight o'clock.", "那个小宝宝通常在八点钟入睡。"]},
    "grandpa": {"sentence": ["My grandpa likes to sit in the garden and read newspapers.", "我爷爷喜欢坐在花园里看报纸。"]},
    "ha ha": {"sentence": ["Ha ha! That is a very funny story you just told us.", "哈哈！你刚才讲的那个故事非常有趣。"]},
    "hall": {"sentence": ["The school meeting will be held in the big school hall.", "学校会议将在学校大礼堂举行。"]},
    "has": {"sentence": ["He has a new schoolbag and two interesting storybooks.", "他有一个新书包和两本有趣的故事书。"]},
    "have breakfast": {"sentence": ["I usually have breakfast with my parents at seven o'clock.", "我通常在七点和父母一起吃早饭。"]},
    "have dinner": {"sentence": ["Our family usually has dinner together at seven every night.", "我们全家人通常在每晚七点一起吃晚饭。"]},
    "have got": {"sentence": ["I have got a new dictionary and it is very useful.", "我得到了一本新字典，它非常有用。"]},
    "have lunch": {"sentence": ["We usually have lunch in the school canteen at twelve.", "我们通常十二点在学校食堂吃午饭。"]},
    "he": {"sentence": ["He is a kind boy and he likes helping his classmates.", "他是一个善良的男孩，他喜欢帮助同学。"]},
    "hear from": {"sentence": ["I hope to hear from my pen friend in England soon.", "我希望很快能收到英国笔友的信。"]},
    "him": {"sentence": ["I saw him playing football on the playground just now.", "我刚才看见他在操场上踢足球。"]},
    "hot dog": {"sentence": ["I like eating hot dogs with a lot of heavy sauce.", "我喜欢吃加了很多厚酱汁的热狗。"]},
    "house": {"sentence": ["My family moved to a small but peaceful house last month.", "上个月我们全家搬到了一所虽小但很宁静的房子里。"]},
    "How about...": {"sentence": ["I like reading books. How about you, my dear friend?", "我喜欢读书。你呢，我亲爱的朋友？"]},
    "hurry up": {"sentence": ["Hurry up! The first English lesson will begin in five minutes.", "快点！第一节英语课五分钟后就开始了。"]},
    "I'm afraid": {"sentence": ["I'm afraid I can't go to your party this Sunday afternoon.", "恐怕这周日下午我不能去参加你的派对。"]},
    "information": {"sentence": ["I use the computer to look up information for my project.", "我用电脑为我的项目查找信息。"]},
    "Internet": {"sentence": ["The Internet is very useful for us to learn new things.", "互联网对我们学习新事物非常有用。"]},
    "IT": {"sentence": ["IT is an interesting subject about computers and technology.", "信息技术是一门关于计算机和技术的有趣的学科。"]},
    "keyboard": {"sentence": ["Please be careful when you use the new computer keyboard.", "使用新电脑键盘时请小心。"]},
    "kilo": {"sentence": ["My mother bought two kilos of fresh apples in the market.", "我妈妈在市场里买了两公斤新鲜苹果。"]},
    "kitchen": {"sentence": ["Mother is busy cooking delicious food in the kitchen now.", "妈妈现在正忙着在厨房里做美味的食物。"]},
    "last name": {"sentence": ["What is your last name? My last name is Green.", "你姓什么？我姓格林。"]}
}

update_json('sentence/【外研版】七年级上册英语电子课本.json', g7_up_fix)
print("Fixed G7 Up missing words.")

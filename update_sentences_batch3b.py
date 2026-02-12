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

# Batch 3b: 七年级下册 (N-Z)
g7_down_entries_nz = {
    "National Day": {"sentence": ["We have a long holiday to celebrate National Day in October.", "我们在十月有一个长假来庆祝国庆节。"]},
    "newspaper": {"sentence": ["My grandfather likes reading the newspaper during breakfast.", "我祖父喜欢在吃早饭时看报纸。"]},
    "nice": {"sentence": ["It's a nice day today, so let's go for a walk in the park.", "今天天气很好，我们去公园散步吧。"]},
    "nobody": {"sentence": ["Nobody was in the classroom when I arrived early this morning.", "今天早晨我早到时，教室里一个人也没有。"]},
    "noisy": {"sentence": ["Don't be so noisy in the library; people are studying here.", "不要在图书馆里这么吵；人们正在这里学习。"]},
    "North American": {"sentence": ["Canada and the USA are famous North American countries.", "加拿大和美国是著名的北美国家。"]},
    "nose": {"sentence": ["The elephant has a very long nose that can pick up food.", "大象有一个能捡起食物的长鼻子。"]},
    "not": {"sentence": ["I am not a teacher; I am a student in the seventh grade.", "我不是老师；我是七年级的学生。"]},
    "not at all": {"sentence": ["- Thank you for your help. - Not at all, I'm happy to help.", "—谢谢你的帮助。—不用谢，我很乐意效劳。"]},
    "not only... but also...": {"sentence": ["She is not only a clever student but also a kind girl.", "她不仅是一个聪明的学生，还是一个善良的女孩。"]},
    "November": {"sentence": ["November is the eleventh month and the weather is getting cold.", "十一月是第十一个月，天气正在变冷。"]},
    "October": {"sentence": ["October is a beautiful month with many golden leaves on trees.", "十月是一个美丽的月份，树上有许多金色的叶子。"]},
    "on": {"sentence": ["There is a big map of China on the wall of our classroom.", "我们教室的墙上挂着一幅巨大的中国地图。"]},
    "once upon a time": {"sentence": ["Once upon a time, there was a king who lived in a big palace.", "从前，有一位住在巨大宫殿里的国王。"]},
    "one": {"sentence": ["I have only one sister, and she is a student in primary school.", "我只有一个姐姐，她是小学的学生。"]},
    "one day": {"sentence": ["I hope to travel all over the world with my family one day.", "我希望有一天能和家人一起周游世界。"]},
    "one of": {"sentence": ["Shanghai is one of the biggest cities in China with many people.", "上海是中国人口众多的最大城市之一。"]},
    "open": {"sentence": ["Please open your books to page twenty and read the text.", "请翻开书到第二十页并读课文。"]},
    "opera": {"sentence": ["My grandparents often enjoy watching Beijing Opera on TV.", "我的祖父母经常喜欢在电视上看京剧。"]},
    "Pacific": {"sentence": ["The Pacific Ocean is the largest ocean in the whole world.", "太平洋是全世界最大的大洋。"]},
    "palace": {"sentence": ["The Forbidden City is a famous ancient palace in Beijing.", "故宫是北京著名的古老宫殿。"]},
    "pay": {"sentence": ["How much did you pay for this new and beautiful schoolbag?", "你买这个漂亮的新书包花了多少钱？"]},
    "phone": {"sentence": ["Can I use your phone to call my mother? I left mine at home.", "我能用你的电话给我妈妈打个电话吗？我把我的忘在家里了。"]},
    "piano": {"sentence": ["She can play the piano very well because she practises every day.", "她钢琴弹得很好，因为她每天都练习。"]},
    "pick": {"sentence": ["The children are picking some colorful flowers in the garden.", "孩子们正在花园里采摘一些彩色的花。"]},
    "pig": {"sentence": ["The little pig on the farm is very cute and likes eating a lot.", "农场里的小猪非常可爱，而且很爱吃。"]},
    "plane": {"sentence": ["We will take a plane to Beijing for our next summer holiday.", "下个暑假我们将坐飞机去北京。"]},
    "play": {"sentence": ["They like to play football on the playground after school.", "他们喜欢在放学后在操场上踢足球。"]},
    "player": {"sentence": ["He is a famous basketball player who has won many matches.", "他是一位赢得了许多比赛的著名篮球运动员。"]},
    "point at": {"sentence": ["It's not polite to point at people while you are talking.", "说话时指着别人是不礼貌的。"]},
    "pop": {"sentence": ["Pop music is very popular among teenagers all over the world.", "流行音乐在全世界的青少年中都很受欢迎。"]},
    "post office": {"sentence": ["I need to go to the post office to send a letter to my friend.", "我需要去邮局给我的朋友寄封信。"]},
    "president": {"sentence": ["The president of the company gave a speech at the meeting.", "公司的总裁在会议上发表了讲话。"]},
    "price": {"sentence": ["What is the price of this dictionary? It's thirty yuan.", "这本字典多少钱？三十元。"]},
    "primary": {"sentence": ["He is a student in a local primary school near our house.", "他是我们家附近一所当地小学的学生。"]},
    "promise": {"sentence": ["I promise to finish my homework before my mother comes back.", "我保证在妈妈回来前完成作业。"]},
    "purple": {"sentence": ["She wore a beautiful purple dress for the school party.", "她穿着一件漂亮的紫色连衣裙参加学校派对。"]},
    "push": {"sentence": ["You should push the door to open it; don't pull it.", "你应该推门来打开它；别拉。"]},
    "question": {"sentence": ["If you have any questions, please raise your hand to ask.", "如果你有任何问题，请举手提问。"]},
    "rain": {"sentence": ["It often rains in spring, which is good for the small trees.", "春天常下雨，这对小树有好处。"]},
    "ready to do sth.": {"sentence": ["We are all ready to start our new class trip to the museum.", "我们都准备好开始去博物馆的新班级旅行了。"]},
    "right": {"sentence": ["Go straight along this road and turn right at the corner.", "沿着这条路直走，在拐角处向右转。"]},
    "river": {"sentence": ["There is a long river flowing through the center of our city.", "有一条长河穿过我们城市的中心。"]},
    "robot": {"sentence": ["My father bought a smart robot that can help clean the house.", "我爸爸买了一个能帮着打扫房子的智能机器人。"]},
    "rude": {"sentence": ["It is rude to talk loudly when people are studying here.", "人们在这里学习时大声说话是不礼貌的。"]},
    "ruler": {"sentence": ["Can I borrow your ruler? I need to draw a straight line.", "可以借用一下你的尺子吗？我需要画一条直线。"]},
    "Russia": {"sentence": ["Russia is a very big country located in both Europe and Asia.", "俄罗斯是一个横跨欧亚两洲的非常大的国家。"]},
    "Russian": {"sentence": ["My neighbor is Russian and he can speak Chinese very well.", "我邻居是俄罗斯人，他中文说得很好。"]},
    "sad": {"sentence": ["She felt very sad because she lost her favourite toy cat.", "她感到非常伤心，因为她丢了她最喜欢的玩具猫。"]},
    "safe": {"sentence": ["It is safe to cross the street when the light is green.", "绿灯亮时过马路是安全的。"]},
    "sale": {"sentence": ["Many beautiful clothes in that shop are on sale this week.", "那家店的许多漂亮衣服本周在打折。"]},
    "sausage": {"sentence": ["My brother likes eating hot dogs with a a big sausage.", "我弟弟喜欢吃夹着大香肠的热狗。"]},
    "sea": {"sentence": ["The blue sea looks very beautiful under the bright sun.", "在灿烂的阳光下，蓝色的大海看起来非常美丽。"]},
    "sell": {"sentence": ["That shop sells many kinds of fresh fruit and vegetables.", "那家商店售卖多种新鲜水果和蔬菜。"]},
    "September": {"sentence": ["The new school year always begins in early September in China.", "在中国，新学年总是从九月初开始。"]},
    "shake hands": {"sentence": ["People usually shake hands when they meet for the first time.", "人们第一次见面时通常会握手。"]},
    "ship": {"sentence": ["A large ship is sailing on the ocean towards the next city.", "一艘大船正行驶在大洋上前往下一个城市。"]},
    "shirt": {"sentence": ["He is wearing a white shirt and a pair of blue trousers today.", "他今天穿着一件白衬衫和一条蓝裤子。"]},
    "shopping": {"sentence": ["I often go shopping with my mother on Sunday mornings.", "我常在周日早晨和妈妈一起去购物。"]},
    "short": {"sentence": ["He has short black hair and wears a pair of small glasses.", "他留着黑色短发，戴着一副小眼镜。"]},
    "sightseeing": {"sentence": ["We decided to go sightseeing in Beijing for our holiday.", "我们决定假期去北京观光。"]},
    "silly": {"sentence": ["Don't be silly! It is impossible for pigs to fly in the sky.", "别傻了！猪是不可能在天空中飞的。"]},
    "size": {"sentence": ["What size of shoes do you wear? I wear size thirty-eight.", "你穿多大码的鞋？我穿三十八码。"]},
    "slow": {"sentence": ["The old man is walking very slow along the quiet river.", "那位老人在宁静的河边走得很慢。"]},
    "so": {"sentence": ["It was raining, so we had to stay at home and read books.", "天在下雨，所以我们不得不待在家里看书。"]},
    "somewhere": {"sentence": ["I think I have seen that tall boy somewhere before last year.", "我觉得去年我在某处见过那个高个子男孩。"]},
    "South American": {"sentence": ["Brazil is the largest South American country with many trees.", "巴西是拥有许多树木的最大南美国家。"]},
    "space": {"sentence": ["Astronauts travel into space to explore different planets.", "宇航员进入太空探索不同的星球。"]},
    "stop": {"sentence": ["Please stop talking and listen to the teacher carefully now.", "现在请停止说话，仔细听老师讲课。"]},
    "street": {"sentence": ["There are many tall buildings and busy shops on this street.", "这条街上有许多高楼和繁忙的商店。"]},
    "summer holiday": {"sentence": ["We will have a long summer holiday after the final school exam.", "期末考试后我们将有一个漫长的暑假。"]},
    "supermarket": {"sentence": ["My mother often buys fresh food in the supermarket near us.", "我妈妈经常在我们附近的超市买新鲜食物。"]},
    "sure": {"sentence": ["Are you sure about the result of the important math test?", "你确定那次重要数学测试的结果吗？"]},
    "swim": {"sentence": ["I often go to swim in the pool with my friends in summer.", "夏天我经常和朋友们去游泳池游泳。"]},
    "take": {"sentence": ["Remember to take your umbrella because it might rain later.", "记得带上你的伞，因为等下可能会下雨。"]},
    "take a walk": {"sentence": ["My grandfather usually takes a walk after dinner every day.", "我祖父通常每天晚饭后散步。"]},
    "tape": {"sentence": ["I used some tape to fix my broken English textbook today.", "今天我用了一些胶带修补我坏掉的英语课本。"]},
    "taxi": {"sentence": ["We took a taxi to the airport because we were in a hurry.", "因为赶时间，我们打了辆出租车去机场。"]},
    "term": {"sentence": ["We will learn many new interesting lessons this term.", "这学期我们将学习许多新的有趣课程。"]},
    "that's all": {"sentence": ["That's all for today's lesson. See you all tomorrow morning.", "今天的课就到这里。明天早上见。"]},
    "then": {"sentence": ["First finish your homework, and then you can watch TV for a while.", "先完成作业，然后你可以看一会儿电视。"]},
    "third": {"sentence": ["He came third in the hundred-meter race yesterday afternoon.", "昨天下午他在百米赛跑中得了第三名。"]},
    "thousand": {"sentence": ["There are more than two thousand students in our big school.", "我们这所大校有超过两千名学生。"]},
    "tidy": {"sentence": ["You should keep your room clean and tidy every day.", "你应该每天保持房间干净整洁。"]},
    "till": {"sentence": ["I stayed in the school library till seven o'clock yesterday.", "昨天我在学校图书馆待到了七点。"]},
    "top": {"sentence": ["We climbed to the top of the hill to see the beautiful sunrise.", "我们爬到山顶去看美丽的日出。"]},
    "tourist": {"sentence": ["Thousands of tourists visit the Great Wall every year.", "每年有数以千计的游客参观长城。"]},
    "traffic jam": {"sentence": ["He was late for the meeting because of the heavy traffic jam.", "因为交通堵塞，他开会迟到了。"]},
    "try on": {"sentence": ["Can I try on this blue shirt? I think it will look nice.", "我能试穿这件蓝衬衫吗？我觉得它会很好看。"]},
    "turn": {"sentence": ["Please turn left at the next corner and you will see the bank.", "请在下个拐角处向左转，你就会看到银行。"]},
    "underground": {"sentence": ["Taking the underground is a very fast way to travel in the city.", "坐地铁是在城市里出行的非常快的方式。"]},
    "up": {"sentence": ["Please stand up and read the text on page thirty clearly.", "请站起来，清晰地读出第三十页上的课文。"]},
    "upon": {"sentence": ["Once upon a time, there lived a brave knight in a small castle.", "从前，一位勇敢的骑士住在一座小城堡里。"]},
    "US": {"sentence": ["The US is a very big country located in North America.", "美国是位于北美洲的一个非常大的国家。"]},
    "village": {"sentence": ["My grandparents live in a small and peaceful village near the sea.", "我祖父母住在一个靠近大海的宁静小村庄里。"]},
    "violin": {"sentence": ["She is learning how to play the violin in the music club now.", "她现在正在音乐俱乐部学习如何拉小提琴。"]},
    "visitor": {"sentence": ["There are many visitors in the museum on Sunday afternoons.", "周日下午博物馆里有很多游客。"]},
    "wait a minute": {"sentence": ["Wait a minute! I need to find my keys before we go out.", "等一下！出发前我需要找到我的钥匙。"]},
    "walk": {"sentence": ["We like to walk in the park to enjoy the fresh air after dinner.", "我们喜欢在晚饭后去公园散步享受新鲜空气。"]},
    "waltz": {"sentence": ["The waltz is a very famous and beautiful kind of dance.", "华尔兹是一种非常著名且优美的舞蹈。"]},
    "watch": {"sentence": ["We like to watch football matches on TV together on weekends.", "我们喜欢在周末一起从电视上看足球赛。"]},
    "way": {"sentence": ["Can you tell me the way to the nearest bus station, please?", "你能告诉我最近的车站怎么走吗？"]},
    "well": {"sentence": ["She can speak English very well after living in London for a year.", "在伦敦住了一年后，她英语说得很好。"]},
    "what": {"sentence": ["What is your favourite subject? My favourite is English.", "你最喜欢的科目是什么？我最喜欢的是英语。"]},
    "whose": {"sentence": ["Whose schoolbag is this? It belongs to the new student, Tom.", "这是谁的书包？它是新同学汤姆的。"]},
    "why": {"sentence": ["Why didn't you come to my birthday party last Saturday night?", "上周六晚上你为什么没来参加我的生日派对？"]},
    "Why not...": {"sentence": ["Why not go to the cinema with us this Sunday afternoon?", "为什么不本周日下午和我们一起去电影院呢？"]},
    "win": {"sentence": ["I hope our school team can win the match this Friday.", "我希望我们校队能赢得本周五的比赛。"]},
    "wonderful": {"sentence": ["We had a wonderful time during our summer holiday in Beijing.", "我们在北京度过了一个美妙的暑假。"]},
    "work": {"sentence": ["My father works very hard in a big company every day.", "我父亲每天在一家大公司工作得很努力。"]},
    "working": {"sentence": ["He is very busy working on his new computer science project.", "他正忙于研究他的新计算机科学项目。"]},
    "world-famous": {"sentence": ["The Great Wall is a world-famous historical place in China.", "长城是中国举世闻名的历史古迹。"]},
    "worry": {"sentence": ["Don't worry about the results; just try your best in the test.", "别担心结果；只要在考试中尽力而为就好。"]},
    "worry about": {"sentence": ["Parents always worry about their children's health and study.", "父母总是担心孩子的健康和学习。"]},
    "would like": {"sentence": ["I would like to have a cup of hot tea and some small cakes.", "我想要一杯热茶和一些小蛋糕。"]},
    "writer": {"sentence": ["He wants to be a famous writer and write many interesting books.", "他想成为一名著名的作家，写许多有趣的书。"]},
    "yesterday": {"sentence": ["I went to the library to study with my classmates yesterday.", "昨天我和同学们去图书馆学习了。"]},
    "young": {"sentence": ["The young man is very kind and often helps the old people.", "那个年轻人很善良，经常帮助老人。"]},
    "yours": {"sentence": ["This dictionary is mine, and that new one is yours.", "这本字典是我的，那本新的是你的。"]}
}

update_json('sentence/【外研版】七年级下册英语电子课本.json', g7_down_entries_nz)

# Batch 3b: 七年级下册(2025春版)
g7_down_spring_entries = {
    "lift sb's spirits": {"sentence": ["Listening to music can always lift my spirits when I am sad.", "当我难过时，听音乐总能振奋我的心情。"]}
}
update_json('sentence/【外研版】七年级下册(2025春版)英语电子课本.json', g7_down_spring_entries)

print("Updated Batch 3b: N-Z and Spring Edition.")

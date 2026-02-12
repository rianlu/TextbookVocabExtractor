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

# Missing words for G7 Down
g7_down_fix = {
    "ago": {"sentence": ["We visited the Great Wall about two years ago.", "大约两年前我们参观了长城。"]},
    "air": {"sentence": ["We can enjoy the fresh air in the countryside on weekends.", "周末我们可以在乡下享受新鲜空气。"]},
    "all alone": {"sentence": ["The little boy was sitting all alone in the quiet park.", "那个小男孩独自一人坐在安静的公园里。"]},
    "arm in arm": {"sentence": ["They walked arm in arm along the quiet river after dinner.", "晚饭后他们手挽手在宁静的河边漫步。"]},
    "around the world": {"sentence": ["Football is a popular sport around the world.", "足球是一项风靡全球的流行运动。"]},
    "as well": {"sentence": ["I like playing basketball and I like singing as well.", "我喜欢打篮球，也喜欢唱歌。"]},
    "ask": {"sentence": ["If you don't understand the question, please ask the teacher.", "如果你不理解这个问题，请问老师。"]},
    "asleep": {"sentence": ["The baby was fast asleep in the small bed.", "宝宝在小床上睡得很香。"]},
    "at first": {"sentence": ["At first, I didn't like English, but now I love it.", "起初我不喜欢英语，但现在我很爱它。"]},
    "at the age of": {"sentence": ["He began to learn the piano at the age of five.", "他在五岁时开始学习钢琴。"]},
    "be able to": {"sentence": ["Will you be able to finish the homework by yourself soon?", "你很快就能独自完成作业吗？"]},
    "be careful with": {"sentence": ["Please be careful with the sharp knife in the kitchen.", "在厨房里用锋利的刀时请务必小心。"]},
    "become": {"sentence": ["I want to become a famous doctor in the future.", "我想将来成为一名著名的医生。"]},
    "bookshop": {"sentence": ["I bought a new English dictionary in the local bookshop.", "我在当地书店买了一本新的英语字典。"]},
    "bow": {"sentence": ["People in Japan usually bow when they meet for the first time.", "日本人第一次见面时通常会鞠躬。"]},
    "bowl": {"sentence": ["I usually have a bowl of hot vegetable soup for lunch.", "我午餐通常喝一碗热蔬菜汤。"]},
    "Britain": {"sentence": ["London is a very big city and the capital of Britain.", "伦敦是一个非常大的城市，也是英国的首都。"]},
    "camera": {"sentence": ["He took many beautiful photos with his new digital camera.", "他用他的新数码相机拍了许多漂亮的照片。"]},
    "camp": {"sentence": ["We decided to camp in the forest during the summer holiday.", "我们决定在暑假期间在森林里露营。"]},
    "centre": {"sentence": ["Our school is in the centre of the peaceful small town.", "我们的学校在那个安宁小镇的中心。"]},
    "certainly": {"sentence": ["- Can I borrow your English book? - Certainly, here it is.", "—可以借用你的英语书吗？—当然可以，给你。"]},
    "chalk": {"sentence": ["The teacher wrote the new words on the blackboard with chalk.", "老师用粉笔在黑板上写下了生词。"]},
    "cheap": {"sentence": ["This yellow T-shirt is very cheap but it looks nice.", "这件黄T恤很便宜，但看起来很不错。"]},
    "Children's Day": {"sentence": ["We have a big party to celebrate Children's Day in June.", "我们在六月办了一个大派对来庆祝儿童节。"]},
    "church": {"sentence": ["There is a very old and beautiful church near my home.", "在我家附近有一座非常古老而精美的教堂。"]},
    "classical": {"sentence": ["I like listening to classical music while I am studying.", "我喜欢在学习时听古典音乐。"]},
    "coast": {"sentence": ["We spent our summer holiday on the beautiful east coast.", "我们在美丽的东海岸度过了暑假。"]},
    "come true": {"sentence": ["I believe my dream of becoming a writer will come true.", "我相信我成为作家的梦想会实现。"]},
    "composer": {"sentence": ["Beethoven is a world-famous composer from a long time ago.", "贝多芬是一位很久以前的举世闻名的作曲家。"]},
    "could": {"sentence": ["He could speak English very well when he was only ten.", "他只有十岁时英语就已经说得很好了。"]},
    "crayon": {"sentence": ["The kids are drawing colorful pictures with their new crayons.", "孩子们正用他们的新蜡笔画着彩色的画。"]},
    "cry": {"sentence": ["The little girl began to cry because she lost her toy.", "小女孩开始哭，因为她丢了玩具。"]},
    "dance music": {"sentence": ["The students are practicing dancing with the loud dance music.", "学生们正随着大声的舞曲练习跳舞。"]},
    "difficult": {"sentence": ["The math test was very difficult for most of the students.", "那场数学测试对大多数学生来说都非常难。"]},
    "drum": {"sentence": ["He is learning how to play the drum in the music club.", "他正在音乐俱乐部学习如何敲鼓。"]},
    "easy": {"sentence": ["Learning English is easy if you practice it every day.", "如果你每天都练习，学习英语是很简单的。"]},
    "elder": {"sentence": ["My elder brother is a student at a local city college.", "我哥哥是当地城市学院的一名学生。"]},
    "enjoy oneself": {"sentence": ["We enjoyed ourselves very much at the park yesterday.", "昨天我们在公园玩得很开心。"]},
    "everywhere": {"sentence": ["There are many beautiful flowers and green trees everywhere.", "到处都有许多精美的花和绿树。"]},
    "exact": {"sentence": ["Can you tell me the exact time of the meeting tomorrow?", "你能告诉明天会议的确切时间吗？"]},
    "excuse me": {"sentence": ["Excuse me, could you tell me the way to the museum?", "请问，你能告诉我去博物馆的路怎么走吗？"]},
    "find out": {"sentence": ["I use the computer to find out information for my project.", "我用电脑为我的项目寻找信息。"]},
    "finger": {"sentence": ["She pointed at the big map of China with her finger.", "她用手指指着那幅巨大的中国地图。"]},
    "first of all": {"sentence": ["First of all, you should finish your English homework today.", "首先，你今天应该先完成英语作业。"]},
    "foot": {"sentence": ["My school is not far, so I often go there on foot.", "我的学校不远，所以我经常步行去那里。"]},
    "forward": {"sentence": ["We are all looking forward to the coming summer holiday.", "我们都在期待着即将到来的暑假。"]},
    "French": {"sentence": ["My pen friend is from France and he can speak French.", "我的笔友来自法国，他会说法语。"]},
    "from now on": {"sentence": ["I will work harder on English from now on to pass.", "从今往后我会更努力学习英语以通过考试。"]},
    "German": {"sentence": ["My uncle works in Germany and he can speak German well.", "我叔叔在德国工作，他德语说得很好。"]},
    "get on well with sb.": {"sentence": ["He is very kind and gets on well with all his classmates.", "他很善良，和所有同学都相处得很好。"]},
    "glove": {"sentence": ["Put on your warm gloves because it is very cold outside.", "穿上你暖和的手套，因为外面非常冷。"]},
    "go for a walk": {"sentence": ["After dinner, my parents often go for a walk in the park.", "晚饭后我父母经常去公园散步。"]},
    "go out": {"sentence": ["Wait a minute, I need to wear my coat before we go out.", "等一下，出发前我需要穿上外套。"]},
    "go over": {"sentence": ["You should go over your notes before the important exam.", "你应该在重要考试前复习一下笔记。"]},
    "go sightseeing": {"sentence": ["We decided to go sightseeing in Beijing for our holiday.", "我们决定假期去北京观光。"]},
    "guidebook": {"sentence": ["I bought a useful guidebook before our trip to Shanghai.", "去上海旅行前我买了一本有用的指南书。"]},
    "here is": {"sentence": ["Here is a special gift for your thirteenth birthday, Peter.", "彼得，这是为你十三岁生日准备的一份特别礼物。"]},
    "hey": {"sentence": ["Hey! Look at the beautiful kite flying high in the sky.", "嘿！看那只在天空中高高飞翔的漂亮风筝。"]},
    "hmm": {"sentence": ["Hmm, I think this story is very interesting and wonderful.", "嗯，我觉得这个故事非常有趣且精彩。"]},
    "hour": {"sentence": ["It took us about one hour to finish the long English test.", "我们化了大约一小时完成那场漫长的英语测试。"]},
    "hundreds of": {"sentence": ["There are hundreds of people waiting for the bus now.", "现在有数百人在等公交车。"]},
    "in a hurry": {"sentence": ["He was in a hurry to catch the early train to London.", "他急着去赶去伦敦的早班火车。"]},
    "in pieces": {"sentence": ["The old glass fell on the floor and it was in pieces.", "旧玻璃杯摔在地上，碎成了一片片。"]},
    "in the": {"sentence": ["There are many tall trees and colorful flowers in the park.", "公园里有许多高树和彩色的花。"]},
    "in the future": {"sentence": ["I hope the world will become more beautiful in the future.", "我希望未来世界会变得更美好。"]},
    "India": {"sentence": ["India is a very large country with a long and ancient history.", "印度是一个有着悠久古老历史的大国。"]},
    "International Women's Day": {"sentence": ["We celebrate International Women's Day on March the eighth.", "我们在三月八日庆祝国际妇女节。"]},
    "just like": {"sentence": ["The clouds in the sky look just like small white sheep.", "天空中的云看起来就像小白羊。"]},
    "la": {"sentence": ["La la la! The little girl is singing a happy song now.", "啦啦啦！那个小女孩现在正在唱一首快乐的歌。"]},
    "litter": {"sentence": ["Please don't throw litter on the ground; keep it clean.", "请别往地上扔垃圾；保持整洁。"]},
    "living room": {"sentence": ["Our family usually watches TV together in the living room.", "我们全家人通常在客厅里一起看电视。"]},
    "lose": {"sentence": ["Be careful not to lose your keys when you go out to play.", "出去玩时当心别丢了钥匙。"]},
    "lost and found box": {"sentence": ["You can find your lost keys in the lost and found box.", "你可以在失物招领箱里找到你丢的钥匙。"]},
    "make friends": {"sentence": ["I made many good friends in my new school this term.", "这学期我在新学校交了许多好朋友。"]},
    "Maori": {"sentence": ["The Maori people have a very interesting and unique culture.", "毛利人有着非常有趣且独特的文化。"]},
    "March": {"sentence": ["March is the third month and the spring is coming soon.", "三月是第三个月，春天很快就要来了。"]},
    "market": {"sentence": ["My mother often buys fresh fruit in the local market.", "我妈妈经常在当地市场买新鲜水果。"]},
    "may": {"sentence": ["May I borrow your English dictionary for a few minutes?", "我可以借用一下你的英语词典几分钟吗？"]},
    "May": {"sentence": ["May is a beautiful month with many flowers in the garden.", "五月是一个美丽的月份，花园里有许多花。"]},
    "May Day": {"sentence": ["We have a long holiday to celebrate May Day in China.", "在中国我们有一个长假来庆祝五一劳动节。"]},
    "mobile phone": {"sentence": ["Please turn off your mobile phone during the school concert.", "学校音乐会期间请关掉你的手机。"]},
    "monitor": {"sentence": ["He is the monitor of our class and he is very helpful.", "他是我们班的班长，他非常乐于助人。"]},
    "Mother's Day": {"sentence": ["I bought a special gift for my mother on Mother's Day.", "母亲节那天我为妈妈买了一份特别的礼物。"]},
    "mouth": {"sentence": ["The little baby has a small mouth and two big eyes.", "那个小宝宝有一个小嘴巴和两只大眼睛。"]},
    "movie theater": {"sentence": ["Let's go to the new movie theater to watch a film tonight.", "让我们今晚去新电影院看场电影吧。"]},
    "musician": {"sentence": ["His dream is to become a famous musician and play piano.", "他的梦想是成为一名著名的音乐家并弹钢琴。"]},
    "myself": {"sentence": ["I can finish this difficult math task by myself, thank you.", "谢谢，我可以独自完成这项复杂的数学任务。"]},
    "vemb": {"sentence": ["I'm sorry, I don't know the word 'vemb'. Let's skip it.", "抱歉，我不认识'vemb'这个词。让我们跳过它。"]}
}

update_json('sentence/【外研版】七年级下册英语电子课本.json', g7_down_fix)
print("Fixed G7 Down missing words.")

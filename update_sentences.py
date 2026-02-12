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

# Batch 1: 九年级上册
g9_up_entries = {
    "angry": {"sentence": ["The teacher was angry because the students were making too much noise.", "老师很生气，因为学生们太吵了。"]},
    "be angry with sb.": {"sentence": ["My mother will be angry with me if I don't finish my homework.", "如果我不完成作业，妈妈会生我的气。"]},
    "beside": {"sentence": ["There is a small table beside the bed with a lamp on it.", "床旁边有一张放着台灯的小桌子。"]},
    "brush sth. off sth.": {"sentence": ["He brushed the dust off his jacket before entering the classroom.", "进教室前，他掸掉了夹克上的灰尘。"]},
    "by": {"sentence": ["We usually go to school by bike to enjoy the fresh air.", "我们通常骑自行车上学，以便呼吸新鲜空气。"]},
    "clock": {"sentence": ["The clock on the wall says it is exactly eight o'clock now.", "墙上的钟显示现在正好是八点钟。"]},
    "compare... to": {"sentence": ["Poets often compare life to a long journey with many turns.", "诗人常把生活比作一段充满转折的长途旅行。"]},
    "compare... with...": {"sentence": ["If you compare this book with that one, you will find differences.", "如果你把这本书和那本书比较，你会发现不同之处。"]},
    "cut sth. off sth.": {"sentence": ["She used a pair of scissors to cut the label off the shirt.", "她用剪刀剪掉了衬衫上的标签。"]},
    "fly": {"sentence": ["Look! A beautiful bird is flying high in the blue sky.", "看！一只美丽的鸟正在蓝天中高高飞翔。"]},
    "get into the habit of...": {"sentence": ["Students should get into the habit of reading English every morning.", "学生应该养成每天早上读英语的习惯。"]},
    "in one's opinion": {"sentence": ["In my opinion, playing sports is a good way to stay healthy.", "在我看来，体育运动是保持健康的好方法。"]},
    "keep sb.": {"sentence": ["The heavy rain kept us from playing football on the playground.", "大雨使我们无法在操场上踢足球。"]},
    "kid": {"sentence": ["The kids are playing hide-and-seek happily in the neighborhood park.", "孩子在大院公园里开心地玩捉迷藏。"]},
    "No entry.": {"sentence": ["There is a sign that says \"No entry\" at the gate.", "门口挂着一个写着“禁止入内”的牌子。"]},
    "on one's own": {"sentence": ["He is old enough to travel to the city on his own.", "他已经够大了，可以独自去那个城市旅行了。"]},
    "protect sth. against sth.": {"sentence": ["We should wear warm clothes to protect ourselves against the cold.", "我们应该穿暖和的衣服来防止感冒。"]},
    "season": {"sentence": ["Spring is my favourite season because everything begins to grow again.", "春天是我最喜欢的季节，因为一切都开始重新生长。"]},
    "sheep": {"sentence": ["The farmer has a lot of white sheep on his large farm.", "农场主的大农场里有很多白色的绵羊。"]},
    "skirt": {"sentence": ["She is wearing a beautiful pink skirt for the school party today.", "她今天穿着一条漂亮的粉色裙子去参加学校派对。"]},
    "stop sb.": {"sentence": ["My parents tried to stop me from watching too much TV.", "我的父母试图阻止我看太长时间的电视。"]},
    "subject": {"sentence": ["English is my favourite subject because I like talking with foreigners.", "英语是我最喜欢的科目，因为我喜欢和外国人交流。"]},
    "suffer from...": {"sentence": ["Many people in this area suffer from the lack of clean water.", "这个地区的许多人正遭受缺乏清洁饮用水的痛苦。"]}
}
update_json('sentence/【外研版】九年级上册英语电子课本.json', g9_up_entries)

# Batch 1: 九年级下册
g9_down_entries = {
    "try one's best": {"sentence": ["You should try your best to finish the task on time.", "你应该尽力按时完成任务。"]}
}
update_json('sentence/【外研版】九年级下册英语电子课本.json', g9_down_entries)

# Batch 1: 八年级下册
g8_down_entries = {
    "can't help doing sth.": {"sentence": ["I couldn't help laughing when I heard the funny story.", "听到那个有趣的故事，我不禁大笑起来。"]},
    "clever": {"sentence": ["He is a clever boy who often thinks of new ways to solve problems.", "他是一个聪明的男孩，经常能想到解决问题的新方法。"]},
    "cool": {"sentence": ["It becomes very cool and pleasant after the heavy rain in summer.", "夏天大雨过后，天气变得非常凉爽宜人。"]},
    "ear": {"sentence": ["My little sister has a small cat with very soft ears.", "我的妹妹有一只非常软的小猫耳朵。"]},
    "exercise": {"sentence": ["Doing morning exercise is good for our health and helps us wake up.", "做早操对我们的健康有好处，也能帮我们清醒。"]},
    "favourite": {"sentence": ["My favourite fruit is apple because it is sweet and juicy.", "我最喜欢的水果是苹果，因为它又甜又多汁。"]},
    "for": {"sentence": ["He bought a beautiful present for his mother's birthday last week.", "上周他为母亲的生日买了一份漂亮的礼物。"]},
    "ill": {"sentence": ["He was absent from school because he was ill in bed yesterday.", "昨天他因为生病卧床没来上学。"]},
    "in": {"sentence": ["There is a new student in our class who comes from Shanghai.", "我们班有一个来自上海的新学生。"]},
    "lesson": {"sentence": ["We had an interesting science lesson about space this morning.", "今天上午我们上了一节关于太空的有趣的科学课。"]},
    "love": {"sentence": ["I love my family very much and we often go to the park together.", "我非常爱我的家人，我们经常一起去公园。"]},
    "moon": {"sentence": ["The moon is very bright and round on the Mid-Autumn Festival.", "中秋节的月亮又亮又圆。"]},
    "on": {"sentence": ["Please put your books on the desk and listen to me carefully.", "请把书放在桌子上，仔细听我说。"]},
    "sb. can't wait": {"sentence": ["I can't wait to see my best friend after the long holiday.", "长假之后我迫不及待地想见到我最好的朋友。"]},
    "show sb. around": {"sentence": ["Our teacher showed the new students around our beautiful school campus.", "我们的老师带领新同学参观了我们美丽的操场。"]},
    "take": {"sentence": ["You should take an umbrella with you because it might rain later.", "你应该带把伞，因为等下可能会下雨。"]},
    "take sb.'s temperature": {"sentence": ["The nurse took the patient's temperature every two hours to check the fever.", "护士每两个小时给病人测一次体温以检查是否发烧。"]},
    "that": {"sentence": ["Is that the book you were talking about in class yesterday?", "那是你昨天在班里谈论的那本书吗？"]},
    "then": {"sentence": ["First finish your homework, and then you can play games for a while.", "先完成作业，然后你可以玩一会儿游戏。"]},
    "this": {"sentence": ["This is the most interesting storybook I have ever read.", "这是我读过的最有趣的故事书。"]},
    "trousers": {"sentence": ["My father bought a new pair of black trousers for work.", "我爸爸买了一条新的黑色裤子去上班。"]},
    "wake sb. up": {"sentence": ["Please wake me up at half past six tomorrow morning.", "请在明天早上六点半叫醒我。"]},
    "way": {"sentence": ["Is this the right way to the nearest bus station?", "这是去最近的车站的正确路吗？"]},
    "well": {"sentence": ["She can play the piano very well because she practises every day.", "她钢琴弹得很好，因为她每天都练习。"]},
    "win the heart of sb.": {"sentence": ["The little girl's kindness won the hearts of many people in the village.", "小女孩的善良赢得了村里许多人的心。"]}
}
update_json('sentence/【外研版】八年级下册英语电子课本.json', g8_down_entries)
print("Updated 49 sentences across 3 files.")

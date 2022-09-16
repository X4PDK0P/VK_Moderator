import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

TOKEN = '0f1d4e6254d63423f1b0868d1bf1c5e8130b123a8a15f6a077edbbd33e07fa8620aecf62dcf0da52700b5'
pref = '..'


vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
botlongpoll = VkBotLongPoll(vk_session, "185696825")
AdminList = {}


# Отправка сообщений в чат
def sender(id_chat, text):
    vk_session.method('messages.send', {'chat_id': id_chat, 'message': text, 'random_id': 0})


# Бот
for event in botlongpoll.listen():
    flag = 0
    if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
        msg = event.message.text
        id_chat = event.chat_id
        id_member = event.message.from_id
        print(id_chat, id_member, msg)
        if (not msg == '..') and msg[:2] == '..':
            member_peer_id = event.obj['message']['peer_id']

            ConversationItems = vk.messages.getConversationMembers(peer_id=member_peer_id)['items']
            name = vk.messages.getConversationMembers(peer_id=member_peer_id)['profiles']

            # Админ
            if not (member_peer_id in AdminList):
                AdminList[member_peer_id] = []
            for id_member_for_check in ConversationItems:
                try:
                    AdminList_temp = AdminList[member_peer_id]
                    if id_member_for_check["is_admin"] and id_member_for_check['member_id'] not in AdminList_temp:
                        AdminList_temp.append(id_member_for_check["member_id"])
                        AdminList[member_peer_id] = AdminList_temp
                except:
                    pass
            print('Администраторы чата', AdminList)

            # Имя
            name = vk.messages.getConversationMembers(peer_id=member_peer_id)['profiles']
            if pref in msg and flag < 1:
                if 'кто я' in msg.lower():
                    for i in range(len(name)):
                        try:
                            if id_member == name[i]['id']:
                                sender(id_chat, 'Вас зовут:\n' + '[id' + str(id_member) + '|' + name[i]['first_name'] + ']')
                                flag += 1
                        except:
                            print('name err')

            # Проверка
            if pref in msg and flag < 1:
                if id_member in AdminList[member_peer_id]:
                    for i in range(len(name)):
                        if id_member == name[i]['id']:
                            if 'проверка' in msg.lower():
                                print('OK')
                                sender(id_chat, '[id' + str(id_member) + '|' + name[i]['first_name'] + ']' + ', модератор.')
                                flag += 1
                else:
                    for i in range(len(name)):
                        if id_member == name[i]['id']:
                            sender(id_chat, '[id' + str(id_member) + '|' + name[i]['first_name'] + ']' + ', не модератор.')
                            flag += 1

            # Эхо
            if pref in msg and flag < 1:
                sender(id_chat, msg[2::])
                flag += 1

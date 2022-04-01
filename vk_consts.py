# OWN CONSTS
PreProcessing = False
MaxCountAttempts = 5
# test
# vk_token = '1e32288d428e53948526b41f111fbee5db59ad318d66527624ed607448179758b372c99593afa96073a9c'
vk_token = 'adb1ea5cd97ebe8ba8621d50392fbf11c5103d005155ebe87a6965637f392a5b09679b739aecec7c3ba85'
link_recall = 'https://vk.com/away.php?to=https%3A%2F%2Fdocs.google.com%2Fforms%2Fd%2Fe' \
              '%2F1FAIpQLScsmu_Wa8HZvlZiSZzIDnzO9R5l8wGsYy8QCVIoI76_Zjci2w%2Fviewform%3Fusp%3Dsf_link&cc_key= '
link_on_regulations = 'https://vk.com/@-210888298-pravila-pervogo-sezona-01032022-31032022'
admin_id = [370285501, 173354038, 190783881]
admin_domain = "kalik_murbanov"
group_id = -210762192
#
filename_start_data = "data/data.csv"
filename_link_data = "data/link_data.csv"
filename_dynamic_data = "data/dynamic_data.csv"
filename_dynamic_link_data = "data/dynamic_link_data.csv"
filename_sorted_users_data = "data/top_users.csv"
#test
# filename_link_data = "data/test_link_data.csv"
# filename_start_data = "data/test_data.csv"

# USERS CONSTS
launch_bot = ["start", "начать", "старт"]
launch_message = "Старт бота"

Info_bottom = "Инфо обо мне"
Info_target_bottom = "Инфо о жертве"
message_death_user = f'Вы умерли и не можете использовать эту кнопку, но зато можете оставить отзыв)))\n' \
                     f'{link_recall}'

IKill_bottom = "Я Убил"
IKill_message = f'Вашей жертве, было отправлено сообщение о ее смерти.\n' \
                f'Сообщение жертве может прийти не сразу.\n' \
                f'Дождитесь подтверждения от жертвы.\n' \
                f'если вам не придет сообщение напишите админу он решит проблему vk.com/id{admin_id[0]}'

IDie_bottom = "Я Умер"
IDie_message = f'Пожалуйста подтвердите свою смерть,' \
               f' если это вас и вправду убили.\n\n' \
               f'Если вас не убивали, то возможно' \
               f' вас пытаются заскамить как мамонта.\n' \
               f'Тогда один из Великих Dungeon Masters\n' \
               f'напишет киллеру и жертве, чтобы узнать подробности инцидента\n' \
               f'Если это будет повторятся мы:\n' \
               f'Снимем баллы вашему убийце.\n' \
               f'Забаним его, если это будет слишком часто\n\n\n' \
               f'Если вы СЛУЧАЙНО нажмете на кнопку мы ответственности не несем\n'
positive_death_conf_bottom = "Меня и вправду убили"
positive_death_conf_message = f'Спасибо, что поиграли в нашу игру\n' \
                              f'Пожалуйста пройдите по ссылке и' \
                              f' оставте свой отзыв об игре:\n' \
                              f'{link_recall}\n' \
                              f'Мы с командой хотели бы развивать игру и ваш отзыв очень важен для этого\n' \
                              f'Если были проблемы с тех частью бота\n' \
                              f'Обязательно напишите Калику Мурбанову(vk.com/{admin_domain})\n' \
                              f'Удачи в следующий раз и обязательно позовите своего убийцу выпить пиво))'

negative_death_conf_bottom = "Меня пытаются заскамить"
negative_death_conf_message = 'Команда Dungeon Masters свяжется с убийцей и с вами,\n' \
                              'чтобы разобраться с ситуацией\n' \
                              'Если у вас возникли критические проблемы\n' \
                              'Можете незамедлительно написать Dungeon Masters' \
                              ' и мы постараемся разрешить проблему в течении дня\n' \
                              'Если ваш убийца продолжит присылать вам подтверждение о смерти\n' \
                              'Мы снимем у него баллы, в крайнем случае забаним\n' \
                              'Уважайте, себя и других и не нагружайте бота.'

positive_death_message_killer = f'Ваша жертва дала подтверждение о своей смерти.' \
                                f'Теперь у вас есть новая цель!!!' \
                                f'Посмотрите информацию о вашей следующей жертве в \"{Info_target_bottom}\"'

negative_death_message_killer = f'Ваша жертва не дала подтверждение о своей смерти\n' \
                                f'Возможно это баг и вы и вправду убили свою жертву и она согласилась с этим на ' \
                                f'словах\n' \
                                f'Тогда мы постараемся это как можно скорее исправить\n' \
                                f'Если у вас возник спор и вы не можете договорится\n' \
                                f'пишите нашим Dungeon Masters(админам группы),\n' \
                                f'мы покажем кто boss of gim  а кто  fucking slave\n' \
                                f'Если это какой то прекол, то\n' \
                                f'Мы снимем вам балы и в крайнем случае забаним и вы больше не сможете играть' \
                                f'В любом случае вам в течении 1-2 дней напишут админы'
negative_death_message_admin = "НЕГАТИВНЫЙ ОТВЕТ НА ПОДТВЕРЖДЕНИЕ О СМЕРТИ\n" \
                               "Убийца: vk.com/id{} отправил запрос на убийство vk.com/id{}\n" \
                               "Жертва не подтвердила свою смерть\n" \
                               "Написать в течение 1 дня киллеру\n"

label_link_on_regulations_bottom = "Ссылка на правила киллера"

exit_bottom = "Выйти"
exit_message = f'Прощай мой  друг T_T'

start_bottom = "Начнем резню!"
start_message = f'Привет я Киллер бот, сейчас я поясню за кнопочки внизу и за общие правила:\n\n\n' \
                f'\"{IKill_bottom}\" - Нажимаете, когда убили цель, жертва должна подтвердить свою смерть.\n' \
                f'Если вы подумали, что убили человека, но он этого не заметил и не подтвердил свою смерть:\n\n' \
                f'(+) Можете написать\n' \
                f'    Dungeon Masters\n ' \
                f'   (админам группы)\n' \
                f'(+) Подойти к жертве и\n' \
                f'    разобраться самому\n' \
                f'    (Очев вы тогда спалитесь)\n' \
                f'(-) Заспамить Жертву\n' \
                f'    сообщениями о ее смерти\n\n' \
                f'Если будете в неразумных количествах использовать кнопку то сначала мы снимем у вас часть belly\n' \
                f'Если это не помжет я вас забаню))))\n\n' \
                f'Если вас убили(или убийца подумал, что вас убил вас), то ' \
                f'у вас появится сообщение о вашей смерти и поменяются кнопки.\n' \
                f'Но что делать в этой нелегкой ситуации??\n' \
                f'Правильно прочитать описание кнопок!!!\n\n' \
                f'Кнопки когда вам придет сообщение о вашей смерти:\n\n' \
                f'\"{positive_death_conf_bottom}\" - Подтверждаете свою смерть и выбываете из игры\n' \
                f'\"{negative_death_conf_bottom}\" - Вы не соглашаетесь со своей смертью.\n' \
                f'Вы остаетесь в игре пока админ не разберется с ситуацией\n' \
                f'Тобишь если какой-то умник решит убить вас во сне, то вы просто можете не согласится!!!' \
                f'\n\n' \
                f'Конечно вы можете злоупотреблять\n' \
                f'      \"{negative_death_conf_bottom}\"\n' \
                f'И\n' \
                f'      \"{IKill_bottom}\"\n' \
                f'Но помните такие вещи считаются за нарушение правил\n' \
                f'А за наршуения правил:\n' \
                f'      С вас снимут штраф в размере 300 handred backs(-300 belly)\n' \
                f'ИЛИ\n' \
                f'      Я Вас забаю)))\n\n' \
                f'Так же у вас есть Кнопки:\n\n' \
                f'\"{Info_bottom}\" - Узнать свой статус и инфу о себе\n' \
                f'(если, что то не совпало напишите админу о проблеме(vk.com/id{admin_id[0]}))\n\n' \
                f'\"{Info_target_bottom}\" - Узнать доступную информацию о цели\n\n' \
                f'\"{label_link_on_regulations_bottom}\" - Вы хотите повторить правила\n\n' \
                f'\"{exit_bottom}\" - Вы не хотите разговаривать с ботом T_T'

# ADMIN CONSTS

admin_status_bottom = "status"
admin_status_message = "Привет шлюха"

admin_data_work_bottom = "Data Work"
admin_data_work_message = "Start Data Work"

admin_count_live_users_bottom = "Users Live"
admin_top_users_bottom = "Top List Users"

admin_back_bottom = "Back"
admin_back_message = "Back bro just back, i fuck this niggers"

find_victim_bottom = "find victim"
find_victim_message = "Input domain name user, and bot give victim this user"

find_killer_bottom = "find killer"
find_killer_message = "Input domain name user, and bot give killer this user"

ban_bottom = "ban user"
ban_message_admin = "enter link to user, who you want to ban"
ban_message_user = "Привет, у меня для тебя радость!!!!\n" \
              "Теперь вы официально в бане!!!!\n" \
              "Мы с Dungeon Masters решили, что вы\n" \
              "\"tool slave for us boss gym\"" \
              "Есть притензии?\n" \
              "Хочешь узнать за что тебя забанили???\n" \
              "Может хочешь обжаловать бан???\n" \
              "У тебя еще шанс!!!!!\n" \
              "Пиши Великим Dungeon Masters(админы группы) и\n" \
              " может у тебя получится востановить свою честь!!!!"


error_server_message = "!!!ОШИБКА НА СЕРВЕРЕ!!!!\n" \
                       "ОШИБКА: {}\n" \
                       "ВЫДАЮ ИНФОРМАЦИЮ О СОСТОЯНИИ\n"
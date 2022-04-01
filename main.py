import table_work
from vk_func import processing, login
from vk_func import crash_server
from table_work import preprocessing_data
from exctention import BotException
from classes import User

LP, api = login()
print(type(LP))

try:
    LP, api = login()
except BotException as error:
    print(f"SERVER SHUTDOWN WITH ERROR: {error}")
else:
    link_data = preprocessing_data(api)

    users_pool = {}
    for index in link_data.index.values:
        user = User(link_data, index)
        users_pool[user.link] = user

    try:
        processing(vk_longpoll=LP, api=api,
                   link_data=link_data,
                   users_pool=users_pool)

    except BotException:
        print("END SERVER")

    except:
        try:
            LP, api = login()
        except BotException as error:
            print(f"SERVER SHUTDOWN WITH ERROR: {error}")
        crash_server(api)
        raise

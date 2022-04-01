import time

import pandas as pd

from exctention import BotException, EnumBotErrors

import vk_api
from vk_api.longpoll import VkLongPoll
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkEventType

import requests
import classes
from classes import vk_requests


import table_work as tw
from table_work import convert_user_link_to_dominian, find_user_id

import vk_consts as vc
from vk_consts import vk_token, launch_bot, start_bottom, IKill_bottom, exit_bottom, \
    label_link_on_regulations_bottom


def login():
    """
    Login bot

    :return LP: for listen users.
    :rtype LP: vk_api.longpoll.VkLongPoll

    :return api: contain method of work with vk
    :rtype api: vk_api.vk_api.VkApiMethod

    """
    print("\n\nSERVER CONNECT TO VK\n")
    attempt = 1
    LP, api = None, None
    while attempt < vc.MaxCountAttempts:
        print(f'{attempt} attempt / {vc.MaxCountAttempts} Max')

        try:
            vk_session = vk_api.VkApi(token=vk_token)

            LP = VkLongPoll(vk_session)
            api = vk_session.get_api()
            break

        except vk_api.exceptions.VkApiError as error:
            print("SERVER CANNOT CONNECT TO VK")
            print(f'ERROR: {error}\n')
            attempt += 1
            time.sleep(5)

    if attempt == vc.MaxCountAttempts:
        print("SERVER COULD NOT CONNECT TO VK")
        print("Maximum attempts were used\n\n")
        raise BotException(EnumBotErrors.ERROR_CONNECT_SERVER_MAX_TRY)
    else:
        print("SERVER WAS SUCCESSFULLY CONNECTED TO VK\n\n")
        return LP, api


def processing(vk_longpoll: vk_api.longpoll.VkLongPoll,
               api: vk_api.vk_api.VkApiMethod,
               link_data: pd.DataFrame,
               users_pool: dict) -> None:
    """

    processing bot.
    Function contain Listen users and handling errors.

    :param vk_longpoll: for listen users.
    :type vk_longpoll: vk_api.longpoll.VkLongPoll

    :param api: contain method of work with vk
    :type api: vk_api.vk_api.VkApiMethod

    :param link_data: link users data
    :type link_data: pd.DataFrame

    :param users_pool: dict with users id : user_inform
    :type users_pool: dict

    :return: None

    """

    print("START LISTEN VK SERVER\n")
    loop = True
    users_requests = {}
    while loop:
        try:
            ListenUsers(vk_longpoll, api,
                        link_data, users_pool,
                        users_requests)

        except requests.exceptions.RequestException as error:
            message = "ERROR SERVER:\n" \
                      f"ERROR: {error}" \
                      "ERROR DESCRIPTION: CONNECT SERVER TO VK\n" \
                      "RECONNECTION SERVER AGAIN\n"

            print(message)
            vk_longpoll, api = login()
            error_on_server(api, message)
            print("RECONNECTION SERVER SUCCESS\n\n")

            continue

        except KeyError as error:
            message = "ERROR SERVER:\n" \
                      f"ERROR: {error}" \
                      "ERROR DESCRIPTION: INDEX ERROR IN DATA\n" \
                      "NEED MANUAL INTERATION\n"

            print(message)
            error_on_server(api, message)
            print("MESSAGE SEND ADMIN\n"
                  "CONTINUATION OF SERVER WORK\n\n")

            continue

        except KeyboardInterrupt:
            message = "SERVER SHUTDOWN"

            print(message)
            error_on_server(api, message)
            raise BotException(EnumBotErrors.SERVER_SHUTDOWN)

        except Exception as error:
            message = "ERROR SERVER:\n" \
                      f"ERROR: {error}" \
                      "ERROR DESCRIPTION: DONT KNOW\n" \
                      "NEED MANUAL INTERATION\n"

            print(message)
            error_on_server(api, message)
            print("MESSAGE SEND ADMIN\n"
                  "CONTINUATION OF SERVER WORK\n\n")

            continue


def ListenUsers(vk_longpoll: vk_api.longpoll.VkLongPoll,
                api: vk_api.vk_api.VkApiMethod,
                link_data: pd.DataFrame,
                users_pool: dict,
                users_requests: dict) -> None:
    """

    Listening users.

    :param vk_longpoll: for listen users.
    :type vk_longpoll: vk_api.longpoll.VkLongPoll

    :param api: contain method of work with vk
    :type api: vk_api.vk_api.VkApiMethod

    :param link_data: link users data
    :type link_data: pd.DataFrame

    :param users_pool: dict with users id : user_inform
    :type users_pool: dict

    :param users_requests: dict vk requests
    :type users_requests: dict

    :return: None
    """

    for event in vk_longpoll.listen():

        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            print_event_status(event)

            # Requests
            event_requests(event, users_pool, users_requests, link_data, api)

            # ADMIN
            admin_event(event, users_requests, link_data, api)

            # USERS
            user_event(event, users_pool, users_requests, api)


def event_requests(event: vk_api.longpoll.Event,
                   users_pool: dict,
                   users_requests: dict,
                   link_data: pd.DataFrame,
                   api: vk_api.vk_api.VkApiMethod) -> None:
    """

    Handling requests from users

    :param event: event like: user write, user send message and more else
    :type event: vk_api.longpoll.Event

    :param users_pool: dict with users id : user_inform
    :type users_pool: dict

    :param users_requests: dict vk requests
    :type users_requests: dict

    :param link_data: link users data
    :type link_data: pd.DataFrame

    :param api: contain method of work with vk
    :type api: vk_api.vk_api.VkApiMethod

    :return: None
    """

    if str(event.peer_id) in users_requests.keys():
        request = users_requests[str(event.peer_id)]

        if request == vk_requests.ADMIN_GET_NAME_VICTIM.value:
            admin_get_name_victim(event, users_pool, api)

        if request == vk_requests.ADMIN_GET_NAME_KILLER.value:
            admin_get_name_killer(event, users_pool, api)

        if request == vk_requests.BAN_USER.value:
            admin_ban_user(event, users_pool, api, link_data)

        if request == vk_requests.DEATH_CONFIRMATION.value:
            death_confirmation(event, users_pool, link_data, api)

        users_requests.pop(str(event.peer_id))


def admin_event(event: vk_api.longpoll.Event,
                users_requests: dict,
                link_data: pd.DataFrame,
                api: vk_api.vk_api.VkApiMethod) -> None:
    """
    event for admin


    :param event: event like: user write, user send message and more else
    :type event: vk_api.longpoll.Event

    :param users_requests: dict vk requests
    :type users_requests: dict

    :param link_data: link users data
    :type link_data: pd.DataFrame

    :param api: contain method of work with vk
    :type api: vk_api.vk_api.VkApiMethod

    :return: None
    """

    if int(event.peer_id) in vc.admin_id:
        if event.text.lower() in vc.admin_status_bottom:
            keyboard = set_admin_keyboard()
            send_message(access_token=vk_token, api=api,
                         peer_id=event.peer_id, message_txt=vc.admin_status_message,
                         keyboard=keyboard.get_keyboard())

        admin_users_work(event, api, users_requests)

        admin_data_work(event, link_data, api)


def user_event(event: vk_api.longpoll.Event,
               users_pool: dict,
               users_requests: dict,
               api: vk_api.vk_api.VkApiMethod) -> None:

    """
    event for users

    :param event: event like: user write, user send message and more else
    :type event: vk_api.longpoll.Event

    :param users_pool: dict with users id : user_inform
    :type users_pool: dict

    :param users_requests: dict vk requests
    :type users_requests: dict

    :param api: contain method of work with vk
    :type api: vk_api.vk_api.VkApiMethod

    :return: None
    """

    if (event.peer_id in users_pool.keys()) or (int(event.peer_id) in vc.admin_id):
        if event.text.lower() in launch_bot:
            from vk_consts import launch_message
            keyboard = set_start_keyboard()
            send_message(access_token=vk_token, api=api,
                         peer_id=event.peer_id, message_txt=launch_message,
                         keyboard=keyboard.get_keyboard())

        if event.text in start_bottom:
            from vk_consts import start_message
            keyboard = set_keyboard()
            send_message(access_token=vk_token, api=api,
                         peer_id=event.peer_id, message_txt=start_message,
                         keyboard=keyboard.get_keyboard())

        # Переделать с юзерами
        if event.text in vc.Info_bottom:
            keyboard = set_keyboard()
            user = users_pool[event.peer_id]
            send_message(access_token=vk_token, api=api,
                         peer_id=event.peer_id, message_txt=user.user_info(),
                         keyboard=keyboard.get_keyboard())

        if event.text in vc.Info_target_bottom:
            keyboard = set_keyboard()
            user = users_pool[event.peer_id]
            if user.status:
                victim = users_pool[user.victim]
                send_message(access_token=vk_token, api=api,
                             peer_id=event.peer_id,
                             message_txt=victim.user_info_for_another_users(level_access=user.level_access),
                             keyboard=keyboard.get_keyboard())
            else:
                send_message(access_token=vk_token, api=api,
                             peer_id=event.peer_id,
                             message_txt=vc.message_death_user,
                             keyboard=keyboard.get_keyboard())

        if event.text in IKill_bottom:
            user = users_pool[event.peer_id]
            if user.status:
                kill(event, users_pool, users_requests, api)
            else:
                keyboard = set_keyboard()
                send_message(access_token=vk_token, api=api,
                             peer_id=event.peer_id, message_txt=vc.message_death_user,
                             keyboard=keyboard.get_keyboard())
            # тут список ебнуть чтобы была связь между 2 людьми и подтверждение

        if event.text in exit_bottom:
            from vk_consts import exit_message
            send_message(access_token=vk_token, api=api,
                         peer_id=event.peer_id, message_txt=exit_message)


def admin_users_work(event: vk_api.longpoll.Event,
                     api: vk_api.vk_api.VkApiMethod,
                     users_requests: dict) -> None:
    """
    work with user: find killer, victim, ban certain user

    :param event: event like: user write, user send message and more else
    :type event: vk_api.longpoll.Event

    :param api: contain method of work with vk
    :type api: vk_api.vk_api.VkApiMethod

    :param users_requests: dict vk requests
    :type users_requests: dict

    :return: None
    """

    if event.text in vc.find_killer_bottom:
        users_requests[str(event.peer_id)] = vk_requests.ADMIN_GET_NAME_KILLER.value
        send_message(access_token=vk_token, api=api,
                     peer_id=event.peer_id, message_txt=vc.find_killer_message)

    if event.text in vc.find_victim_bottom:
        users_requests[str(event.peer_id)] = vk_requests.ADMIN_GET_NAME_VICTIM.value
        send_message(access_token=vk_token, api=api,
                     peer_id=event.peer_id, message_txt=vc.find_victim_message)

    if event.text in vc.ban_bottom:
        users_requests[str(event.peer_id)] = vk_requests.BAN_USER.value
        send_message(access_token=vk_token, api=api,
                     peer_id=event.peer_id, message_txt=vc.ban_message_admin)


def admin_data_work(event: vk_api.longpoll.Event,
                    link_data: pd.DataFrame,
                    api: vk_api.vk_api.VkApiMethod) -> None:

    """

    allow admin work with data: find alive users or find top10 user in game

    :param event: event like: user write, user send message and more else
    :type event: vk_api.longpoll.Event

    :param link_data: link users data
    :type link_data: pd.DataFrame

    :param api: contain method of work with vk
    :type api: vk_api.vk_api.VkApiMethod

    :return: None
    """

    if event.text in vc.admin_data_work_bottom:
        keyboard = set_admin_data_work_keyboard()
        send_message(access_token=vk_token, api=api,
                     peer_id=event.peer_id, message_txt=vc.admin_data_work_message,
                     keyboard=keyboard.get_keyboard())

    if event.text in vc.admin_count_live_users_bottom:
        keyboard = set_admin_data_work_keyboard()
        message = tw.pool_alive_users(link_data)
        send_message(access_token=vk_token, api=api,
                     peer_id=event.peer_id, message_txt=message,
                     keyboard=keyboard.get_keyboard())

    if event.text in vc.admin_top_users_bottom:
        keyboard = set_admin_data_work_keyboard()
        message = tw.top_belly_users(link_data)
        send_message(access_token=vk_token, api=api,
                     peer_id=event.peer_id, message_txt=message,
                     keyboard=keyboard.get_keyboard())

    if event.text in vc.admin_back_bottom:
        keyboard = set_admin_keyboard()
        send_message(access_token=vk_token, api=api,
                     peer_id=event.peer_id, message_txt=vc.admin_back_message,
                     keyboard=keyboard.get_keyboard())


def death_confirmation(event: vk_api.longpoll.Event,
                       users_pool: dict,
                       link_data: pd.DataFrame,
                       api: vk_api.vk_api.VkApiMethod) -> None:
    """

    :param event: event like: user write, user send message and more else
    :type event: vk_api.longpoll.Event

    :param users_pool: dict with users id : user_inform
    :type users_pool: dict

    :param link_data: link users data
    :type link_data: pd.DataFrame

    :param api: contain method of work with vk
    :type api: vk_api.vk_api.VkApiMethod

    :return:
    """
    keyboard = set_keyboard()
    if event.text in vc.negative_death_conf_bottom:
        victim = users_pool[event.peer_id]
        killer = users_pool[victim.killer]

        send_message(access_token=vk_token, api=api,
                     peer_id=killer.link, message_txt=vc.negative_death_message_killer,
                     keyboard=keyboard.get_keyboard())
        send_message(access_token=vk_token, api=api,
                     peer_id=event.peer_id, message_txt=vc.negative_death_conf_message,
                     keyboard=keyboard.get_keyboard())
        send_message(access_token=vk_token, api=api,
                     peer_id=vc.admin_id[0],
                     message_txt=vc.negative_death_message_admin.format(killer.link, victim.link))

    if event.text in vc.positive_death_conf_bottom:
        user = users_pool[event.peer_id]
        killer = users_pool[user.killer]
        new_victim = users_pool[user.victim]
        print(user.link, user.index_in_data)
        print(killer.link, killer.index_in_data)
        print(new_victim.link, new_victim.index_in_data)
        murder(killer, user, new_victim, link_data)

        send_message(access_token=vk_token, api=api,
                     peer_id=killer.link, message_txt=vc.positive_death_message_killer,
                     keyboard=keyboard.get_keyboard())
        send_message(access_token=vk_token, api=api,
                     peer_id=user.link, message_txt=vc.positive_death_conf_message,
                     keyboard=keyboard.get_keyboard())


def murder(killer: classes.User,
           victim: classes.User,
           new_victim: classes.User,
           dynamic_link_data: pd.DataFrame) -> None:
    """

    'killer' kill 'victim'.
    new victim 'killer' is 'new_vicitm'
    record these in 'dynamic_link_data'

    :param killer: info about killer
    :type killer: classes.User

    :param victim: info about victim
    :type victim: classes.User

    :param new_victim: indo about new victim
    :type new_victim: classes.User

    :param dynamic_link_data: dynamic link users data
    :type dynamic_link_data: pd.DataFrame
    :return: None
    """

    tw.data_change_status_user(dynamic_link_data, victim)
    tw.data_change_victim_user(dynamic_link_data, killer)
    tw.data_change_killer_user(dynamic_link_data, new_victim)

    victim.user_was_killed()
    killer.user_killed_victim(victim)
    new_victim.user_change_killer(killer)


def kill(event: vk_api.longpoll.Event,
         users_pool: dict, users_requests: dict,
         api: vk_api.vk_api.VkApiMethod) -> None:
    """

    crate kill requests( need victim confirm for kill)

    :param event: event like: user write, user send message and more else
    :type event: vk_api.longpoll.Event

    :param users_pool: dict with users id : user_inform
    :type users_pool: dict

    :param users_requests: dict vk requests
    :type users_requests: dict

    :param api: contain method of work with vk
    :type api: vk_api.vk_api.VkApiMethod

    :return: None
    """

    from vk_consts import IKill_message, IDie_message

    killer_keyboard = set_keyboard()
    victim_keyboard = set_victim_keyboard()

    killer = users_pool[event.peer_id]
    victim = users_pool[killer.victim]

    users_requests[str(victim.link)] = vk_requests.DEATH_CONFIRMATION.value

    send_message(access_token=vk_token, api=api,
                 peer_id=event.peer_id, message_txt=IKill_message,
                 keyboard=killer_keyboard.get_keyboard())
    send_message(access_token=vk_token, api=api,
                 peer_id=victim.link, message_txt=IDie_message,
                 keyboard=victim_keyboard.get_keyboard())


def admin_ban_user(event: vk_api.longpoll.Event,
                   users_pool: dict,
                   api: vk_api.vk_api.VkApiMethod,
                   link_data: pd.DataFrame) -> None:
    """

    Ban user (this function make certain ban requests, not create)

    :param event: event like: user write, user send message and more else
    :type event: vk_api.longpoll.Event

    :param users_pool: dict with users id : user_inform
    :type users_pool: dict

    :param api: contain method of work with vk
    :type api: vk_api.vk_api.VkApiMethod

    :param link_data: link users data
    :type link_data: pd.DataFrame

    :return: None
    """

    admin_keyboard = set_admin_keyboard()
    user_keyboard = set_keyboard()
    link = event.text

    try:
        link = convert_user_link_to_dominian(link)
    except BotException as e:
        print(e)
        print(f'new weird link {link}')

    user_id = find_user_id(link, api)

    if user_id in users_pool.keys():
        user = users_pool[user_id]
        killer = users_pool[user.killer]
        new_victim = users_pool[user.victim]
        murder(killer, user, new_victim, link_data)

        send_message(access_token=vk_token, api=api,
                     peer_id=user_id, message_txt=vc.ban_message_user,
                     keyboard=user_keyboard.get_keyboard())
        send_message(access_token=vk_token, api=api,
                     peer_id=event.peer_id, message_txt="user success baned",
                     keyboard=admin_keyboard.get_keyboard())
    else:
        send_message(access_token=vk_token, api=api,
                     peer_id=event.peer_id, message_txt="user didn't baned\n"
                                                        "Try again",
                     keyboard=admin_keyboard.get_keyboard())


def admin_get_name_victim(event: vk_api.longpoll.Event,
                          users_pool: dict,
                          api: vk_api.vk_api.VkApiMethod) -> None:
    """

    admin get info about victim certain user.

    :param event: event like: user write, user send message and more else
    :type event: vk_api.longpoll.Event

    :param users_pool: dict with users id : user_inform
    :type users_pool: dict

    :param api: contain method of work with vk
    :type api: vk_api.vk_api.VkApiMethod

    :return: None
    """

    keyboard = set_admin_keyboard()
    link = event.text

    try:
        link = convert_user_link_to_dominian(link)
    except BotException as e:
        print(e)
        print(f'new weird link {link}')

    user_id = find_user_id(link, api)

    if user_id in users_pool.keys():
        user = users_pool[users_pool[user_id].victim]
        send_message(access_token=vk_token, api=api,
                     peer_id=event.peer_id, message_txt=user.admin_info_text_about_user(),
                     keyboard=keyboard.get_keyboard())
    else:
        send_message(access_token=vk_token, api=api,
                     peer_id=event.peer_id, message_txt=f'dont find user with domain link: vk.com/{link}\n'
                                                        f'or id: vk.com/id{user_id}\n'
                                                        f'please try again',
                     keyboard=keyboard.get_keyboard())


def admin_get_name_killer(event: vk_api.longpoll.Event,
                          users_pool: dict,
                          api: vk_api.vk_api.VkApiMethod) -> None:
    """

    admin get info about killer certain user.

    :param event: event like: user write, user send message and more else
    :type event: vk_api.longpoll.Event

    :param users_pool: dict with users id : user_inform
    :type users_pool: dict

    :param api: contain method of work with vk
    :type api: vk_api.vk_api.VkApiMethod

    :return: None
    """

    keyboard = set_admin_keyboard()
    link = event.text
    try:
        link = convert_user_link_to_dominian(link)
    except BotException as e:
        print(e)
        print(f'new weird link {link}')

    user_id = find_user_id(link, api)

    if user_id in users_pool.keys():
        user = users_pool[users_pool[user_id].killer]
        send_message(access_token=vk_token, api=api,
                     peer_id=event.peer_id, message_txt=user.admin_info_text_about_user(),
                     keyboard=keyboard.get_keyboard())
    else:
        send_message(access_token=vk_token, api=api,
                     peer_id=event.peer_id, message_txt=f'dont find user with domain link: {link}\n'
                                                        f'or  id: vk.com/id{user_id}\n'
                                                        f'please try again',
                     keyboard=keyboard.get_keyboard())


def set_victim_keyboard() -> vk_api.keyboard.VkKeyboard:
    """
    set keyboard when receive death conformation

    :return: vk_api.keyboard.VkKeyboard
    """

    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(label=vc.positive_death_conf_bottom, color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button(label=vc.negative_death_conf_bottom, color=VkKeyboardColor.NEGATIVE)
    return keyboard


def set_start_keyboard() -> vk_api.keyboard.VkKeyboard:
    """
    set start bot keyboard

    :return: vk_api.keyboard.VkKeyboard
    """

    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(label=start_bottom, color=VkKeyboardColor.POSITIVE)
    return keyboard


def set_keyboard() -> vk_api.keyboard.VkKeyboard:
    """
    set standard user keyboard

    :return:vk_api.keyboard.VkKeyboard
    """

    from vk_consts import link_on_regulations
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(IKill_bottom, color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button(vc.Info_bottom, color=VkKeyboardColor.SECONDARY)
    keyboard.add_button(vc.Info_target_bottom, color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_openlink_button(label=label_link_on_regulations_bottom, link=link_on_regulations)
    keyboard.add_line()
    keyboard.add_button(exit_bottom, color=VkKeyboardColor.PRIMARY)
    return keyboard


def set_admin_data_work_keyboard() -> vk_api.keyboard.VkKeyboard:
    """
    set admin data work keyboard

    :return: vk_api.keyboard.VkKeyboard
    """

    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(vc.admin_count_live_users_bottom, color=VkKeyboardColor.NEGATIVE)
    keyboard.add_button(vc.admin_top_users_bottom, color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button(vc.admin_back_bottom, color=VkKeyboardColor.SECONDARY)
    return keyboard


def set_admin_keyboard() -> vk_api.keyboard.VkKeyboard:
    """
    set standard admin keyboard

    :return: vk_api.keyboard.VkKeyboard
    """

    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(vc.find_victim_bottom, color=VkKeyboardColor.NEGATIVE)
    keyboard.add_button(vc.find_killer_bottom, color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button(vc.ban_bottom, color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button(vc.admin_data_work_bottom, color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button(exit_bottom, color=VkKeyboardColor.PRIMARY)
    return keyboard


def time_in_ms() -> int:
    """
    currently time

    :return: currently time
    """

    ms = int(round(time.time() * 1000))
    return ms


def send_message(access_token: str,
                 api: vk_api.vk_api.VkApiMethod,
                 peer_id: str or int,
                 message_txt: str,
                 keyboard: vk_api.keyboard.VkKeyboard = None) -> None:
    """

    send user message

    :param access_token: special token for access send message and another thing
    :type access_token: str

    :param api: contain method of work with vk
    :type api: vk_api.vk_api.VkApiMethod

    :param peer_id:
    :type peer_id: str or int

    :param message_txt: message text
    :type message_txt: str

    :param keyboard: keyboard bot, which showed user
    :type keyboard: vk_api.keyboard.VkKeyboard

    :return: None
    """

    # try:
    rand_id = time_in_ms()
    api.messages.send(access_token=access_token,
                      random_id=rand_id,
                      peer_id=str(peer_id),
                      message=message_txt,
                      keyboard=keyboard,
                      v="5.131"
                      )


# except x:
#     rand_id = time_in_ms()
#     api.messages.send(access_token=access_token,
#                       random_id=rand_id,
#                       peer_id=str(vc.admin_id),
#                       message=message_txt,
#                       keyboard=keyboard,
#                       v="5.131"
#                       )


def print_event_status(event: vk_api.longpoll.Event) -> None:
    """
    status event for debug

    :param event: event like: user write, user send message and more else
    :type event: vk_api.longpoll.Event

    :return: None
    """

    print()
    print(f'time output mes:{event.timestamp}')
    print()
    print(f'from_user:      {event.from_user}')
    print(f'from_chat:      {event.from_chat}')
    print(f'from_group:     {event.from_group}')
    print(f'peer_id:        {event.peer_id}')
    print(f'user_id:        {event.user_id}')
    print(f'to_me:          {event.to_me}')
    print(f'from_me:        {event.from_me}')
    print(f'attachments:    {event.attachments}')
    if hasattr(event, 'text'):
        print(f'text message:   {event.text}')
    print()


def error_on_server(api: vk_api.vk_api.VkApiMethod,
                    error: str) -> None:
    """
    send all admins message about error in server

    :param api: contain method of work with vk
    :type api: vk_api.vk_api.VkApiMethod

    :param error: error message
    :type error: str

    :return: None
    """

    for admin in vc.admin_id:
        send_message(access_token=vk_token, api=api,
                     peer_id=str(admin),
                     message_txt=error)

    time.sleep(5)


def crash_server(api: vk_api.vk_api.VkApiMethod) -> None:
    """
    send all admin message about crush server
    :param api: contain method of work with vk
    :type api: vk_api.vk_api.VkApiMethod

    :return: None
    """

    message = "!!!ПАДЕНИЕ СЕРВЕРА!!!"
    for admin in vc.admin_id:
        send_message(access_token=vk_token, api=api,
                     peer_id=str(admin),
                     message_txt=message)

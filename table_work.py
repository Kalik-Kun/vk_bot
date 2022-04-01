from time import time
import pandas as pd
import numpy as np
import vk_api
import classes
from vk_consts import filename_start_data, filename_link_data
from vk_consts import filename_dynamic_data, filename_dynamic_link_data
from vk_consts import filename_sorted_users_data
from vk_consts import PreProcessing
from exctention import BotException, EnumBotErrors


# todo do class data

def convert_user_link_to_dominian(string: str) -> str:
    """
    Convert link on user to him domain name
    Example:
    https:/vk.com/id343232 -> id343232

    :param string: link on user
    :type string: str

    :return: return domain or id name
    :rtype: str
    """
    ind = string.rfind('/')
    if ind == -1:
        ind = string.rfind('@')
        if ind == -1:
            raise BotException(EnumBotErrors.DONT_FIND_SYMB)

    return string[ind + 1:]


def create_link_killer_list(data: pd.DataFrame) -> pd.DataFrame:

    """
    input data comes from the file: filename_start_data(watch in vk_consts.py)

    Function make new DataFrame table: link_data.
    link_data have columns

    Contain in old(input) data:
    1.  'last name': last name user.
    2.  'first name': first name user.
    3.  'patronymic': patronymic user.
    4.  'group': number group in MIPT University.
    5.  'course': number course in MIPT University.
    6.  'room': room of user in dormitory MIPT university.
    7.  'link': link on user in vk.
    8.  'size': size clothes user.
    9.  'frequency': frequency of appearance in the dormitory.
    10. 'mail': user mail.

    New data was created in function.
    11. 'link killer': link on user, who wants kill certain user*.
    12. 'link victim': link on user. That user is target to kill for certain user*.
    13. 'index killer': index on user in link_data(new output data), who wants kill certain user*.
    14. 'index victim': index on user in link_data(new output data). That user is target to kill for certain user*.
    15. 'belly': belly certain user*.(Points)
    16. 'kills': hom many kills were made by certain user*.
    17. 'kill_list': links on users were killed by certain user*.
    18. 'level access': level access certain user*.
    19. 'live flag': dead or alive user (in code of program may use another terminus: die, live)

    Link data record.
    Record in: filename_link_data(watch in vk_consts.py)

    the list of killers is done by shuffling users and shifting links and indexes by 1.
    (Need new algorithm)

    :param data: input table with users info
    :type data: dp.DataFrame

    :return: linked user list
    :rtype: pd.DataFrame
    """

    sample_data = data.sample(frac=1)
    link_data = sample_data.loc[:, 'last name': 'mail'].copy()

    link_victim = pd.Series(np.append(sample_data['link'].values[1:], sample_data['link'].values[0]),
                            index=sample_data.index)

    index_victim = pd.Series([i % sample_data.index.size for i in range(1, sample_data.index.size + 1)],
                             index=sample_data.index)

    link_killer = pd.Series(np.append(sample_data['link'].values[-1], sample_data['link'].values[:-1]),
                            index=sample_data.index)
    index_killer = pd.Series(np.append([sample_data.index.size - 1], [i for i in range(0, sample_data.index.size - 1)]),
                             index=sample_data.index)

    live_flag = pd.Series([1 for _ in range(len(data.index.values))], index=sample_data.index)
    belly_count_self = pd.Series(pd.Series([1000.0 for _ in range(len(data.index.values))], index=sample_data.index))
    kills = pd.Series([0 for _ in range(len(data.index.values))], index=sample_data.index)
    kills_list = pd.Series([" " for _ in range(len(data.index.values))], index=sample_data.index, dtype=str)
    level_access = pd.Series([0 for _ in range(len(data.index.values))], index=sample_data.index)

    link_data['link killer'] = link_killer
    link_data['link victim'] = link_victim
    link_data['index killer'] = index_killer
    link_data['index victim'] = index_victim
    link_data['belly'] = belly_count_self
    link_data['kills'] = kills
    link_data['kill_list'] = kills_list
    link_data['level access'] = level_access
    link_data['live flag'] = live_flag

    link_data = link_data.reset_index(drop=True)
    print("Colums data:")
    print(link_data.columns)

    link_data.to_csv(filename_link_data)

    return link_data


def preprocessing_data(api: vk_api.vk_api.VkApiMethod) -> pd.DataFrame:
    """
    if consts PreProcessing (watch in vk_consts.py) True:

    Preprocessing data:
    convert links on user to domain name user(convert_users_links_in_data),
    create link data(create_link_killer_list),

    if consts PreProcessing (watch in vk_consts.py) False:
    Use Dinamic link data, without preprocessing

    :param api: contain method of work with vk
    :type api: 'vk_api.vk_api.VkApiMethod'

    :return: new linked data
    :rtype: pd.DataFrame
    """

    if PreProcessing:
        print("Start Preprocessing Data")

        data = pd.read_csv(filename_start_data)
        print("Convert domain links to id links")
        start_data = convert_users_links_in_data(data, api)
        print("Convert Done")

        print("Start write data in file: {}".format(filename_dynamic_link_data))
        link_data = create_link_killer_list(start_data)
        link_data.to_csv(filename_dynamic_link_data)
        print("End write data in file: {}".format(filename_dynamic_link_data))

        print("PreProcessing Data End")

    else:
        print("Read dynamic link data")
        link_data = pd.read_csv(filename_dynamic_link_data)

        if 'Unnamed: 0' in link_data.columns:
            link_data = link_data.drop('Unnamed: 0', axis=1)

        print("Colums data:")
        print(link_data.columns)
        print("Read done")
    return link_data


def find_user_id(link: str, api: vk_api.vk_api.VkApiMethod) -> str:
    """
    Give id user.

    :param link: link on user
    :type link: str

    :param api: contain method of work with vk
    :type api: vk_api.vk_api.VkApiMethod

    :return: id user(without id, Example id343234 -> 343234)
    :rtype: str
    """

    from vk_consts import vk_token
    print(link)
    vk_user_data = api.users.get(access_token=vk_token, user_ids=link)
    print(vk_user_data)
    user_id = vk_user_data[0]['id']
    return user_id


def convert_users_links_in_data(data: pd.DataFrame, api: vk_api.vk_api.VkApiMethod) -> pd.DataFrame:
    """
    Convert link on user to him domain name in data.
    Function use convert_user_link_to_dominian.
    Example:
    https:/vk.com/id343232 -> id343232

    :param data: input data with bad link on user
    :type data: pd.DataFrame

    :param api: contain method of work with vk
    :type api: 'vk_api.vk_api.VkApiMethod'

    :return: data with converted links
    :rtype: pd.DataFrame
    """

    for str_ind in data['link'].index:
        data['link'].values[str_ind] = convert_user_link_to_dominian(data['link'].values[str_ind])
        data['link'].values[str_ind] = find_user_id(data['link'].values[str_ind], api)
    return data


def update_dynamic_data(data: pd.DataFrame) -> None:
    """
    Record data

    :param data: input data
    :type data: pd.DataFrame

    :return: None
    """
    print("\n\nSTART Update dynamic link data: {}\n".format(filename_dynamic_link_data))
    data.to_csv(filename_dynamic_link_data)
    print("END Update dynamic link data: {}\n\n\n".format(filename_dynamic_link_data))


# Event - some user killed the killer of the current user, the function changes the user's killer
def data_change_killer_user(data: pd.DataFrame, user: classes.User) -> None:
    """

    Event - some user killed the killer of the current user,
    the function changes the user's killer.

    :param data: input link data with all users
    :type data: pd.DataFrame

    :param user: information about certain user
    :type user: classes.User

    :return: None
    """

    print("\n\n\n"
          "CHANGE DYNAMIC DATA, EVENT - user change killer\n\n"
          "user:\n"
          "user.link: {}, user.index_in_data: {}"
          "\n\n".format(data.loc[data.index == user.index_in_data, 'link'].values,
                        user.index_in_data))
    print("Old killer was killed\n\n"
          "old killer:\n"
          "old killer.link: {},\n"
          "old killer.index_in_data:{}"
          "\n\n".format(data.loc[data.index == user.index_in_data, 'link killer'].values,
                        data.loc[data.index == user.index_in_data, 'index killer'].values))

    data['link killer'].values[user.index_in_data] = \
        data['link killer'].values[user.killer_ind]
    data['index killer'].values[user.index_in_data] = \
        data['index killer'].values[user.killer_ind]

    print("New killer, who kill old killer\n\n"
          "new killer:\n"
          "new killer.link: {}, new killer.index_in_data:{}"
          "\n\n".format(data.loc[data.index == user.index_in_data, 'link killer'].values,
                        data.loc[data.index == user.index_in_data, 'index killer'].values))

    update_dynamic_data(data)

    print("CHANGE DYNAMIC DATA DONE\n\n\n")


def data_change_victim_user(data: pd.DataFrame, user: classes.User) -> None:
    """

    Event - The user killed his victim.
    the function give user new victim,
    update kills, belly , kill_list user

    :param data: input link data with all users
    :type data: pd.DataFrame

    :param user: information about certain user
    :type user: classes.User

    :return: None
    """

    print("\n\n\n"
          "CHANGE DYNAMIC DATA, EVENT - user kill victim, change victim\n\n"
          "user:\n"
          "user.link: {}, user.index_in_data: {},\n"
          "user.belly: {},\n"
          "user.kill_count: {}\n"
          "user.kill_list: {}"
          "\n\n".format(data.loc[data.index == user.index_in_data, 'link'].values,
                        user.index_in_data,
                        data.loc[data.index == user.index_in_data, 'belly'].values,
                        data.loc[data.index == user.index_in_data, 'kills'].values,
                        data.loc[data.index == user.index_in_data, 'kill_list'].values))
    print("old victim was killed\n\n"
          "old victim:\n"
          "old victim.link: {}, old victim.index_in_data:{}"
          "\n\n".format(data.loc[data.index == user.index_in_data, 'link victim'].values,
                        data.loc[data.index == user.index_in_data, 'index victim'].values))

    data['belly'].values[user.index_in_data] += \
        100 + 0.2 * data['belly'].values[user.victim_ind]
    data['kills'].values[user.index_in_data] += 1
    data['kill_list'].values[user.index_in_data] += \
        f' vk.com/id{data["link victim"].values[user.index_in_data]} |'

    data['link victim'].values[user.index_in_data] = \
        data['link victim'].values[user.victim_ind]

    data['index victim'].values[user.index_in_data] = \
        data['index victim'].values[user.victim_ind]

    print("user:\n"
          "user.link: {}, user.index_in_data: {},\n"
          "user.belly: {},\n"
          "user.kill_count: {}\n"
          "user.kill_list: {}"
          "\n\n".format(data.loc[data.index == user.index_in_data, 'link'].values,
                        user.index_in_data,
                        data.loc[data.index == user.index_in_data, 'belly'].values,
                        data.loc[data.index == user.index_in_data, 'kills'].values,
                        data.loc[data.index == user.index_in_data, 'kill_list'].values))
    print("new victim:\n"
          "new victim.link: {}, new victim.index_in_data: {}"
          "\n\n".format(data.loc[data.index == user.index_in_data, 'link victim'].values,
                        data.loc[data.index == user.index_in_data, 'index victim'].values))

    update_dynamic_data(data)

    print("CHANGE DYNAMIC DATA DONE\n\n\n")


def data_change_status_user(data: pd.DataFrame, user: classes.User) -> None:
    """
    Event - user was killed.
    Change live flag.

    :param data: input link data with all users
    :type data: pd.DataFrame

    :param user: information about certain user
    :type user: classes.User

    :return: None
    """

    print("\n\n\n"
          "CHANGE DYNAMIC DATA, EVENT - user was killed\n\n"
          "user:\n"
          "user.link: {}, user.index_in_data: {},\n"
          "user.status: {}"
          "\n\n".format(data.loc[data.index == user.index_in_data, 'link'].values,
                        user.index_in_data,
                        data.loc[data.index == user.index_in_data, 'live flag'].values))

    data['live flag'].values[user.index_in_data] = 0

    print("user:\n"
          "user.link: {}, user.index_in_data: {},\n"
          "user.status: {}"
          "\n\n".format(data.loc[data.index == user.index_in_data, 'link'].values,
                        user.index_in_data,
                        data.loc[data.index == user.index_in_data, 'live flag'].values))

    update_dynamic_data(data)

    print("CHANGE DYNAMIC DATA DONE\n\n\n")


def count_alive_users(link_data: pd.DataFrame) -> int:
    """

    Calculate count of alive users.

    :param link_data: input link data.
    :type link_data: pd.DataFrame.

    :return: count of alive users
    :rtype: int
    """
    return link_data[link_data['live flag'] == 1]['live flag'].sum()


def pool_alive_users(link_data: pd.DataFrame) -> str:
    """

    Output str list with pool alive users.

    :param link_data: input link data
    :type link_data: pd.DataFrame

    :return: list with alive users
    :rtype: str
    """

    message = str()
    message += "Users ALive: "
    message += str(count_alive_users(link_data))
    message += "\n\n"
    message += "Pool Alive users:\n"
    f = lambda x: "vk.com/id" + str(x)

    for i in link_data[link_data['live flag'] == 1]['link'].index:
        message += f(link_data.iloc[i]['link'])
        message += "  kills: "
        message += str(link_data.iloc[i]['kills']) + '\n'

    return message


def top_belly_users(link_data: pd.DataFrame) -> str:
    """

    Output str list with top belly user.

    :param link_data: input link data
    :type link_data: pd.DataFrame

    :return: list with top belly user
    :rtype: str
    """
    message = str()
    message += "Top List Users:\n"
    sorted_data = link_data.sort_values(by='belly', ascending=False)
    sorted_data = sorted_data.reset_index(drop=True)
    sorted_data.to_csv(filename_sorted_users_data)
    f = lambda x: "vk.com/id" + str(x)

    for i in range(min(sorted_data.shape[0], 10)):
        message += f"\nUser {i}:\n"
        message += "live: "
        message += str(sorted_data.iloc[i]['live flag']) + '\n'
        message += "link: "
        message += f(sorted_data.iloc[i]['link']) + '\n'
        message += "belly: "
        message += str(sorted_data.iloc[i]['belly']) + '\n'
        message += "kills: "
        message += str(sorted_data.iloc[i]['kills']) + '\n'

    return message

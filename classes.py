from pandas import DataFrame
from enum import Enum
from vk_consts import admin_id
import typing


class User:
    def __init__(self, link_data: 'DataFrame', index_in_data: int) -> None:
        """
        Class that stores all information about a specific user.
        Initialized by viewing a specific row in a table with user information

        :param link_data: Input table
        :type link_data: DataFrame

        :param index_in_data: Index in table
        :type index_in_data: int
        """

        info_series = link_data.iloc[index_in_data]
        self.status = link_data['live flag'].values[index_in_data]
        self.index_in_data = index_in_data
        self.level_access = link_data['level access'].values[index_in_data]  # User access
        if info_series['link'] in admin_id:
            self.level_access = 10

        self.last_name = info_series['last name']
        self.first_name = info_series['first name']
        self.patronymic = info_series['patronymic']

        self.group = info_series['group']
        self.course = info_series['course']
        self.room = info_series['room']

        self.link = info_series['link']
        self.size = info_series['size']
        self.frequency = info_series['frequency']
        self.mail = info_series['mail']

        self.killer_ind = link_data['index killer'].values[index_in_data]
        killer_series = link_data.iloc[self.killer_ind]
        # print(killer_series)
        self.killer = killer_series['link']
        # print(self.killer)

        self.victim_ind = link_data['index victim'].values[index_in_data]
        victim_series = link_data.iloc[self.victim_ind]
        self.victim = victim_series['link']

        self.belly = link_data['belly'].values[index_in_data]
        self.kill_count = link_data['kills'].values[index_in_data]
        self.kill_list = link_data['kill_list'].values[index_in_data]

    def user_change_killer(self, new_killer: 'User') -> None:
        """
        Change killer of user on new_killer

        :param new_killer: user who becomes a new killer
        :type new_killer: User

        :return None
        """

        print("\n\n\n"
              "CHANGE USER, EVENT - user change killer\n\n"
              "user:\n"
              "user.link: {}, user.index_in_data: {}"
              "\n\n".format(self.link,
                            self.index_in_data))
        print("Old killer was killed\n\n"
              "old killer:\n"
              "old killer.link: {}\n"
              "old killer.index_in_data:{}"
              "\n\n".format(self.killer,
                            self.killer_ind))

        self.killer = new_killer.link
        self.killer_ind = new_killer.index_in_data

        print("New killer, who kill old killer\n\n"
              "new killer:\n"
              "new killer.link: {}, new killer.index_in_data:{}"
              "\n\n".format(self.killer,
                            self.killer_ind))
        print("CHANGE USER DONE\n\n\n")

    def user_killed_victim(self, new_victim: 'User') -> None:
        """
        Change victim of user on new victim

        :param new_victim: new victim for user
        :type new_victim: User

        :return: None
        """

        print("\n\n\n"
              "CHANGE USER, EVENT - user kill victim, change victim\n\n"
              "user:\n"
              "user.link: {}, user.index_in_data: {},\n"
              "user.belly: {},\n"
              "user.kill_count: {}\n"
              "user.kill_list: {}"
              "\n\n".format(self.link,
                            self.index_in_data,
                            self.belly,
                            self.kill_count,
                            self.kill_list))
        print("old victim was killed\n\n"
              "old victim:\n"
              "old victim.link: {}, old victim.index_in_data:{}"
              "\n\n".format(self.victim,
                            self.victim_ind))

        self.belly += 100 + 0.2 * new_victim.belly
        self.kill_count += 1
        self.kill_list += f'vk.com/id{new_victim.link} |'

        self.victim = new_victim.victim
        self.victim_ind = new_victim.victim_ind

        print("user:\n"
              "user.link: {}, user.index_in_data: {},\n"
              "user.belly: {},\n"
              "user.kill_count: {}\n"
              "user.kill_list: {}"
              "\n\n".format(self.link,
                            self.index_in_data,
                            self.belly,
                            self.kill_count,
                            self.kill_list))
        print("new victim:\n"
              "new victim.link: {}, new victim.index_in_data: {}"
              "\n\n".format(self.victim,
                            self.victim_ind))
        print("CHANGE USER DONE\n\n\n")

    def user_was_killed(self) -> None:
        """
        User be killed, Change status user(live -> die)

        :return: None
        """

        print("\n\n\n"
              "CHANGE USER, EVENT - user was killed\n\n"
              "user:\n"
              "user.link: {}, user.index_in_data: {},\n"
              "user.status: {}"
              "\n\n".format(self.link,
                            self.index_in_data,
                            self.status))

        self.status = False

        print("user:\n"
              "user.link: {}, user.index_in_data: {},\n"
              "user.status: {}"
              "\n\n".format(self.link,
                            self.index_in_data,
                            self.status))

        print("CHANGE USER DONE\n\n\n")

    def user_info(self) -> str:
        """
        Information about the user,
        that is shown to the user himself.

        :return: Cropped user information
        :rtype str
        """

        return f'????????????:    ' \
               f'{self.status * "live" or ((not self.status) * "die")}\n' \
               f'??????????????:   {self.last_name}\n' \
               f'??????:       {self.first_name}\n' \
               f'????????????????:  {self.patronymic}\n' \
               f'???????? ????????: vk.com/id{self.victim}\n' \
               f'???????????????????? belly:\n' \
               f'           {self.belly}\n' \
               f'???????????????????? ??????????????:\n' \
               f'           {self.kill_count}\n' \
               f'???? ?????? ??????????:\n' \
               f'           {self.kill_list}'

    def user_info_for_another_users(self, level_access: int = 0) -> str:
        """
        Information about the user,
        that is shown to the another user.
        The amount of information shown depends on
        the access level of the requesting user

        :param level_access: access level of the requesting user(0 by default)
        :type level_access: int

        :return: Cropped user info
        :rtype: str
        """

        if level_access > 0:
            return f'????????????:    ' \
                   f'{self.status * "live" or ((not self.status) * "die")}\n' \
                   f'??????????????:   {self.last_name}\n' \
                   f'??????:       {self.first_name}\n' \
                   f'????????????????:  {self.patronymic}\n' \
                   f'????????????:    vk.com/id{self.link}\n' \
                   f'?????? ?????????? ???????????????????? ?? ????????????:\n' \
                   f'           {self.frequency}\n' \
                   f'????????????:    {self.group}\n' \
                   f'????????:      {self.course}\n' \
                   f'??????????????:   {self.room}\n' \
                   f'???? ???????????????? ??????????:\n' \
                   f'           vk.com/id{self.victim}\n' \
                   f'???????????????????? belly:\n' \
                   f'           {self.belly}\n' \
                   f'???????????????????? ??????????????:\n' \
                   f'           {self.kill_count}\n' \
                   f'?????? ????????:\n' \
                   f'           {self.kill_list}'

        return f'????????????:    ' \
               f'{self.status * "live" or ((not self.status) * "die")}\n' \
               f'??????????????:   {self.last_name}\n' \
               f'??????:       {self.first_name}\n' \
               f'????????????????:  {self.patronymic}\n' \
               f'????????????:    vk.com/id{self.link}\n' \
               f'?????? ?????????? ???????????????????? ?? ????????????:\n' \
               f'           {self.frequency}\n\n' \
               f'????????????:    {self.group}\n' \
               f'????????:      {self.course}\n' \
               f'??????????????:   {self.room}\n' \
               f'???? ???????????????? ??????????:\n' \
               f'           SKV3##KNJ#\n' \
               f'???????????????????? ??????????:\n' \
               f'           KJN%#W12\n' \
               f'???????????????????? ??????????????:\n' \
               f'           JH21@&^#SD\n' \
               f'?????? ????????:\n' \
               f'           SDFIE8&###\n' \
               f'!!!LOW ACCESS LEVEL!!!\n'

    def admin_info_text_about_user(self) -> str:
        """
        Full user information for the admin.

        :return: Full user information
        :rtype: str
        """

        return f'????????????:    ' \
               f'{self.status * "live" or ((not self.status) * "die")}\n' \
               f'level_access:\n' \
               f'           {self.level_access}\n' \
               f'index_in_data:\n' \
               f'           {self.index_in_data}\n' \
               f'??????????????:   {self.last_name}\n' \
               f'??????:       {self.first_name}\n' \
               f'????????????????:  {self.patronymic}\n' \
               f'????????????:    {self.group}\n' \
               f'????????:      {self.course}\n' \
               f'??????????????:   {self.room}\n' \
               f'????????????:    vk.com/id{self.link}\n' \
               f'???????????? ????????????????:\n' \
               f'           {self.size}\n' \
               f'?????? ?????????? ???????????????????? ?? ????????????:\n' \
               f'           {self.frequency}\n' \
               f'??????????:     {self.mail}\n\n' \
               f'?????? ?????? ??????????????, ???????? ???? ??????????????\n' \
               f'?????? ???????????????? ??????????(killer):\n' \
               f'           vk.com/id{self.killer}\n' \
               f'killer index data:\n' \
               f'           {self.killer_ind}\n' \
               f'???? ???????????????? ??????????(victim):\n' \
               f'           vk.com/id{self.victim}\n' \
               f'victim index data:\n' \
               f'           {self.victim_ind}\n' \
               f'???????????????????? belly:\n' \
               f'           {self.belly}\n' \
               f'???????????????????? ??????????????:\n' \
               f'           {self.kill_count}\n' \
               f'?????? ????????:\n' \
               f'           {self.kill_list}'


class vk_requests(Enum):
    """
    Enum Class with requests users.
    """
    UNKNOWN = 0
    ADMIN_GET_NAME_VICTIM = 1
    ADMIN_GET_NAME_KILLER = 2
    KILL_CONFIRMATION = 3
    DEATH_CONFIRMATION = 4
    BAN_USER = 5

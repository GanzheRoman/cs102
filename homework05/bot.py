import requests
import config
import telebot
from bs4 import BeautifulSoup


bot = telebot.TeleBot(config.access_token)


def get_page(group, week=''):
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain,
        week=week,
        group=group)
    response = requests.get(url)
    web_page = response.text
    return web_page


def parse_schedule_for_a_monday(web_page):
    soup = BeautifulSoup(web_page, "html5lib")
    schedule_table = soup.find("table", attrs={"id": "1day"})
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list] 
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    return times_list, locations_list, lessons_list


@bot.message_handler(commands=['monday'])
def get_monday(message):
    """ Получить расписание на понедельник """
    group = message.text.split()
    web_page = get_page(group)
    times_lst, locations_lst, lessons_lst = \
        parse_schedule_for_a_monday(web_page)
    resp = ''
    for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message):
    """ Получить расписание на указанный день """
    day, week, group = message.text.split()
    web_page = get_page(group, week)
    schedule = parse_schedule(web_page, day[1:])
    if schedule is None:
        resp = 'Занятий нет'
    else:
        times_lst, locations_lst, rooms_lst, lessons_lst = schedule
        resp = ''
        for time, location, room, lession in zip(times_lst, locations_lst, rooms_lst,
                        lessons_lst):
            resp += '<b>{}</b>, {}, {}, {}\n'.format(time, location, room, lession)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')
    pass


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    group = message.text.split()
    today = int(datetime.datetime.today().weekday())
    week = (int(datetime.datetime.now().isocalendar()[1]) + 1) % 2
    web_page = get_page(group, week)
    schedule = parse_schedule(web_page, week_list[today])
    resp = ''
    flag = 0
    if schedule is None:
        while flag == 0:
            if today == 6:
                today = 0
                week = (week + 1) % 2
            else:
                today += 1
            web_page = get_page(group, week)
            next_schedule = parse_schedule(web_page, week_list[today])
            if next_schedule is not None:
                time, location, room, lession = next_schedule
                resp += '\n' + '\n' + "<b>{}:</b>".format(week_list_rus[today]) + '\n' + '\n'
                resp += '<b>{}</b>, {}, {}, {}\n'.format(time[0], location[0], room[0], lession[0])
                flag = 1
    else:
        times_lst, locations_lst, rooms_lst, lessons_lst = schedule
        minute_now = datetime.datetime.now().minute
        hour_now = datetime.datetime.now().hour
        for time, location, room, lession in zip(times_lst, locations_lst, rooms_lst, lessons_lst):
            beginning, _ = time.split('-')
            hour, minute = beginning.split(':')
            if hour[0] == '0':
                hour_int = int(hour[1])
            else:
                hour_int = int(hour[0]) * 10 + int(hour[1])
            if minute[0] == '0':
                minute_int = int(minute[1])
            else:
                minute_int = int(minute[0]) * 10 + int(minute[1])
            if hour_int == hour_now:
                if minute_int >= minute_now:
                    resp += '\n' + '\n' + "<b>{}:</b>".format(week_list_rus[today]) + '\n' + '\n'
                    resp += '<b>{}</b>, {}, {}, {}\n'.format(time, location, room, lession)
                    break
            elif hour_int > hour_now:
                resp += '\n' + '\n' + "<b>{}:</b>".format(week_list_rus[today]) + '\n' + '\n'
                resp += '<b>{}</b>, {}, {}, {}\n'.format(time, location, room, lession)
                break
        if resp == '':
            while flag == 0:
                if today == 6:
                    today = 0
                    week = (week + 1) % 2
                else:
                    today += 1
                web_page = get_page(group, week)
                next_schedule = parse_schedule(web_page, week_list[today])
                if next_schedule is not None:
                    time, location, room, lession = next_schedule
                    resp += '\n' + '\n' + "<b>{}:</b>".format(week_list_rus[today]) + '\n' + '\n'
                    resp += '<b>{}</b>, {}, {}, {}\n'.format(time[0], location[0], room[0], lession[0])
                    flag = 1
    bot.send_message(message.chat.id, resp, parse_mode='HTML')
    pass


@bot.message_handler(commands=['tommorow'])
def get_tommorow(message):
    """ Получить расписание на следующий день """
    group = message.text.split()
    today = int(datetime.datetime.today().weekday())
    if today == 6:
        week = int(datetime.datetime.now().isocalendar()[1]) % 2
        today = 0
    else:
        today += 1
        week = (int(datetime.datetime.now().isocalendar()[1]) + 1) % 2
    web_page = get_page(group, week)
    schedule = parse_schedule(web_page, week_list[today])
    if schedule is None:
        resp = 'В этот день занятий нет!'
    else:
        times_lst, locations_lst, rooms_lst, lessons_lst = schedule
        resp = ''
        for time, location, room, lession in zip(times_lst, locations_lst, rooms_lst, lessons_lst):
            resp += '<b>{}</b>, {}, {}, {}\n'.format(time, location, room, lession)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')
    pass


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    week, group = message.text.split()
    web_page = get_page(group, week)
    for day in range(7):
        schedule = parse_schedule(web_page, week_list[day])
        resp = '\n' + '\n' + "<b>{}:</b>".format(week_list_rus[day]) + '\n' + '\n'
        if schedule is None:
            resp += 'Занятий нет'
        else:
            times_lst, locations_lst, rooms_lst, lessons_lst = schedule
            for time, location, room, lession in zip(times_lst, locations_lst,
                        rooms_lst, lessons_lst):
                resp += '<b>{}</b> {} {} {}\n'.format(time, location, room, lession)
        bot.send_message(message.chat.id, resp, parse_mode='HTML')
    pass


if __name__ == '__main__':
    bot.polling(none_stop=True)



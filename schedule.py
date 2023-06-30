import datetime
import requests
from bs4 import BeautifulSoup

def scrape_schedule(username, password, request_type):
    today = datetime.date.today()

    # Perform login process with the provided username and password
    User_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0'
    Host = 'portal.nupp.edu.ua'
    
    url = 'https://portal.nupp.edu.ua/login'
    headers = {
        'User-agent': User_agent,
        'Host': Host,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,V*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    }

    s = requests.Session()
    d = s.get(url)
    csrf_token = s.cookies['_csrf-frontend']
    advanced_token = s.cookies['advanced-frontend']

    bs = BeautifulSoup(d.text, 'lxml')
    form_csrf_frontend = bs.find('input', {'name': '_csrf-frontend'})['value']

    url = 'https://portal.nupp.edu.ua/login'
    headers = {
        'advanced-frontend': advanced_token,
        '_csrf-frontend': csrf_token,
        'Referer': 'https://portal.nupp.edu.ua/login',
        'Connection': 'keep-alive',
    }

    data = {
        '_csrf-frontend': form_csrf_frontend,
        'LoginForm[username]': username,
        'LoginForm[password]': password,
        'LoginForm[rememberMe]': '0',
        'LoginForm[rememberMe]': '1',
        'login-button': ''
    }

    dd = s.post(url, data=data, headers=headers)
    identity_token = s.cookies['_identity-frontend']

    # Determine the date range based on user's request
    if request_type == 'today':
        date_start = today
        date_end = date_start
    elif request_type == 'this week':
        date_start = today - datetime.timedelta(today.weekday())
        date_end = date_start + datetime.timedelta(4)  # Only display 5 days
    else:
        date_start = today - datetime.timedelta(today.weekday()) + datetime.timedelta(7)
        date_end = date_start + datetime.timedelta(4)  # Only display 5 days

    url = 'https://portal.nupp.edu.ua/self/time-table'
    headers = {
        'advanced-frontend': advanced_token,
        '_csrf-frontend': csrf_token,
        '_identity-frontend': identity_token,
    }

    dd = s.get(url, headers=headers)
    dd.encoding = 'utf-8'
    bs = BeautifulSoup(dd.text, features="lxml")
    form_csrf_frontend = bs.find('meta', {'name': 'csrf-token'})['content']

    data = {
        '_csrf-frontend': form_csrf_frontend,
        'date-picker': f'{date_start.strftime("%d.%m.%Y")}+-+{date_end.strftime("%d.%m.%Y")}',
        'SelfTimeTableForm[dateStart]': date_start.strftime('%d.%m.%Y'),
        'SelfTimeTableForm[dateEnd]': date_end.strftime('%d.%m.%Y'),
        'SelfTimeTableForm[indicationDays]': '5',
        'time-table-type': '1'
    }
    dd = s.post(url, data=data, headers=headers)
    dd.encoding = 'utf-8'
    bs = BeautifulSoup(dd.text, features="lxml")
    table = bs.find('table', {'id': 'timeTable'})

    if table is not None:
        lessons = table.find_all('div', {'data-toggle': 'popover'})
        lesson_data = []
        for lesson in lessons:
            title = lesson['title'].replace('<br>', ' ')
            title = title.replace('пара', 'class')
            if '1 class' in title:
                title = '1⃣ ' + title
            if '2 class' in title:
                title = '2⃣ ' + title
            if '3 class' in title:
                title = '3⃣ ' + title
            if '4 class' in title:
                title = '4⃣ ' + title
            if '5 class' in title:
                title = '5⃣ ' + title
            if '6 class' in title:
                title = '6⃣ ' + title
            lesson_name = lesson['data-content'].partition('Додано')[0].replace('<br>', ' ')
            lesson_data.append(f"{title}\n{lesson_name}\n")

        if lesson_data:
            return lesson_data
        else:
            return "No lessons found."
    else:
        return "Unable to fetch schedule."


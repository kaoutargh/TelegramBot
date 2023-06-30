import requests
import pytz
from datetime import datetime

def get_air_raid_alert():
    url = 'https://api.ukrainealarm.com/api/v3/alerts/1060'
    headers = {
        'Authorization': 'Api Key',
        'accept': 'application/json',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }

    s = requests.Session()
    d = s.get(url, headers=headers)
    body_dict = d.json()

    date_now = datetime.now(pytz.timezone('Europe/Kiev'))
    date_now = date_now.replace(tzinfo=None) 
    formatted_date_now = date_now.strftime('%Y-%m-%d %H:%M')
    
    alert_message = None
    formatted_last_update = None
    duration = None

    if body_dict[0]['activeAlerts'] == []:
        alert_message = '🔕 POLTAVA REGION - NO AIR RAID ALERT IN ALL DIRECTIONS!😌'
        return alert_message, formatted_last_update, formatted_date_now, duration
        
    else:
        alert_type = body_dict[0]['activeAlerts'][0]['type']
        if alert_type == "AIR":
            alert_message = '🔔 ATTENTION! POLTAVA REGION - AIR RAID ALERT! MISSILE DANGER!💥'
        elif alert_type == "ARTILLERY":
            alert_message = '🔔 ATTENTION! POLTAVA REGION - AIR RAID ALERT! SHELLING THREAT!💥'
        elif alert_type == "STREET":
            alert_message = '🔔 ATTENTION! POLTAVA REGION - AIR RAID ALERT! STREET SHELLING THREAT!💥'
        elif alert_type == "CHEMICAL":
            alert_message = '🔔 ATTENTION! POLTAVA REGION - AIR RAID ALERT! CHEMICAL THREAT!💥'
        elif alert_type == "NUCLEAR":
            alert_message = '🔔 ATTENTION! POLTAVA REGION - AIR RAID ALERT! RADIATION THREAT!💥'
        else:
            alert_message = 'Unknown air raid alert type'
        
        last_update = datetime.strptime(body_dict[0]['lastUpdate'], '%Y-%m-%dT%H:%M:%SZ')
        last_update = pytz.timezone('Europe/Kiev').localize(last_update)
        formatted_last_update = last_update.strftime('%Y-%m-%d %H:%M')
        
        last_update_datetime = datetime.strptime(formatted_last_update, '%Y-%m-%d %H:%M')
        duration = date_now - last_update_datetime
    
    return alert_message, formatted_last_update, formatted_date_now, duration

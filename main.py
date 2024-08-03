import os
import configparser
from json import dumps, loads, load
from httplib2 import Http


def get_app_file_path(file):
    """
        Return the absolute path of the app's files.s
    """
    folder, _ = os.path.split(__file__)
    file_path = os.path.join(folder, file)
    return file_path


APP_CONFIG = configparser.ConfigParser()
APP_CONFIG.read(get_app_file_path('app.config'))
WEBHOOK_URL = APP_CONFIG['dev']['endpoint']


def insert_monitoring_id(rsp, id):
    """
        insert the alarm id in to the database
    """
    rsp_data = loads(str(rsp[1], encoding="utf-8"))

    alarms_info_db = get_app_file_path("tbl_alarms.json")

    # load the data
    with open(alarms_info_db, "r", encoding='utf8') as file:
        data = load(file)

    thread_name = rsp_data['thread']['name']
    msg_ns = rsp_data['name'].split('/')
    message_id = '/'.join(msg_ns[2:])

    alarm_obj = {'thread_name': thread_name, "message_id": message_id}

    data[id] = alarm_obj

    # write back
    data = dumps(data, indent=4)
    with open(alarms_info_db, "w", encoding='utf8') as file:
        file.write(data)


def get_thread_name(id):
    """
        Return the thread name of the message
    """
    alarms_info_db = get_app_file_path("tbl_alarms.json")
    with open(alarms_info_db, "r", encoding='utf8') as file:
        data = load(file)
    return data[id]['thread_name']


def send_text_message_by_webhook(web_hook_url, msg, alarm_id):
    """
        Send by using the google api web hook with explicit api and token key
    """
    message_headers = {"Content-Type": "application/json; charset=UTF-8"}
    web_hook_url = web_hook_url + "&client-custom-name"
    app_message = {
        "text": msg,
    }
    http_obj = Http()
    response = http_obj.request(
        uri=web_hook_url,
        method="POST",
        headers=message_headers,
        body=dumps(app_message),
    )

    insert_monitoring_id(response, alarm_id)
    return response


def send_thread_message_by_webhook(web_hook_url, msg, alarm_id):
    """
        Reply in thread to ease observation
    """
    web_hook_url = web_hook_url + \
        "&messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD"

    thread_name = get_thread_name(str(alarm_id))
    app_message = {
        "text": msg,
        "thread": {"name": thread_name}
    }
    message_headers = {"Content-Type": "application/json; charset=UTF-8"}
    http_obj = Http()
    response = http_obj.request(
        uri=web_hook_url,
        method="POST",
        headers=message_headers,
        body=dumps(app_message),
    )
    return response


def send_message_as_card(web_hook_url):
    message_headers = {"Content-Type": "application/json; charset=UTF-8"}
    
    # sample read card format
    data = get_app_file_path("chat_sample_card.json")
    with open(data, "r", encoding='utf8') as file:
        card_message = load(file)


    web_hook_url = WEBHOOK_URL + "&client-custom-name"

    http_obj = Http()
    response = http_obj.request(
        uri=web_hook_url,
        method="POST",
        headers=message_headers,
        body=dumps(card_message),
    )
    return response


def main():
    """
    main program here
    """

    # send_text_message_by_webhook(
    #     WEBHOOK_URL, "INCIDENT: I am Alert message - with monitoring ID 7896", 7896)
    # send_thread_message_by_webhook(
    #     WEBHOOK_URL, 'RESOLVED: I am thread message', 7896)

    send_message_as_card(WEBHOOK_URL)


if __name__ == "__main__":
    main()

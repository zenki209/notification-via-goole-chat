import os
import configparser
from json import dumps, loads, load
from httplib2 import Http


def get_app_file_path(file):
    """Return the absolute path of the app's files. They should be in the same folder as this py file."""
    folder, _ = os.path.split(__file__)
    file_path = os.path.join(folder, file)
    return file_path


def insert_monitoring_id(rsp, id):
    rsp_data = loads(str(rsp[1], encoding="utf-8"))
    # thread_name = response_data['thread']['name']
    alarms_info_db = (get_app_file_path("tbl_alarms.json"))

    # load the data
    with open(alarms_info_db, "r") as inFile:
        data = load(inFile)

    thread_name = rsp_data['thread']['name']
    msg_ns = rsp_data['name'].split('/')
    message_id = '/'.join(msg_ns[2:])

    alarm_obj = {'thread_name': thread_name, "message_id": message_id}

    data[id] = alarm_obj

    # write back
    data = dumps(data, indent=4)
    with open(alarms_info_db, "w") as outFile:
        outFile.write(data)


def get_thread_key(id):
    alarms_info_db = (get_app_file_path("tbl_alarms.json"))
    with open(alarms_info_db, "r") as inFile:
        data = load(inFile)
    return data[id]['thread_name']

def get_message_id(id):
    alarms_info_db = (get_app_file_path("tbl_alarms.json"))
    with open(alarms_info_db, "r") as inFile:
        data = load(inFile)
    return data[id]['message_id']



def send_text_message_by_webhook(webhookUrl, msg, id):
    message_headers = {"Content-Type": "application/json; charset=UTF-8"}
    webhookUrl = webhookUrl + "&client-custom-name"
    app_message = {
        "text": msg,
    }
    http_obj = Http()
    response = http_obj.request(
        uri=webhookUrl,
        method="POST",
        headers=message_headers,
        body=dumps(app_message),
    )

    insert_monitoring_id(response, id)
    return response


def send_thread_message_by_webhook(webhookUrl, msg, id):
    webhookUrl = webhookUrl + "&messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD"

    thread_name = get_thread_key(str(id))
    app_message = {
        "text": msg,
        "thread": {"name": thread_name}
    }
    message_headers = {"Content-Type": "application/json; charset=UTF-8"}
    http_obj = Http()
    response = http_obj.request(
        uri=webhookUrl,
        method="POST",
        headers=message_headers,
        body=dumps(app_message),
    )
    return response


def main():
    APP_CONFIG = configparser.ConfigParser()
    APP_CONFIG.read(get_app_file_path('app.config'))

    WEBHOOK_URL = APP_CONFIG['dev']['endpoint']

    response = send_text_message_by_webhook(
        WEBHOOK_URL, "INCIDENT: I am Alert message - with monitoring ID 7896", 7896)
    reply = send_thread_message_by_webhook(
       WEBHOOK_URL, 'RESOLVED: I am thread message', 7896)


if __name__ == "__main__":
    main()

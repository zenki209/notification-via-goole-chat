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

    data[id] = rsp_data['thread']['name']

    # write back
    data = dumps(data, indent=4)
    with open(alarms_info_db, "w") as outFile:
        outFile.write(data)


def get_thread_key(id):
    alarms_info_db = (get_app_file_path("tbl_alarms.json"))
    with open(alarms_info_db, "r") as inFile:
        data = load(inFile)
    return data[id]


def resolve_incident(webhookUrl, id):
    thread_name = get_thread_key(str(id))
    print(thread_name)


def send_text_message_by_webhook(webhookUrl, msg, id):
    message_headers = {"Content-Type": "application/json; charset=UTF-8"}
    app_message = {
        "text": msg
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

    # response = send_text_message_by_webhook(
    #     WEBHOOK_URL, "INCIDENT: I am Alert message - with monitoring ID 4567", 4567)
    # reply = send_thread_message_by_webhook(
    #    WEBHOOK_URL, 'I am thread message', 4567)

    resolve_incident(WEBHOOK_URL, 4567)


if __name__ == "__main__":
    main()

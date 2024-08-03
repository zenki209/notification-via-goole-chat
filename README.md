# Notes:

This repo is a sample of using the google api to send the message as a plain text or we can send as a card

The documentation of the google API as below

```
    API information:
    https://developers.google.com/workspace/chat/quickstart/webhooks


    Card Builder - Using cardV2:
    https://addons.gsuite.google.com/uikit/builder
```

In order to use this code - please create the file __app.config__ and input the endpoint of your environment syntax below


```
[prod]
endpoint=''

[dev]
endpoint='https://chat.googleapis.com/v1/spaces/AAAAYILywMY/messages?key=xxxxxxxI&token=xxxxxxx'
```

The card message would be like 
![card-images](https://github.com/user-attachments/assets/0449f215-18bd-4d89-869c-2449e4496920)

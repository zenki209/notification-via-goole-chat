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
![stack Overflow]([http://lmsotfy.com/so.png](https://github.com/zenki209/notification-via-goole-chat/blob/master/images/card-images.png))

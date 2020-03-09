# comics publisher

This script downloads a random [xkcd](https://xkcd.com) comic and uploads it to your [VK](https://vk.com/) group.

![gif](xkcd.gif)

### How to install

1. Create a VK group for your posts.
2. Create an `.env` file in the project directory and save group id there:
```
VK_GROUP_ID='your group id'
```
You can get group id [here](http://regvk.com/id/).
3. Use [VK developers page](https://vk.com/dev) to create your app. For more information please read the [documentation](https://vk.com/dev/vkapp_create) on how to create VK apps. Select `standalone app` as a platform.
4.  Save `client_id` of your app in the `.env` file:
```
VK_GROUP_ID='your group id'
VK_APP_ID='your app client id'
```
5. Use Implicit Flow to collect your `access_token` save it to the `.env` file:
```
VK_GROUP_ID='your group id'
VK_APP_ID='your app client id'
VK_ACCESS_TOKEN='your access token'
```
For more inforation on the topic please read the [documentation](https://vk.com/dev/implicit_flow_user).
6. Python3 should be already installed. 
Use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

### Launch

```
python3 main.py
```

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).

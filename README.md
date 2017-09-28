# twitter-hq-image-upload-web
Web Service for support high quality image upload to Twitter


How to works
-----

Twitter resizes your upload image for reduce traffic and storage usage. But only JPG files.
The PNG file with transparent pixel will not resized by Twitter. So you can upload high quality image to Twitter.
This server application uses that trick. When you upload image to this server, this server will modify the last of pixel to transparently. Then Twitter doesn't reduce the image qulity.

How to use
-----

1. Go to Twitter developer site and make the new app and get 4 tokens below at this section.
2. Fix the default constant variables to use (web_password, default_resize_rate).
3. Run this server.py with python3.
4. Connect to this server with the specified port(default 12345).

Twitter Image API only suuport the image size up to 5MB. You should modify the constant variable 'default_resize_rate' by your uploading image file size. This variable will resize the resolution of your uploading image.

```python
consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''
```

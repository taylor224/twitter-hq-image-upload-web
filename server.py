import os
import io
import requests
import tempfile
import datetime
import time
import tweepy
import time
import math
from StringIO import StringIO
from PIL import Image, ImageFilter, ImageFont, ImageDraw, ImageFile
from flask import Flask, request, send_from_directory, send_file, abort, redirect, url_for, render_template, session

consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

my_id = None
my_name = None
my_screen_name = None

web_password = 'default_password'
default_resize_rate = 0.5


# set the project root directory as the static folder, you can set others.
app = Flask(__name__)
app.secret_key = 'Web_Application_Secret_Key'

def get_pil_image(pil_img, resize):
    name = str(time.time()) + '.png'
    #img_io = StringIO()
    width, height = pil_img.size
    width = width * resize
    height = height * resize
    im = pil_img.resize((int(math.floor(width)), int(math.floor(height))), Image.ANTIALIAS)
    im.save(name, 'PNG', quality=90, optimize=True)
    return name


@app.route("/robots.txt")
def robots_txt():
    return "User-agent: *\nDisallow: /"


@app.route('/view/login')
def view_login():
    return render_template('login.html')


@app.route('/make/login', methods=['POST'])
def make_login():
    password = request.form.get('password')

    if not password == web_password:
        return abort(401)

    session['login'] = True

    return redirect(url_for('view_upload'))


@app.route('/view/upload')
def view_upload():
    if not session.get('login'):
        return redirect(url_for('view_login'))

    return render_template('upload.html')

@app.route('/make/upload', methods=['POST'])
def make_upload():
    if not session.get('login'):
        return abort(404)

    imagefile = request.files.get('uploadimage', '')
    message = request.form.get('message')

    if not imagefile:
        return abort(405)

    image = Image.open(imagefile.stream)
    new_image = Image.new('RGBA', image.size)
    new_image.paste(image)

    pixeldata = list(new_image.getdata())
    listpixel = list(pixeldata[-1])
    listpixel[3] = 240
    pixeldata[-1] = tuple(listpixel)
    new_image.putdata(pixeldata)

    if not message or message.strip() == '':
        message = 'Default Twitter Message '

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)

    filename = get_pil_image(new_image, default_resize_rate)
    api.update_with_media(filename, status=message)
    os.remove(filename)

    return redirect(url_for('view_upload'))

if __name__ == "__main__":
    app.run('0.0.0.0', debug=False, port=12345)

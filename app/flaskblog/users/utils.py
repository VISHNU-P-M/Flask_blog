from flaskblog import mail
import os
from flask import url_for, current_app as app
from PIL import Image
from flask_mail import Message






def save_image(profile_pic, username):
    _, file_ext = os.path.splitext(profile_pic.filename)
    image_name = username + file_ext
    image_path = os.path.join(app.root_path,'static/profile_pic', image_name )
    image = Image.open(profile_pic)
    width, height = image.size
    if width == height:
        return image
    offset  = int(abs(height-width)/2)
    if width>height:
        image = image.crop([offset,0,width-offset,height])
    else:
        image = image.crop([0,offset,width,height-offset])
    image.save(image_path)

    return image_name




def send_mail(user):
    token = user.request_token()
    print(token)
    msg = Message('Password Reset Request', 
                    sender='noreply@gmail.com', 
                    recipients=[user.email])
    msg.body='''
            To reset password, visit following link
{url_for('users.reset_password', token = token, _external=True)}

if you not request for this, then ignore.
    '''

    mail.send(msg)



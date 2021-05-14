from server import STATIC_PATH

from flask import request, send_file, render_template
import qrcode
import uuid
from PIL import Image, ImageFont, ImageDraw, ImageOps

IMAGE_FILE_PATH = STATIC_PATH + "/temp/"
FONTS_PATH = STATIC_PATH + "/fonts"
BORDER_SIZE = 5
FONT_SIZE = 20

def add_border(input_image, output_image, border, color=0):
    img = Image.open(input_image)
    if isinstance(border, int) or isinstance(border, tuple):
        bimg = ImageOps.expand(img, border=border, fill=color)
    else:
        raise RuntimeError('Border is not an integer or tuple!')
    bimg.save(output_image)

def createQRCode(trackingLink, trackingLinkIdentifier, __filepath__):
    # prepare qrcode
    qr = qrcode.QRCode(version=1, box_size=3, border=BORDER_SIZE)
    qr.add_data(trackingLink)
    qr.make(fit=True)

    # generate name for the img
    if trackingLinkIdentifier:
        imgname = "QRCode_" + str(trackingLinkIdentifier) + "_" + str(uuid.uuid1())[:8] + ".png"
    else:
        imgname = "QRCode_" +  str(uuid.uuid1())[:8] + ".png"
    imgpath = __filepath__ + imgname 

    # create QRCode
    img = qr.make_image(fill='black', back_color='white')
    im_size = img.size

    # change size
    new_im = Image.new("RGB", (int((im_size[0]+(len(imgname)*FONT_SIZE))-int(len(str(trackingLinkIdentifier))*FONT_SIZE)/2), im_size[1]) , (255,255,255))
    new_im_size = new_im.size

    new_im.paste(img, (0, 0))
    new_im.save(imgpath)
    print(imgpath)

    # add text to image
    im = Image.open(imgpath)
    new_im_size = im.size

    myfont = ImageFont.truetype(FONTS_PATH+"/Verdana.ttf", FONT_SIZE)
    d = ImageDraw.Draw(im)
    if trackingLinkIdentifier:
        text = "Id: " + trackingLinkIdentifier + "\n" + imgname
    else:
        text = "" + "\n" + imgname
    d.text(((im_size[0]), new_im_size[1]/2 - int(1.5* FONT_SIZE)), text, font=myfont, fill= (0,0,0))      
    im.save(imgpath)

    add_border(imgpath, output_image=imgpath, border=4, color=(0,0,0))

    return imgpath

def return_template(__template__):
    # if website returns tracking link
    if request.method == 'POST':
        #catch data of form
        trackingLink = request.form['trackingLink']
        trackingLinkIdentifier = request.form['trackingLinkIdentifier']

        return str(render_template(__template__, QRCodeIMGStyle="", QRCodeIMGFilename=createQRCode(trackingLink, trackingLinkIdentifier)))
    else:
        return str(render_template(__template__, QRCodeIMGStyle="display: none;"))
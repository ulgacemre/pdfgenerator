from __future__ import print_function
from flask_jwt import jwt_required
from z3c.rml import reference, rml2pdf
import glob
import os, base64, preppy
from random import shuffle, random
from xml.sax.saxutils import escape, unescape
from django.template.loader import get_template
from django.template.context import Context
import PIL
from django.conf import settings
from jinja2 import Template
settings.configure()
from flask import Flask, request, flash, send_from_directory, send_file, render_template
from trml2pdf import trml2pdf
from werkzeug.utils import redirect, secure_filename
from flask_httpauth import HTTPBasicAuth



app = Flask(__name__)

auth = HTTPBasicAuth()

DATA_DIR = 'data'
app.config["UPLOAD_FOLDER"] = "/Users/emreulgac/PycharmProjects/xysınav/app/static/img"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG"]


class PDF(object):
    "Empty class to hold parsed product attributes"
    pass



@auth.verify_password
def verify_password(username, password):
    if username == 'xysinav' and password == 'yGCH2ta4724bqbPBjG6KM2hWP':
        return True
    return False



@app.route('/' ,methods=['GET'])
def fix():
   return "Hello Pdf Api"

def create_pdf(files, template,first_page_title_size="38",first_page_title_x="80",first_page_title_y="700",first_page_title_font="Helvetica-Bold",
               first_page_title=" ",first_page_title_color="blue",question_top_padding="35",question_bottom_padding="55",question_numbers_offsetY="-30",
               both_side_mode="True",pages_bottom_title="xysinav",pages_bottom_title_font="Helvetica-Bold",pages_bottom_title_size="10",pages_bottom_title_color="black",
               pdf_filename="output",question_count="2"):
    """Creates PDF as a binary stream in memory, and returns it

    This can then be used to write to disk from management commands or crons,
    or returned to caller via Django views.
    """
    RML_DIR = 'rml'

    content = """<?xml version="1.0" encoding="utf-8" standalone="no" ?>
        <!DOCTYPE document SYSTEM "rml.dtd">

    <document filename="harwoodgame_flyer.pdf">



    <docinit>
        <registerTTFont faceName="HelveticaNeue-Light" fileName="rml/fonts/LTe50263.ttf"/>
        <registerTTFont faceName="HelveticaNeue-Bold" fileName="rml/fonts/LTe50261.ttf"/>
    </docinit>

    <template pageSize="(595, 842)" leftMargin="50" topMargin="30" showBoundary="0">
            <pageTemplate id="front-page">
            <pageGraphics>
                <image file="rml/front-1.jpg" x="0" y="0" width="595" height="842"/>
                <fill color="red"/>
                <setFont name="HelveticaNeue-Light" size="12"/>
                <drawCenteredString x="297" y="40"></drawCenteredString>
                <fill color="{first_page_titlecolor}"/>
                <setFont name="{first_page_title_font}" size="{first_page_title_size}"/>
                <drawString x="{first_page_title_x}" y="{first_page_title_y}">{first_page_title}</drawString>
            </pageGraphics>

             <frame id="main" x1="5%" y1="8%" width="43%" height="90%"/>
        </pageTemplate>
        <pageTemplate id="questions">
            <pageGraphics>
                <image file="rml/Bel12-1.jpg" x="0" y="0" width="595" height="1000"/>
                <fill color="red"/>
                <setFont name="HelveticaNeue-Light" size="12"/>
                <drawCenteredString x="297" y="40"></drawCenteredString>

                <fill color="{pages_bottom_title_color}"/>
                <setFont name="{pages_bottom_title_font}" size="{pages_bottom_title_size}"/>
                <drawCenteredString x="297" y="30">{pages_bottom_title}</drawCenteredString>

            </pageGraphics>

         {both_side_mode}


        </pageTemplate>




    </template>

    <stylesheet>

        <paraStyle name="h1"
        fontName="HelveticaNeue-Light"
        fontSize="27"
        leading="17"
        spaceBefore = "30"
        />


            <paraStyle name="front-h1"
        fontName="HelveticaNeue-Light"
        fontSize="27"
        leading="17"
        spaceBefore="10in"


        />




        <paraStyle name="h2"
        fontName="HelveticaNeue-Bold"
        fontSize="15"
        leading="17"
        spaceBefore = "15"
        />

        <paraStyle name="prod_name"
        fontName="HelveticaNeue-Light"
        fontSize="14.5"
        leading="14"
        spaceBefore = "14"
        />

        <paraStyle name="prod_summary"
        fontName="HelveticaNeue-Light"
        fontSize="12"


        />



    <listStyle
     name="lili"
     rightIndent="15"
    bulletOffsetY="{question_numbers_offsetY}"


     />

        <paraStyle name="prod_price"
        fontName="HelveticaNeue-Bold"
        fontSize="7.5"
        leading="14"
        spaceBefore = "4"
        textColor="green"
        />
            <paraStyle name="normal" fontName="Helvetica" fontSize="10" leading="12" />
        <paraStyle name="bullet" parent="normal" bulletFontName = "Helvetica" bulletFontSize="5"/>

    </stylesheet>






    <story>



    <setNextTemplate name="front-page"  />


        <setNextTemplate name="questions" />



        <nextFrame/>


    <ol bulletColor="red"   bulletFontName="Times-Roman" >

       {images_last}


        </ol>

    </story>


    </document>
            """

    templateName = os.path.join(RML_DIR, template)
    template = preppy.getModule(templateName)
    namespace = {
        'files':files,
        'RML_DIR': RML_DIR,
        'IMG_DIR': 'img',
        'first_page_title_size':first_page_title_size,
        'first_page_title_x':first_page_title_x,
        'first_page_title_y':first_page_title_y,
        'first_page_title_font':first_page_title_font,
        'first_page_title' :first_page_title,
        'first_page_title_color':first_page_title_color,
        'question_top_padding':question_top_padding,
        'question_bottom_padding':question_bottom_padding,
        'question_numbers_offsetY':question_numbers_offsetY,
        'both_side_mode':both_side_mode,
        'pages_bottom_title':pages_bottom_title,
        'pages_bottom_title_font':pages_bottom_title_font,
        'pages_bottom_title_size':pages_bottom_title_size,
        'pages_bottom_title_color':pages_bottom_title_color,
        'question_count':question_count

        }



    i=0
    images_last = " "
    while i < question_count:


        images='<li style="lili"  bulletColor="black"    bulletFontName="Helvetica"> <imageAndFlowables  imageName="app/static/img/{URL}" imageTopPadding="{question_top_padding}" imageBottomPadding="{question_bottom_padding}"> </imageAndFlowables></li>'

        images=images.format(URL=files[i],question_top_padding=question_top_padding,question_bottom_padding=question_bottom_padding)
        images_last=images_last + images

        i=i+1


    f = open("latest-2.rml", "w+")

    if both_side_mode == "True":
        last_content = content.format(first_page_titlecolor=first_page_title_color,
                                 first_page_title_size=first_page_title_size,
                                 first_page_title_font=first_page_title_font,
                                 first_page_title_x=first_page_title_x, first_page_title_y=first_page_title_y,
                                 first_page_title=first_page_title,
                                 pages_bottom_title_color=pages_bottom_title_color,
                                 pages_bottom_title_font=pages_bottom_title_font,
                                 pages_bottom_title_size=pages_bottom_title_size
                                 , pages_bottom_title=pages_bottom_title,question_numbers_offsetY=question_numbers_offsetY,
                                      both_side_mode='<frame id="left" x1="5%" y1="8%" width="43%" height="90%"/> <frame id="right" x1="55%" y1="8%" width="43%" height="90%"/>',images_last=images_last)
    else:
        last_content = content.format(first_page_titlecolor=first_page_title_color,
                                 first_page_title_size=first_page_title_size,
                                 first_page_title_font=first_page_title_font,
                                 first_page_title_x=first_page_title_x, first_page_title_y=first_page_title_y,
                                 first_page_title=first_page_title,
                                 pages_bottom_title_color=pages_bottom_title_color,
                                 pages_bottom_title_font=pages_bottom_title_font,
                                 pages_bottom_title_size=pages_bottom_title_size
                                 , pages_bottom_title=pages_bottom_title,question_numbers_offsetY=question_numbers_offsetY,
                                 both_side_mode='<frame id="left" x1="5%" y1="8%" width="43%" height="90%"/>',images_last=images_last)

    f.write(last_content)

    f.close()

    return   rml2pdf.go('latest-2.rml', pdf_filename +'.pdf')




def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def sort_images():

    os.chdir('/Users/emreulgac/PycharmProjects/xysınav/app/static/img/')
    files = os.listdir(os.getcwd())
    files.sort(key=lambda f: os.stat(f).st_size, reverse=True)
    os.chdir('/Users/emreulgac/PycharmProjects/xysınav/')

    print(len(files))
    print(files)
    i=0
    j=0
    new_list=[]

    while j <=len(files)-1:
        print(j)
        if j%2 == 0:
            new_list.append(files[j])
        else:
            new_list.append(files[-j])

        j=j+1
        i=i+1

    return new_list


@app.route('/create' ,methods=['GET', 'POST'])
@auth.login_required
def main():


    first_page_title = request.form.get('first_page_title')
    first_page_title_size=request.form.get('first_page_title_size')
    first_page_title_font = request.form.get('first_page_title_font')
    first_page_title_x = request.form.get('first_page_title_x')
    first_page_title_y = request.form.get('first_page_title_y')
    first_page_title_color = request.form.get('first_page_title_color')
    pdf_filename = request.form.get('filename')
    question_top_padding = request.form.get('question_top_padding')
    question_bottom_padding=request.form.get('question_bottom_padding')
    question_numbers_offsetY=request.form.get('question_numbers_offsetY')
    both_side_mode=request.form.get('both_side_mode')
    pages_bottom_title=request.form.get('pages_bottom_title')
    pages_bottom_title_font = request.form.get('pages_bottom_title_font')
    pages_bottom_title_size = request.form.get('pages_bottom_title_size')
    pages_bottom_title_color = request.form.get('pages_bottom_title_color')


    # check if the post request has the file part
    if 'questions' not in request.files:
        flash('No file part')
    files =request.files.getlist("questions")

    for file in files:
         if file and allowed_image(file.filename):
             filename = secure_filename(file.filename)
             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
             l = os.listdir(os.path.join(app.config['UPLOAD_FOLDER']))




    pdf = create_pdf(sort_images(), 'flyer_template.prep', first_page_title_size,first_page_title_x,
                     first_page_title_y,first_page_title_font,first_page_title,
                     first_page_title_color,question_top_padding,question_bottom_padding,question_numbers_offsetY,both_side_mode,
                     pages_bottom_title,pages_bottom_title_font,pages_bottom_title_size,pages_bottom_title_color,pdf_filename,len(files))

    filename = pdf_filename+'.pdf'



    files = glob.glob('/Users/emreulgac/PycharmProjects/xysınav/app/static/img/*')
    for f in files:
        os.remove(f)

    path= '/Users/emreulgac/PycharmProjects/xysınav/'+filename
    return send_file(path, as_attachment=True)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

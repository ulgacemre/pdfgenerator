from __future__ import print_function
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import reportlab
from z3c.rml import reference, rml2pdf
import glob
import os, base64
from random import shuffle, random
from xml.sax.saxutils import escape, unescape
import PIL
from flask import Flask, jsonify, request, flash, send_from_directory, send_file, render_template, make_response
#from trml2pdf import trml2pdf
from werkzeug.utils import redirect, secure_filename
from flask_httpauth import HTTPBasicAuth
from wtforms import Form, BooleanField, StringField, PasswordField, validators



BASE_DIR = '/Users/emreulgac/PycharmProjects/pdfgenerator'

reportlab.rl_config.TTFSearchPath.append(BASE_DIR + '/fontlar')
reportlab.rl_config.TTFSearchPath.append('/rml-files/fonts')
reportlab.rl_config.TTFSearchPath.append(BASE_DIR + '/')
reportlab.rl_config.TTFSearchPath.append('/fontlar')
#reportlab.rl_config.TTFSearchPath.append('/app/static/img')
reportlab.rl_config.TTFSearchPath.append('/img')
reportlab.rl_config.TTFSearchPath.append(BASE_DIR + '/img')


app = Flask(__name__)

auth = HTTPBasicAuth()

DATA_DIR = 'data'
app.config["UPLOAD_FOLDER"] = BASE_DIR + "/img"
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

    #RML_DIR = 'rml-files'

    content = """<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
        <!DOCTYPE document SYSTEM "rml.dtd">

    <document filename="harwoodgame_flyer.pdf"  xmlns:doc="http://namespaces.zope.org/rml/doc">


    <docinit>
       <registerTTFont faceName="Arial" fileName="/Users/emreulgac/PycharmProjects/pdfgenerator/fontlar/Arial.ttf"/>
       <registerTTFont faceName="Nunito-Regular" fileName="/Users/emreulgac/PycharmProjects/pdfgenerator/fontlar/Nunito-Regular.ttf"/>
       <registerTTFont faceName="Helvetica" fileName="/Users/emreulgac/PycharmProjects/pdfgenerator/fontlar/Helvetica.ttf"/>
       <registerTTFont faceName="HelveticaNeue-Light" fileName="/Users/emreulgac/PycharmProjects/pdfgenerator/fontlar/LTe50263.ttf"/>
       <registerTTFont faceName="HelveticaNeue-Bold" fileName="/Users/emreulgac/PycharmProjects/pdfgenerator/fontlar/LTe50261.ttf"/>
    </docinit>

    <template pageSize="(595, 842)" leftMargin="50" topMargin="30" showBoundary="0">
            <pageTemplate id="front-page">
            <pageGraphics>
                <image file="/Users/emreulgac/PycharmProjects/pdfgenerator/rml-files/front-1.jpg" x="0" y="0" width="595" height="842"/>
                <fill color="red"/>
                <setFont name="Helvetica" size="12"/>
                <drawCenteredString x="297" y="40"></drawCenteredString>
                <fill color="{first_page_titlecolor}"/>
                <setFont name="{first_page_title_font}" size="{first_page_title_size}"/>
                <drawString x="{first_page_title_x}" y="{first_page_title_y}">{first_page_title}</drawString>
                
            </pageGraphics>

             <frame id="main" x1="5%" y1="8%" width="43%" height="90%"/>
        </pageTemplate>
        <pageTemplate id="questions">
            <pageGraphics>
    
                
         <image file="/Users/emreulgac/PycharmProjects/pdfgenerator/rml-files/p1.jpg" x="0" y="80" width="595" height="750" />
                <fill color="red"/>
                <setFont name="Helvetica" size="12"/>
                <drawCenteredString x="297" y="40"></drawCenteredString>
                    <image file="/Users/emreulgac/PycharmProjects/pdfgenerator/rml-files/logo.jpg" x="15" y="755" width="100" height="100"/>
            

         
<fill color= "blue" />
<rect x="30" y = "45" width="535" height="1" round="1"  stroke="0" fill="1"  />
                <fill color="black"/>
                <drawString x="32" y="30">{first_page_title}</drawString>
                
            <fill color="black"/>
           <drawString x="297" y="30"><pageNumber/></drawString>
           
             <fill color="black"/>
           <drawString x="447" y="30">Diğer sayfaya geçiniz</drawString>
          
<fill color= "blue" />
<rect x="30" y = "22" width="535" height="1" round="1" fill="1"   stroke="0" />


            </pageGraphics>
            
                 
    
        
         {both_side_mode}

        

        </pageTemplate>
        
        
        
        <pageTemplate id="questions-2">
            <pageGraphics>
              
             <image file="/Users/emreulgac/PycharmProjects/pdfgenerator/rml-files/p2.jpg" x="0" y="80" width="595" height="750" />
              <fill color="red"/>
                <setFont name="Helvetica" size="12"/>
             <drawCenteredString x="297" y="40"></drawCenteredString>
                <image file="/Users/emreulgac/PycharmProjects/pdfgenerator/rml-files/logo.jpg" x="15" y="755" width="100" height="100"/>
            
<fill color= "blue" />
<rect x="30" y = "45" width="535" height="1" round="1"  stroke="0" fill="1"  />
                <fill color="black"/>
                <drawString x="32" y="30">{first_page_title}</drawString>
                
            <fill color="black"/>
           <drawString x="297" y="30"><pageNumber/></drawString>
           
             <fill color="black"/>
           <drawString x="447" y="30">Diğer sayfaya geçiniz</drawString>
          
<fill color= "blue" />
<rect x="30" y = "22" width="535" height="1" round="1" fill="1"   stroke="0" />


            </pageGraphics>
            
                 
    
        
         {both_side_mode}

        

        </pageTemplate>
    </template>

    <stylesheet>

        <paraStyle name="h1"
        fontName="Helvetica"
        fontSize="27"
        leading="17"
        spaceBefore = "30"
        />
            <paraStyle name="front-h1"
        fontName="Helvetica"
        fontSize="27"
        leading="17"
        spaceBefore="10in"
        />
        <paraStyle name="h2"
        fontName="Helvetica"
        fontSize="15"
        leading="17"
        spaceBefore = "15"
        />

        <paraStyle name="prod_name"
        fontName="Helvetica"
        fontSize="14.5"
        leading="14"
        spaceBefore = "14"
        />

        <paraStyle name="prod_summary"
        fontName="Helvetica"
        fontSize="12"
        />

     <listStyle name="blah" spaceAfter="10" bulletType="A" spaceBefore="23" />
	<listStyle name="square" spaceAfter="10" bulletType="bullet" spaceBefore="23" bulletColor="red" start="square"/>

        <paraStyle name="prod_price"
        fontName="Helvetica"
        fontSize="7.5"
        leading="14"
        spaceBefore = "4"
        textColor="green"
        />
            <paraStyle name="normal" fontName="Helvetica" fontSize="10" leading="12" />
        <paraStyle name="bullet" parent="normal" bulletFontName = "Helvetica" bulletFontSize="5"/>

           <listStyle
        name="Ordered"
        bulletFontName="Nunito"
        bulletFontSize="13"
        bulletFormat="%s."
        bulletDedent="25"
        bulletType="1"
       bulletColor="black"
        leftIndent="25"
        
             
    bulletOffsetY="{question_numbers_offsetY}"
        />
    </stylesheet>

    <story>
      
         <setNextTemplate name="front-page"  />

     
        <setNextTemplate name="questions-2"  />
        <nextFrame/>


    
    
        
    <ol style="Ordered"  >

       {images_last}
 
        </ol>
      

    </story>
    
 


    </document>
            """

    i=0
    images_last = " "
    while i < question_count:
        print("hallo"+files[i])

        if files[i] == '.DS_Store':
            i = i + 1

        images='<li   bulletColor="black"   bulletFontName="Helvetica"> <imageAndFlowables  imageName="/Users/emreulgac/PycharmProjects/pdfgenerator/img/{URL}" imageTopPadding="{question_top_padding}" imageBottomPadding="{question_bottom_padding}"> </imageAndFlowables> </li>'


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
                                      both_side_mode='<frame id="left" x1="3%" y1="2%" width="42%" height="90%"/> <frame id="right" x1="54%" y1="2%" width="42%" height="90%"/>',images_last=images_last)
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
                                 both_side_mode='<frame id="left" x1="3%" y1="2%" width="44%" height="90%"/>',images_last=images_last)

    f.write(last_content)

    f.close()

    print(last_content)

    return   rml2pdf.go('latest-2.rml',BASE_DIR + '/output/' +pdf_filename +'.pdf')



def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def sort_images():

    os.chdir(BASE_DIR + '/img/')
    files = os.listdir(os.getcwd())
    files.sort(key=lambda f: os.stat(f).st_size, reverse=True)
    os.chdir('/')

    print(len(files))
    print(files)
    i=0
    j=0
    new_list=[]

    while j <=len(files)-1:

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
    if first_page_title is None:
        return make_response(jsonify(first_page_title='First page title required.'), 400)
    first_page_title_size=request.form.get('first_page_title_size')
    if first_page_title_size is None:
        return make_response(jsonify(first_page_title_size='First page title size required.'), 400)
    first_page_title_font = request.form.get('first_page_title_font')
    if first_page_title_font is None:
        return make_response(jsonify(first_page_title_font='First page title font required.'), 400)
    first_page_title_x = request.form.get('first_page_title_x')
    if first_page_title_x is None:
        return make_response(jsonify(first_page_title_x='First page title x coordinate required.'), 400)
    first_page_title_y = request.form.get('first_page_title_y')
    if first_page_title_y is None:
        return make_response(jsonify(first_page_title_y='First page title y coordinate required.'), 400)
    first_page_title_color = request.form.get('first_page_title_color')
    if first_page_title_color is None:
        return make_response(jsonify(first_page_title_color='First page title color required.'), 400)
    pdf_filename = request.form.get('filename')
    if pdf_filename is None:
        return make_response(jsonify(pdf_filename='Pdf filename required.'),400)
    question_top_padding = request.form.get('question_top_padding')
    if question_top_padding is None:
        return make_response(jsonify(question_top_padding='Questions top padding required.'), 400)
    question_bottom_padding=request.form.get('question_bottom_padding')
    if question_bottom_padding is None:
        return make_response(jsonify(question_bottom_padding='Questions bottom padding required.'), 400)
    question_numbers_offsetY=request.form.get('question_numbers_offsetY')
    if question_numbers_offsetY is None:
        return make_response(jsonify(question_numbers_offsetY='Questions numbers Y offset required.'), 400)
    both_side_mode=request.form.get('both_side_mode')
    if both_side_mode is None:
        return make_response(jsonify(both_side_mode='Both side mode required.'), 400)
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

    files2 = os.listdir(BASE_DIR +'/img/')

    for file in files2:
        if file.endswith('.jpg'):
            os.remove(BASE_DIR + '/img/' + file)


    path= BASE_DIR + '/output/'+filename


    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

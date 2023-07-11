from flask import Flask,render_template,jsonify,request
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import logging

app = Flask(__name__)

@app.route('/',methods=['GET'])

def homepage():
    return render_template('index.html')

@app.route('/review',methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ","")
            url = "https://www.flipkart.com/search?q=" + searchString
            uClient = uReq(url)

            FlipKart_Page = uClient.read()
            uClient.close()

            html_flipkart = bs(FlipKart_Page, "html.parser")
            boxes = html_flipkart.findAll("div", {"class": "_1AtVbE col-12-12"})

            del boxes[0:3]
            box = boxes[0]

            ProductLink = "https://www.flipkart.com" + box.div.div.div.a['href']
            prodRes = requests.get(ProductLink)
            prodRes.encoding='utf-8'
            prod_html = bs(prodRes.text, "html.parser")

            print(prod_html)
            Comm_box = prod_html.find_all('div', {'class': "_16PBlm"})

            file = searchString + ".csv"
            fw = open(file, "w")
            headers = "Product, Customer Name, Rating, Heading, Comment \n"
            fw.write(headers)

            reviews = []
            for box in Comm_box:
                try:

                    name = box.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text

                except:
                    logging.info("name")

                try:

                    rating = box.div.div.div.div.text


                except:
                    rating = 'No Rating'
                    logging.info("rating")

                try:

                    commentHead = box.div.div.div.p.text

                except:
                    commentHead = 'No Comment Heading'
                    logging.info(commentHead)
                try:
                    comtag = box.div.div.find_all('div', {'class': ''})

                    custComment = comtag[0].div.text
                except Exception as e:
                    logging.info(e)

                mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commentHead,
                          "Comment": custComment}
        
                reviews.append(mydict)
            
            logging.info("log my final result {}".format(reviews))
            return render_template('result.html', reviews=reviews[0:(len(reviews)-1)])
        
        except Exception as e:
            logging.info(e)
            return 'something is wrong'


    else:
        return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)
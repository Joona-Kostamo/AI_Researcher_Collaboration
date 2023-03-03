from flask import Flask, request
app = Flask(__name__)

from werkzeug.middleware.proxy_fix import ProxyFix

app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

import os
from sentence_transformers import SentenceTransformer, util
import pandas as pd
from math import isnan
model = SentenceTransformer(os.getcwd())

excel_filename = "Abstract"
abstract_df = pd.read_excel(excel_filename + ".xls")
embeddings = []
with open ("Abstract_embeddings.txt", 'r') as embeddings_file:
    line = embeddings_file.readline()
    while line != "":
        embeddings.append([float(item) for item in line.split(",")[:-1]])
        line = embeddings_file.readline()

def find_n_most_similar(abstract_to_search_embedded, embeddings_to_search, n = 5):
    if n > len(embeddings_to_search) or n <= 0 or n > 100:
        n = min(100, len(embeddings_to_search))
    similarities = []
    for abstract in embeddings_to_search:
        similarities.append(util.cos_sim(abstract_to_search_embedded, abstract))
    indexes = range(len(similarities))
    most_similar_indexes = [index for (similarity,index) in sorted(zip(similarities, indexes), reverse=True, key=lambda pair: pair[0])][0:n]
    return most_similar_indexes

excel_filename = "WoS_All_Most_cited"
papers_df = pd.read_excel(excel_filename + ".xls")

def get_paper_by_index(df, indexes):
    similar_papers_df = df.iloc[indexes]
    return similar_papers_df

@app.route('/')
def index():
    return """<head>
      <meta charset="UTF-8">
      <meta http-equiv="X-UA-Compatible" content="IE=edge">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>COINS Course</title>
    </head>
    <html lang="en" style="background-color:silver" class = "align-item-center">

         <div class="header" style="background-color:violet">
              <h1>COINS Course</h1>
              <p>Tool to search similar papers based on Abstract provided using ML learning models.</p>
         </div>

         <div class="header" style="background-color:yellow">
              <h3>Purpose</h3>
              <p>This API can be used to search for research papers based on an abstract provided based on AI & ML models.<br/></p>
         </div>

        <div class="header" style="background-color:lightgreen">
             <h3>Response</h3>
             <p>Similar papers are provided as a response based on similarity of abstracts.<br/></p>
        </div>

        <div class="header" style="background-color:lightblue">
             <h3>Working</h3>
             <p>The search is performed over a data set of highly cited AI & ML papers fetched from Web of Science. Web of Science: https://clarivate.com/webofsciencegroup/solutions/web-o>             <p>The similarity comparison is performed by a transfer-trained SBERT model. SBERT docs: https://www.sbert.net/<br/></p>
        </div>
        <br/>
    <body>
      <form action="/search_papers" method="GET">
        <label> Write down the abstract to search with in the below textarea:<br/>
          <textarea id="s_abstract" name="s_abstract" minlength="3" maxlength="4000" rows="10" cols="150" required></textarea>
        </label>
        <br/><br/>
        <label> Write down the number of results you want (100 max):<br/>
            <input type="text" id="s_number" name="s_number" minlength="1" maxlength="3" value=3 required>
        </label>
        <br/><br/>                                                                                                                                          <button id="s_button" type="sub> </html>
 <br/><br/>
 <div class="header" style="background-color:black; color: white">                                                                                       <h3> Tips </h3>
     <p>To perform the search directly request subdomain<br/>/search_papers?s_number=&#60;Number_of_papers_you_want&#62&s_abstract=&#60;Abstract_you_want_to_search_with&#62&as_json=&#60;T>                                                                                                                                                     </div>
<div class="header" style="background-color:white; color: black">
   <h3> Example search with Python </h3>
        <p> import requests </p>
             <p> import pandas as pd </p>
                 <p> pd.set_option('display.max_colwidth', None)</p>
                     <p> abstract = "This is an example abstract to be used for the search" </p>
                         <p> parameters = {'s_number': 3, 'as_json': True, 's_abstract': abstract} </p>
                             <p> response = requests.get('http://168.119.239.210/search_papers',params=parameters) </p>
                                 <p> df = pd.read_json(response.url, orient='table') </p>
                                     <p> select_columns = ["Authors", "Article Title", "Publication Year"] </p>
                                         <p> for i in range(df.shape[0]): </p>
                                             <p>  &emsp;print(df.iloc[i][select_columns]) </p>
                                             </div>
                                                                                                                                                     """

@app.route('/search_papers')
def get_papers():
    n_papers = int(request.args.get('s_number'))
    abstract = str(request.args.get('s_abstract'))
    as_json = request.args.get('as_json', default="False")
    abstract_to_search_embedded = model.encode([abstract])
    indexes = find_n_most_similar(abstract_to_search_embedded, embeddings, n=n_papers)
    found_papers_df = get_paper_by_index(papers_df, indexes)
    if as_json == "False":
        found_papers_df = found_papers_df.loc[:,["Authors", "Article Title", "Publication Year", "Publisher", "Volume", "Issue", "Abstract"]]
        out_string = ""
        paper_counter = 1
        for _, row in found_papers_df.iterrows():
            out_string += str(paper_counter) + ". most similar paper based on abstract:<br/>"
            for label, item in row.items():
                if label == "Publication Year" and type(item) == float and not isnan(item):
                    item = int(item)
                out_string += str(label) + ": " + str(item) + "<br/>"
                print(out_string)
            out_string += "<br/><br/>"
            paper_counter += 1
        return out_string

    return found_papers_df.to_json(indent=4, orient='table')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
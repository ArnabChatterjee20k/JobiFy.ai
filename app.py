from flask import Flask,render_template,request,redirect,url_for
from generate_content import get_files , generate_content
from dotenv import load_dotenv
load_dotenv(".env")
app = Flask(__name__,template_folder=".",static_folder="./contents")
app.config["TEMPLATES_AUTO_RELOAD"] = True
@app.get("/")
def main():
    return render_template("index.html")

@app.post("/generate")
def generate():
    url = request.form.get("url")    
    company_name = request.form.get("company_name")    

    generate_content(company_name,url)

    return redirect(url_for("static",filename=f"{company_name}.txt"))

@app.get("/previous")
def see_previous():
    return render_template("previous.html",content=get_files())

# @app.get("/<path:path>")
# def send_file(path):
#     return send_file(path)
app.run(debug=True)
import openai 
import json
from flask import Flask, render_template, request
from dotenv import dotenv_values

config = dotenv_values('.env')
openai.api_key = config['OPENAI_API_KEY']

app = Flask(__name__, 
    template_folder='templates',
    static_url_path='',
    static_folder='static'
)

def get_colors(msg):
    prompt = f"""You are a color palette generating assistant that responds to text prompts for color palettes. You should generate color palettes that fit the theme,mood, or instructions in the prompt. The palettes should be between 2 and 8 colors.

    Q: Convert the following verbal description of a color palette into a list of colors: The Indian Flag
    A: ["#FF9933", "#FFFFFF", "#138808",#000080"]

    Q: Convert the following verbal description of a color palette into a list of colors: The Beach
    A: ["#F9D199", "#FDD8B5", "#F6E3D4", "#BBDBF7", "#92C4EE", "#64ABE3"]

    Q: Convert the following verbal description of a color palette into a list of colors: The Mediterranean Sea
    A: ["#006699", "#66CCCC", "#F0E68C", "#008000", "#F08080"]


    Desired Format: a JSON array of hexadecimal color codes
    Q: Convert the following verbal description of a color palette into a list of colors: {msg}
    A:
    """

    response = openai.Completion.create( model="text-davinci-003",
                        prompt=prompt,
                        max_tokens=200,)
    colors = json.loads(response["choices"][0]["text"])
    return colors


@app.route("/palette", methods=["POST"])
def prompt_to_palette():
    app.logger.info("HIT THE POST REQUEST ROUTE")
    query = request.form.get("query")
    colors = get_colors(query)
    return {"colors": colors }
   

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

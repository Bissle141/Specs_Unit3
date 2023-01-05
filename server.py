from flask import Flask, render_template, redirect, flash, request
import jinja2
import melons

app = Flask(__name__)
app.jinja_env.undefined = jinja2.StrictUndefined  # for debugging purposes

@app.route("/")
def homepage():
   return render_template("base.html")

@app.route("/melons")
def all_melons():
   """Return a page listing all the melons available for purchase."""

   melon_list = melons.get_all()
   return render_template("all_melons.html", melon_list=melon_list)

@app.route("/melon/<melon_id>")
def melon_details(melon_id):
   """Return a page showing all info about a melon. Also, provide a button to buy that melon."""

   detailed_melon = melons.melon_look_up(melon_id)
   
   return render_template("melon_details.html", melon=detailed_melon)

@app.route("/add_to_cart/<melon_id>")
def add_to_cart(melon_id):
   """Add a melon to the shopping cart."""

   return f"{melon_id} added to cart"

@app.route("/cart")
def show_shopping_cart():
   """Display contents of shopping cart."""

   return render_template("cart.html")

if __name__ == "__main__":
   app.env = "development"
   app.run(debug = True, port = 8000, host = "localhost")
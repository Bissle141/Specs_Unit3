from flask import Flask, render_template, redirect, flash, request, session, url_for
from melons import get_all, melon_look_up
from forms import LoginForm, AddQuanMelonCartForm
import customers
import jinja2
import melons
import pprint
from customers import get_by_username


app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = jinja2.StrictUndefined  # for debugging purposes

@app.route("/")
def homepage():
   return render_template("base.html")

@app.route("/login", methods=["GET", "POST"])
def login():
   """Log user into site."""
   
   form = LoginForm(request.form)
   
   if form.validate_on_submit():
      username = form.username.data
      password = form.password.data
      
      
      if get_by_username(username):
         if get_by_username(username)['password'] == password:
            session['username'] = username
            flash("Login successful")
            return redirect(url_for('all_melons'))
         else:
            flash('Invalid password.')
      else:
         flash('Invalids username.')
      
   return render_template("login.html", form=form)

@app.route('/logout')
def logout():
   del session['username']
   session["cart"] = {}
   
   flash("Logged out.")
   
   return redirect(url_for('homepage'))

@app.route("/melons")
def all_melons():
   """Return a page listing all the melons available for purchase."""

   melon_list = melons.get_all()
   return render_template("all_melons.html", melon_list=melon_list)


@app.route("/melon/<melon_id>", methods=["GET", "POST"])
def melon_details(melon_id):
   """Return a page showing all info about a melon. Also, provide a button to buy that melon."""
   form = AddQuanMelonCartForm(request.form)
   
   if form.is_submitted():
      if 'username' not in session:
         flash("Please login first.")
         return redirect(url_for("login"))
      else:
         quan = form.quantity.data
         return redirect(url_for('add_to_cart', melon_id=melon_id, quantity=quan))

   detailed_melon = melons.melon_look_up(melon_id)
   
   return render_template("melon_details.html", melon=detailed_melon, form=form)

@app.route("/add_to_cart/<melon_id>", methods=["GET", "POST"])
def add_to_cart(melon_id):
   """Add a melon to the shopping cart."""
   
   if 'username' not in session:
      flash("Please login first.")
      return redirect(url_for("login"))
   
   if 'cart' not in session:
      session['cart'] = {}
   
   cart = session['cart']
   
   
   cart[melon_id] = cart.get(melon_id, 0) + int(request.args.get('quantity', 1))
   
   session.modified = True
   flash("Melon successfully added to cart.")
   
   return redirect(url_for('all_melons'))

@app.route("/cart")
def show_shopping_cart():
   """Display contents of shopping cart."""
   
   if 'username' not in session:
      flash("Please login first.")
      return redirect(url_for("login"))
   
   
   # Get cart dict from session (or an empty one if none exists yet)
   cart = session.get("cart", {})

   order_total = 0
   cart_melons = []

   for melon_id, quantity in cart.items():
      melon = melons.melon_look_up(melon_id)
      total_cost = quantity * melon.price
      order_total += total_cost
      
      melon.quantity = quantity
      melon.total_cost = total_cost
      
      cart_melons.append(melon)

   return render_template("cart.html", cart_melons=cart_melons, order_total=order_total)

@app.route("/empty-cart")
def empty_cart():
   session["cart"] = {}

   return redirect("/cart")

@app.errorhandler(404)
def error_404(e):
   return render_template('error_404.html')

if __name__ == "__main__":
   app.env = "development"
   app.run(debug = True, port = 8000, host = "localhost")
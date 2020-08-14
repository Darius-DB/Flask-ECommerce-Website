from flask import request, render_template, Blueprint
from flaskecommerce.models import Item
from flaskecommerce import app




@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    items = Item.query.order_by(Item.id.desc()).paginate(page=page, per_page=4)
    return render_template('index.html', items=items)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact-us.html')


@app.route('/thanks')
def thanks():
    return render_template('thank.html')

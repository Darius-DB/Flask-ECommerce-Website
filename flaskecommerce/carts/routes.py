from flask import Blueprint, request, session, redirect, url_for, render_template
from flaskecommerce.models import Item
from flaskecommerce.carts.utils import MagerDicts
from flask_login import login_required
from flaskecommerce import app


@app.route('/addcart', methods=['POST'])
@login_required
def AddCart():
    try:
        item_id = request.form.get('item_id')
        quantity = int(request.form.get('quantity'))
        size = request.form.get('size')
        item = Item.query.filter_by(id=item_id).first()

        if request.method == "POST":
            DictItems = {item_id: {'name': item.item_title, 'price': float(
                item.item_price), 'quantity': quantity, 'image': item.image_1}}
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if item_id in session['Shoppingcart']:
                    for key, item in session['Shoppingcart'].items():
                        if int(key) == int(item_id):
                            session.modified = True
                            item['quantity'] += 1
                else:
                    session['Shoppingcart'] = MagerDicts(
                        session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)
            else:
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)

    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)


@app.route('/carts')
@login_required
def getCart():
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    subtotal = 0
    grandtotal = 0
    for key, item in session['Shoppingcart'].items():
        #discount = (item['discount']/100) * float(item['price'])
        subtotal += float(item['price']) * int(item['quantity'])
        #subtotal -= discount
        tax = ("%.2f" % (.06 * float(subtotal)))
        grandtotal = float("%.2f" % (1.06 * subtotal))
    return render_template('cart.html', tax=tax, grandtotal=grandtotal)


@app.route('/deleteitem/<int:id>')
@login_required
def deleteitem(id):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
                return redirect(url_for('getCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))


@app.route('/clearcart')
@login_required
def clearcart():
    try:
        session.pop('Shoppingcart', None)
        return redirect(url_for('home'))
    except Exception as e:
        print(e)

import os
import stripe
import pdfkit
import secrets
from flask import (Blueprint, request, redirect, url_for, flash, render_template,
                    session, make_response)
from flaskecommerce.orders.utils import updateshoppingcart
from flaskecommerce.models import CustomerOrder, User
from flask_login import current_user, login_required
from flaskecommerce import db, app



publishable_key = os.environ.get('STRIPE_PUB_KEY')
stripe.api_key = os.environ.get('STRIPE_API_KEY')


@app.route('/payment', methods=['POST'])
def payment():
    invoice = request.form.get('invoice')
    amount = request.form.get('amount')
    customer = stripe.Customer.create(
        email=request.form['stripeEmail'],
        source=request.form['stripeToken'],
    )
    charge = stripe.Charge.create(
        customer=customer.id,
        description='Myshop',
        amount=amount,
        currency='usd',
    )
    orders = CustomerOrder.query.filter_by(
        customer_id=current_user.id, invoice=invoice).order_by(CustomerOrder.id.desc()).first()
    orders.status = 'Paid'
    db.session.commit()
    return redirect(url_for('thanks'))


@app.route('/getorder')
@login_required
def get_order():
    if current_user.is_authenticated:
        user_id = current_user.id
        invoice = secrets.token_hex(5)
        updateshoppingcart
        try:
            order = CustomerOrder(
                invoice=invoice, customer_id=user_id, orders=session['Shoppingcart'])
            db.session.add(order)
            db.session.commit()
            session.pop('Shoppingcart')
            flash('Your order has been sent successfully', 'success')
            return redirect(url_for('orders', invoice=invoice))
        except Exception as e:
            print(e)
            flash('Something went wrong while geting your order', 'danger')
            return redirect(url_for('getCart'))


@app.route('/orders/<invoice>')
@login_required
def orders(invoice):
    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        user_id = current_user.id
        user = User.query.filter_by(id=user_id).first()
        orders = CustomerOrder.query.filter_by(
            customer_id=user_id, invoice=invoice).order_by(CustomerOrder.id.desc()).first()
        for _key, item in orders.orders.items():
            #discount = (item['discount']/100) * float(item['price'])
            subTotal += float(item['price']) * int(item['quantity'])
            #subTotal -= discount
            tax = ("%.2f" % (.06 * float(subTotal)))
            grandTotal = ("%.2f" % (1.06 * float(subTotal)))

    else:
        return redirect(url_for('login'))
    return render_template('checkout.html', invoice=invoice, tax=tax, subTotal=subTotal, grandTotal=grandTotal, user=user, orders=orders)


@app.route('/get_pdf/<invoice>', methods=['POST'])
@login_required
def get_pdf(invoice):
    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        user_id = current_user.id
        if request.method == "POST":
            user = User.query.filter_by(id=user_id).first()
            orders = CustomerOrder.query.filter_by(
                customer_id=user_id, invoice=invoice).order_by(CustomerOrder.id.desc()).first()
            for _key, item in orders.orders.items():
                #discount = (item['discount']/100) * float(item['price'])
                subTotal += float(item['price']) * int(item['quantity'])
                #subTotal -= discount
                tax = ("%.2f" % (.06 * float(subTotal)))
                grandTotal = float("%.2f" % (1.06 * subTotal))

            rendered = render_template(
                'pdf.html', invoice=invoice, tax=tax, grandTotal=grandTotal, user=user, orders=orders)
            pdf = pdfkit.from_string(rendered, False)
            response = make_response(pdf)
            response.headers['content-Type'] = 'orderslication/pdf'
            response.headers['content-Disposition'] = 'inline; filename=' + \
                invoice+'.pdf'
            return response
    return request(url_for('orders'))

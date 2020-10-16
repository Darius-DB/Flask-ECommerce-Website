import secrets
from flask import Blueprint, render_template, abort, redirect, url_for, request, flash, current_app
from flaskecommerce.models import User, Item
from flaskecommerce.products.forms import AddItemForm
from flaskecommerce import photos, db, app
from flask_login import current_user, login_required


@app.route('/item/new', methods=['GET', 'item'])
@login_required
def new_item():
    admin = User.query.get(1)
    form = AddItemForm()
    if form.validate_on_submit() and current_user.username == admin.username and 'picture_1' in request.files and 'picture_2' in request.files and 'picture_3' in request.files:
        image_1 = photos.save(request.files.get(
            'picture_1'), name=secrets.token_hex(10) + ".")
        image_2 = photos.save(request.files.get(
            'picture_2'), name=secrets.token_hex(10) + ".")
        image_3 = photos.save(request.files.get(
            'picture_3'), name=secrets.token_hex(10) + ".")
        

        item = Item(
            category=form.category.data,
            sub_category=form.sub_category.data,
            item_title=form.title.data,
            item_price=form.price.data,
            stock=form.stock.data,
            item_description=form.description.data,
            item_size=form.size.data,
            image_1=image_1,
            image_2=image_2,
            image_3=image_3
        )

        db.session.add(item)
        db.session.commit()
        flash('The item was added!', 'success')
        return redirect(url_for('home'))
    elif current_user.username != admin.username:
        abort(403)
    return render_template('add_item.html', form=form)


@app.route('/item/<int:id>', methods=['GET', 'item'])
def item(id):
    item = Item.query.get_or_404(id)
    return render_template('shop-detail.html', item=item)


@app.route('/item/<int:id>/update', methods=['GET', 'item'])
@login_required
def update_item(id):
    item = Item.query.get_or_404(id)
    admin = User.query.get(1)
    form = AddItemForm()
    if current_user.username != admin.username:
        abort(403)

    if form.validate_on_submit() and current_user.username == admin.username:
        if request.files.get('image_1'):
            try:
                
                item.image_1 = photos.save(request.files.get(
                    'image_1'), name=secrets.token_hex(10) + ".")
            except:
                item.image_1 = photos.save(request.files.get(
                    'image_1'), name=secrets.token_hex(10) + ".")

        if request.files.get('image_2'):
            try:

                item.image_2 = photos.save(request.files.get(
                    'image_2'), name=secrets.token_hex(10) + ".")
            except:
                item.image_2 = photos.save(request.files.get(
                    'image_2'), name=secrets.token_hex(10) + ".")

        if request.files.get('image_3'):
            try:

                item.image_3 = photos.save(request.files.get(
                    'image_3'), name=secrets.token_hex(10) + ".")
            except:
                item.image_3 = photos.save(request.files.get(
                    'image_3'), name=secrets.token_hex(10) + ".")

        item.category = form.category.data
        item.sub_category = form.sub_category.data
        item.item_title = form.title.data
        item.item_price = form.price.data
        item.stock = form.stock.data
        item.item_description = form.description.data
        item.item_size = form.size.data

        db.session.commit()
        flash('Item has been updated', 'success')
        return redirect(url_for('item', id=item.id))

    elif request.method == 'GET':
        form.category.data = item.category
        form.sub_category.data = item.sub_category
        form.title.data = item.item_title
        form.price.data = item.item_price
        form.stock.data = item.stock
        form.description.data = item.item_description
        form.size.data = item.item_size

    return render_template('add_item.html', form=form, item=item, admin=admin)


@app.route('/item/<int:id>/delete', methods=['GET', 'item'])
@login_required
def delete_item(id):
    item = Item.query.get_or_404(id)
    admin = User.query.get(1)
    form = AddItemForm()
    if current_user.username != admin.username:
        abort(403)
    db.session.delete(item)
    db.session.commit()
    flash('Item has been deleted!', 'success')
    return redirect(url_for('home'))

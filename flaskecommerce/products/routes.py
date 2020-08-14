import secrets
from flask import Blueprint, render_template, abort, redirect, url_for, request, flash
from flaskecommerce.models import User, Item
from flaskecommerce.products.forms import AddItemForm
from flaskecommerce import photos, db, app
from flask_login import current_user, login_required


@app.route('/item/new', methods=['GET', 'POST'])
@login_required
def new_item():
    admin = User.query.get(1)
    form = AddItemForm()
    if form.validate_on_submit() and current_user.username == admin.username:
        if form.picture_1.data:
            picture_1 = photos.save(
                form.picture_1.data, name=secrets.token_hex(10) + ".")
            item = Item(image_1=picture_1)
        if form.picture_2.data:
            picture_2 = photos.save(
                form.picture_2.data, name=secrets.token_hex(10) + ".")
            item = Item(image_2=picture_2)
        if form.picture_3.data:
            picture_3 = photos.save(
                form.picture_3.data, name=secrets.token_hex(10) + ".")
            item = Item(image_3=picture_3)

        item = Item(
            category=form.category.data,
            sub_category=form.sub_category.data,
            item_title=form.title.data,
            item_price=form.price.data,
            stock=form.stock.data,
            item_description=form.description.data,
            item_size=form.size.data
        )

        db.session.add(item)
        db.session.commit()
        flash('The item was added!', 'success')
        return redirect(url_for('home'))
    elif current_user.username != admin.username:
        abort(403)
    return render_template('add_item.html', form=form)


@app.route('/item/<int:id>', methods=['GET', 'POST'])
def item(id):
    item = Item.query.get_or_404(id)
    return render_template('shop-detail.html', item=item)


@app.route('/item/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_item(id):
    item = Item.query.get_or_404(id)
    admin = User.query.get(1)
    form = AddItemForm()
    if current_user.username != admin.username:
        abort(403)

    if form.validate_on_submit() and current_user.username == admin.username:
        if form.picture_1.data:
            picture_1 = photos.save(
                form.picture_1.data, name=secrets.token_hex(10) + ".")
            item.image_1 = picture_1
        if form.picture_2.data:
            picture_2 = photos.save(
                form.picture_2.data, name=secrets.token_hex(10) + ".")
            item.image_2 = picture_2
        if form.picture_3.data:
            picture_3 = photos.save(
                form.picture_3.data, name=secrets.token_hex(10) + ".")
            item.image_3 = picture_3

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


@app.route('/item/<int:id>/delete', methods=['GET', 'POST'])
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

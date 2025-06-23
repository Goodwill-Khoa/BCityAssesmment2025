from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db, Client, Contact
from models.client import Client
from models.contact import Contact
from models.client_contact import ClientContact
from models.user import User  # Add this import for the User model
from forms.auth_forms import UserForm  # Add this import, adjust the module if needed

admin_bp = Blueprint('admin', __name__)

# Admin routes for managing clients, contacts, and users
MODEL_MAP = {
    "client": Client,
    "contact": Contact,
}

@admin_bp.route('/admin/update_database', methods=['GET', 'POST'])
@login_required
def update_database():
    db_choice = request.args.get('db')
    records = []
    columns = []
    model = None

    if db_choice == 'contact':
        model = Contact
    elif db_choice == 'client':
        model = Client

    if model:
        records = model.query.order_by(model.id.asc()).all()
        if records:
            columns = [col for col in vars(records[0]).keys() if not col.startswith('_')]

    return render_template(
        'update_database.html',
        db_choice=db_choice,
        records=records,
        columns=columns,
    )

@admin_bp.route('/admin/update_delete_record/<model_name>/<int:record_id>', methods=['POST'])
@login_required
def update_delete_record(model_name, record_id):
    model = MODEL_MAP.get(model_name)
    if not model:
        flash("Invalid table.")
        return redirect(url_for('admin.update_database', db=model_name))

    record = model.query.get(record_id)
    if not record:
        flash("Record not found.")
        return redirect(url_for('admin.update_database', db=model_name))

    action = request.form.get('action')
    if action == 'delete':
        if model_name == 'contact':
            ClientContact.query.filter_by(contact_id=record_id).delete()
        else:
            ClientContact.query.filter_by(client_id=record_id).delete()
        db.session.delete(record)
        db.session.commit()
        flash("Deleted.")
    elif action == 'update':
        for col in request.form:
            if hasattr(record, col) and col not in ('id', 'action'):
                setattr(record, col, request.form[col])
        db.session.commit()
        flash("Updated.")
    return redirect(url_for('admin.update_database', db=model_name))

@admin_bp.route('/admin')
@login_required
def admin_dashboard():
    return render_template('admin_dashboard.html')

@admin_bp.route('/admin/user_manage', methods=['GET', 'POST'])
@login_required
def user_manage():
    users = User.query.order_by(User.id.asc()).all()
    form = UserForm()
    # Add user management logic here as previously discussed
    return render_template('user_manage.html', users=users, form=form)

@admin_bp.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        if form.password.data:
            user.set_password(form.password.data)
        user.is_superuser = form.is_superuser.data
        db.session.commit()
        flash('User updated successfully.')
        return redirect(url_for('admin.user_manage'))
    return render_template('user_manage.html', users=User.query.all(), form=form)

@admin_bp.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully.')
    return redirect(url_for('admin.user_manage'))

@admin_bp.route('/admin/confirm_delete/<model_name>/<int:record_id>', methods=['GET', 'POST'])
@login_required
def confirm_delete(model_name, record_id):
    model = MODEL_MAP.get(model_name)
    record = model.query.get_or_404(record_id) if model else None

    if not record:
        flash("Record not found.")
        return redirect(url_for('admin.update_database', db=model_name))

    if request.method == "POST":
        # Actually delete the record
        if model_name == 'contact':
            ClientContact.query.filter_by(contact_id=record_id).delete()
        else:
            ClientContact.query.filter_by(client_id=record_id).delete()
        db.session.delete(record)
        db.session.commit()
        flash(f"{model_name.capitalize()} deleted.")
        return redirect(url_for('admin.update_database', db=model_name))

    # GET: Show confirmation
    return render_template(
        "confirm_delete.html",
        type=model_name.capitalize(),
        obj=record
    )
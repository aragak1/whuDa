# _*_ coding:utf8 _*_
from whuDa import app
from flask import render_template


@app.route('/admin')
def admin_index():
    return render_template('admin/index.html')


@app.route('/admin/manage_admin')
def admin_blank():
    return render_template('admin/manage_admin.html.html')


@app.route('/admin/manage_user')
def admin_buttons():
    return render_template('admin/manage_user.html')


@app.route('/admin/flot')
def admin_flot():
    return render_template('admin/flot.html')


@app.route('/admin/forms')
def admin_forms():
    return render_template('admin/forms.html')


@app.route('/admin/grid')
def admin_grid():
    return render_template('admin/grid.html')


@app.route('/admin/icons')
def admin_icons():
    return render_template('admin/icons.html')


# login页面可能要找重新找模板写
@app.route('/admin/login')
def admin_login():
    return render_template('admin/login.html')


@app.route('/admin/morris')
def admin_morris():
    return render_template('admin/morris.html')


@app.route('/admin/notifications')
def admin_notifications():
    return render_template('admin/notifications.html')


@app.route('/admin/panels-wells')
def admin_panels_wells():
    return render_template('admin/panels-wells.html')


@app.route('/admin/tables')
def admin_tables():
    return render_template('admin/tables.html')


@app.route('/admin/typography')
def admin_typography():
    return render_template('admin/typography.html')


@app.route('/admin/topic')
def admin_topic():
    return render_template('admin/topic.html')

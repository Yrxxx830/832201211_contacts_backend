from flask import Flask, jsonify, request, render_template, session
from flask_cors import CORS, cross_origin

from models import db, Contact
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
cors = CORS()
db.init_app(app)

with app.app_context():
    db.create_all()


# 登录功能
@app.route('/login', methods=['POST'])
@cross_origin()
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if username == 'admin' and password == '123456':
        session['logged_in'] = True  # 设置 session 标记用户已登录
        return jsonify({'message': 'Login successful'})
    return jsonify({'message': 'Invalid username or password'}), 401


# 注销功能
@app.route('/logout', methods=['POST'])
@cross_origin()
def logout():
    session.pop('logged_in', None)
    return jsonify({'message': 'Logged out successfully'})


# 增加联系人
@app.route('/contacts/add', methods=['POST'])
@cross_origin()
def add_contact():
    data = request.json
    new_contact = Contact(name=data['name'], phone=data['phone'], email=data.get('email'), address=data.get("address"))
    db.session.add(new_contact)
    db.session.commit()
    return jsonify({'message': 'Contact added successfully'})


# 查询联系人
@app.route('/contacts/list', methods=['GET'])
@cross_origin()
def get_contacts():
    contacts = Contact.query.all()
    return jsonify(
        [{'id': c.id, 'name': c.name, 'phone': c.phone, 'email': c.email, "address": c.address} for c in contacts])


# 联系人信息
@app.route('/contacts/info/<int:id>', methods=['GET'])
@cross_origin()
def contacts_info(id):
    c = Contact.query.filter_by(id=id).first()
    return jsonify({'id': c.id, 'name': c.name, 'phone': c.phone, 'email': c.email, "address": c.address})


# 更新联系人
@app.route('/contacts/edit/<int:id>', methods=["POST"])
@cross_origin()
def update_contact(id):
    data = request.json
    contact = Contact.query.get(id)
    if contact:
        contact.name = data['name']
        contact.phone = data['phone']
        contact.email = data.get('email')
        contact.address = data.get('address')
        db.session.commit()
        return jsonify({'message': 'Contact updated successfully'})
    return jsonify({'message': 'Contact not found'}), 404


# 删除联系人
@app.route('/contacts/delete/<int:id>', methods=['DELETE'])
@cross_origin()
def delete_contact(id):
    contact = Contact.query.get(id)
    if contact:
        db.session.delete(contact)
        db.session.commit()
        return jsonify({'message': 'Contact deleted successfully'})
    return jsonify({'message': 'Contact not found'}), 404


if __name__ == '__main__':
    app.run(debug=True, port=8888, host="0.0.0.0")

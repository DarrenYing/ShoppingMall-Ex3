from flask import Flask, request, redirect, url_for, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import and_

import random
import timeit
import time

import hashlib

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:hitsz1234@127.0.0.1:3306/mall_system?charset=utf8'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_ECHO'] = True  # 显示错误信息
app.config['SQLALCHEMY_RECORD_QUERIES'] = True  # 启用查询记录
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # 追踪数据库修改

app.config['CORS_ORIGIN_ALLOW_ALL'] = True
app.config['CORS_ALLOW_CREDENTIALS'] = True

db = SQLAlchemy(app)

from models import *


# db.drop_all()
# db.create_all()

@app.route('/register', methods=["POST"])
def register():
    username = request.form.get("username")
    pswrd = request.form.get("password")
    pswrd_ck = request.form.get("pswrd_ck")
    authority = request.form.get("authority")
    email = request.form.get("email")
    dic = {"username": username, "password": pswrd}
    print(dic)
    if username == '' or pswrd == '' or email == '':
        return jsonify({'code': 500})
    elif get_account(username):
        return jsonify({'code': 300})
    elif username and pswrd and pswrd == pswrd_ck:
        insert_account(username, pswrd, email, authority)
        return jsonify({'code': 200})
    else:
        return jsonify({'code': 400,
                        'account': dic})

def get_account(username):
    res = User.query.filter(User.username == username).first()
    return res

def insert_account(username, password, email, authority=0):
    # md5 = hashlib.md5()
    # password = password.encode(encoding='utf-8')
    # md5.update(password)
    account = User(username=username, password=password, email=email, role=authority)
    info = UserInfo(username)
    info.user = account
    info.user_create_time = account.user_create_time
    cart = Cart(0)
    cart.user = account
    db.session.add(account)
    db.session.commit()

@app.route('/login', methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    print(username, password)
    md5 = hashlib.md5()

    cur_user = User.query.first()
    if username and password and cur_user:
        res = get_account(username)
        if res:
            print(res.username)
            # print(res.password==password)
            if res.password == password:
                username = username + res.role
                username = username.encode(encoding='utf-8')
                md5.update(username)
                token = md5.hexdigest()
                # login_user(cur_user, username)
                return jsonify({"code": 200, "token": token})
    return jsonify({"code": 400})

@app.route('/')
def hello_world():
    # create_data()

    return 'Hello World!'

@app.route('/product/all', methods=['GET', 'POST'])
def product_all():
    results = db.session.query(Product.product_id, Product.name, Category.name, Product.price, Product.info) \
        .join(Category, Product.category_id == Category.category_id).all()

    print(results)
    ret = []
    for result in results:
        ans = {}
        ans['id'] = result[0]
        ans['pname'] = result[1]
        ans['cname'] = result[2]
        ans['price'] = str(result[3])
        ans['info'] = result[4]
        ret.append(ans)

    return jsonify(ret)

@app.route('/product/item', methods=['GET', 'POST'])
def product_query():
    pname = request.json.get("pname")
    cname = request.json.get("cname")
    minprice = request.json.get("minprice")
    maxprice = request.json.get("maxprice")

    condition = (Product.product_id>0)
    if not pname == "":
        condition = and_(condition, Product.name==pname)
    if not cname == "":
        condition = and_(condition, Category.name==cname)
    if not minprice == "":
        condition = and_(condition, Product.price>=minprice)
    if not maxprice == "":
        condition = and_(condition, Product.price<=maxprice)

    results = db.session.query(Product.product_id, Product.name, Category.name, Product.price, Product.info)\
        .join(Category, Product.category_id==Category.category_id)\
        .filter(condition).all()

    print(results)
    ret = []
    for result in results:
        ans = {}
        ans['id'] = result[0]
        ans['pname'] = result[1]
        ans['cname'] = result[2]
        ans['price'] = str(result[3])
        ans['info'] = result[4]
        ret.append(ans)

    return jsonify(ret)

@app.route('/category/query', methods=['GET', 'POST'])
def category_query():

    results = db.session.query(Category.category_id, Category.name).all()
    print(results)

    ret = []
    for result in results:
        ans = {}
        ans['category_id'] = result[0]
        ans['cname'] = result[1]
        ret.append(ans)

    return jsonify(ret)

@app.route('/product/details', methods=['GET', 'POST'])
def product_details():
    id = request.json.get('id')

    results = db.session.query(Product.name, Category.name, Product.price, Product.info,
                                Category.info, Product.status, Product.image_url, Category.category_id)\
        .join(Category, Product.category_id==Category.category_id)\
        .filter(Product.product_id==id).all()

    print(results)
    dic = {'1':'在售','2':'下架','3':'无货'}
    ans = {}
    for result in results:
        ans['pname'] = result[0]
        ans['cname'] = result[1]
        ans['price'] = str(result[2])
        ans['product_info'] = result[3]
        ans['category_info'] = result[4]
        ans['status'] = dic[result[5]]
        ans['image_url'] = result[6]
        ans['category_id'] = result[7]

    return jsonify(ans)

@app.route('/product/add', methods=['GET', 'POST'])
def product_add():
    pname = request.json.get('pname')
    category_id = request.json.get('category_id')
    info = request.json.get('info')
    price = request.json.get('price')
    image_url = request.json.get('image_url')

    new_product = Product(pname, price, info)
    if not image_url=="":
        new_product.image_url = image_url
    category = Category.query.filter(Category.category_id==category_id).first()
    new_product.category = category

    db.session.add(new_product)
    db.session.commit()

    return jsonify("success!")

@app.route('/category/add', methods=['GET', 'POST'])
def category_add():
    cname = request.json.get('cname')
    info = request.json.get('info')

    new_category = Category(cname, info)

    db.session.add(new_category)
    db.session.commit()

    return jsonify("success!")

@app.route('/product/delete', methods=['GET', 'POST'])
def product_delete():
    product_id = request.json.get("product_id")
    product = Product.query.filter(Product.product_id==product_id).first()

    db.session.delete(product)
    db.session.commit()

    return jsonify("success!")

@app.route('/product/update', methods=['GET', 'POST'])
def product_update():
    product_id = request.json.get("product_id")
    pname = request.json.get("pname")
    category_id = request.json.get("category_id")
    price = request.json.get("price")
    product_info = request.json.get("product_info")
    category_info = request.json.get("category_info")
    image_url = request.json.get("image_url")

    print(image_url)
    print(product_id, pname, category_id, price, product_info, category_info)

    result = Product.query.filter(Product.product_id==product_id).first()
    result2 = Category.query.filter(Category.category_id==category_id).first()

    result.name = pname
    result.price = price
    result.info = product_info
    result.image_url = image_url
    result2.info = category_info
    result.category = result2

    db.session.commit()

    return jsonify("success!")

@app.route('/product/cart', methods=['GET', 'POST'])
def cart_query():
    username = request.json.get('username')
    user_id = db.session.query(User.id).filter(User.username==username).first()[0]
    result1 = db.session.query(Cart.cart_id, Cart.create_time, Cart.total_price)\
        .filter(Cart.user_id==user_id).all()

    print(result1)
    cart_id = str(result1[0][0])

    result2 = db.session.query(Product.name, Category.name, Product.price,
                               cart_product.quantity)\
        .join(Product, cart_product.product_id==Product.product_id)\
        .join(Category, Product.category_id==Category.category_id)\
        .filter(cart_product.cart_id==cart_id).all()


    print(result2)

    ret = []
    for result in result1:
        ans = {}
        ans['cart_id'] = result[0]
        ans['create_time'] = result[1].strftime('%Y-%m-%d %H:%M:%S')
        ans['total_price'] = str(result[2])
        ans['items'] = []
        for item in result2:
            ans2 = {}
            ans2['pname'] = item[0]
            ans2['cname'] = item[1]
            ans2['unit_price'] = str(item[2])
            ans2['quantity'] = item[3]
            ans['items'].append(ans2)
        ans['user_id'] = user_id
        ret.append(ans)

    return jsonify(ret)

@app.route('/product/cart/add', methods=['GET', 'POST'])
def cart_add():
    username = request.json.get('username')
    product_id = request.json.get("product_id")

    user_id = db.session.query(User.id).filter(User.username == username).first()[0]
    cart_id = db.session.query(Cart.cart_id).filter(Cart.user_id==user_id).first()[0]

    record = cart_product.query.filter(cart_product.product_id==product_id).first()
    if record:
        record.quantity += 1
    else:
        new_record = cart_product(cart_id=cart_id, product_id=product_id)
        db.session.add(new_record)

    db.session.commit()

    return jsonify("add success!")

@app.route('/product/cart/update', methods=['GET', 'POST'])
def cart_update():
    pname = request.json.get('pname')
    quantity = request.json.get('quantity')

    product_id = db.session.query(Product.product_id).filter(Product.name == pname).first()

    record = cart_product.query.filter(cart_product.product_id == product_id[0]).first()
    if quantity>0:
        record.quantity = quantity
    else:
        db.session.delete(record)

    db.session.commit()

    return jsonify("add success!")

@app.route('/address/query', methods=['GET', 'POST'])
def address_query():
    user_id = request.json.get('user_id')

    results = db.session.query(Address.province, Address.city, Address.address,
                               Address.name, Address.phone, Address.addr_id)\
        .filter(Address.user_id==user_id).all()

    print(results)
    ret = []
    for result in results:
        ans = {}
        ans['address'] = result[0]+result[1]+result[2]
        ans['rname'] = result[3]
        ans['phone'] = result[4]
        ans['addr_id'] = result[5]
        ret.append(ans)

    return jsonify(ret)

@app.route('/cart/payment', methods=['GET', 'POST'])
def cart_payment():
    user_id = request.json.get('user_id')
    total_price = request.json.get('total_price')
    addr_id = request.json.get('addr_id')
    method = request.json.get('method') #支付方式

    if addr_id == "": #使用新建的地址
        rname = request.json.get('rname')
        phone = request.json.get('phone')
        province = request.json.get('province')
        city = request.json.get('city')
        address = request.json.get('address')

        submit_address = Address(rname, phone, province, city, address)
    else:
        submit_address = Address.query.filter(Address.addr_id==addr_id).first()

    # 创建新订单
    order_no = ''.join(str(i) for i in random.sample(range(1,9), 2))\
        .join(str(i) for i in random.sample(range(0,9), 7))[:13] #随机生成订单号
    carriage = random.randint(0,10) #随机生成运费
    create_time = generateDatetime()
    # other_time = datetime.timedelta(hours=5)
    new_order = MallOrder(order_no, int(total_price), carriage, 3,
                          create_time, create_time, create_time, create_time)
    submit_user = User.query.filter(User.id==user_id).first()
    new_order.user = submit_user
    new_order.address = submit_address
    submit_address.user = submit_user

    #创建新的支付信息
    payment_id = ''.join(str(i) for i in random.sample(range(0, 9), 6))  # 随机生成支付id
    payment_no = ''.join(str(create_time.strftime("%Y%m%d%H%M%S")))\
        .join(str(i) for i in random.sample(range(0,9), 7))[:28]    # 随机生成支付流水号
    print(payment_no)
    new_payment = Payment(payment_id, payment_no, method)
    new_payment.mallOrder = new_order

    #创建订单项
    #根据user_id查cart，一一查出
    cart = db.session.query(Cart.cart_id).filter(Cart.user_id==user_id).first()
    results = db.session.query(Product, cart_product.quantity,
                               Product.price)\
            .join(Product, Product.product_id==cart_product.product_id)\
            .filter(cart_product.cart_id==cart[0]).all()
    print(results)

    for result in results:
        item = OrderItem(result[2], result[1])
        item.product = result[0]
        item.mallOrder = new_order

    db.session.add(new_order)

    #结算完成，清空购物车
    cart_product.query.delete()

    db.session.commit()

    return jsonify("Success")


@app.route('/order/order', methods=['GET', 'POST'])
def order_query():
    username = request.json.get('username')
    user_id = db.session.query(User.id).filter(User.username == username).first()[0]

    results = db.session.query(MallOrder.order_id, MallOrder.order_no, MallOrder.payment,
                               MallOrder.carriage, MallOrder.order_status, MallOrder.send_time,
                               MallOrder.pay_time, MallOrder.finish_time, MallOrder.create_time,
                               Address.province, Address.city, Address.address,
                               Payment.payment_method, Payment.payment_no)\
        .join(Address, MallOrder.addr_id==Address.addr_id)\
        .join(Payment, MallOrder.order_no==Payment.order_no)\
        .filter(MallOrder.user_id==user_id)\
        .order_by(MallOrder.order_id).all()

    print(results)
    dic = {'0':'已取消', '1':'未付款', '2':'已付款', '3':'交易完成'}
    ret = []
    for result in results:
        ans = {}
        ans['order_id'] = result[0]
        ans['order_no'] = result[1]
        ans['payment'] = str(result[2])
        ans['carriage'] = str(result[3])
        ans['status'] = dic[result[4]]
        ans['send_time'] = result[5].strftime('%Y %m %d %H:%M:%S')
        ans['pay_time'] = result[6].strftime('%Y %m %d %H:%M:%S')
        ans['finish_time'] = result[7].strftime('%Y %m %d %H:%M:%S')
        ans['create_time'] = result[8].strftime('%Y %m %d %H:%M:%S')
        ans['addr'] = result[9]+result[10]+result[11] #地址拼接
        ans['payment_method'] = result[12]
        ans['payment_no'] = result[13]
        print(ans)
        ret.append(ans)

    return jsonify(ret)

@app.route('/order/details', methods=['GET', 'POST'])
def order_details():
    order_no = request.json.get('id')

    results = db.session.query(Product.name, Category.name, OrderItem.unit_price,
                               OrderItem.quantity, OrderItem.total_price)\
        .join(Product, OrderItem.product_id==Product.product_id)\
        .join(Category, Product.category_id==Category.category_id)\
        .filter(OrderItem.order_no==order_no).all()

    print(results)
    ret = []
    for result in results:
        ans = {}
        ans['pname'] = result[0]
        ans['cname'] = result[1]
        ans['unit_price'] = str(result[2])
        ans['quantity'] = str(result[3])
        ans['total_price'] = str(result[4])
        ret.append(ans)
    return jsonify(ret)

@app.route('/authority/query', methods=['GET', 'POST'])
def authority_query():
    username = request.json.get('username')
    authority = db.session.query(User.role).filter(User.username==username).first()[0]
    # dic = {'0': 'true', '1': 'false'}
    if authority == '2': #普通用户
        authority = 0
    else:
        authority = 1
    return jsonify(authority)

@app.route('/user/userinfo', methods=['GET', 'POST'])
def userinfo_query():
    username = request.json.get('username')
    user_id = db.session.query(User.id).filter(User.username == username).first()[0]

    results = db.session.query(UserInfo.username, UserInfo.gender, UserInfo.birthday,
                               UserInfo.profession, UserInfo.keyword,
                               UserInfo.user_create_time)\
        .filter(UserInfo.user_id==user_id).all()

    print(results)
    ans = {}
    for result in results:
        ans['username'] = result[0]
        ans['gender'] = result[1]
        if not result[2] == None:
            ans['birthday'] = result[2].strftime('%Y-%m-%d')
        else:
            ans['birthday'] = ''
        ans['profession'] = result[3]
        ans['key_word'] = []
        for val in result[4].split(','):
            ans['key_word'].append(val)
        ans['create_time'] = result[5].strftime('%Y-%m-%d')
        ans['user_id'] = user_id
        print(ans)
    return jsonify(ans)

@app.route('/user/userinfo/update', methods=['GET', 'POST'])
def userinfo_update():
    user_id = request.json.get('user_id')
    username = request.json.get('username')
    gender = request.json.get('gender')
    birthday = request.json.get('birthday')
    profession = request.json.get('profession')
    keyword = request.json.get('key_word')
    keyword = keyword.replace("，", ",")
    print(keyword)

    result = UserInfo.query.filter(UserInfo.user_id == user_id).first()

    result.username = username
    result.gender = gender
    result.birthday = birthday
    result.profession = profession
    result.keyword = keyword

    db.session.commit()
    return jsonify('update success')

@app.route('/user/password/update', methods=['GET', 'POST'])
def password_update():
    oldpassword = request.json.get('oldpassword')
    newpassword = request.json.get('newpassword')
    newpasswordck = request.json.get('newpasswordck')
    cur_user = request.json.get('username')
    if cur_user and oldpassword and newpassword and newpasswordck:
        if get_account(cur_user).password == oldpassword:
            if newpassword == newpasswordck:
                change_password(username=cur_user, newpassword=newpassword)
                return {'code': 200}
            else:
                return {'code': 300}
        else:
            return {'code': 301}
    else:
        return {'code': 400}

def change_password(username, newpassword):
    try:
        User.query.filter_by(username=username).update({User.password: newpassword})
        db.session.commit()
    except Exception as e:
        # 加入数据库commit提交失败，必须回滚！！！
        db.session.rollback()
        raise e

@app.route('/user/manage', methods=['GET', 'POST'])
def user_manage():
    results = db.session.query(User.id, User.username, User.role, User.user_create_time).all()

    print(results)
    dic = {'0': '超级用户', '1': '管理员', '2': '普通用户', '3':'已禁用'}
    ret = []
    for result in results:
        if result[2] == '0':
            continue
        ans = {}
        ans['user_id'] = result[0]
        ans['username'] = result[1]
        ans['authority'] = dic[result[2]]
        ans['create_time'] = result[3].strftime('%Y-%m-%d')
        state = 1 if result[2]=='3' else 0
        ans['state'] = state
        ret.append(ans)

    return jsonify(ret)


@app.route('/user/query', methods=['GET', 'POST'])
def user_query():
    username = request.json.get('username')

    results = db.session.query(User.id, User.username,
                               User.role, User.user_create_time)\
        .filter(User.username==username).first()

    dic = {'0': '超级用户', '1': '管理员', '2': '普通用户', '3':'已禁用'}
    ret = []
    for result in results:
        if result[2] == '0':
            continue
        ans = {}
        ans['user_id'] = result[0]
        ans['username'] = result[1]
        ans['authority'] = dic[result[2]]
        ans['create_time'] = result[3].strftime('%Y-%m-%d')
        ret.append(ans)

    return jsonify(ret)

@app.route('/user/forbidden', methods=['GET', 'POST'])
def user_forbidden():
    user_id = request.json.get('user_id')

    user = User.query.filter(User.id==user_id).first()
    if user.role == '3':
        user.role = '2'
    else:
        user.role = '3' #管理员被禁用后再解禁，也是普通用户。

    return jsonify("Change Success!")

@app.route('/user/authority/update', methods=['GET', 'POST'])
def authority_update():
    user_id = request.json.get('user_id')
    radio = request.json.get('radio')

    user = User.query.filter(User.id==user_id).first()
    if not user.role == '3':
        if radio=='1':
            user.role = 1
        elif radio=='2':
            user.role = 2
    else:
        return jsonify({"code": 400})

    return jsonify({"code": 200})

def create_data():
    # 创建用户
    # user1 = User("碎竹", "123456")
    # user2 = User("班长", "123456")

    # 创建商品
    p1 = Product('iphone 12', 8000)
    p2 = Product('v30 pro', 4000)
    p3 = Product('零食大礼包', 100)
    p4 = Product('滚筒洗衣机', 5600)

    #创建商品类别
    c1 = Category('1001', '家用电器')
    c2 = Category('1002', '食品')
    c3 = Category('1003', '电子产品')

    p1.category = c3
    p2.category = c3
    p3.category = c2
    p4.category = c1

    db.session.add(c1)
    db.session.add(c2)
    db.session.add(c3)
    db.session.commit()

def create_data2():
    user = User('root', '123456', 0)
    userinfo = UserInfo('root', '男')

    addr1 = Address('收货人1', '18688888888', '浙江省', '宁波市', '江北区湖心村31号', '315031')
    addr2 = Address('收货人2', '15124306666', '浙江省', '杭州市', '西湖灵隐寺大门口', '310000')

    order1 = MallOrder('1491753014256', 12000, 0, 3,
                       '2017-04-09 23:50:14', '2017-04-08 11:20:14',
                       '2017-04-10 12:50:10', '2017-04-08 11:20:00')
    order2 = MallOrder('1491830695216', 5800, 10)
    order3 = MallOrder('1492091141269', 10000, 0)

    item11 = OrderItem(8000, 1)
    item12 = OrderItem(4000, 1)
    item21 = OrderItem(5600, 1)
    item22 = OrderItem(100, 2)
    item31 = OrderItem(5600, 1)
    item32 = OrderItem(4000, 1)
    item33 = OrderItem(100, 4)

    pay1 = Payment('000001', '2017040921001004300200116250')
    pay2 = Payment('000002', '2019011721001004300208792341')
    pay3 = Payment('000003', '2019011721001004300209125752')

    userinfo.user = user

    addr1.user = user
    addr2.user = user

    order1.user = user
    order2.user = user
    order3.user = user

    order1.address = addr1
    order2.address = addr1
    order3.address = addr2

    item11.mallOrder = order1
    item12.mallOrder = order1
    item21.mallOrder = order2
    item22.mallOrder = order2
    item31.mallOrder = order3
    item32.mallOrder = order3
    item33.mallOrder = order3

    pay1.mallOrder = order1
    pay2.mallOrder = order2
    pay3.mallOrder = order3

    db.session.add(order1)
    db.session.add(order2)
    db.session.add(order3)
    db.session.commit()




# 该函数随机生成未来一个月内的日期
def generateDatetime():
    dateTime_s = time.time()  # 获取当前时间戳
    dateTime_s = datetime.datetime.fromtimestamp(dateTime_s)  # 将时间戳转换为日期
    # print(dateTime_s)
    str_p = datetime.datetime.strftime(dateTime_s, '%Y-%m-%d %H:%M:%S')  # 将日期转换为字符串
    # print(str_p)

    # 当前日期加一个月
    month = datetime.timedelta(days=30)
    dateTime_end = dateTime_s + month
    # print(dateTime_end)
    dateTime_end = datetime.datetime.strftime(dateTime_end, '%Y-%m-%d %H:%M:%S')  # 将日期转换为字符串
    # print(dateTime_end)

    # 将字符串转换为时间戳
    dateTime_s_stamp = time.mktime(time.strptime(str_p, '%Y-%m-%d %H:%M:%S'))
    # print(dateTime_s_stamp)

    dateTime_e_stamp = time.mktime(time.strptime(dateTime_end, '%Y-%m-%d %H:%M:%S'))
    # print(dateTime_e_stamp)

    t = random.randint(dateTime_s_stamp, dateTime_e_stamp)
    date_touple = time.localtime(t)  # 将时间戳生成时间元组
    date = time.strftime("%Y-%m-%d %H:%M:%S", date_touple)  # 将时间元组转成格式化字符串（1976-05-21）
    date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    # print(date)
    return date


if __name__ == '__main__':
    app.run()

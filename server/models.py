from app import db
import datetime

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    # userinfo_id = db.Column(db.String(6))
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(30))
    role = db.Column(db.String(1), nullable=False) #权限 0-超级用户 1-管理员 2-普通用户 3-封号
    user_create_time = db.Column(db.DateTime)

    receiver_addr = db.relationship('Address', backref='user')
    order = db.relationship('MallOrder', backref='user')
    cart = db.relationship('Cart', backref='user')

    userinfo = db.relationship('UserInfo', backref='user', uselist=False) #1对1

    def __init__(self, username, password, email=None, role=2, create_time=datetime.datetime.now()):
        self.username = username
        self.password = password
        self.email = email
        self.role = role
        self.user_create_time = create_time


class UserInfo(db.Model):
    __tablename__ = "userinfo"
    userinfo_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    username = db.Column(db.String(20), unique=True)
    gender = db.Column(db.String(6))
    birthday = db.Column(db.DateTime)
    profession = db.Column(db.String(20))
    keyword = db.Column(db.String(50))
    user_create_time = db.Column(db.DateTime)

    def __init__(self, username, gender='', birthday=None, profession='', keyword='', create_time=None):
        self.username = username
        self.gender = gender
        self.birthday = birthday
        self.profession = profession
        self.keyword = keyword
        self.user_create_time = create_time

class Address(db.Model):
    __tablename__ = "address"
    addr_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    name = db.Column(db.String(20))
    phone = db.Column(db.String(11))
    province = db.Column(db.String(10))
    city = db.Column(db.String(10))
    address = db.Column(db.String(200))
    zipcode = db.Column(db.String(6))

    order = db.relationship('MallOrder', backref='address')

    def __init__(self, name, phone, province, city, address, zipcode=None):
        self.name = name
        self.phone = phone
        self.province = province
        self.city = city
        self.address = address
        self.zipcode = zipcode

# table_cart_product = db.Table('association',
#                 db.Column('cart_id', db.String(6), db.ForeignKey('cart.cart_id')),
#                 db.Column('product_id', db.Integer, db.ForeignKey('product.product_id')),
#                 db.Column('quantity', db.Integer)
#                 )

class cart_product(db.Model):
    __tablename__ = 'cart_product'
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.cart_id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), primary_key=True)
    quantity = db.Column(db.Integer)

    def __init__(self, cart_id, product_id, quantity=1):
        self.cart_id = cart_id
        self.product_id = product_id
        self.quantity = quantity

class Cart(db.Model):
    __tablename__ = "cart"
    cart_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    cart_status = db.Column(db.String(1)) # 0-未结算，1-已结算
    create_time = db.Column(db.DateTime)  # 创建时间
    total_price = db.Column(db.DECIMAL(10, 2))
    # products = db.relationship('Product', secondary=cart_product, backref=db.backref('cart'))

    def __init__(self, cart_status, create_time=datetime.datetime.now()):
        self.cart_status = cart_status
        self.create_time = create_time

class Category(db.Model):
    __tablename__ = "category"
    category_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(40))
    info = db.Column(db.String(200)) #描述信息

    product = db.relationship('Product', backref='category')

    def __init__(self, name, info="这是一个商品类别"):
        self.name = name
        self.info = info

class Product(db.Model):
    __tablename__ = "product"
    product_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey(Category.category_id))
    name = db.Column(db.String(30))
    image_url = db.Column(db.String(400))
    info = db.Column(db.String(200)) #描述信息
    price = db.Column(db.DECIMAL(10, 2))
    status = db.Column(db.String(1)) #商品状态.1-在售 2-下架 3-无货

    item = db.relationship('OrderItem', backref='product', uselist=False)

    def __init__(self, name, price, info="这是一个商品",
                 image_url="https://s2.ax1x.com/2019/12/27/lVFIqP.th.jpg", status=1):
        self.name = name
        self.price = price
        self.info = info
        self.status = status
        self.image_url = image_url


class MallOrder(db.Model):
    __tablename__ = "mall_order"
    order_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    # payment_id = db.Column(db.String(6))
    addr_id = db.Column(db.Integer, db.ForeignKey(Address.addr_id))
    order_no = db.Column(db.String(50), unique=True)
    payment = db.Column(db.DECIMAL(10, 2))
    carriage = db.Column(db.DECIMAL(4, 2))
    order_status = db.Column(db.String(3))  #订单状态:0-已取消,1-未付款,2-已付款,3-交易完成
    send_time = db.Column(db.DateTime)      #发货时间
    pay_time = db.Column(db.DateTime)       #付款时间
    finish_time = db.Column(db.DateTime)    #结算时间
    create_time = db.Column(db.DateTime)    #创建时间

    item = db.relationship('OrderItem', backref='mallOrder')
    payment_info = db.relationship('Payment', backref='mallOrder', uselist=False)

    def __init__(self, order_no, payment, carriage, order_status=3,
                 send_time=datetime.datetime(2018, 1, 17, 21, 8, 41, 964000),
                 pay_time=datetime.datetime(2018, 1, 17, 21, 8, 41, 965000),
                 finish_time=datetime.datetime(2018, 1, 17, 21, 8, 41, 966000),
                 create_time=datetime.datetime(2018, 1, 17, 21, 8, 41, 960000)):
        self.order_no = order_no
        self.payment = payment
        self.carriage = carriage
        self.order_status = order_status
        self.send_time = send_time
        self.pay_time = pay_time
        self.finish_time = finish_time
        self.create_time = create_time


class OrderItem(db.Model):
    __tablename__ = "order_item"
    item_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    order_no = db.Column(db.String(50), db.ForeignKey(MallOrder.order_no))
    product_id = db.Column(db.Integer, db.ForeignKey(Product.product_id))
    unit_price = db.Column(db.DECIMAL(10, 2))   #单价
    quantity = db.Column(db.Integer)            #数量
    total_price = db.Column(db.DECIMAL(10, 2))  #总价

    def __init__(self, unit_price, quantity=1):
        self.unit_price = unit_price
        self.quantity = quantity
        self.total_price = unit_price*quantity

class Payment(db.Model):
    __tablename__ = "payment"
    payment_id = db.Column(db.String(6), primary_key=True, nullable=False)
    order_no = db.Column(db.String(50), db.ForeignKey(MallOrder.order_no))
    payment_no = db.Column(db.String(400)) #支付流水号
    payment_method = db.Column(db.String(10))
    payment_status = db.Column(db.String(10)) # 0-未付款 1-已付款

    def __init__(self, payment_id, payment_no, payment_method="支付宝", payment_status=1):
        self.payment_id = payment_id
        self.payment_no = payment_no
        self.payment_method = payment_method
        self.payment_status = payment_status

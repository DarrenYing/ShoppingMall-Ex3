use mall_system;

# alter table order_item add column product_id integer;

# alter table order_item add constraint FK_product_item foreign key (product_id)
#      references product (product_id) on delete restrict on update restrict;
 
# alter table order_item add constraint FK_product_item2 foreign key (order_no)
#     references mall_order (order_no) on delete restrict on update restrict;

# alter table cart add column total_price decimal(10,2);
# alter table cart add column create_time datetime;

# create table cart_product
# (
#    cart_id              integer not null,
#    product_id           integer not null,
#    primary key (cart_id, product_id)
# );

# alter table cart_product add constraint FK_cart_product foreign key (cart_id)
#      references cart (cart_id) on delete restrict on update restrict;

# alter table cart_product add constraint FK_cart_product2 foreign key (product_id)
#       references product (product_id) on delete restrict on update restrict;

# alter table cart_product add column quantity integer;

# alter table category modify category_id integer auto_increment;
# alter table product modify category_id integer;
# alter table product add constraint FK_product_category foreign key (category_id)
#      references category (category_id) on delete restrict on update restrict;

# alter table user modify password varchar(100);
# alter table cart_product drop foreign key FK_cart_product;
# drop table cart_product;
# drop table association;
# alter table cart modify cart_id integer auto_increment; 

# 创建视图
# create view user_infomations as 
# select id, u1.username, u1.role, email, u1.user_create_time, gender, birthday
# from user u1, userinfo u2 
# where u1.id=u2.user_id; 

# create view cart_details as 
# select user_id, c1.cart_id, p1.product_id, quantity, price, info 
# from cart_product c1, product p1, cart
# where c1.product_id=p1.product_id and c1.cart_id=cart.cart_id;
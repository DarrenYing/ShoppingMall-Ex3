/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2020/4/12 17:01:55                           */
/*==============================================================*/


/*==============================================================*/
/* Table: address                                               */
/*==============================================================*/
create table address
(
   addr_id              varchar(6) not null,
   id                   char(6) not null,
   receiver_name        varchar(20),
   receiver_phone       char(11),
   province             varchar(10),
   city                 varchar(10),
   receiver_address     varchar(200),
   receiver_zipcode     char(6),
   primary key (addr_id)
);

/*==============================================================*/
/* Table: cart                                                  */
/*==============================================================*/
create table cart
(
   cart_id              varchar(6) not null,
   id                   char(6),
   cart_status          char(1),
   primary key (cart_id)
);

/*==============================================================*/
/* Table: cart_product                                          */
/*==============================================================*/
create table cart_product
(
   cart_id              varchar(6) not null,
   product_id           varchar(6) not null,
   primary key (cart_id, product_id)
);

/*==============================================================*/
/* Table: category                                              */
/*==============================================================*/
create table category
(
   category_id          varchar(6) not null,
   category_name        varchar(40),
   category_info        text,
   primary key (category_id)
);

/*==============================================================*/
/* Table: "order"                                               */
/*==============================================================*/
create table mall_order
(
   order_id             varchar(20) not null,
   id                   char(6) not null,
   payment_id           varchar(6),
   addr_id              varchar(6) not null,
   order_no             varchar(50) not null,
   payment              decimal(10,2) not null,
   carriage             decimal(4,2) not null,
   order_status         char(3) not null,
   send_time            datetime,
   payment_time         datetime,
   finish_time          datetime,
   order_create_time    datetime,
   primary key (order_id)
);

/*==============================================================*/
/* Table: order_item                                            */
/*==============================================================*/
create table order_item
(
   item_id              varchar(6) not null,
   order_id             varchar(20) not null,
   order_seq            varchar(50),
   unit_price           decimal(10,2),
   product_count        int,
   primary key (item_id)
);

/*==============================================================*/
/* Table: payment_info                                          */
/*==============================================================*/
create table payment_info
(
   payment_id           varchar(6) not null,
   order_id             varchar(20),
   payment_no           varchar(400),
   payment_method       varchar(10),
   payment_status       varchar(10),
   primary key (payment_id)
);

/*==============================================================*/
/* Table: product                                               */
/*==============================================================*/
create table product
(
   product_id           varchar(6) not null,
   category_id          varchar(6),
   product_name         varchar(30),
   product_image_url    varchar(400),
   product_info         text,
   product_price        decimal(10,2),
   product_status       char(1),
   primary key (product_id)
);

/*==============================================================*/
/* Table: user                                                  */
/*==============================================================*/
create table user
(
   id                   char(6) not null,
   userinfo_id          varchar(6),
   username             varchar(20),
   password             varchar(16) not null,
   email                varchar(30),
   role                 char(1) not null,
   user_create_time     date,
   primary key (id)
);

/*==============================================================*/
/* Table: user_info                                             */
/*==============================================================*/
create table user_info
(
   userinfo_id          varchar(6) not null,
   id                   char(6),
   uname                varchar(20),
   gender               char(6),
   birthday             date,
   profession           varchar(20),
   keyword              text,
   sign_time            date,
   primary key (userinfo_id)
);

alter table address add constraint FK_user_receiver_addr foreign key (id)
      references user (id) on delete restrict on update restrict;

alter table cart add constraint FK_user_cart foreign key (id)
      references user (id) on delete restrict on update restrict;

alter table cart_product add constraint FK_cart_product foreign key (cart_id)
      references cart (cart_id) on delete restrict on update restrict;

alter table cart_product add constraint FK_cart_product2 foreign key (product_id)
      references product (product_id) on delete restrict on update restrict;

alter table mall_order add constraint FK_order_payment foreign key (payment_id)
      references payment_info (payment_id) on delete restrict on update restrict;

alter table mall_order add constraint FK_order_receiver_addr foreign key (addr_id)
      references address (addr_id) on delete restrict on update restrict;

alter table mall_order add constraint FK_user_order foreign key (id)
      references user (id) on delete restrict on update restrict;

alter table order_item add constraint FK_order_item foreign key (order_id)
      references mall_order (order_id) on delete restrict on update restrict;

alter table payment_info add constraint FK_order_payment2 foreign key (order_id)
      references mall_order (order_id) on delete restrict on update restrict;

alter table product add constraint FK_product_category foreign key (category_id)
      references category (category_id) on delete restrict on update restrict;

alter table user add constraint FK_user_userinfo2 foreign key (userinfo_id)
      references user_info (userinfo_id) on delete restrict on update restrict;

alter table user_info add constraint FK_user_userinfo foreign key (id)
      references user (id) on delete restrict on update restrict;


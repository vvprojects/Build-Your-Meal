CREATE TABLE "Group" (
  "group_id" integer PRIMARY KEY,
  "name" varchar
);

CREATE TABLE "User" (
  "user_id" integer PRIMARY KEY,
  "adress" varchar,
  "first_name" varchar,
  "last_nam" varchar,
  "login" varchar,
  "password" varchar
);

CREATE TABLE "Group_User" (
  "group_id" integer,
  "user_id" integer,
  PRIMARY KEY ("group_id", "user_id")
);

CREATE TABLE "Category" (
  "category_id" integer PRIMARY KEY,
  "name" varchar,
  "supreme_category_id" integer
);

CREATE TABLE "Personalization" (
  "user_id" integer,
  "category_id" integer,
  "restricted" blob,
  PRIMARY KEY ("user_id", "category_id")
);

CREATE TABLE "Dish" (
  "dish_id" integer PRIMARY KEY,
  "pers_num" integer,
  "name" varchar,
  "calories" decimal,
  "proteins" decimal,
  "carbohydrates" decimal,
  "fats" decimal,
  "country_id" integer,
  "recipy" varchar,
  "type_id" integer,
  "ready" blob
);

CREATE TABLE "Country" (
  "country_id" integer PRIMARY KEY,
  "name" varchar
);

CREATE TABLE "Dish_Type" (
  "type_id" integer PRIMARY KEY,
  "name" varchar
);

CREATE TABLE "Dish_Category" (
  "dish_id" integer,
  "category_id" integer,
  "amount" decimal,
  PRIMARY KEY ("dish_id", "category_id")
);

CREATE TABLE "Unit_of_Measure" (
  "unit_id" integer PRIMARY KEY,
  "name" varchar
);

CREATE TABLE "Conversion" (
  "category_id" integer,
  "unit_id" integer,
  "coefficient" decimal,
  PRIMARY KEY ("category_id", "unit_id")
);

CREATE TABLE "Shop" (
  "shop_id" integer PRIMARY KEY,
  "name" varchar,
  "link" varchar
);

CREATE TABLE "Product" (
  "product_id" integer PRIMARY KEY,
  "name" varchar,
  "price" decimal,
  "production_date" datetime,
  "expiration_date" datetime,
  "amount" decimal,
  "category_id" integer,
  "unit_id" integer,
  "shop_id" integer
);

CREATE TABLE "Category_Product" (
  "product_id" integer,
  "category_id" integer,
  "value" decimal,
  PRIMARY KEY ("product_id", "category_id")
);

CREATE TABLE "Product_Logs" (
  "log_id" integer PRIMARY KEY,
  "name" varchar,
  "price" decimal,
  "production_date" datetime,
  "expiration_date" datetime,
  "amount" decimal,
  "order_id" integer,
  "user_id" integer,
  "category_id" integer,
  "unit_id" integer,
  "shop_id" integer,
  "do_not_include" blob
);

CREATE TABLE "Order" (
  "order_id" integer PRIMARY KEY,
  "order_date" datetime,
  "user_id" integer
);

CREATE TABLE "Menu" (
  "dish_id" integer,
  "order_id" integer,
  "position" varchar,
  "cook_date" datetime,
  PRIMARY KEY ("dish_id", "order_id")
);

ALTER TABLE "Group" ADD FOREIGN KEY ("group_id") REFERENCES "Group_User" ("group_id");

ALTER TABLE "User" ADD FOREIGN KEY ("user_id") REFERENCES "Group_User" ("user_id");

ALTER TABLE "User" ADD FOREIGN KEY ("user_id") REFERENCES "Personalization" ("user_id");

ALTER TABLE "Category" ADD FOREIGN KEY ("category_id") REFERENCES "Personalization" ("category_id");

ALTER TABLE "Category" ADD FOREIGN KEY ("supreme_category_id") REFERENCES "Category" ("category_id");

ALTER TABLE "Dish" ADD FOREIGN KEY ("dish_id") REFERENCES "Dish_Category" ("dish_id");

ALTER TABLE "Category" ADD FOREIGN KEY ("category_id") REFERENCES "Dish_Category" ("category_id");

ALTER TABLE "Country" ADD FOREIGN KEY ("country_id") REFERENCES "Dish" ("country_id");

ALTER TABLE "Dish_Type" ADD FOREIGN KEY ("type_id") REFERENCES "Dish" ("type_id");

ALTER TABLE "Category" ADD FOREIGN KEY ("category_id") REFERENCES "Conversion" ("category_id");

ALTER TABLE "Unit_of_Measure" ADD FOREIGN KEY ("unit_id") REFERENCES "Conversion" ("unit_id");

ALTER TABLE "Category" ADD FOREIGN KEY ("category_id") REFERENCES "Product" ("category_id");

ALTER TABLE "Shop" ADD FOREIGN KEY ("shop_id") REFERENCES "Product" ("shop_id");

ALTER TABLE "Unit_of_Measure" ADD FOREIGN KEY ("unit_id") REFERENCES "Product" ("unit_id");

ALTER TABLE "Category" ADD FOREIGN KEY ("category_id") REFERENCES "Product_Logs" ("category_id");

ALTER TABLE "Shop" ADD FOREIGN KEY ("shop_id") REFERENCES "Product_Logs" ("shop_id");

ALTER TABLE "Unit_of_Measure" ADD FOREIGN KEY ("unit_id") REFERENCES "Product_Logs" ("unit_id");

ALTER TABLE "User" ADD FOREIGN KEY ("user_id") REFERENCES "Product_Logs" ("user_id");

ALTER TABLE "Order" ADD FOREIGN KEY ("order_id") REFERENCES "Product_Logs" ("order_id");

ALTER TABLE "User" ADD FOREIGN KEY ("user_id") REFERENCES "Order" ("user_id");

ALTER TABLE "Order" ADD FOREIGN KEY ("order_id") REFERENCES "Menu" ("order_id");

ALTER TABLE "Menu" ADD FOREIGN KEY ("dish_id") REFERENCES "Dish" ("dish_id");

ALTER TABLE "Product" ADD FOREIGN KEY ("product_id") REFERENCES "Category_Product" ("product_id");

ALTER TABLE "Category" ADD FOREIGN KEY ("category_id") REFERENCES "Category_Product" ("product_id");

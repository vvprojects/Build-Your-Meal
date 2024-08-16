CREATE TABLE "User" (
  "id" integer PRIMARY KEY,
  "last_adress" varchar,
  "nickname" varchar,
  "login" varchar
);

CREATE TABLE "Category" (
  "id" integer PRIMARY KEY,
  "name" varchar,
  "supreme_category_id" integer
);

CREATE TABLE "CategoryImage" (
  "id" integer PRIMARY KEY,
  "category_id" integer,
  "image" image
);

CREATE TABLE "Dish" (
  "id" integer PRIMARY KEY,
  "cooking_time" integer,
  "name" varchar,
  "calories" decimal,
  "proteins" decimal,
  "carbohydrates" decimal,
  "fats" decimal,
  "recipy" varchar,
  "ready" blob,
  "image" image
);

CREATE TABLE "DishTypeTree" (
  "id" integer PRIMARY KEY,
  "dish_id" integer,
  "type_id" integer,
  "order" integer
);

CREATE TABLE "DishType" (
  "id" integer PRIMARY KEY,
  "name" varchar,
  "supreme_type_id" integer
);

CREATE TABLE "CookingStage" (
  "id" integer PRIMARY KEY,
  "description" varchar,
  "order" integer,
  "image" image,
  "dish_id" integer
);

CREATE TABLE "DishCategory" (
  "id" integer PRIMARY KEY,
  "dish_id" integer,
  "category_id" integer,
  "amount" decimal,
  "unit_id" integer
);

CREATE TABLE "UnitOfMeasure" (
  "id" integer PRIMARY KEY,
  "name" varchar
);

CREATE TABLE "Conversion" (
  "id" integer PRIMARY KEY,
  "category_id" integer,
  "unit_id" integer,
  "coefficient" decimal
);

CREATE TABLE "Shop" (
  "id" integer PRIMARY KEY,
  "name" varchar,
  "link" varchar
);

CREATE TABLE "Product" (
  "id" integer PRIMARY KEY,
  "user_id" integer,
  "name" varchar,
  "price" decimal,
  "amount" decimal,
  "quantity" integer,
  "link" varchar,
  "unit_id" integer,
  "shop_id" integer
);

CREATE TABLE "ProductLogs" (
  "id" integer PRIMARY KEY,
  "name" varchar,
  "price" decimal,
  "amount" decimal,
  "quantity" integer,
  "order_id" integer,
  "shop_id" integer,
  "unit_id" integer,
  "link" varchar
);

CREATE TABLE "Order" (
  "id" integer PRIMARY KEY,
  "order_date" datetime,
  "user_id" integer
);

CREATE TABLE "Menu" (
  "id" integer PRIMARY KEY,
  "dish_id" integer,
  "order_id" integer,
  "position" varchar,
  "cook_date" datetime
);

ALTER TABLE "Category" ADD FOREIGN KEY ("supreme_category_id") REFERENCES "Category" ("id");

ALTER TABLE "Category" ADD FOREIGN KEY ("id") REFERENCES "CategoryImage" ("category_id");

ALTER TABLE "Dish" ADD FOREIGN KEY ("id") REFERENCES "DishCategory" ("dish_id");

ALTER TABLE "Category" ADD FOREIGN KEY ("id") REFERENCES "DishCategory" ("category_id");

ALTER TABLE "UnitOfMeasure" ADD FOREIGN KEY ("id") REFERENCES "DishCategory" ("unit_id");

ALTER TABLE "DishTypeTree" ADD FOREIGN KEY ("type_id") REFERENCES "DishType" ("id");

ALTER TABLE "DishTypeTree" ADD FOREIGN KEY ("dish_id") REFERENCES "Dish" ("id");

ALTER TABLE "CookingStage" ADD FOREIGN KEY ("dish_id") REFERENCES "Dish" ("id");

ALTER TABLE "Category" ADD FOREIGN KEY ("id") REFERENCES "Conversion" ("category_id");

ALTER TABLE "UnitOfMeasure" ADD FOREIGN KEY ("id") REFERENCES "Conversion" ("unit_id");

ALTER TABLE "User" ADD FOREIGN KEY ("id") REFERENCES "Product" ("user_id");

ALTER TABLE "Shop" ADD FOREIGN KEY ("id") REFERENCES "Product" ("shop_id");

ALTER TABLE "UnitOfMeasure" ADD FOREIGN KEY ("id") REFERENCES "Product" ("unit_id");

ALTER TABLE "Shop" ADD FOREIGN KEY ("id") REFERENCES "ProductLogs" ("shop_id");

ALTER TABLE "UnitOfMeasure" ADD FOREIGN KEY ("id") REFERENCES "ProductLogs" ("unit_id");

ALTER TABLE "Order" ADD FOREIGN KEY ("id") REFERENCES "ProductLogs" ("order_id");

ALTER TABLE "User" ADD FOREIGN KEY ("id") REFERENCES "Order" ("user_id");

ALTER TABLE "Order" ADD FOREIGN KEY ("id") REFERENCES "Menu" ("order_id");

ALTER TABLE "Menu" ADD FOREIGN KEY ("dish_id") REFERENCES "Dish" ("id");

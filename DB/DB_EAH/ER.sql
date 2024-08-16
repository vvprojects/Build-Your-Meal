CREATE TABLE "public.Recipes" (
	"Uid" TEXT NOT NULL,
	"Name" varchar(255) NOT NULL UNIQUE,
	"Time" integer NOT NULL DEFAULT '-1',
	"EpUid" TEXT NOT NULL,
	"CuisineUid" TEXT NOT NULL,
	"Url" varchar(255) NOT NULL UNIQUE,
	CONSTRAINT "Recipes_pk" PRIMARY KEY ("Uid")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "public.Eps" (
	"Uid" TEXT NOT NULL,
	"Calories" FLOAT NOT NULL,
	"Proteins" FLOAT NOT NULL,
	"Fats" FLOAT NOT NULL,
	"Carbonhydrates" FLOAT NOT NULL,
	CONSTRAINT "Eps_pk" PRIMARY KEY ("Uid")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "public.Images" (
	"Uid" TEXT NOT NULL,
	"RecipeUid" TEXT NOT NULL,
	"Image" TEXT NOT NULL,
	"ImageType" TEXT NOT NULL,
	"Hash" TEXT(32) NOT NULL UNIQUE,
	CONSTRAINT "Images_pk" PRIMARY KEY ("Uid")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "public.Ingredients" (
	"Uid" TEXT NOT NULL,
	"Name" varchar(255) NOT NULL UNIQUE,
	CONSTRAINT "Ingredients_pk" PRIMARY KEY ("Uid")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "public.IngredientsRel" (
	"Uid" TEXT NOT NULL,
	"IngredientUid" TEXT NOT NULL,
	"Amount" FLOAT NOT NULL,
	"UnitUid" TEXT NOT NULL,
	"RecipeUid" TEXT NOT NULL,
	"Portions" integer NOT NULL DEFAULT '1',
	CONSTRAINT "IngredientsRel_pk" PRIMARY KEY ("Uid")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "public.Units" (
	"Uid" TEXT NOT NULL,
	"Name" varchar(255) NOT NULL UNIQUE,
	CONSTRAINT "Units_pk" PRIMARY KEY ("Uid")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "public.Videos" (
	"Uid" TEXT NOT NULL,
	"Url" TEXT NOT NULL,
	"RecipeUid" TEXT NOT NULL,
	CONSTRAINT "Videos_pk" PRIMARY KEY ("Uid")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "public.CookingStages" (
	"Uid" TEXT NOT NULL,
	"Text" TEXT NOT NULL,
	"ImageUid" TEXT NOT NULL,
	"Order" integer NOT NULL,
	"RecipeUid" TEXT NOT NULL,
	CONSTRAINT "CookingStages_pk" PRIMARY KEY ("Uid")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "public.Cuisines" (
	"Uid" TEXT NOT NULL,
	"Name" varchar(255) NOT NULL UNIQUE,
	CONSTRAINT "Cuisines_pk" PRIMARY KEY ("Uid")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "public.ImageType" (
	"Uid" TEXT NOT NULL,
	"Name" varchar(255) NOT NULL UNIQUE,
	"Description" TEXT NOT NULL,
	CONSTRAINT "ImageType_pk" PRIMARY KEY ("Uid")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "public.RatingHistories" (
	"Uid" TEXT NOT NULL,
	"Score" FLOAT NOT NULL,
	"RecipeUid" TEXT NOT NULL,
	"UserUid" TEXT(32) NOT NULL,
	CONSTRAINT "RatingHistories_pk" PRIMARY KEY ("Uid")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "public.Categories" (
	"Uid" TEXT NOT NULL,
	"Name" varchar(255) NOT NULL UNIQUE,
	CONSTRAINT "Categories_pk" PRIMARY KEY ("Uid")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "public.CategoriesRel" (
	"Uid" TEXT NOT NULL,
	"CategoryUid" TEXT NOT NULL,
	"RecipeUid" TEXT NOT NULL,
	"Order" integer NOT NULL,
	CONSTRAINT "CategoriesRel_pk" PRIMARY KEY ("Uid")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "public.Likes" (
	"Uid" TEXT(32) NOT NULL,
	"UserUid" TEXT(32) NOT NULL,
	"RecipeUid" TEXT(32) NOT NULL,
	CONSTRAINT "Likes_pk" PRIMARY KEY ("Uid")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "public.Users" (
	"Uid" TEXT(32) NOT NULL,
	"Username" varchar(255) NOT NULL UNIQUE,
	"Password" varchar(128) NOT NULL,
	"Email" varchar(255) NOT NULL UNIQUE,
	"FirstName" varchar(255) NOT NULL,
	"LastName" varchar(255) NOT NULL,
	"Age" integer,
	"CityUid" TEXT,
	"Sex" BOOLEAN,
	"Status" integer NOT NULL,
	CONSTRAINT "Users_pk" PRIMARY KEY ("Uid")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "public.FavoriteCategories" (
	"Uid" TEXT NOT NULL,
	"CategoryUid" TEXT NOT NULL,
	"UserUid" TEXT NOT NULL,
	CONSTRAINT "FavoriteCategories_pk" PRIMARY KEY ("Uid")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "public.Cities" (
	"Uid" TEXT NOT NULL,
	"Name" TEXT NOT NULL UNIQUE,
	CONSTRAINT "Cities_pk" PRIMARY KEY ("Uid")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "public.RefreshTokens" (
	"Uid" TEXT NOT NULL,
	"Token" TEXT NOT NULL UNIQUE,
	"Expires" DATETIME NOT NULL,
	"CreatedIp" VARCHAR(255) NOT NULL,
	"RevokedIp" VARCHAR(255),
	"CreatedAt" DATETIME NOT NULL,
	"RevokedAt" DATETIME,
	"UserUid" TEXT NOT NULL,
	CONSTRAINT "RefreshTokens_pk" PRIMARY KEY ("Uid")
) WITH (
  OIDS=FALSE
);



ALTER TABLE "Recipes" ADD CONSTRAINT "Recipes_fk0" FOREIGN KEY ("EpUid") REFERENCES "Eps"("Uid");
ALTER TABLE "Recipes" ADD CONSTRAINT "Recipes_fk1" FOREIGN KEY ("CuisineUid") REFERENCES "Cuisines"("Uid");


ALTER TABLE "Images" ADD CONSTRAINT "Images_fk0" FOREIGN KEY ("RecipeUid") REFERENCES "Recipes"("Uid");
ALTER TABLE "Images" ADD CONSTRAINT "Images_fk1" FOREIGN KEY ("ImageType") REFERENCES "ImageType"("Uid");


ALTER TABLE "IngredientsRel" ADD CONSTRAINT "IngredientsRel_fk0" FOREIGN KEY ("IngredientUid") REFERENCES "Ingredients"("Uid");
ALTER TABLE "IngredientsRel" ADD CONSTRAINT "IngredientsRel_fk1" FOREIGN KEY ("UnitUid") REFERENCES "Units"("Uid");
ALTER TABLE "IngredientsRel" ADD CONSTRAINT "IngredientsRel_fk2" FOREIGN KEY ("RecipeUid") REFERENCES "Recipes"("Uid");


ALTER TABLE "Videos" ADD CONSTRAINT "Videos_fk0" FOREIGN KEY ("RecipeUid") REFERENCES "Recipes"("Uid");

ALTER TABLE "CookingStages" ADD CONSTRAINT "CookingStages_fk0" FOREIGN KEY ("ImageUid") REFERENCES "Images"("Uid");
ALTER TABLE "CookingStages" ADD CONSTRAINT "CookingStages_fk1" FOREIGN KEY ("RecipeUid") REFERENCES "Recipes"("Uid");



ALTER TABLE "RatingHistories" ADD CONSTRAINT "RatingHistories_fk0" FOREIGN KEY ("RecipeUid") REFERENCES "Recipes"("Uid");
ALTER TABLE "RatingHistories" ADD CONSTRAINT "RatingHistories_fk1" FOREIGN KEY ("UserUid") REFERENCES "Users"("Uid");


ALTER TABLE "CategoriesRel" ADD CONSTRAINT "CategoriesRel_fk0" FOREIGN KEY ("CategoryUid") REFERENCES "Categories"("Uid");
ALTER TABLE "CategoriesRel" ADD CONSTRAINT "CategoriesRel_fk1" FOREIGN KEY ("RecipeUid") REFERENCES "Recipes"("Uid");

ALTER TABLE "Likes" ADD CONSTRAINT "Likes_fk0" FOREIGN KEY ("UserUid") REFERENCES "Users"("Uid");
ALTER TABLE "Likes" ADD CONSTRAINT "Likes_fk1" FOREIGN KEY ("RecipeUid") REFERENCES "Recipes"("Uid");

ALTER TABLE "Users" ADD CONSTRAINT "Users_fk0" FOREIGN KEY ("CityUid") REFERENCES "Cities"("Uid");

ALTER TABLE "FavoriteCategories" ADD CONSTRAINT "FavoriteCategories_fk0" FOREIGN KEY ("CategoryUid") REFERENCES "Categories"("Uid");
ALTER TABLE "FavoriteCategories" ADD CONSTRAINT "FavoriteCategories_fk1" FOREIGN KEY ("UserUid") REFERENCES "Users"("Uid");


ALTER TABLE "RefreshTokens" ADD CONSTRAINT "RefreshTokens_fk0" FOREIGN KEY ("UserUid") REFERENCES "Users"("Uid");




















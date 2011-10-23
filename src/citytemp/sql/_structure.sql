--
-- This file isn't used by Django.  I'm just including it for anyone else who
-- might use this database for non-django projects.
--

BEGIN;

CREATE TABLE "citytemp_city" (
    "id" serial NOT NULL PRIMARY KEY,
    "country" varchar(32) NOT NULL,
    "city" varchar(32) NOT NULL,
    "code" varchar(4) NOT NULL,
    "location" geography(POINT,4326) NOT NULL,
    "elevation" integer
);

CREATE TABLE "citytemp_temperature" (
    "id" serial NOT NULL PRIMARY KEY,
    "airport_id" integer NOT NULL REFERENCES "citytemp_city" ("id") DEFERRABLE INITIALLY DEFERRED,
    "month" integer CHECK ("month" >= 0) NOT NULL,
    "day" integer CHECK ("day" >= 0) NOT NULL,
    "high" integer,
    "low" integer,
    "mean" integer,
    "rhigh" integer,
    "rlow" integer
);

CREATE INDEX "citytemp_city_location_id" ON "citytemp_city" USING GIST ( "location" );
CREATE INDEX "citytemp_temperature_airport_id" ON "citytemp_temperature" ("airport_id");

COMMIT;

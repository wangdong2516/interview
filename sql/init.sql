# 初始化数据库表结构
SET FOREIGN_KEY_CHECKS=0;


DROP TABLE IF EXISTS province;
CREATE TABLE province (
  id            int,
  province_name           varchar(64),
  PRIMARY KEY (id)
);


DROP TABLE IF EXISTS city;
CREATE TABLE city (
  id           int,
  city_name          varchar(64),
  province_id   varchar(12),
  PRIMARY KEY (id)
);


DROP TABLE IF EXISTS county;
CREATE TABLE county (
  id  int,
  county_name varchar(64),
  city_id varchar(12),
  PRIMARY KEY (id)
);


DROP TABLE IF EXISTS town;
CREATE TABLE town (
  id  int,
  town_name varchar(64),
  county_id varchar(12),
  PRIMARY KEY (id)
);


DROP TABLE IF EXISTS village;
CREATE TABLE village (
  id  int,
  village_name varchar(64),
  town_id varchar(12),
  PRIMARY KEY (id)
);

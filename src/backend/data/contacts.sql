/*
 Navicat Premium Data Transfer

 Source Server         : 1
 Source Server Type    : SQLite
 Source Server Version : 3030001
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3030001
 File Encoding         : 65001

 Date: 23/01/2026 16:32:22
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for contacts
-- ----------------------------
DROP TABLE IF EXISTS "contacts";
CREATE TABLE "contacts" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "account_id" TEXT,
  "name" TEXT NOT NULL,
  "tag" TEXT,
  "type" TEXT,
  "last_updated" DATETIME,
  FOREIGN KEY ("account_id") REFERENCES "wechat_accounts" ("account_id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  UNIQUE ("account_id" ASC, "name" ASC, "tag" ASC, "type" ASC),
   (type IN ('friend', 'group'))
);

PRAGMA foreign_keys = true;

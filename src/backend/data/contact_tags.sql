/*
 Navicat Premium Data Transfer

 Source Server         : 1
 Source Server Type    : SQLite
 Source Server Version : 3030001
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3030001
 File Encoding         : 65001

 Date: 23/01/2026 16:32:28
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for contact_tags
-- ----------------------------
DROP TABLE IF EXISTS "contact_tags";
CREATE TABLE "contact_tags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "account_id" TEXT NOT NULL,
  "tag_name" TEXT NOT NULL,
  "contact_count" INTEGER DEFAULT 0,
  "last_updated" DATETIME,
  FOREIGN KEY ("account_id") REFERENCES "wechat_accounts" ("account_id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  UNIQUE ("account_id" ASC, "tag_name" ASC)
);

-- ----------------------------
-- Auto increment value for contact_tags
-- ----------------------------
UPDATE "sqlite_sequence" SET seq = 8 WHERE name = 'contact_tags';

PRAGMA foreign_keys = true;

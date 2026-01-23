/*
 Navicat Premium Data Transfer

 Source Server         : 1
 Source Server Type    : SQLite
 Source Server Version : 3030001
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3030001
 File Encoding         : 65001

 Date: 23/01/2026 16:31:35
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for groups
-- ----------------------------
DROP TABLE IF EXISTS "groups";
CREATE TABLE "groups" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "account_id" TEXT NOT NULL,
  "name" TEXT NOT NULL,
  "tag" TEXT DEFAULT '',
  "last_updated" DATETIME,
  FOREIGN KEY ("account_id") REFERENCES "wechat_accounts" ("account_id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  UNIQUE ("account_id" ASC, "name" ASC)
);

-- ----------------------------
-- Auto increment value for groups
-- ----------------------------
UPDATE "sqlite_sequence" SET seq = 368 WHERE name = 'groups';

PRAGMA foreign_keys = true;

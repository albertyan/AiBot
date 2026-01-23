/*
 Navicat Premium Data Transfer

 Source Server         : 1
 Source Server Type    : SQLite
 Source Server Version : 3030001
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3030001
 File Encoding         : 65001

 Date: 23/01/2026 16:32:08
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for friends
-- ----------------------------
DROP TABLE IF EXISTS "friends";
CREATE TABLE "friends" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "account_id" TEXT NOT NULL,
  "wxid" TEXT NOT NULL,
  "name" TEXT NOT NULL,
  "nickname" TEXT,
  "remark" TEXT,
  "tag" TEXT,
  "is_new" INTEGER DEFAULT 0,
  "created_at" DATETIME DEFAULT CURRENT_TIMESTAMP,
  "last_updated" DATETIME,
  FOREIGN KEY ("account_id") REFERENCES "wechat_accounts" ("account_id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  UNIQUE ("account_id" ASC, "wxid" ASC, "tag" ASC)
);

-- ----------------------------
-- Auto increment value for friends
-- ----------------------------
UPDATE "sqlite_sequence" SET seq = 1344 WHERE name = 'friends';

PRAGMA foreign_keys = true;

/*
 Navicat Premium Data Transfer

 Source Server         : 1
 Source Server Type    : SQLite
 Source Server Version : 3030001
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3030001
 File Encoding         : 65001

 Date: 23/01/2026 16:31:26
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for wechat_accounts
-- ----------------------------
DROP TABLE IF EXISTS "wechat_accounts";
CREATE TABLE "wechat_accounts" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "nickname" TEXT NOT NULL,
  "account_id" TEXT,
  "last_updated" DATETIME,
  UNIQUE ("account_id" ASC),
  UNIQUE ("nickname" ASC, "account_id" ASC)
);

-- ----------------------------
-- Auto increment value for wechat_accounts
-- ----------------------------
UPDATE "sqlite_sequence" SET seq = 26 WHERE name = 'wechat_accounts';

PRAGMA foreign_keys = true;

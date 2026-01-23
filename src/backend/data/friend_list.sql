/*
 Navicat Premium Data Transfer

 Source Server         : 1
 Source Server Type    : SQLite
 Source Server Version : 3030001
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3030001
 File Encoding         : 65001

 Date: 23/01/2026 16:32:14
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for friend_list
-- ----------------------------
DROP TABLE IF EXISTS "friend_list";
CREATE TABLE "friend_list" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "wxid" TEXT NOT NULL,
  "remark" TEXT,
  "tags" TEXT,
  "nickname" TEXT,
  "status" TEXT DEFAULT 'pending',
  "error" TEXT,
  "created_at" DATETIME DEFAULT CURRENT_TIMESTAMP,
  "updated_at" DATETIME DEFAULT CURRENT_TIMESTAMP,
  "account_id" TEXT,
  UNIQUE ("wxid" ASC),
   (status IN ('pending', 'added', 'failed', 'unknown', 'already'))
);

PRAGMA foreign_keys = true;

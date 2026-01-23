/*
 Navicat Premium Data Transfer

 Source Server         : 1
 Source Server Type    : SQLite
 Source Server Version : 3030001
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3030001
 File Encoding         : 65001

 Date: 23/01/2026 16:31:59
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for group_members
-- ----------------------------
DROP TABLE IF EXISTS "group_members";
CREATE TABLE "group_members" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "group_name" TEXT NOT NULL,
  "nickname" TEXT NOT NULL,
  "gender" TEXT,
  "wx_id" TEXT,
  "region" TEXT,
  "is_friend" INTEGER DEFAULT 0,
  "last_updated" DATETIME,
  UNIQUE ("group_name" ASC, "nickname" ASC)
);

PRAGMA foreign_keys = true;

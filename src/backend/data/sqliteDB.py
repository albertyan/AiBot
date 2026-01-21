import sqlite3
import os
# import baseUtil
from contextlib import contextmanager
from typing import List, Tuple, Optional, Any


class SQLiteDB:
    def __init__(self, db_path: str):
        """
        初始化数据库连接
        :param db_path: 数据库文件路径（自动创建不存在的目录）
        """
        # os.makedirs(os.path.dirname(baseUtil.get_root_path(db_path)), exist_ok=False)
        self.db_path = db_path
        self.conn = None
    
    @contextmanager
    def _get_cursor(self):
        """上下文管理器自动处理连接和事务"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.execute("PRAGMA foreign_keys = OFF;")  # 禁用外键约束
            self.conn.row_factory = sqlite3.Row  # 返回字典式结果
            cursor = self.conn.cursor()
            yield cursor
            self.conn.commit()
        except sqlite3.Error as e:
            if self.conn:
                self.conn.rollback()
            raise DatabaseError(f"SQLite error: {e}") from e
        finally:
            if self.conn:
                self.conn.close()

    def execute(self, sql: str, params: tuple = ()) -> int:
        """执行SQL语句并返回影响行数"""
        with self._get_cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.rowcount

    def executemany(self, sql: str, params_list: List[tuple]) -> int:
        """批量执行SQL语句"""
        with self._get_cursor() as cursor:
            cursor.executemany(sql, params_list)
            return cursor.rowcount

    def fetchone(self, sql: str, params: tuple = ()) -> Optional[dict]:
        """查询单条记录"""
        with self._get_cursor() as cursor:
            cursor.execute(sql, params)
            row = cursor.fetchone()
            return dict(row) if row else None

    def fetchall(self, sql: str, params: tuple = ()) -> List[dict]:
        """查询所有记录"""
        with self._get_cursor() as cursor:
            cursor.execute(sql, params)
            return [dict(row) for row in cursor.fetchall()]

    def create_table(self, table_sql: str):
        """创建数据表"""
        self.execute(table_sql)
    
    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
            self.conn = None


class DatabaseError(Exception):
    """自定义数据库异常"""
    def __init__(self, Error='数据库操作失败！'):
        super().__init__(Error)



# Example usage:
if __name__ == "__main__":
    global db
    try:
        db = SQLiteDB("wechat_contacts.db")
        db.close()
    except OSError as e:
        print(f"Error initializing database: {e}")
    # else:    
    #     db.create_table('''
    #         CREATE TABLE "contact_tags" (
    #         "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    #         "account_id" TEXT NOT NULL,
    #         "tag_name" TEXT NOT NULL,
    #         "contact_count" INTEGER DEFAULT 0,
    #         "last_updated" DATETIME,
    #         FOREIGN KEY ("account_id") REFERENCES "wechat_accounts" ("account_id") ON DELETE NO ACTION ON UPDATE NO ACTION,
    #         UNIQUE ("account_id" ASC, "tag_name" ASC)
    #         );
    #     ''')

    #     db.create_table('''
    #         CREATE TABLE "contacts" (
    #         "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    #         "account_id" TEXT,
    #         "name" TEXT NOT NULL,
    #         "tag" TEXT,
    #         "type" TEXT,
    #         "last_updated" DATETIME,
    #         FOREIGN KEY ("account_id") REFERENCES "wechat_accounts" ("account_id") ON DELETE NO ACTION ON UPDATE NO ACTION,
    #         UNIQUE ("account_id" ASC, "name" ASC, "tag" ASC, "type" ASC),
    #         CONSTRAINT "type" CHECK (type IN ('friend', 'group'))
    #         );
    #     ''')

    #     db.create_table('''
    #         CREATE TABLE "friend_list" (
    #         "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    #         "wxid" TEXT NOT NULL,
    #         "remark" TEXT,
    #         "tags" TEXT,
    #         "nickname" TEXT,
    #         "status" TEXT DEFAULT 'pending',
    #         "error" TEXT,
    #         "created_at" DATETIME DEFAULT CURRENT_TIMESTAMP,
    #         "updated_at" DATETIME DEFAULT CURRENT_TIMESTAMP,
    #         UNIQUE ("wxid" ASC),
    #         CONSTRAINT "status" CHECK (status IN ('pending', 'added', 'failed', 'unknown', 'already'))
    #         );
    #     ''')
    #     db.create_table('''
    #         CREATE TABLE "group_members" (
    #         "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    #         "group_name" TEXT NOT NULL,
    #         "nickname" TEXT NOT NULL,
    #         "gender" TEXT,
    #         "wx_id" TEXT,
    #         "region" TEXT,
    #         "is_friend" INTEGER DEFAULT 0,
    #         "last_updated" DATETIME,
    #         UNIQUE ("group_name" ASC, "nickname" ASC)
    #         );
    #     ''')

    #     db.create_table('''
    #         CREATE TABLE "wechat_accounts" (
    #         "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    #         "nickname" TEXT NOT NULL,
    #         "account_id" TEXT,
    #         "last_updated" DATETIME,
    #         UNIQUE ("account_id" ASC),
    #         UNIQUE ("nickname" ASC, "account_id" ASC)
    #         );
    #     ''')
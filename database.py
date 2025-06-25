import sqlite3
from typing import Optional

class Database:
    def __init__(self, db_path: str = "qdb.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """初始化数据库，创建keys表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                token TEXT UNIQUE NOT NULL,
                api_key TEXT NOT NULL,
                provider TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建触发器，自动更新updated_at字段
        cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS update_keys_timestamp
            AFTER UPDATE ON keys
            FOR EACH ROW
            BEGIN
                UPDATE keys SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
            END
        ''')
        
        conn.commit()
        conn.close()
    
    def get_api_key_by_token(self, token: str) -> Optional[str]:
        """根据token查询api_key"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT api_key FROM keys WHERE token = ?', (token,))
        result = cursor.fetchone()
        
        conn.close()
        
        if result:
            return result[0]
        return None
    
    def token_exists(self, token: str) -> bool:
        """检查token是否存在"""
        return self.get_api_key_by_token(token) is not None

# 全局数据库实例
db = Database()
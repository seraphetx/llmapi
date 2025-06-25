import sqlite3
from database import db

def init_sample_data():
    """初始化示例数据"""
    conn = sqlite3.connect("qdb.db")
    cursor = conn.cursor()
    
    # 插入示例数据
    sample_data = [
        ("测试key1", "test_token_123", "your_openrouter_api_key_here", "openrouter"),
        ("测试key2", "test_token_456", "your_openrouter_api_key_here", "openrouter"),
    ]
    
    try:
        cursor.executemany(
            "INSERT OR IGNORE INTO keys (name, token, api_key, provider) VALUES (?, ?, ?, ?)",
            sample_data
        )
        conn.commit()
        print("示例数据初始化完成")
        
        # 显示当前数据
        cursor.execute("SELECT * FROM keys")
        rows = cursor.fetchall()
        print("\n当前数据库中的数据:")
        print("ID | Name | Token | API Key | Provider | Created At | Updated At")
        print("-" * 80)
        for row in rows:
            print(f"{row[0]} | {row[1]} | {row[2][:15]}... | {row[3][:15]}... | {row[4]} | {row[5]} | {row[6]}")
            
    except Exception as e:
        print(f"初始化数据时发生错误: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    print("初始化数据库...")
    db.init_db()
    init_sample_data()
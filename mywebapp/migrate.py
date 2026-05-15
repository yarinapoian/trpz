#!/usr/bin/env python3
import sys
import argparse
import mysql.connector

def migrate_database(host: str, user: str, password: str, database: str) -> bool:
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            status VARCHAR(50) NOT NULL DEFAULT 'todo',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_status (status),
            INDEX idx_created_at (created_at)
        )
    """)

    connection.commit()
    print("Database migration completed successfully")

    cursor.close()
    connection.close()
    return True


def main():
    parser = argparse.ArgumentParser(description='Task Tracker Database Migration')
    parser.add_argument('--host', type=str, default='127.0.0.1', help='Database host')
    parser.add_argument('--user', type=str, default='app', help='Database user')
    parser.add_argument('--password', type=str, default='app', help='Database password')
    parser.add_argument('--database', type=str, default='task_tracker', help='Database name')
    
    args = parser.parse_args()
    
    success = migrate_database(args.host, args.user, args.password, args.database)
    
    if not success:
        sys.exit(1)


if __name__ == '__main__':
    main()


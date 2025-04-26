from sqlalchemy import text
import json
from db import get_db_connection

def update_publication_tags():
    conn = get_db_connection()
    if conn is None:
        return

    # Lấy tất cả sách
    books = conn.execute(text("SELECT id FROM publications")).fetchall()

    for book in books:
        book_id = book.id

        # Lấy topics, categories, authors liên quan
        topics = conn.execute(text("""
            SELECT t.name FROM topics t
            JOIN topic_publication pt ON pt.topic_id = t.id
            WHERE pt.publication_id = :book_id
        """), {"book_id": book_id}).fetchall()

        categories = conn.execute(text("""
            SELECT c.name FROM categories c
            JOIN category_publication pc ON pc.category_id = c.id
            WHERE pc.publication_id = :book_id
        """), {"book_id": book_id}).fetchall()

        authors = conn.execute(text("""
            SELECT a.full_name as name FROM authors a
            JOIN author_publication pa ON pa.author_id = a.id
            WHERE pa.publication_id = :book_id
        """), {"book_id": book_id}).fetchall()

        # Gộp tất cả thành list tags
        tags = [row.name for row in topics + categories + authors]
        tags_json = json.dumps(tags, ensure_ascii=False)  # Lưu kiểu JSON

        # Cập nhật cột tags
        conn.execute(text("""
            UPDATE publications SET tags = :tags_json WHERE id = :book_id
        """), {"tags_json": tags_json, "book_id": book_id})

    conn.commit()
    conn.close()
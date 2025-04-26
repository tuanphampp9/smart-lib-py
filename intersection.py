from db import get_db_connection
import pandas as pd
from collections import Counter

def jaccard_similarity(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    intersection = set1 & set2
    union = set1 | set2
    return len(intersection) / len(union) if union else 0

def fetch_recommendations_for_user(user_id, exclude_book_id=None):
    conn = get_db_connection()

    # Lấy thông tin người dùng
    query = f"SELECT interests FROM users WHERE id = '{user_id}'"
    user_df = pd.read_sql(query, conn)
    # Lấy interest của user
    user_interests = eval(user_df['interests'].values[0])

    # Lấy thông tin sách
    book_df = pd.read_sql("SELECT id, tags FROM publications", conn)
    book_df['tags'] = book_df['tags'].apply(eval)
    conn.close()
    # Tính điểm trùng lặp
    book_df['score'] = book_df['tags'].apply(lambda tags: jaccard_similarity(user_interests, tags))

    # Sắp xếp theo score giảm dần
    top_books = book_df.sort_values(by='score', ascending=False)

    # Nếu có exclude_book_id, loại ra khỏi kết quả
    if exclude_book_id is not None:
        top_books = top_books[top_books['id'] != exclude_book_id]

    # Lấy tối đa 5 sách
    top_books = top_books.head(5)
    return {
        "recommended_books": top_books['id'].tolist()
    }
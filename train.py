import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from db import get_db_connection

def fetch_latest_ratings():
    conn = get_db_connection()
    query = "SELECT user_id, publication_id, rating, created_at FROM publication_ratings"
    df = pd.read_sql(query, conn)
    conn.close()

    df['created_at'] = pd.to_datetime(df['created_at'])
    latest_ratings = df.sort_values('created_at').groupby(['user_id', 'publication_id']).last().reset_index()

    return latest_ratings

def train_model():
    df = fetch_latest_ratings()
    
    if df.empty:
        return None  # Không có dữ liệu
    
    ratings_matrix = df.pivot(index='publication_id', columns='user_id', values='rating').fillna(0)
    similarity_matrix = pd.DataFrame(cosine_similarity(ratings_matrix), index=ratings_matrix.index, columns=ratings_matrix.index)
    
    return similarity_matrix

# Khởi tạo model khi server chạy
book_similarity = train_model()

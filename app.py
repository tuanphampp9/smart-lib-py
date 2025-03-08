from flask import Flask, jsonify
from train import train_model

app = Flask(__name__)

# 🔹 Khởi tạo model rỗng
book_similarity = None

# 🔥 API gợi ý sách
@app.route('/recommendations/<int:book_id>', methods=['GET'])
def recommend_books(book_id):
    global book_similarity

    if book_similarity is None:
        return jsonify({"error": "Model not trained"}), 500
    
    if book_id not in book_similarity.index:
        return jsonify({"recommended_books": []}), 200

    # Lọc bỏ chính book_id khỏi danh sách
    similar_books = book_similarity[book_id].drop(index=book_id, errors='ignore').sort_values(ascending=False)[:5]

    return jsonify({
        "recommended_books": similar_books.index.tolist()
    })
# 🔄 API cập nhật dữ liệu & retrain
@app.route('/train', methods=['POST'])
def retrain():
    global book_similarity
    book_similarity = train_model()
    
    if book_similarity is None:
        return jsonify({"error": "No data to train"}), 500

    return jsonify({"message": "Model retrained successfully"}), 200

if __name__ == '__main__':
    print("🚀 Flask API is running on http://localhost:8000")
    app.run(host='localhost', port=8000, debug=True)

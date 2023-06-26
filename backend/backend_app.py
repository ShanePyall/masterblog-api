from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def sort_validator(data):
    if data == "title" or data == "content":
        return data
    return "Sort only accepts: title or content", 405


def direction_validator(data):
    if data != "asc" or data != "desc":
        return data
    return "Direction only accepts: asc or desc", 405


@app.route('/api/posts', methods=['GET'])
def get_posts():
    sort_data = request.args.get('sort', '')
    direction_data = request.args.get('direction', '')

    if type(sort_validator(sort_data)) == tuple:
        return sort_validator(sort_data)
    if type(direction_validator(direction_data)) == tuple:
        return direction_validator(direction_data)
    
    if sort_data == "title":
        sort_list = [post['title'] for post in POSTS]
    else:
        sort_list = [post['content'] for post in POSTS]
    if direction_data == "asc":
        sort_list.sort(key=len)
    else:
        sort_list.sort(key=len, reverse=True)
    res = [post for data in sort_list for post in POSTS if data in post.values()]
    return jsonify(res)


@app.route('/api/posts', methods=['POST'])
def add_posts():
    data = request.get_json()
    if data['title'] not in data or data['content'] not in data:
        return "Bad Request, 1 or more fields left empty", 400
    num_list = [item['id'] for item in POSTS]
    if not num_list:
        num_list.append(1)
    num_list.sort()
    new_id = (num_list[-1]) + 1
    new_dict = {'id': new_id, 'title': data['title'], 'content': data['content']}
    POSTS.append(new_dict)
    return jsonify(POSTS)


@app.route('/api/posts/<post_id>', methods=['DELETE'])
def delete_posts(post_id):
    checker = 0
    for item in POSTS:
        if item['id'] == int(post_id):
            POSTS.remove(item)
            checker += 1
    if checker == 0:
        return f"Post with id {post_id} not found", 404
    return {"message": f"Post with id {post_id} has been deleted successfully."}


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update(post_id):
    found = [post for post in POSTS if post['id'] == post_id]
    if not found:
        return f"Post with id {post_id} not found", 404
    data = request.get_json()
    found[0].update(data)
    return jsonify(found[0])


@app.route('/api/posts/search')
def search():
    title = request.args.get('title', '')
    content = request.args.get('content', '')
    results_list = []
    for post in POSTS:
        if title in post['title'] or post['title'] in title:
            results_list.append(post)
        elif content in post['content'] or post['content'] in content:
            results_list.append(post)
    if not results_list:
        return "We could not find a post with those parameters", 404
    return jsonify(results_list)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)

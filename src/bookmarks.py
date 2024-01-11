from src.constants.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from flask import Blueprint, request
from flask.json import jsonify
import validators
from flask_jwt_extended import get_jwt_identity, jwt_required
from src.database import Bookmark, db

bookmarks = Blueprint("bookmarks", __name__, url_prefix="/api/v1/bookmarks")


@bookmarks.route('/', methods=['POST', 'GET'])
@jwt_required()
def get_bookmarks():
    current_user = get_jwt_identity()
    if request.method == 'POST':
        body=request.get_json().get('body', '')
        url=request.get_json().get('url', '')

        if not validators.url(url):
            return jsonify({"error": "url is not valid"}), HTTP_400_BAD_REQUEST
        
        if Bookmark.query.filter_by(url=url).first():
            return jsonify({"error": "url already exists"}), HTTP_409_CONFLICT
        bookmark = Bookmark(url=url, body=body, user_id=current_user)
        db.session.add(bookmark)
        db.session.commit()
        return jsonify({
            "id": bookmark.id,
            "url": bookmark.url,
            "short_url": bookmark.short_url,
            "visit": bookmark.visits,
            "body": bookmark.body,
            "created_at": bookmark.created_at,
            "updated_at": bookmark.updated_at
        }), HTTP_201_CREATED
        
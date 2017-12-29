from flask import Blueprint, jsonify, request, render_template, send_file, redirect, url_for
from sqlalchemy import exc
from server.api.models import User, FileContents, Photo
from server import db, photos
from io import BytesIO


users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@users_blueprint.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        filea = request.files['inputFile']
        newFile = FileContents(name=filea.filename, data=filea.read())
        db.session.add(newFile)
        db.session.commit()

        return filea.filename

    else:
        return render_template('index.html')


@users_blueprint.route('/upload2', methods=['GET', 'POST'])
def upload2():
    if request.method == 'POST':
        filename = photos.save(request.files['inputFile'])
        url = photos.url(filename)
        newFile = Photo(filename=filename, url=url)
        db.session.add(newFile)
        db.session.commit()

        return redirect(url_for('users.show', id=newFile.id))

    else:
        return render_template('upload2.html')


@users_blueprint.route('/photo/<id>')
def show(id):
    myphoto = Photo.query.filter_by(id=id).first()
    url = photos.url(myphoto.filename)
    print('*******************************************************' + url)
    return render_template('show.html', url=url, photo=myphoto.filename)


@users_blueprint.route('/download', methods=['GET'])
def download():
    file_data = FileContents.query.filter_by(id=1).first()
    return send_file(BytesIO(file_data.data), attachment_filename='test.png')


@users_blueprint.route('/users', methods=['POST'])
def add_user():
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
    username = post_data.get('username')
    email = post_data.get('email')
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            db.session.add(User(username=username, email=email))
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': f'{email} was added!'
            }
            return jsonify(response_object), 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Sorry. That email already exists.'
            }
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400


@users_blueprint.route('/users', methods=['GET'])
def get_all_users():
    """Get all users"""
    users = User.query.all()
    users_list = []
    for user in users:
        user_object = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at
        }
        users_list.append(user_object)
    response_object = {
        'status': 'success',
        'data': {
            'users': users_list
        }
    }
    return jsonify(response_object), 200

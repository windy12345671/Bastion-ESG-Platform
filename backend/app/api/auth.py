"""
认证API路由
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import hashlib
import time

auth_bp = Blueprint('auth', __name__)

# 模拟用户数据库
users_db = {
    'admin@bastion.com': {
        'id': '1',
        'password': hashlib.sha256('admin123'.encode()).hexdigest(),
        'name': '管理员',
        'role': 'admin'
    }
}


@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')
    name = data.get('name')

    if not all([email, password, name]):
        return jsonify({'error': '缺少必填字段'}), 400

    if email in users_db:
        return jsonify({'error': '用户已存在'}), 400

    # 创建用户
    users_db[email] = {
        'id': str(int(time.time())),
        'password': hashlib.sha256(password.encode()).hexdigest(),
        'name': name,
        'role': 'user'
    }

    return jsonify({
        'message': '注册成功',
        'user': {
            'id': users_db[email]['id'],
            'email': email,
            'name': name
        }
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({'error': '缺少必填字段'}), 400

    user = users_db.get(email)
    if not user:
        return jsonify({'error': '用户不存在'}), 401

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if user['password'] != hashed_password:
        return jsonify({'error': '密码错误'}), 401

    # 生成JWT token
    access_token = create_access_token(identity=email)

    return jsonify({
        'access_token': access_token,
        'user': {
            'id': user['id'],
            'email': email,
            'name': user['name'],
            'role': user['role']
        }
    })


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required()
def refresh():
    """刷新Token"""
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify({'access_token': access_token})


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    """获取用户信息"""
    email = get_jwt_identity()
    user = users_db.get(email)

    if not user:
        return jsonify({'error': '用户不存在'}), 404

    return jsonify({
        'id': user['id'],
        'email': email,
        'name': user['name'],
        'role': user['role']
    })

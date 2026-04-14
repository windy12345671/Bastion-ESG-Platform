"""
Bastion ESG Platform - Flask Backend Application
武汉Bastion信息科技有限公司
"""

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from redis import Redis
import os
from datetime import timedelta

# 导入API路由
from app.api.auth import auth_bp
from app.api.companies import companies_bp
from app.api.assessment import assessment_bp
from app.api.report import report_bp
from app.api.data import data_bp

def create_app():
    app = Flask(__name__)

    # 配置
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'bastion-esg-secret-key-2024')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'bastion-jwt-secret')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

    # 初始化扩展
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    JWTManager(app)

    # Redis连接
    try:
        app.redis = Redis(host='localhost', port=6379, db=0, decode_responses=True)
        app.redis.ping()
    except:
        app.redis = None
        print("Warning: Redis not available, caching disabled")

    # 注册蓝图
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(companies_bp, url_prefix='/api/companies')
    app.register_blueprint(assessment_bp, url_prefix='/api/assessment')
    app.register_blueprint(report_bp, url_prefix='/api/report')
    app.register_blueprint(data_bp, url_prefix='/api/data')

    # 健康检查端点
    @app.route('/api/health')
    def health():
        return jsonify({
            'status': 'healthy',
            'platform': 'Bastion ESG Intelligence Platform',
            'company': '武汉Bastion信息科技有限公司',
            'version': '1.0.0'
        })

    # 全局错误处理
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'Endpoint not found'}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({'error': 'Internal server error'}), 500

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)

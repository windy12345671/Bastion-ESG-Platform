"""
Bastion ESG Platform - 后端服务启动脚本
武汉Bastion信息科技有限公司
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    print("=" * 60)
    print("Bastion ESG Intelligence Platform")
    print("武汉Bastion信息科技有限公司")
    print("=" * 60)
    print("API服务启动中...")
    print("访问地址: http://localhost:5000")
    print("API文档: http://localhost:5000/api/health")
    print("=" * 60)

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )

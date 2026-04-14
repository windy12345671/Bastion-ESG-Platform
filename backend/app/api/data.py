"""
数据API路由
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import random
from datetime import datetime, timedelta

data_bp = Blueprint('data', __name__)

# 行业数据
industry_data = {
    'manufacturing': {'name': '制造业', 'avg_score': 580, 'company_count': 1200},
    'finance': {'name': '金融业', 'avg_score': 650, 'company_count': 450},
    'tech': {'name': '科技业', 'avg_score': 620, 'company_count': 800},
    'energy': {'name': '能源业', 'avg_score': 550, 'company_count': 380},
    'retail': {'name': '零售业', 'avg_score': 520, 'company_count': 950},
    'service': {'name': '服务业', 'avg_score': 590, 'company_count': 720}
}


@data_bp.route('/industry/<industry_id>', methods=['GET'])
def get_industry_data(industry_id):
    """获取行业数据"""
    industry = industry_data.get(industry_id)
    if not industry:
        return jsonify({'error': '行业不存在'}), 404

    return jsonify({
        'id': industry_id,
        'name': industry['name'],
        'avg_score': industry['avg_score'],
        'company_count': industry['company_count'],
        'trend': random.uniform(-5, 10),
        'top_issues': [
            '碳排放管理',
            '供应链透明度',
            '信息披露合规'
        ]
    })


@data_bp.route('/industries', methods=['GET'])
def list_industries():
    """获取所有行业"""
    return jsonify({
        'industries': [
            {'id': k, 'name': v['name'], 'avg_score': v['avg_score']}
            for k, v in industry_data.items()
        ]
    })


@data_bp.route('/trends', methods=['GET'])
def get_esg_trends():
    """获取ESG趋势数据"""
    # 生成近12个月的趋势数据
    trends = []
    base_score = 600
    for i in range(12):
        month = (datetime.now() - timedelta(days=30 * (11 - i))).strftime('%Y-%m')
        trends.append({
            'month': month,
            'avg_score': round(base_score + random.uniform(-20, 30), 1),
            'e_score': round(base_score + random.uniform(-30, 20), 1),
            's_score': round(base_score + random.uniform(-20, 25), 1),
            'g_score': round(base_score + random.uniform(-15, 35), 1)
        })
        base_score += random.uniform(-5, 8)

    return jsonify({
        'trends': trends,
        'period': '最近12个月',
        'overall_direction': '上升'
    })


@data_bp.route('/ranking', methods=['GET'])
def get_ranking():
    """获取ESG排名"""
    industry = request.args.get('industry')
    limit = request.args.get('limit', 10, type=int)

    # 生成模拟排名数据
    rankings = []
    for i in range(limit):
        rankings.append({
            'rank': i + 1,
            'company': f'示例企业{i + 1}',
            'industry': industry or 'manufacturing',
            'score': round(950 - i * random.uniform(5, 20), 1),
            'rating': 'AAA' if i < 3 else 'AA' if i < 10 else 'A',
            'change': round(random.uniform(-5, 15), 1)
        })

    return jsonify({
        'ranking': rankings,
        'total_companies': 5000,
        'industry': industry or 'all'
    })


@data_bp.route('/comparison', methods=['POST'])
def get_comparison():
    """对比分析"""
    data = request.get_json()
    companies = data.get('companies', [])

    if len(companies) < 2:
        return jsonify({'error': '至少需要2家公司进行对比'}), 400

    comparison = {
        'companies': [],
        'metrics': ['E得分', 'S得分', 'G得分', '综合得分', '评级'],
        'analysis': {
            'strengths': '环境管理体系完善',
            'weaknesses': '信息披露透明度有待提升',
            'opportunities': '绿色金融支持力度加大',
            'threats': '监管要求日益严格'
        }
    }

    for company in companies:
        comparison['companies'].append({
            'name': company.get('name', '未知企业'),
            'scores': {
                'E': round(random.uniform(500, 900), 1),
                'S': round(random.uniform(500, 900), 1),
                'G': round(random.uniform(500, 900), 1),
                'total': round(random.uniform(500, 900), 1)
            },
            'rating': random.choice(['AAA', 'AA', 'A', 'BBB', 'BB'])
        })

    return jsonify(comparison)


@data_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """获取ESG统计数据"""
    return jsonify({
        'total_companies': 50000,
        'avg_score': 610,
        'rating_distribution': {
            'AAA': 500,
            'AA': 2500,
            'A': 8000,
            'BBB': 15000,
            'BB': 12000,
            'B': 8000,
            'CCC': 3000,
            'CC': 1000
        },
        'industry_averages': industry_data,
        'top_themes': [
            {'theme': '碳中和', 'mentions': 15000},
            {'theme': '绿色金融', 'mentions': 12000},
            {'theme': '社会责任', 'mentions': 9500},
            {'theme': '公司治理', 'mentions': 8000},
            {'theme': '供应链ESG', 'mentions': 6500}
        ]
    })


@data_bp.route('/news', methods=['GET'])
def get_news():
    """获取ESG相关资讯"""
    limit = request.args.get('limit', 10, type=int)

    news = [
        {
            'id': i,
            'title': f'ESG热点新闻 {i}：企业可持续发展新动向',
            'source': random.choice(['ESG日报', '绿色金融', '可持续商业']),
            'date': (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d'),
            'summary': '随着监管要求的提升和投资者关注度的增加，企业ESG表现日益重要...'
        }
        for i in range(limit)
    ]

    return jsonify({'news': news})


@data_bp.route('/carbon_market', methods=['GET'])
def get_carbon_market():
    """获取碳市场数据"""
    return jsonify({
        'cea_price': round(random.uniform(70, 90), 2),
        'ccer_price': round(random.uniform(30, 50), 2),
        'daily_volume': random.randint(1000000, 5000000),
        'trend': random.choice(['up', 'down', 'stable']),
        'predictions': {
            '1month': round(random.uniform(-5, 10), 1),
            '3month': round(random.uniform(-10, 15), 1),
            '1year': round(random.uniform(-15, 25), 1)
        }
    })

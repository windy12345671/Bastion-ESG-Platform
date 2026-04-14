"""
企业API路由
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import uuid
from datetime import datetime

companies_bp = Blueprint('companies', __name__)

# 模拟企业数据库
companies_db = {}


@companies_bp.route('', methods=['GET'])
def list_companies():
    """获取企业列表"""
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    industry = request.args.get('industry')

    # 过滤企业
    companies = list(companies_db.values())
    if industry:
        companies = [c for c in companies if c.get('industry') == industry]

    # 分页
    start = (page - 1) * page_size
    end = start + page_size
    paginated = companies[start:end]

    return jsonify({
        'total': len(companies),
        'page': page,
        'page_size': page_size,
        'companies': [{
            'id': c['id'],
            'name': c['name'],
            'industry': c.get('industry'),
            'rating': c.get('esg_rating'),
            'score': c.get('esg_score'),
            'created_at': c.get('created_at')
        } for c in paginated]
    })


@companies_bp.route('/<company_id>', methods=['GET'])
def get_company(company_id):
    """获取企业详情"""
    company = companies_db.get(company_id)
    if not company:
        return jsonify({'error': '企业不存在'}), 404

    return jsonify(company)


@companies_bp.route('/search', methods=['POST'])
def search_companies():
    """搜索企业"""
    data = request.get_json()
    keyword = data.get('keyword', '')
    industry = data.get('industry')
    min_score = data.get('min_score', 0)
    max_score = data.get('max_score', 1000)

    results = []
    for company in companies_db.values():
        # 关键词匹配
        if keyword and keyword.lower() not in company.get('name', '').lower():
            continue

        # 行业过滤
        if industry and company.get('industry') != industry:
            continue

        # 分数过滤
        score = company.get('esg_score', 0)
        if score < min_score or score > max_score:
            continue

        results.append(company)

    return jsonify({
        'total': len(results),
        'results': results
    })


@companies_bp.route('/import', methods=['POST'])
def import_companies():
    """批量导入企业"""
    data = request.get_json()
    companies = data.get('companies', [])

    imported = []
    for company_data in companies:
        company_id = str(uuid.uuid4())
        company = {
            'id': company_id,
            'name': company_data.get('name'),
            'industry': company_data.get('industry'),
            'description': company_data.get('description'),
            'founded_year': company_data.get('founded_year'),
            'employee_count': company_data.get('employee_count'),
            'revenue': company_data.get('revenue'),
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        companies_db[company_id] = company
        imported.append({
            'id': company_id,
            'name': company['name']
        })

    return jsonify({
        'message': f'成功导入 {len(imported)} 家企业',
        'imported': imported
    }), 201


@companies_bp.route('/<company_id>', methods=['PUT'])
def update_company(company_id):
    """更新企业信息"""
    if company_id not in companies_db:
        return jsonify({'error': '企业不存在'}), 404

    data = request.get_json()
    companies_db[company_id].update(data)
    companies_db[company_id]['updated_at'] = datetime.now().isoformat()

    return jsonify(companies_db[company_id])


@companies_bp.route('/<company_id>', methods=['DELETE'])
def delete_company(company_id):
    """删除企业"""
    if company_id not in companies_db:
        return jsonify({'error': '企业不存在'}), 404

    del companies_db[company_id]
    return jsonify({'message': '企业已删除'})

"""
ESG评估API路由
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import uuid
from datetime import datetime
from app.ml.esg_scorer import calculate_company_esg

assessment_bp = Blueprint('assessment', __name__)

# 模拟评估记录数据库
assessments_db = {}


@assessment_bp.route('/start', methods=['POST'])
def start_assessment():
    """
    启动ESG评估
    输入: 企业名称 + ESG报告/PDF/URL
    输出: 评估任务ID
    """
    data = request.get_json()

    company_name = data.get('company_name')
    industry = data.get('industry', 'manufacturing')
    report_type = data.get('report_type', 'manual')  # manual, pdf, url, esg_report
    report_data = data.get('report_data', {})

    if not company_name:
        return jsonify({'error': '企业名称不能为空'}), 400

    # 创建评估任务
    assessment_id = str(uuid.uuid4())
    assessment = {
        'id': assessment_id,
        'company_name': company_name,
        'industry': industry,
        'report_type': report_type,
        'status': 'processing',
        'created_at': datetime.now().isoformat(),
        'progress': 0
    }
    assessments_db[assessment_id] = assessment

    # 异步执行评估 (这里简化处理)
    result = calculate_company_esg({
        'name': company_name,
        **report_data
    }, industry)

    # 更新评估结果
    assessment['status'] = 'completed'
    assessment['progress'] = 100
    assessment['completed_at'] = datetime.now().isoformat()
    assessment['result'] = result

    return jsonify({
        'assessment_id': assessment_id,
        'status': 'completed',
        'result': result
    })


@assessment_bp.route('/<assessment_id>', methods=['GET'])
def get_assessment(assessment_id):
    """获取评估结果"""
    assessment = assessments_db.get(assessment_id)
    if not assessment:
        return jsonify({'error': '评估记录不存在'}), 404

    return jsonify(assessment)


@assessment_bp.route('/<assessment_id>/report', methods=['GET'])
def get_assessment_report(assessment_id):
    """获取评估报告"""
    assessment = assessments_db.get(assessment_id)
    if not assessment:
        return jsonify({'error': '评估记录不存在'}), 404

    if assessment['status'] != 'completed':
        return jsonify({'error': '评估尚未完成'}), 400

    result = assessment.get('result', {})

    # 生成报告内容
    report = {
        'company_name': result.get('company_name'),
        'industry': result.get('industry'),
        'scores': result.get('scores'),
        'rating': result.get('rating'),
        'percentile': result.get('percentile'),
        'industry_rank': result.get('industry_rank'),
        'trend': result.get('trend'),
        'details': result.get('details'),
        'recommendations': result.get('recommendations'),
        'generated_at': datetime.now().isoformat()
    }

    return jsonify(report)


@assessment_bp.route('/<assessment_id>/score', methods=['GET'])
def get_score_details(assessment_id):
    """获取评分详情"""
    assessment = assessments_db.get(assessment_id)
    if not assessment:
        return jsonify({'error': '评估记录不存在'}), 404

    if assessment['status'] != 'completed':
        return jsonify({'error': '评估尚未完成'}), 400

    result = assessment.get('result', {})

    return jsonify({
        'scores': result.get('scores'),
        'rating': result.get('rating'),
        'details': result.get('details'),
        'percentile': result.get('percentile'),
        'industry_rank': result.get('industry_rank')
    })


@assessment_bp.route('/history', methods=['GET'])
def get_assessment_history():
    """获取评估历史"""
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)

    assessments = list(assessments_db.values())
    assessments.sort(key=lambda x: x.get('created_at', ''), reverse=True)

    start = (page - 1) * page_size
    end = start + page_size
    paginated = assessments[start:end]

    return jsonify({
        'total': len(assessments),
        'page': page,
        'page_size': page_size,
        'assessments': [{
            'id': a['id'],
            'company_name': a['company_name'],
            'industry': a.get('industry'),
            'status': a['status'],
            'created_at': a['created_at'],
            'rating': a.get('result', {}).get('rating') if a['status'] == 'completed' else None
        } for a in paginated]
    })


@assessment_bp.route('/batch', methods=['POST'])
def batch_assessment():
    """批量评估"""
    data = request.get_json()
    companies = data.get('companies', [])

    results = []
    for company_data in companies:
        result = calculate_company_esg(company_data, company_data.get('industry', 'manufacturing'))
        results.append(result)

    return jsonify({
        'total': len(results),
        'results': results
    })

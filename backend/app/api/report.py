"""
报告生成API路由
"""

from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required
import uuid
from datetime import datetime
from app.ml.esg_scorer import calculate_company_esg

report_bp = Blueprint('report', __name__)

# 模拟报告数据库
reports_db = {}


@report_bp.route('/generate', methods=['POST'])
def generate_report():
    """
    生成ESG报告
    输入: 企业数据 或 评估ID
    输出: 报告ID
    """
    data = request.get_json()

    assessment_id = data.get('assessment_id')
    company_data = data.get('company_data', {})
    template = data.get('template', 'standard')  # standard, detailed, bank
    format_type = data.get('format', 'pdf')  # pdf, docx, html

    if not assessment_id and not company_data:
        return jsonify({'error': '缺少评估ID或企业数据'}), 400

    # 如果有评估ID，获取评估结果
    if assessment_id:
        company_data = {
            'name': company_data.get('name', '示例企业'),
            **company_data
        }

    # 生成报告
    report_id = str(uuid.uuid4())
    report = {
        'id': report_id,
        'assessment_id': assessment_id,
        'company_name': company_data.get('name'),
        'template': template,
        'format': format_type,
        'status': 'generating',
        'created_at': datetime.now().isoformat()
    }
    reports_db[report_id] = report

    # 模拟生成报告内容
    esg_result = calculate_company_esg(company_data, company_data.get('industry', 'manufacturing'))

    report['status'] = 'completed'
    report['completed_at'] = datetime.now().isoformat()
    report['content'] = generate_report_content(esg_result, template)

    return jsonify({
        'report_id': report_id,
        'status': 'completed',
        'download_url': f'/api/report/{report_id}/download'
    })


def generate_report_content(result: dict, template: str) -> dict:
    """生成报告内容"""
    scores = result.get('scores', {})

    content = {
        'title': f'{result.get("company_name")} ESG评估报告',
        'summary': f'''
        本报告对{result.get("company_name")}的环境、社会和治理（ESG）表现进行了全面评估。
        该企业在ESG领域获得{result.get("rating")}评级，综合得分为{scores.get("total", 0)}分，
        处于行业{round(result.get("percentile", 50))}百分位，行业排名第{result.get("industry_rank", "-")}位。
        ''',
        'scores': {
            'environmental': {
                'score': scores.get('E', 0),
                'description': '环境维度评估',
                'details': result.get('details', {}).get('environmental', {})
            },
            'social': {
                'score': scores.get('S', 0),
                'description': '社会维度评估',
                'details': result.get('details', {}).get('social', {})
            },
            'governance': {
                'score': scores.get('G', 0),
                'description': '治理维度评估',
                'details': result.get('details', {}).get('governance', {})
            }
        },
        'recommendations': result.get('recommendations', []),
        'generated_at': datetime.now().isoformat()
    }

    if template == 'detailed':
        content['sections'] = [
            {'title': 'Executive Summary', 'content': content['summary']},
            {'title': 'ESG评分详解', 'content': str(scores)},
            {'title': '环境绩效', 'content': str(content['scores']['environmental'])},
            {'title': '社会绩效', 'content': str(content['scores']['social'])},
            {'title': '治理绩效', 'content': str(content['scores']['governance'])},
            {'title': '改进建议', 'content': str(content['recommendations'])}
        ]

    if template == 'bank':
        content['sections'].append({
            'title': '银行评估补充',
            'content': f'''
            根据银行ESG评估标准，该企业的风险等级为{
                '低风险' if scores.get('total', 0) > 700 else '中等风险' if scores.get('total', 0) > 400 else '高风险'
            }。
            建议关注：{result.get('recommendations', [{}])[0].get('suggestion', '无')}
            '''
        })

    return content


@report_bp.route('/<report_id>', methods=['GET'])
def get_report(report_id):
    """获取报告内容"""
    report = reports_db.get(report_id)
    if not report:
        return jsonify({'error': '报告不存在'}), 404

    return jsonify(report)


@report_bp.route('/<report_id>/download', methods=['GET'])
def download_report(report_id):
    """下载报告"""
    report = reports_db.get(report_id)
    if not report:
        return jsonify({'error': '报告不存在'}), 404

    if report['status'] != 'completed':
        return jsonify({'error': '报告生成中'}), 400

    # 返回JSON格式的报告内容 (实际可转换为PDF/DOCX)
    return jsonify({
        'message': '报告已生成',
        'report': report,
        'download_format': report.get('format', 'pdf')
    })


@report_bp.route('/template', methods=['POST'])
def create_template():
    """创建自定义模板"""
    data = request.get_json()

    template_id = str(uuid.uuid4())
    template = {
        'id': template_id,
        'name': data.get('name'),
        'description': data.get('description'),
        'sections': data.get('sections', []),
        'created_at': datetime.now().isoformat()
    }

    return jsonify(template), 201


@report_bp.route('/templates', methods=['GET'])
def list_templates():
    """获取模板列表"""
    templates = [
        {
            'id': 'standard',
            'name': '标准报告',
            'description': '适用于一般企业的ESG评估报告'
        },
        {
            'id': 'detailed',
            'name': '详细报告',
            'description': '包含完整分析和建议的详细报告'
        },
        {
            'id': 'bank',
            'name': '银行评估版',
            'description': '针对银行金融机构的ESG评估报告'
        }
    ]

    return jsonify({'templates': templates})

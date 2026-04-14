# API模块初始化
from .auth import auth_bp
from .companies import companies_bp
from .assessment import assessment_bp
from .report import report_bp
from .data import data_bp

__all__ = ['auth_bp', 'companies_bp', 'assessment_bp', 'report_bp', 'data_bp']

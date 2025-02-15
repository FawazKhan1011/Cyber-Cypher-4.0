from flask import Blueprint
from .auth_controller import register, login

auth_bp = Blueprint('auth', __name__)

auth_bp.route('/register', methods=['POST'])(register)
auth_bp.route('/login', methods=['POST'])(login)
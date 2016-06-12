from flask import jsonify

def make_error(status_code, sub_code, message, action, errors=None):
    errors = errors or {}
    response = jsonify({
        'status': status_code,
        'sub_code': sub_code,
        'message': message,
        'action': action,
        'errors': errors
    })
    response.status_code = status_code
    return response
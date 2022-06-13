from data.models import db
from data import models
from .utils import *

from datetime import datetime
import flask
from flask import request, Blueprint

app = Blueprint('api', __name__)


@app.route('/register', methods=['POST'])
def register():
    """
    Register user:
        {
            "login":
        }
    """
    content = request.json
    login = content.get("login", '')
    if not validate_login(login):
        return flask.jsonify({'error': 'login should contain between 3 and 128 symbols'}), 400
    user = models.User(login=login)
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        return flask.jsonify({'error': 'internal error: {}'.format(str(e))}), 500
    return flask.jsonify({'OK': 'created user with login {}'.format(login)}), 201


@app.route('/fetch_new_messages', methods=['PUT'])
def fetch_new_messages():
    """
    Fetch new messages from sender to recipient:
        {
            "sender": sender login
            "recipient": recipient login
        }

    :returns
    {
        "messages": [
            {
                "sender": sender login
                "recipient": recipient login
                "timestamp": timestamp
                "message": message text
            }
        ]
    }
    """
    content = request.json
    sender_login = content.get('sender', '')
    sender = models.User.query.filter_by(login=sender_login).first()
    if not sender:
        return flask.jsonify({'error': 'user with login {} not found'.format(sender_login)}), 400

    recipient_login = content.get('recipient', '')
    recipient = models.User.query.filter_by(login=recipient_login).first()
    if not recipient:
        return flask.jsonify({'error': 'user with login {} not found'.format(recipient_login)}), 400

    try:
        messages = models.Messages.query.filter_by(is_read=False, sender=sender.id, recipient=recipient.id).all()
        result = []
        for message in messages:
            result.append({
                "sender": sender.login,
                "recipient": recipient.login,
                "timestamp": message.timestamp,
                "message": message.content
            })
            message.is_read = True

        db.session.commit()
    except Exception as e:
        return flask.jsonify({'error': 'internal error: {}'.format(str(e))}), 500

    return flask.jsonify({'messages': result}), 200


@app.route('/fetch_messages', methods=['PUT'])
def fetch_messages():
    """
    Fetch messages from sender to recipient:
        {
            "sender": sender login
            "recipient": recipient login
            "period_start": period start timestamp
            "period_end": period end timestamp
        }

    :returns
    {
        "messages": [
            {
                "sender": sender login
                "recipient": recipient login
                "timestamp": timestamp
                "message": message text
            }
        ]
    }
    """
    content = request.json
    sender_login = content.get('sender', '')
    sender = models.User.query.filter_by(login=sender_login).first()
    if not sender:
        return flask.jsonify({'error': 'user with login {} not found'.format(sender_login)}), 400

    recipient_login = content.get('recipient', '')
    recipient = models.User.query.filter_by(login=recipient_login).first()
    if not recipient:
        return flask.jsonify({'error': 'user with login {} not found'.format(recipient_login)}), 400

    period_start = datetime.fromisoformat(content['period_start'])
    period_end = datetime.fromisoformat(content['period_end'])

    messages = db.session.query(models.Messages).filter(
        models.Messages.timestamp.between(period_start, period_end)) \
        .order_by(models.Messages.timestamp).all()

    result = []
    for message in messages:
        result.append({
            "sender": sender.login,
            "recipient": recipient.login,
            "timestamp": message.timestamp,
            "message": message.content
        })
        message.is_read = True

    db.session.commit()

    return flask.jsonify({'messages': result}), 200


@app.route('/send_message', methods=['POST'])
def send_message():
    """
    Send from sender to recipient:
        {
            "sender": sender login
            "recipient": recipient login
            "message": message
        }
    """
    content = request.json
    sender_login = content.get('sender', '')
    sender = models.User.query.filter_by(login=sender_login).first()
    if not sender:
        return flask.jsonify({'error': 'user with login {} not found'.format(sender_login)}), 400

    recipient_login = content.get('recipient', '')
    recipient = models.User.query.filter_by(login=recipient_login).first()
    if not recipient:
        return flask.jsonify({'error': 'user with login {} not found'.format(recipient_login)}), 400

    message = models.Messages(sender=sender.id, recipient=recipient.id,
                              content=content["message"])
    db.session.add(message)
    db.session.commit()

    return flask.jsonify({'OK': 'message sent successfully'}), 201


@app.route('/delete_messages', methods=['DELETE'])
def delete_messages():
    """
    Delete messages from sender to recipient:
        {
            "sender": sender login
            "recipient": recipient login
            "timestamps": [message timestamps]
        }
    """
    content = request.json
    sender_login = content.get('sender', '')
    sender = models.User.query.filter_by(login=sender_login).first()
    if not sender:
        return flask.jsonify({'error': 'user with login {} not found'.format(sender_login)}), 400

    recipient_login = content.get('recipient', '')
    recipient = models.User.query.filter_by(login=recipient_login).first()
    if not recipient:
        return flask.jsonify({'error': 'user with login {} not found'.format(recipient_login)}), 400

    timestamps = list(map(lambda timestamp: datetime.fromisoformat(timestamp), content["timestamps"]))

    delete_q = models.Messages.__table__.delete().where(models.Messages.timestamp.in_(timestamps))
    db.session.execute(delete_q)
    db.session.commit()

    return flask.jsonify({'OK': 'messages deleted'}), 201


@app.route('/delete_message', methods=['DELETE'])
def delete_message():
    """
    Delete message from sender to recipient:
        {
            "sender": sender login
            "recipient": recipient login
            "timestamp": message timestamp
        }
    """
    content = request.json
    sender_login = content.get('sender', '')
    sender = models.User.query.filter_by(login=sender_login).first()
    if not sender:
        return flask.jsonify({'error': 'user with login {} not found'.format(sender_login)}), 400

    recipient_login = content.get('recipient', '')
    recipient = models.User.query.filter_by(login=recipient_login).first()
    if not recipient:
        return flask.jsonify({'error': 'user with login {} not found'.format(recipient_login)}), 400

    timestamp = datetime.fromisoformat(content["timestamp"])

    if not sender or not recipient:
        return flask.jsonify({'error': 'login not found'}), 400

    message = db.session.query(models.Messages).filter(models.Messages.timestamp == timestamp)
    if not message.first():
        return "message not found"
    else:
        message.delete()

    db.session.commit()

    return flask.jsonify({'OK': 'message deleted'}), 201


@app.route('/health', methods=['GET'])
def health():
    response = app.response_class(
        status=200,
    )
    return response

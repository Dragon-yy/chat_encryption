from application import manage, socketio
from flask_script import Server
from www import app

manage.add_command('runserver', Server(host='0.0.0.0', port=app.config['SERVER_PORT'], use_debugger=True, threaded=True))
manage.add_command('runserver', socketio.run(app=app, host='0.0.0.0', port=app.config['SERVER_PORT'])) # 新加入的代码，重写manager的run命令

def main():
    manage.run()


if __name__ == '__main__':
    try:
        import sys
        sys.exit(main())
    except Exception as e:
        import traceback
        traceback.print_exc()
#  set ops_config=local&&python manager.py runserver

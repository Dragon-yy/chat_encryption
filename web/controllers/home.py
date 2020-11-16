from flask import Blueprint, render_template, request, flash, jsonify, sessions
from flask_login import login_required, current_user
from common.models.User import Post, User
from config import local_setting
from utils.database_connection_pool import OPMysql
# from utils.encryption import Encryption
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP, PKCS1_v1_5
import json
from application import socketio
import urllib
import base64

route_home = Blueprint('home', __name__)
route_user = Blueprint('user_posts', __name__)
target_name = ''  # 要发送的目标
user_sid = []
count = 0
mysqlInfo = {
    'host': local_setting.HOST,
    'port': local_setting.PORT,
    'user': local_setting.USER,
    'passwd': local_setting.PASSWD,
    'db': local_setting.DATABASE
}
# 申请资源
opm = OPMysql(mysqlInfo)


@route_home.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('index.html', currentUser=current_user.login_name)


@route_home.route('/data1', methods=['GET', 'POST'])  # 路由
@login_required
def data1():
    if request.method == 'POST':
        print('++' * 100)
        print('post')
        info = json.loads(request.form.get('data'))  # 获取前端传来的数据
        user = info.get('content').replace(' ', '').replace('\n', '')
        print(user)
        sql = "select login_name, avatar from user where login_name='%s'" % (user)
        data = opm.op_select(sql)
        for i in range(len(data)):
            data[i]['avatar'] = '../static/user_pics/' + data[0]['avatar']
    if request.method == 'GET':
        print('++' * 100)
        print('get')
        pass
    return jsonify({'data': data})


@route_home.route('/data2', methods=['GET', 'POST'])  # 路由
@login_required
def data2():
    if request.method == 'POST':
        print('++' * 100)
        print('post2')
        info = json.loads(request.form.get('data'))  # 获取前端传来的数据
        ip = info.get('ip')
        name = info.get('target_name')
        print(ip)
        print('目标' + name)
        global target_name
        target_name = name

    if request.method == 'GET':
        print('++' * 100)
        print('get2')
        pass
    return jsonify({'data': 'success'})


@socketio.on("login")
@login_required
def quotations_func(mes):
    """客户端连接"""
    print('客户端连接')
    print(mes)
    sid = request.sid  # io客户端的sid, socketio用此唯一标识客户端.
    print('客户端sid')
    print(sid)
    with open('utils/my_rsa_public.pem', 'r') as file:
        PUBLIC_KEY = file.read()

    global user_sid
    # 有用户连接先判断user_sid里是否已记录了该用户，
    # 如果已经记录就覆盖原先的sid，如果没有就添加该用户
    if len(user_sid) == 0:  # 第一个用户先添加
        user_sid.append({'user': mes['user'], 'sid': sid})
    else:
        flag = True
        for i in range(len(user_sid)):
            if user_sid[i]['user'] == mes['user']:  # 该用户已存在于列表中
                user_sid[i] = {'user': mes['user'], 'sid': sid}
                flag = False
        if flag:  # 如果没找到该用户就添加
            user_sid.append({'user': mes['user'], 'sid': sid})

    print(user_sid)
    can = False
    host = request.host
    host_list = ['127.0.0.1']
    """
    根据页面的访问地址决定是否允许连接, 你可以自己实现自己对访问的控制逻辑.
    最后决定是允许连接还是使用socketio.server.disconnect(sid)断开链接.
    """
    if host in host_list:
        can = True
    elif host.startswith("192.168") or host.startswith("172") or host.startswith("local"):
        can = True
    else:
        pass
    if can:
        print('允许连接')
        socketio.emit(event="login",
                      data=json.dumps({"message": "connect success!", "sid": sid, "PUBLIC_KEY": PUBLIC_KEY}))
    else:
        print('拒绝连接')
        socketio.emit(event="login", data=json.dumps({"message": "connect refuse!"}))
        socketio.server.disconnect(sid)


# @route_home.route("/listen", methods=['post', 'get'])
@socketio.on('listen')
@login_required
def listen_func(data):
    """"监听发送来的消息,并使用socketio向所有客户端发送消息"""
    sender_sid = request.sid
    global user_sid
    for i in range(len(user_sid)):
        if user_sid[i]['user'] == data['user']:
            user_sid[i] = {'user': data['user'], 'sid': sender_sid}

    print(data)
    value = data['data']
    value = value.replace('%u', '\\u')  # 将%uxxxx 替换换 \uxxxx 这才可以进行utf-8解码
    byts = urllib.parse.unquote_to_bytes(value)  # 返回的 byte
    data['data'] = byts.decode('unicode-escape')  # decode UTF-8 解码只能解开 \uXXXX 的Unicode 标准形式
    print(data['data'])

    default_length = 128
    private_key = RSA.import_key(
        open("utils/my_private_rsa_key.bin").read(),
        passphrase='123456'
    )
    encrypt_byte = base64.b64decode(data['data'].encode())
    length = len(encrypt_byte)
    cipher_rsa = PKCS1_v1_5.new(private_key)
    if length < default_length:
        decrypt_byte = cipher_rsa.decrypt(data['data'], None)
    else:
        offset = 0
        res = []
        while length - offset > 0:
            if length - offset > default_length:
                res.append(cipher_rsa.decrypt(encrypt_byte[offset: offset +
                                                                   default_length], 'failure'))
            else:
                res.append(cipher_rsa.decrypt(encrypt_byte[offset:], 'failure'))
            offset += default_length
        decrypt_byte = b''.join(res)
    data['data'] = decrypt_byte.decode()
    print(data['data'])
    value = data['data']
    value = value.replace('%u', '\\u')  # 将%uxxxx 替换换 \uxxxx 这才可以进行utf-8解码
    byts = urllib.parse.unquote_to_bytes(value)  # 返回的 byte
    data['data'] = byts.decode('unicode-escape')  # decode UTF-8 解码只能解开 \uXXXX 的Unicode 标准形式
    print(data['data'])

    mes = {"message": "unknown error"}
    # data = request.args['data'] if request.args.get('data') else request.form.get('data')
    # sid = request.args['sid'] if request.args.get('sid') else request.form.get('sid')
    print(sender_sid)
    print(user_sid)
    '''
    两种逻辑实现chat 
    1.向除了自己的所有人发送信息
    2.找到要发送用户对应的sid向该用户（sid）发送信息 
    '''
    '''
    方法一
    '''
    # if data is not None:
    #     if sender_sid == user_sid[0]['sid']:
    #         print('a')
    #         print(user_sid[1]['sid'])
    #         socketio.emit(data=data, event="mes", room=user_sid[1]['sid'])  # js客户端on绑定的就是这个event的事件
    #         mes['message'] = "success"
    #     else:
    #         print('b')
    #         print(user_sid[0]['sid'])
    #         socketio.emit(data=data, event="mes", room=user_sid[0]['sid'])  # js客户端on绑定的就是这个event的事件
    #         mes['message'] = "success"
    # else:
    #     pass

    # sql = "select avatar from user where login_name='%s'" % (data['target'])
    # avatar = '../static/user_pics/' + opm.op_select(sql)[0]['avatar']
    '''
    方法二
    '''
    data['target'] = data['target'].replace(' ', '').replace('\n', '')
    if data is not None:
        for i in range(len(user_sid)):
            print('sender' + data['user'])
            print('target' + data['target'])
            if data['target'] == user_sid[i]['user']:
                # data.update({'target_avatar': avatar})
                socketio.emit(data=data, event="mes", room=user_sid[i]['sid'])  # js客户端on绑定的就是这个event的事件
                mes['message'] = "success"
    else:
        pass
    return json.dumps(mes)

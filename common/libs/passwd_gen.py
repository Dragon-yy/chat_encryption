import base64
from hashlib import md5


def passwd_gen( pwd, salt ):
    m = md5()
    pwd_gen = '%s-%s'%(base64.encodebytes(pwd.encode('utf-8')), salt)
    m.update(pwd_gen.encode('utf-8'))
    return m.hexdigest()


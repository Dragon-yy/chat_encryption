$(function () {
    var url = "http://" + document.domain + ':' + location.port;
    var sid;
    console.log(url);
    var io_client = io.connect(url);
    var user = $('#user').text();
    var PUBLIC_KEY;  //后端传来的公钥
    io_client.on('connect', function () {
        console.log('connect');
        // 连接成功时的事件
        io_client.emit('login', {data: 'I\'m connected!', user: user});
    });
    io_client.on("login", function (resp) {
        // 绑定的事件, 对应py文件中的event参数的值
        var resp = JSON.parse(resp);
        sid = resp['sid'];
        PUBLIC_KEY = resp['PUBLIC_KEY'];
        // console.log(sid)
    });
    io_client.on("mes", function (resp) {
        // 绑定的事件, 对应py文件中的event参数的值
        console.log('response');
        console.log(resp['data']);

        var target = $('.chat__person').text();
        console.log(target)
        var target_avatar;
        var data = {
            data: JSON.stringify({
                content: target,
            })
        };
        $.ajax({
            type: "post",
            url: "data1",
            data: data,
            dataType: "json",
            cache: false,
            async: false,
            success: function (json) {
                console.log('url提交成功');
                // console.log($("#retShow"))
                console.log(json['data']);
                if (json['data'].length === 0) {
                    alert('未找到该用户')
                }
                for (var i = 0; i < json['data'].length; i++) {
                    target_avatar = json['data'][i]['avatar'];
                    console.log(target_avatar);
                    // $('#u1').text(login_name)
                }
            }
        });

        $('#chat_msgRow').append(
            ' <div class="chat__msgRow">\n' +
            '               <img src=' + target_avatar + ' alt="" class="contact_chat_photo"/>' +
            '                <div class="chat__message notMine">' + resp['data'] + '</div>\n' +
            '</div>'
        );
    });

    $(document).on("click", ".chat__back", function (event) {
        $('#chat_msgRow').empty();
        io_client.disconnect(url)
    });

    $(document).on("click", ".contact", function (event) {
        io_client.connect(url)
    });

    // 回车触发按钮点击事件
    $(document).keyup(function (event) {
        if (event.keyCode == 13) {
            $("#submit").trigger("click");
        }
    });
    // 发送按钮事件
    $("#submit").click(function (event) {
        var user = $('#user').text();
        var target = $('.chat__person').text();
        console.log(user);
        console.log(target);
        var content = $('#msg').val();
        // socket.emit('my event', {data: content});
        // 如果用户提交数据为空拒绝提交
        if (content === "") {
            // nothing...
        } else {
            var avatar;
            var data = {
                data: JSON.stringify({
                    content: user,
                })
            };
            $.ajax({
                type: "post",
                url: "data1",
                data: data,
                dataType: "json",
                cache: false,
                async: false,
                success: function (json) {
                    console.log('url提交成功');
                    // console.log($("#retShow"))
                    console.log(json['data']);
                    if (json['data'].length === 0) {
                        alert('未找到该用户')
                    }
                    for (var i = 0; i < json['data'].length; i++) {
                        avatar = json['data'][i]['avatar'];
                        console.log(avatar);
                        // $('#u1').text(login_name)
                    }
                }
            });


            $('#chat_msgRow').append(
                ' <div class="chat__msgRow">\n' +
                '               <img src=' + avatar + ' alt="" class="contact_chat_photo" style="float: right"/>' +
                '                <div class="chat__message mine">' + content + '</div>\n' +
                '</div>'
            );
            console.log(content);
            console.log(escape(content));
            console.log(sid);

            var encrypt = new JSEncrypt();
            encrypt.setPublicKey(PUBLIC_KEY);
            let ciphertext = encrypt.encrypt(escape(content));

            // 公钥加密
            // console.log(PUBLIC_KEY);
            // let ciphertext = rsaUtil.encrypt(escape(content), PUBLIC_KEY);
            // console.log("公钥加密后：" + ciphertext);
            //私钥解密
            // let plaintext = rsaUtil.decrypt(ciphertext, keyPair.privateKey);


            io_client.emit('listen', {data: escape(ciphertext), user: user, target: target});
            $("#msg").val("");  // 清空输入内容
        }
    });
});

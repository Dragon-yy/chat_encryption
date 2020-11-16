function searchUser(obj) {
    //1键盘抬起时获得输入框的内容
    //alert(obj.value);
    var content = $(obj).val();
    //2根据输入框的内容去数据库中模糊查询---List<Product>
    console.log(content);
    var data = {
        data: JSON.stringify({
            content: content,
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
            if (json['data'].length===0){
                alert('未找到该用户')
            }
            for (var i = 0; i < json['data'].length; i++) {
                var avatar = json['data'][i]['avatar'];
                var login_name = json['data'][i]['login_name'];
                console.log(avatar);
                console.log(login_name);
                // $('#u1').text(login_name)
                $('#users').append(
                    '<div class="contact">\n' +
                    '            <img src='+avatar+' alt="" class="contact__photo"/>\n' +
                    '            <span id="u1" class="contact__name">' + login_name + '</span>\n' +
                    '            <span class="contact__status online"></span>\n' +
                    '</div>'
                )
            }
        }
    });

}

// function searchWord(obj) {
//        //1键盘抬起时获得输入框的内容
//        //alert(obj.value);
//        var word = $(obj).val();
//        //2根据输入框的内容去数据库中模糊查询---List<Product>
//        var content = "";
//        $.ajax({
//            url:"${pageContext.request.contextPath}/searchWord",
//            type:"POST",
//            contentType: "application/x-www-form-urlencoded; charset=utf-8",
//            data:{"word":word},
//            success:function (data) {
//                //3将返回的商品名称显示在showDiv中
//                if (data.length>0){
//                    for (var i = 0;i<data.length;i++){
//                        content+="<div style='padding: 5px;cursor: pointer' οnclick='clickFn(this)' οnmοuseοver='overFn(this)' οnmοuseοut='outFn(this)'>"+data[i]+"</div>";
//                    }
//                    $("#showDiv").html(content);
//                    $("#showDiv").css("display","block");
//                }
//            },
//            dataType:"json",
//            }
//
//        );
//
//    }

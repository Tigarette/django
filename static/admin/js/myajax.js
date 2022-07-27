function GetInfo(){
    var param ={
        "username": $('#username').val(),
        "password": $('#password').val(),
    };
    $.ajax({
        type: "POST",
        data: param,
        cache: false,
        async: true,
        datatype: 'text',
        success: function (data) {
            if(data == "登录成功"){
                window.location.href = "/draw/";
            }else{
                document.getElementById("error_msg").innerHTML = "<i class='nav-icon fas fa-exclamation-triangle'></i>" + data;
            }
        },
        error: function() {
            alert ("请刷新后重试！");
        }
    })
}
function register(){
    var param = {
        "username": $('#username').val(),
        "nick_name": $('#nick_name').val(),
        "password": $('#password').val(),
        "re_password": $('#re_password').val(),
        "email": $('#email').val(),
        "code": $('#code').val(),
    }
    $.ajax({
        type: "POST",
        data: param,
        cache: false,
        async: true,
        datatype: 'text',
        success:function (data){
            if(data == "all_empty"){
                var result = "<i class='nav-icon fas fa-exclamation-triangle'></i>用户名或密码或邮箱为空,请检查是否输入!"
                document.getElementById("error").innerHTML = result;
            }else if(data == "password_error"){
                var result = "<i class='nav-icon fas fa-exclamation-triangle'></i>两次输入密码不同,请检查是否相同!"
                document.getElementById("error").innerHTML = result;
            }else if(data == "have_username"){
                var result = "<i class='nav-icon fas fa-exclamation-triangle'></i>该用户名已注册!"
                document.getElementById("error").innerHTML = result;
            }else if(data == "have_email"){
                var result = "<i class='nav-icon fas fa-exclamation-triangle'></i>该邮箱已绑定账户!"
                document.getElementById("error").innerHTML = result;
            }else if(data == "less_password"){
                var result = "<i class='nav-icon fas fa-exclamation-triangle'></i>密码需要大于等于六位数!"
                document.getElementById("error").innerHTML = result;
            }else if(data == "not_code"){
                var result = "<i class='nav-icon fas fa-exclamation-triangle'></i>验证码不正确!"
                document.getElementById("error").innerHTML = result;
            } else if(data == "success"){
                window.location.href = "/draw/login/";
            }
        },
        error: function (){
            alert ("请刷新后重试！")
        }
    })
}
function logout(){
    $.ajax({
        url: "/draw/logout/",
        type: "POST",
        cache: false,
        async: true,
        datatype: 'text',
        success:function (data){
            if(data == "success"){
                window.location.href = "/draw/";
            }
        },
        error:function (){
            alert("请刷新后重试")
        }
    })
}
function AddNewDraw(){
    var param = {
        "draw_name": $('#draw_name').val(),
        "human_num": $('#human_num').val(),
        "boom_num": $('#boom_num').val(),
    }
    $.ajax({
        type: "POST",
        cache: false,
        async: true,
        datatype: 'text',
        data:param,
        success: function (data){
            if(data == "success"){
                alert("添加成功");
                window.location.href = "/draw/detail/";
            }else if(data == "less_human"){
                document.getElementById("error_msg").innerHTML = "<i class='nav-icon fas fa-exclamation-triangle'></i>参与人数不得少于奖励数量!"
            }else if(data == "empty"){
                document.getElementById("error_msg").innerHTML = "<i class='nav-icon fas fa-exclamation-triangle'></i>可能存在尚未填写的内容!"
            }else if(data == "less_num"){
                document.getElementById("error_msg").innerHTML = "<i class='nav-icon fas fa-exclamation-triangle'></i>参与人数或奖励数量不得少于1!"
            }else if(data == "same_name"){
                document.getElementById("error_msg").innerHTML = "<i class='nav-icon fas fa-exclamation-triangle'></i>已有相同名称的主题!"
            }
        },
        error:function (){
            alert("请刷新后重试");
        }
    })
}
function AddNewPower(){
    var add_draw = document.getElementById("add_draw").checked ? "yes" : "no";
    var add_power = document.getElementById("add_power").checked ? "yes" : "no";
    var param = {
        "username": $('#username').val(),
        "add_draw": add_draw,
        "add_power": add_power,
    }
    $.ajax({
        type: "POST",
        cache: false,
        async: true,
        datatype: 'text',
        data:param,
        success: function (data){
            if(data == "success"){
                alert("添加成功")
                window.location.href = "/draw/";
            }else if(data == "nobody"){
                document.getElementById("error_msg").innerHTML = "<i class='nav-icon fas fa-exclamation-triangle'></i>该用户不存在!"
            }else if(data == "name_empty"){
                document.getElementById("error_msg").innerHTML = "<i class='nav-icon fas fa-exclamation-triangle'></i>用户名为空!"
            }else if(data == "no_choice"){
                document.getElementById("error_msg").innerHTML = "<i class='nav-icon fas fa-exclamation-triangle'></i>请选择要赋予的权限,不然来干嘛!"
            }
        },
        error: function (){
            alert("请刷新后重试")
        }
    })
}
function DrawView(s,e){
    var choice_id = s;
    var param = {
        "choice_id": choice_id,
    }
    $.ajax({
        type: "POST",
        cache: false,
        async: true,
        datatype: 'text',
        data:param,
        success: function (data){
            if(data == "success"){
                document.getElementById(s).disabled = true;
                var url = "/draw/" + e + "/draw/";
                window.location.href = url;
            }else if(data == "is_choice"){
                alert("你已经选择过一个选项了,请勿再次选择,不过你要看的话管不着.")
            }
        },
        error: function (){
            alert("请刷新后重试")
        }
    })
}
function EmailRight(){
    $.ajax({
        type: "POST",
        data: {
            "email": $('#email').val(),
            "type": "register",
        },
        cache: false,
        async: true,
        datatype: 'text',
        url: "/draw/sendemail/",
        success: function (data){
            if(data == "success"){
                document.getElementById("code_code").innerHTML = "<input type=\"text\" class=\"form-control\" placeholder=\"验证码\" autocomplete=\"off\" id=\"code\">"
            }
            if(data == "empty"){
                document.getElementById("error").innerHTML = "<i class='nav-icon fas fa-exclamation-triangle'></i>邮箱为空,检查是否输入!"
            }else if(data == "not_email"){
                document.getElementById("error").innerHTML = "<i class='nav-icon fas fa-exclamation-triangle'></i>邮箱格式错误!"
            }else if(data == "have_user"){
                document.getElementById("error").innerHTML = "<i class='nav-icon fas fa-exclamation-triangle'></i>该邮箱已被注册!"
            }
        },
        error: function (){
            alert("请刷新后重试")
        }
    })
}
function ForgetPsw(){
    var param = {
        "username": $('#username').val(),
        "password": $('#password').val(),
        "re_password": $('#re_password').val(),
        "email": $('#email').val(),
        "code": $('#code').val(),
    }
    $.ajax({
        type: "POST",
        data: param,
        cache: false,
        async: true,
        datatype: 'text',
        success:function (data){
            if(data == "success"){
                alert("修改成功")
                window.location.href = "/draw/login/";
            }else if(data == "all_empty"){
                document.getElementById("error_msg").innerHTML = "<i class='nav-icon fas fa-exclamation-triangle'></i>可能存在尚未填写的内容!"
            }else if(data == "password_error"){
                document.getElementById("error_msg").innerHTML = "<i class='nav-icon fas fa-exclamation-triangle'></i>两次密码输入不一致!"
            }else if(data == "no_username"){
                document.getElementById("error_msg").innerHTML = "<i class='nav-icon fas fa-exclamation-triangle'></i>该用户不存在!"
            }else if(data == "no_email"){
                document.getElementById("error_msg").innerHTML = "<i class='nav-icon fas fa-exclamation-triangle'></i>该用户绑定的邮箱输入错误!"
            }else if(data == "less_password"){
                document.getElementById("error_msg").innerHTML = "<i class='nav-icon fas fa-exclamation-triangle'></i>密码不得少于六位数!"
            }else if(data == "not_code"){
                document.getElementById("error_msg").innerHTML = "<i class='nav-icon fas fa-exclamation-triangle'></i>验证码错误!"
            }
        },
        error: function (){
            alert ("请刷新后重试！")
        }
    })
}
function EmailRightTwo(){
    $.ajax({
        type: "POST",
        data: {
            "email": $('#email').val(),
            "type": "forget",
        },
        cache: false,
        async: true,
        datatype: 'text',
        url: "/draw/sendemail/",
        success: function (data){
            if(data == "success"){
                document.getElementById("code_code").innerHTML = "<input type=\"text\" class=\"form-control\" placeholder=\"验证码\" autocomplete=\"off\" id=\"code\">"
            } else if(data == "empty"){
                document.getElementById("error_msg").innerHTML = "<i class='nav-icon fas fa-exclamation-triangle'></i>邮箱为空,检查是否输入!"
            }else if(data == "not_email"){
                document.getElementById("error_msg").innerHTML = "<i class='nav-icon fas fa-exclamation-triangle'></i>邮箱格式错误!"
            }
        },
        error: function (){
            alert("请刷新后重试")
        }
    })
}
// 新添加
function ChangePsw(){
    if(!$('#code').val()){
        var param = {
            "username": $('#username').val(),
            "old_password": $('#old_password').val(),
            "new_password": $('#new_password').val(),
            "email": $('#email').val(),
            "code": '',
        }
    }else {
        var param = {
            "username": $('#username').val(),
            "old_password": $('#old_password').val(),
            "new_password": $('#new_password').val(),
            "email": $('#email').val(),
            "code": $('#code').val(),
        }
    }
    $.ajax({
        type: "POST",
        data: param,
        cache: false,
        async: true,
        datatype: 'text',
        success: function (data){
            if(data == "success"){
                alert("修改成功")
                window.location.href = "/draw/login/"
            } else if(data == "empty"){
                document.getElementById("error_msg").innerHTML = "<i class='nav-icon fas fa-exclamation-triangle'></i>旧密码未输入!"
            }else if(data == "error_psw"){
                document.getElementById("error_msg").innerHTML = "<i class='nav-icon fas fa-exclamation-triangle'></i>旧密码错误!"
            }else if(data == "less_psw"){
                document.getElementById("error_msg").innerHTML = "<i class='nav-icon fas fa-exclamation-triangle'></i>新密码长度不得小于6!"
            }else if(data == 'same'){
                document.getElementById("error_msg").innerHTML = "<i class='nav-icon fas fa-exclamation-triangle'></i>两次密码相同,真的要改吗?"
            }else if(data == 'code_error'){
                document.getElementById("error_msg").innerHTML = "<i class='nav-icon fas fa-exclamation-triangle'></i>验证码错了哦!"
            }else if(data == 'no_change'){
                alert("无修改")
                window.location.href = "/draw/";
            }else if(data == 'change_psw'){
                alert("修改成功")
                window.location.href = "/draw/login/"
            }else if(data == 'change_email'){
                alert("修改成功")
                window.location.href = "/draw/";
            }
        },
        error: function (){
            alert("请刷新后重试")
        }
    })
}
// 新添加
function EmailRightThree(){
    $.ajax({
        type: "POST",
        data: {
            "username": $('#username').val(),
            "email": $('#email').val(),
            "type": "change",
        },
        cache: false,
        async: true,
        datatype: 'text',
        url: "/draw/sendemail/",
        success: function (data){
            if(data == "success"){
                document.getElementById("code_code").innerHTML = "<input type=\"text\" class=\"form-control\" placeholder=\"验证码\" autocomplete=\"off\" id=\"code\">"
            } else if(data == "empty"){
                document.getElementById("error_msg").innerHTML = "<i class='nav-icon fas fa-exclamation-triangle'></i>邮箱为空,检查是否输入!"
            }else if(data == "not_email"){
                document.getElementById("error_msg").innerHTML = "<i class='nav-icon fas fa-exclamation-triangle'></i>邮箱格式错误!"
            }else if(data == "have_user"){
                document.getElementById("error_msg").innerHTML = "<i class='nav-icon fas fa-exclamation-triangle'></i>该邮箱已被绑定!"
            }
        },
        error: function (){
            alert("请刷新后重试")
        }
    })
}
function UpdateLog(){
    var have_log = $('#have_log').val();
    var not_log = $('#not_log').val();
    if(typeof (not_log) == "undefined"){
        var msg = 1;
    }else{
        var msg = 0;
    }
    $.ajax({
        type: "POST",
        data: {
            "have_log":$('#have_log').val(),
            "not_log":$('#not_log').val(),
            "msg":msg,
        },
        cache: false,
        async: true,
        datatype: 'text',
        success: function (data){
            if(data == "success"){
                document.getElementById("error_msg").innerHTML = "修改成功"
            }
        },
        error: function (){
            alert("请刷新后重试")
        }
    })
}
function AddLikes(liked_id,like_id){
    $.ajax({
        type: "POST",
        data: {
            "liked_id":liked_id,
            "like_id":like_id,
            "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val(),
        },
        cache: false,
        async: true,
        datatype: 'text',
        url:'/draw/addLike/',
        success: function (data){
            if(data == "not_login"){
                alert("请先登录");
            }
            var data = data.split('+');
            if(data[0] == "like"){
                document.getElementById(liked_id).className = "fa-solid fa-thumbs-up"
                document.getElementById(liked_id + "999").innerHTML = data[1]
            }else if (data[0] == "not_like") {
                document.getElementById(liked_id).className = "fa-regular fa-thumbs-up"
                document.getElementById(liked_id + "999").innerHTML = data[1]
            }
        },
        error: function (){
            alert("请刷新后重试")
        }
    })
}

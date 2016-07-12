function register() {
    var username = $('#username').val()
    var password = $('#password').val()
    var repeat_password = $('#repeat_password').val()
    var email = $('#email').val()

    if (username == "") {
        alert('请填写用户名！')
        return false
    }
    if (email == "") {
        alert('请填写邮箱！')
        return false
    }
    if (password == "") {
        alert('请填写密码！')
        return false
    }
    if (repeat_password == "") {
        alert('请再次填写密码！')
        return false
    }
    if (password != repeat_password) {
        alert('两次填写的密码不一致！')
        return false
    }
    $.post('/register',
        {
        username:username,
        password:password,
        repeat_password:repeat_password,
        email:email
        },
        function (result, status) {
            if (result == 'success') {
                alert('注册成功！')
            }
            else if(result == 'error1') {
                alert('两次输入的密码不一致！')
                location.reload()
            }
            else if(result == 'error2') {
                alert('用户名或者邮箱已存在，请重新输入！')
                location.reload()
            }
        }
    )
}
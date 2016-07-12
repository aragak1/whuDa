function check_mail(mail) {
    var filter  = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/

    if (filter.test(mail))
        return true
    else
        return false
}

function check_username(username) {
    var matchstr = /^[a-z][a-z_0-9]*$/i;
    if (matchstr.test(username))
        return true
    else
        return false
}

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
    if (!check_mail(email)) {
        alert('请输入正确的邮箱！')
        location.reload()
    }
    if (!check_username(username)) {
        alert('请输入正确的用户名，只能字母，下划线和数字且必须以字母开头。')
        location.reload()
    }
    $.post('/register',
        {
            username:username,
            password:password,
            repeat_password:repeat_password,
            email:email
        },function (result) {
            if (result == 'success') {
                alert('注册成功！')
                location.href = '/'
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

function login() {
    var username = $('#l_username').val()
    var password = $('#l_password').val()
    var login_type = ''

    if (check_mail(username))
        login_type = 'email'
    else
        login_type = 'username'

    $.post('/login',{
        username:username,
        password:password,
        login_type:login_type
    },function (result) {
            if (result == 'success'){
                location.href = '/'
            }
            else {
                alert('用户名或密码错误！')
                location.reload()
            }
        }
    )
}
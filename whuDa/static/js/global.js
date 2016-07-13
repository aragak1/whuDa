function register() {
    var username = $('#username').val()
    var password = $('#password').val()
    var repeat_password = $('#repeat_password').val()
    var email = $('#email').val()
    
    $.post('/register',
        {
            username:username,
            password:password,
            repeat_password:repeat_password,
            email:email
        },function (result) {
            if (result == 'error1') {
                alert('用户名不能为空')
            }
            else if (result == 'error2') {
                alert('邮箱不能为空')
            }
            else if (result == 'error3') {
                alert('密码不能为空')
            }
            else if (result == 'error4') {
                alert('请再次确认密码')
            }
            else if (result == 'error5') {
                alert('两次输入的密码不一致！')
                location.reload()
            }
            else if (result == 'error6') {
                alert('用户名必须以字母开头')
            }
            else if (result == 'error7') {
                alert('邮箱名非法，请正确填写')
            }
            else if (result == 'error8') {
                alert('用户名或者邮箱已存在，请重新输入！')
                location.reload()
            }
            else {
                alert('注册成功！')
                location.href = '/'
            }
        }
    )
}

function login() {
    var username = $('#l_username').val()
    var password = $('#l_password').val()
    $.post('/login',{
        username:username,
        password:password,
    },function (result) {
            if (result == 'error1')
            {
                alert('用户名不能为空')
            }
            else if (result == 'error2')
            {
                alert('密码不能为空')
            }
            else if (result == 'success'){
                location.href = '/'
            }
            else {
                alert('用户名或密码错误！')
                location.reload()
            }
        }
    )
}

$('#aw_edit_topic_title').bind('input propertychange', function () {
    var text = $('#aw_edit_topic_title').val()
    alert(text)
})
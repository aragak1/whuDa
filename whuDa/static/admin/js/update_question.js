var editor
$(document).ready(function () {
     editor = new wangEditor('update_question_content');
        editor.config.menus =     [
        'source',
        'bold',
        'underline',
        'italic',
        'strikethrough',
        'eraser',
        'quote',
        'head',
        'unorderlist',
        'orderlist',
        'link',
        'unlink',
        'table',
        'img',
        'insertcode',
        'undo',
        'redo',
        'fullscreen'
    ];
    editor.create();
});
function submit(){
    var title = $('update_question_title').val()
    var content =  editor.$txt.html();
    var topics = new Array()
    $('a.text').each(function () {
        topics.push($(this).text())
    });

    $.post(window.location.href.slice(19),{
        title:title,
        content:content
    },function (status) {
        if (status == 'empty_title') {
            alert('标题不能为空')
        }
        else if (status == 'empty_topics') {
            alert('至少应该选择一个话题')
        }
        else if(status == 'empty_content') {
            alert('请填写回复内容')
        }
        else{
            alert('发布成功')
            location.href = '/admin/questions'
        }
    });
    $.post(window.location.href.slice(19));
}

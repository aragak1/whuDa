$(document).ready(function () {
    //判断是否有通知
    var ul=$('#notifications_list');
    if(ul.children().length==0){
        ul.append('<p style="padding: 15px 0" align="center">没有通知哦</p>')
    //查看更多
    $('#notifications_more').remove();
    $('#notifications_more').hide();
    var page=0;
    $('#notifications_more').onClick(function(){
        page++;
        var option='more';
        $.post('/notifications',{
            option,
            page
            },function(json){
            alter(json);
        });
    })
}

});
function has_read(this_element,notification_id){
    var option='has_read';
    var notification_id=notification_id;
    $.post('/notifications',{
    option,
    notification_id
    },function(text){
    this_element.text(text);
    location.reload(true);
    });
}
function remove_notification(this_element,notification_id){
    var option='delete';
    var notification_id=notification_id;
    this_element.parent().parent().remove();
    $.post('/notifications',{
    option,
    notification_id
    },function(text){
    this_element.text(text);
    location.reload(true) ;
    });
}
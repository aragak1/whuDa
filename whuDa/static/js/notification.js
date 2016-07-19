var notifications_list
var page=0;
var notification_more
var read_all
var unread_num=0
$(document).ready(function () {

    get_more();
    //alert("I am an alert box!!");
    notifications_list=$('#notifications_list');
    notification_more=$('#notifications_more');
    read_all=$('#unread_notification_num');
    //alert($('#notifications_list').text());
    //判断是否有未读通知

    //查看更多
    //alert("I am an alert box!!");
    //alert(page);
    notification_more.click(function(){
        //alert(page);
        get_more();
    });

});
function has_read(this_element,notification_id){
    var option='has_read';
    var notification_id=notification_id;
    var list=this_element.parent().parent();
    if(list.hasClass("active")){
        unread_num-=1;
        refresh_read_all();
        list.removeClass("active");
    }
    else{
        unread_num+=1;
        refresh_read_all();
        list.addClass("active");
    }
    $.post('/notifications',{
    'option':option,
    'notification_id':notification_id
    },function(text){
    this_element.text(text);
    });
}
function remove_notification(this_element,notification_id){
    var option='delete';
    var notification_id=notification_id;
    var list=this_element.parent().parent();
    if(list.hasClass("active")){
        unread_num-=1;
        refresh_read_all();
    }
    list.remove();
    $.post('/notifications',{
    'option':option,
    'notification_id':notification_id
    });
}
function refresh_read_all(){
    if(unread_num==0){
        read_all.text("全部通知已读");
    }
    else{
        read_all.text("有"+unread_num+"条未读通知");
        //alert(unread_num+"read_all:"+read_all.text());
        read_all.hover(function(){
            read_all.text("全部标记为已读");
        },function(){
            refresh_read_all();
        });
        read_all.click(function(){
            if(unread_num==0)return
            //alert(unread_num);
            var option='read_all';
            read_all.text("全部通知已读");
            unread_num=0;
            $('li').removeClass("active");
            $('.has_read').text("标记为未读");
            $.post('/notifications',{
            'option':option
            });
        });
    }
}
function get_more(){
var post_url = '/notifications.json';
    $.post(post_url,{'page_num':page},function(datas){
        //alert(datas);
        var more=datas.more;
        unread_num=datas.unread;
        //alert("unread_num:"+unread_num);

        //alert(unread_num+"read_all:"+read_all.text());
        refresh_read_all();
        page+=1
        //alert("page_num:"+page);
        if(more==1){
            notification_more.text("更多");
            notification_more.removeClass("disabled");
        }
        else{
            notification_more.text("没有更多了哦！");
            notification_more.addClass("disabled");
        }
        $.each(datas.notifications,function(i,item){
            var dom
            if(item.is_read==0){
                dom="<li class=\"active\">";
            }
            else{
                dom="<li>";
            }
            dom+="<p class=\"moreContent\">"+
                "<a href=\"question/"+item.quesion_id+"\">"+item.question_title+"</a>"+
                item.content+
                "<a href=\"user/"+item.sender_uid+"\">"+item.sender_name+"</a>"+
                "<span class=\"icon-tips\"></span>"+
                "</p>"+
                "<p class=\"text-color-999\">"+
                item.past_time+
                "<a class=\"read pull-right has_read\" onclick=\"has_read($(this),"+item.notification_id+")\">";
            if(item.is_read==0){
                dom+="标记为已读";
            }
            else{
                dom+="标记为未读";
            }
            dom+="</a>"+
            "<a class=\"read pull-right delete\" onclick=\"remove_notification($(this),"+item.notification_id+")\">删除</a>"+
            "</p>"+
            "</li>";
            //alert(dom);
            notifications_list.append(dom);
        })
    },"json");
}

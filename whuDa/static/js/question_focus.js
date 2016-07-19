var page=0;
var all_focus_more
var all_focus_list
$(document).ready(function () {

    get_more();
    //alert("I am an alert box!!");
    all_focus_more=$('#all_focus_more');
    all_focus_list=$('#main_contents');
    //alert(all_focus_more);
    //查看更多
    //alert("I am an alert box!!");
    //alert(page);
    all_focus_more.click(function(){
        //alert(page);
        get_more();
    });

});
function get_more(){
var post_url = '/all_focus.json';
    $.post(post_url,{'page_num':page},function(datas){
        //alert(datas);
        var more=datas.more;
        //alert("more:"+more);
        page+=1;
        if(more==1){
            all_focus_more.text("更多");
            all_focus_more.removeClass("disabled");
        }
        else{
            all_focus_more.text("没有更多了哦！");
            all_focus_more.addClass("disabled");
        }
        $.each(datas.all_focus,function(i,item){
            //alert("json");
            var dom="<div class=\"aw-item\">"+
            "<div class=\"mod-head\">"+
            "<a class=\"aw-user-img aw-border-radius-5\" href=\"/people/"+item.username+"\"><img src=\"/static/common/avatar-mid-img.png\" alt=\""+item.username+"\"></a>"+
            "<p class=\"text-color-999\">"+
            "<a href=\"/question/"+item.question_id+"\" class=\"text-color-999\">"+item.c_answer+" 个回复</a>"+
            "•"+
            "<a href=\"/question/"+item.question_id+"\" class=\"text-color-999\">添加话题</a>"+
            "</p>"+
            "<h4><a href=\"/question/"+item.question_id+"\">"+item.question_name+"</a></h4>"+
            "</div>"+
            "</div>";
            //alert(dom);
            all_focus_list.append(dom);
        })
    },"json");
}
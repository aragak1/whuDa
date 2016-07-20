$(function()
{
	//侧边栏话题编辑记录收缩
	$('.topic-edit-notes .icon-down').click(function() {
		if (!$(this).parents('.topic-edit-notes').find('.mod-body').is(':visible'))
		{
			$(this).parents('.topic-edit-notes').find('.mod-body').fadeIn();
			$(this).addClass('active');
		}
		else
		{
			$(this).parents('.topic-edit-notes').find('.mod-body').fadeOut();	
			$(this).removeClass('active');
		}
	});
});
function switch_focus(this_element){
    //如果已关注 取消关注
    var topic_id=topic_detail_page_topic_id;
    if(this_element.hasClass('active')){
        this_element.children('span').text("关注");
        this_element.removeClass('active');
        this_element.children('b').text(Number(this_element.children('b').text())-1);
        $.post('/topic/cancel_focus',{'topic_id':topic_id});
    }
    //如果未关注 添加关注
    else{
        var topic_id=topic_detail_page_topic_id;
        this_element.children('span').text("取消关注");
        this_element.addClass('active');
        this_element.children('b').text(Number(this_element.children('b').text())+1);
        $.post('/topic/add_focus',{'topic_id':topic_id});
    }
}
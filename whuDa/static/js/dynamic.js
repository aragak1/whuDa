function focus_topic(this_element,topic_id){
    //alert(topic_id);
    //添加关注
    //var topic_id=topic_detail_page_topic_id;
    this_element.parents('dd').first().append('<p class="icon-inverse follow tooltips iconp"">您已关注</p>');
    this_element.addClass('active');
    $.post('/topic/add_focus',{'topic_id':topic_id});
}
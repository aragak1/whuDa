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
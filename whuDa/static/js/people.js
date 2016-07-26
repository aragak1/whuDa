$(document).ready(function () {
	if (window.location.hash)
	{
		if (document.getElementById(window.location.hash.replace('#', '')))
		{
			document.getElementById(window.location.hash.replace('#', '')).click();
		}
	}
	
	$('.aw-tabs li').click(function() {
		$(this).addClass('active').siblings().removeClass('active');
		
		$('#focus .aw-user-center-follow-mod').eq($(this).index()).show().siblings().hide();
	});
});
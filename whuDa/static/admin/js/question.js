function delete_question(this_element,question_id){
    alert(this_element.text()+question_id);
    $.post('/question/delete_question',
    {'question_id':question_id});
    this_element.parent().parent().remove();
}
function get_page(this_element){
    var this_parent=this_element.parent();
    var active=this_parent.parent().find('.active');
    if (this_parent.hasClass('disabled')){
        alert('disabled');
        return
    }
    else if (this_parent.hasClass('active')){
        alert('active');
        alert(Number(this_element.text()));
        return;
    }
    else if(this_parent.hasClass('previous')){
        this_parent.parent().children('.next').removeClass('disabled');
        alert('previous');
        page=Number(active.children('a').text())-1;
        $.post('/admin/questions',{'page':page},function(datas){
            $('tbody').empty();
            $.each(datas,function(i,item){
                var html_doc="<tr><td>"+item.id+"</td><td>"+item.title+"</td><td>"+item.content+"</td>"+
                "<td><p><button type=\"button\" class=\"btn btn-outline btn-primary\">修 改</button></p></td>"+
                "<td><button type=\"button\" class=\"btn btn-outline btn-danger\" onclick=\"delete_question($(this),"+item.id+")\">删 除</button></td></tr>";
                alert(html_doc);
                $('tbody').append(html_doc);
            });
            if(!active.prev().hasClass('previous')){
                active.prev().addClass('active');
                active.removeClass('active');
                active=active.prev();
            }
        },'json');
        alert(page);
        return;
    }
    else if(this_parent.hasClass('next')){
        this_parent.parent().children('.previous').removeClass('disabled');
        alert('next');
        page=Number(active.children('a').text())+1;
        $.post('/admin/questions',{'page':page},function(datas){
            $('tbody').empty();
            $.each(datas,function(i,item){
                var html_doc="<tr><td>"+item.id+"</td><td>"+item.title+"</td><td>"+item.content+"</td>"+
                "<td><p><button type=\"button\" class=\"btn btn-outline btn-primary\">修 改</button></p></td>"+
                "<td><button type=\"button\" class=\"btn btn-outline btn-danger\" onclick=\"delete_question($(this),"+item.id+")\">删 除</button></td></tr>";
                alert(html_doc);
                $('tbody').append(html_doc);
            });
            if(!active.next().hasClass('next')){
                active.next().addClass('active');
                active.removeClass('active');
                active=active.next();
            }
        },'json');
        alert(page);
        return;
    }
    else{
        alert(this_element.text());
        page=Number(this_element.text());
        this_parent.parent().children('.disabled').removeClass('disabled');
        $.post('/admin/questions',{'page':page},function(datas){
            $('tbody').empty();
            $.each(datas,function(i,item){
                var html_doc="<tr><td>"+item.id+"</td><td>"+item.title+"</td><td>"+item.content+"</td>"+
                "<td><p><button type=\"button\" class=\"btn btn-outline btn-primary\">修 改</button></p></td>"+
                "<td><button type=\"button\" class=\"btn btn-outline btn-danger\" onclick=\"delete_question($(this),"+item.id+")\">删 除</button></td></tr>";
                alert(html_doc);
                $('tbody').append(html_doc);
            });
            active.removeClass('active');
            active=this_parent;
            active.addClass('active');
            if(active.next().hasClass('next')){
                active.next().addClass('disabled');
            }
            else if(active.prev().hasClass('previous')){
                active.prev().addClass('disabled');
            }
        },'json');
    }
}
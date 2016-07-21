function deleteTopic(obj) {
    var r = confirm("确定要删除这个话题吗？请谨慎操作!");
    if (r == true) {
        var topic_id = obj.getAttribute('data-topicId')
        $.post('/admin/topic/delete', {
            'topic_id':topic_id
        }, function (result) {
            if (result == 'success') {
                alert('删除成功！');
                location.reload();
            } else if (result == 'error') {
                alert('删除失败!');
            } else if (result == 'not_null') {
                alert('话题下问题数不为0，无法删除!');
            }
        })
    } else {
        location.reload()
    }
}
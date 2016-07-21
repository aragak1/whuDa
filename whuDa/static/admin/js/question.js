function delete_question(this_element,question_id){
    alert(this_element.text()+question_id);
    $.post('/question/delete_question',
    {'question_id':question_id});
    this_element.parent().parent().remove();
}
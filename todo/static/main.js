function first_todo(userid){
        $.get('/firstitem/'+userid, function(resp){
	data = resp.split(';');
	console.log(resp);
	$('.first-todo h2').html(data[0]);
	$('.first-todo h5').html(data[1]);
	});
}

function deletebutton(){
	console.log('loaded')
	$(".todo-list, .shopping-list").on("click", ".delete-btn", function() {
	console.log('delete btn clicked');
	link = $(this).parent().attr('action');
	$(this).closest("li").remove();
	event.preventDefault();
	$.post(link);
	if ($('.todo-list li').length==0){
		$('.first-todo').remove();
	}
	console.log(link[link.length-1]);
	userid=link.split('/')[4];
	first_todo(userid);
});		
}

function tick(){
	console.log('tickfunction')
	$(".todo-list, .shopping-list").on("click", ".tickitem", function() {
	link = $(this).closest('form').attr('action');
	if ($(this).is(':checked')){
		link=link+'checked';
		$(this).parent().css('text-decoration','line-through');
		$(this).parent().next().html('');
	} else {
		link=link+'none';
		$(this).parent().css('text-decoration','');
		$(this).parent().next().html('Overdue');
	}
	$.post(link);
	userid=link.split('/')[4];
	console.log(userid);
	first_todo(userid);
});		
}

$(deletebutton);
$(tick);



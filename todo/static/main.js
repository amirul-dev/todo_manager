function deletebutton(){
	console.log('loaded')
	$(".todo-list, .shopping-list").on("click", ".delete-btn", function() {
	console.log('delete btn clicked');
	link = $(this).parent().attr('action');
	console.log(link);
	$(this).closest("li").remove();
	event.preventDefault();
	$.post(link);
	if ($('.todo-list li').length==0){
		$('.first-todo').remove();
	}
});		
}

function tick(){
	console.log('tickfunction')
	$(".todo-list, .shopping-list").on("click", ".tickitem", function() {
	link = $(this).closest('form').attr('action');
	if ($(this).is(':checked')){
		link=link+'checked';
		$(this).parent().css('text-decoration','line-through');
	} else {
		link=link+'none';
		$(this).parent().css('text-decoration','');
	}
	$.post(link);
});		
}

$(deletebutton);
$(tick);



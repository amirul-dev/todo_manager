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

$(deletebutton);


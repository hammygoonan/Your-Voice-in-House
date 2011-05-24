$(document).ready(function(){
	// accordion bit
	$('.primary_member_details').toggle(
		function(){
			$(this).next('.seconday_member_details').slideDown();
		},
		function(){
			$(this).next('.seconday_member_details').slideUp();
		}
	);
	$('.seconday_member_details').css('display', 'none');
	$('.primary_member_details').css('cursor', 'pointer');
	
	// form validation
	$('#MemberEmailForm').validate();
	$('.terms').click(function(){
		$('.dialog').dialog({
			modal: true,
			title: 'Terms & Conditions',
			width: 800,
			height: 600
		});
		$.post('/yvih2/members/terms', function(data){
			$('.dialog').html(data);
		});
		return false;
	});
	
	// ajax search
	
	var input_value = Array();
	var hidden_value = Array();;
	
	$('#MemberMember').autocomplete({		
		source: function(request, response){
			var term = request.term.split(',');
			$.get('/yvih2/members/ajax_autocomplete/' + $.trim(term[term.length - 1]), function(data){
				response($.map(data, function(item){
					return{
						label: item.Member.first_name + ' ' + item.Member.second_name + " (" + item.Electorate.name + ')',
						value: item.Member.id
					}
				}));
			}, 'json');
		},
		select: function( event, ui ){
			// update what is displayed in the text box
			
			input_value.push(ui.item.label);
			for(var i in input_value){
				if(i == 0){
					var input_display = input_value[i];
				}
				else{
					input_display = input_display + ', ' + input_value[i];
				}
			}
			$('#MemberMember').val(input_display);
			
			//update what is displayed in the hidden field
			
			hidden_value.push(ui.item.value);
			for(var i in hidden_value){
				if(i == 0){
					var input_hidden = hidden_value[i];
				}
				else{
					input_hidden = input_hidden + ',' + hidden_value[i];
				}
			}
			$('#MemberId').val(input_hidden);

			return false;
		},
		dataType: 'json',
		minLength: 2
	});
}); // end ready

 jQuery.validator.addMethod("multiemail", function(value, element) {
                    if (this.optional(element)) {
                        return true;
                    }
                    var emails = value.split( new RegExp( "\\s*,\\s*", "gi" ) );
                    valid = true;
                    for(var i in emails) {
                        value = emails[i];
                        valid=valid && jQuery.validator.methods.email.call(this, value,element);
                    }
                    return valid;}, "Invalid email format");

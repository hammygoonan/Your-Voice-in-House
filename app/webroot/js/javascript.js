var root = '/yvih2/';

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
	$('#ApiSignupForm').validate();
	$('.terms').click(function(){
		$('.dialog').dialog({
			modal: true,
			title: 'Terms & Conditions',
			width: 800,
			height: 600
		});
		$.post(root + 'members/terms', function(data){
			$('.dialog').html(data);
		});
		return false;
	});
	
	// ajax search
	
	var input_value = Array();
	var hidden_value = Array();;
	
	// member_autocomplete
	if($('#MemberMember').length > 0){ // if we are on the first page
		$.get(root + 'members/ajax_autocomplete/', function(data){
			var results = $.map(data, function(item){
				return{
					label: item.Member.first_name + ' ' + item.Member.second_name + " (" + item.Electorate.name + ')',
					value: item.Member.id
				}
			});
			
			$('#MemberMember').autocomplete({		
				source: results,
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
			dataType: 'json'
		});	
		}, 'json');
	}
	
	
	//electorate Autocomplete
	if($('#MemberElectorate').length > 0){ // if we are on the first page
		$.get(root + 'electorates/ajax_autocomplete/', function(data){
			var electorates = $.map(data, function(item){
				return{
					label: item.Electorate.name + ' (' + item.House.name + ', ' + item.House.state + ')',
					value: item.Electorate.id
				}
			});
			$('#MemberElectorate').autocomplete({
				source: electorates,
				select: function( event, ui ){
					// update what is displayed in the text box
					
					$('#MemberElectorate').val(ui.item.label);
					
					//update what is displayed in the hidden field
					$('#MemberElectorateId').val(ui.item.value);
		
					return false;
				},
				dataType: 'json'
				}, 'json');
		});
	}
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
	return valid;},
	"Invalid email format");

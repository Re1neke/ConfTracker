{{!write_modal}}
<script type="text/javascript">
	% if id: 
		fillAttendeeForm({{id}});
	% end
	loadForm({{!'"/api/attendees/{}"'.format(id) if id else '"/api/attendees"'}}, "attendee_form", {{!'"PUT"' if id else '"POST"'}}, attendeeFormToJSON, formResponse);
</script>
<form id="attendee_form" class="data_form">
	<h2>Attendee</h2>
	<div class=info></div>
	<div class="data_block">
		<div class="data_col">
			<div class="data_box">
				First name<span>*</span>: <input type="text" name="name">
			</div>
			<div class="data_box">
				Last name<span>*</span>: <input type="text" name="surname">
			</div>
		</div>
		<div class="data_col">
			<div class="data_box">
				Organization:
				<input type="text" name="organization">
			</div>
			<div class="data_box">
				Degree:
				<input type="text" name="degree">
			</div>
		</div>
	</div>
	<br>
	<div class="check_block">
		<div class="data_col">
			<div class="check_box">
				<input type="checkbox" name="is_activated"> Activated
			</div>
		</div>
	</div>
	<h2>Sections</h2>
	<div class="check_block">
		<div class="data_col">
			% for section in sections[:len(sections) // 2]: 
			<div class="check_box">
				<input type="checkbox" name="{{section["id"]}}"> {{section["name"]}}
			</div>
			% end
		</div>
		<div class="data_col">
			% for section in sections[len(sections) // 2:]: 
			<div class="check_box">
				<input type="checkbox" name="{{section["id"]}}"> {{section["name"]}}
			</div>
			% end
		</div>
	</div>
	<input type="submit" value="Submit">
</form>
<script type="text/javascript">setOnchangeForm("attendee_form", {{"false" if id else "true"}});</script>
<button class="big_write_button">Write card</button>

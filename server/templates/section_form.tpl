<script type="text/javascript">
	% if id: 
		fillSectionForm({{id}}); 
	% end
	loadForm({{!'"/api/sections/{}"'.format(id) if id else '"/api/sections"'}}, "section_form", {{!'"PUT"' if id else '"POST"'}}, sectionFormToJSON, formResponse);
</script>
<form id="section_form" class="data_form">
	<h2>Section</h2>
	<div class=info></div>
	<div class="data_block">
		<div class="data_col">
			<div class="data_box">
				Name<span>*</span>:
				<input type="text" name="name">
			</div>
		</div>
		<div class="data_col">
			<div class="data_box">
				Building<span>*</span>:
				<input type="text" name="building">
			</div>
			<div class="data_box">
				Room<span>*</span>:
				<input type="text" name="room">
			</div>
		</div>
	</div>
	<input type="submit" value="Submit">
</form>
<script type="text/javascript">setOnchangeForm("section_form", false);</script>

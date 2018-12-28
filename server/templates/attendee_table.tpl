{{!write_modal}}
<div class="table">
	<h2>List of Attendees</h2>
	<table id="attendee_table" class="data_table"></table>
</div>
<script type="text/javascript">
	updateAttendees();
	var attendeesUpdater = setInterval(updateAttendees, 3000);
</script>

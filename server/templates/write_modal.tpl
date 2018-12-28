<div id="write_modal" class="modal">
	<div class="modal_msg">
		<div class="modal_header"><img src="/card.svg" alt="card">WRITE USERDATA TO CARD<div class="close">&times;</div></div>
		<div class="modal_body"><span id="modal_text">Attach card to NFC module</span></div>
		<div class="modal_ok">OK</div>
	</div>
</div>
<script type="text/javascript">
	var write_modal = document.getElementById('write_modal');
	var close_button = write_modal.getElementsByClassName("close")[0];
	var ok_button = write_modal.getElementsByClassName("modal_ok")[0];
	close_button.addEventListener("click", closeWriteModal);
	ok_button.addEventListener("click", closeWriteModal);
</script>
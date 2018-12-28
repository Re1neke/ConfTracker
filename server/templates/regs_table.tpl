<div class="table">
	<h2>Registered on "{{section["name"]}}"</h2>
	<table id="reg_table" class="data_table"></table>
</div>
<script type="text/javascript">
	var  updateFunc = updateRegs({{section["id"]}});
	updateFunc();
	var regUpdater = setInterval(updateFunc, 3000);
</script>

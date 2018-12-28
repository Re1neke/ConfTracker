<!DOCTYPE html>
<html>
<head>
<title>{{title}} | Conf Tracker</title>
<link rel="stylesheet" type="text/css" href="/styles.css">
<script type="text/javascript" src="/scripts.js"></script>
</head>
<body>
<div id="sidebar">
	<ul class="menu">
		<li>
			<a href="/attendees">Attendees</a>
			<ul class="submenu">
				<li><a href="/attendees/add">Add attendee</a>
			</ul>
		</li>
		<li>
			<a href="/sections">Sections</a>
			<ul class="submenu">
				<li><a href="/sections/add">Add section</a>
			</ul>
		</li>
	</ul>
</div>
<div id="body">
	% if show_searchbox:
	<form action="#" id="searchbar">
		<input type="text" placeholder="Filter" name="search">
		<!-- <button type="submit">Submit</button> -->
	</form>
	% end
	{{!body}}
</div>
</body>
</html>
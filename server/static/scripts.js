
function updateTableData(uri, tableHandler) {
	var xhttp = new XMLHttpRequest();
	xhttp.addEventListener("load", function(event) {
		var data = JSON.parse(event.target.responseText);
		tableHandler(data);
	});
	xhttp.open("GET", uri, true);
	xhttp.send();
}

function refreshTable(tableId, addTableHeaderHandler, addTableRowHandler, tableData) {
	var tableObj = document.getElementById(tableId);
	while (tableObj.firstChild)
		tableObj.removeChild(tableObj.firstChild);
	// if (tableData.length == 0)
	// 	noData(tableObj);
	// else {
		addTableHeaderHandler(tableObj);
		tableData.forEach(addTableRowHandler(tableObj));
	// }
}

function noData(tableObj) {
	tr = document.createElement("tr");
	td = document.createElement("td");
	td.appendChild(document.createTextNode("NO DATA"));
	tr.appendChild(td);
	tableObj.appendChild(tr);
}

function addRowToAttendeeTable(tableObj) {
	return function(attendeeData) {
		tr = document.createElement("tr");
		td = document.createElement("td");
		img = document.createElement("img");
		img.classList.add("attendee_status");
		if (parseInt(attendeeData["is_activated"]) == 1) {
			img.setAttribute("title", "Activated");
			img.src = "/check.svg";
			img.alt = "activated";
		}
		td.appendChild(img);
		tr.appendChild(td);
		td = document.createElement("td");
		td.appendChild(document.createTextNode(attendeeData["name"] + " " + attendeeData["surname"]));
		tr.appendChild(td);
		td = document.createElement("td");
		td.appendChild(document.createTextNode(attendeeData["organization"]));
		tr.appendChild(td);
		td = document.createElement("td");
		td.appendChild(document.createTextNode(attendeeData["degree"]));
		tr.appendChild(td);
		td = document.createElement("td");
		a = document.createElement("a");
		a.classList.add("edit_button");
		a.setAttribute("title", "Edit");
		a.href = `/attendees/${attendeeData["id"]}/edit`;
		td.appendChild(a);
		tr.appendChild(td);
		td = document.createElement("td");
		button = document.createElement("button");
		button.classList.add("write_button");
		button.setAttribute("title", "Write card");
		if (Boolean(attendeeData["card_written"]))
			button.classList.add("written_button");
		else
			button.classList.add("unwritten_button");
		button.onclick = writeCard(attendeeData["id"]);
		td.appendChild(button);
		tr.appendChild(td);
		tableObj.appendChild(tr);
	};
}

function addHeaderToAttendeeTable(tableObj) {
	tr = document.createElement("tr");
	th = document.createElement("th");
	th.setAttribute("title", "Activated");
	th.appendChild(document.createTextNode("Act."));
	tr.appendChild(th);
	th = document.createElement("th");
	th.appendChild(document.createTextNode("Name"));
	tr.appendChild(th);
	th = document.createElement("th");
	th.appendChild(document.createTextNode("Org."));
	th.setAttribute("title", "Organization");
	tr.appendChild(th);
	th = document.createElement("th");
	th.appendChild(document.createTextNode("Degree"));
	tr.appendChild(th);
	th = document.createElement("th");
	th.style = "width: 32px";
	tr.appendChild(th);
	th = document.createElement("th");
	th.style = "width: 32px";
	tr.appendChild(th);
	tableObj.appendChild(tr);
}

function updateAttendees() {
	updateTableData("/api/attendees", function(tableData) {
		refreshTable("attendee_table", addHeaderToAttendeeTable, addRowToAttendeeTable, tableData);
	});
}

function addRowToRegTable(tableObj) {
	return function(attendeeData) {
		tr = document.createElement("tr");
		td = document.createElement("td");
		img = document.createElement("img");
		img.classList.add("attendee_status");
		if (parseInt(attendeeData["status"]) == 2) {
			img.setAttribute("title", "Came in");
			img.src = "/entrance.svg";
			img.alt = "came in";
		} else if (parseInt(attendeeData["status"]) == 3) {
			img.setAttribute("title", "Came out");
			img.src = "/exit.svg";
			img.alt = "came out";
		} else {
			// img.setAttribute("title", "Not present");
			//img.src = "/not_present.svg";
			//img.alt = "not present";
		}
		td.appendChild(img);
		tr.appendChild(td);
		td = document.createElement("td");
		td.appendChild(document.createTextNode(attendeeData["name"] + " " + attendeeData["surname"]));
		tr.appendChild(td);
		td = document.createElement("td");
		td.appendChild(document.createTextNode(attendeeData["organization"]));
		tr.appendChild(td);
		td = document.createElement("td");
		td.appendChild(document.createTextNode(attendeeData["degree"]));
		tr.appendChild(td);
		td = document.createElement("td");
		a = document.createElement("a");
		a.classList.add("edit_button");
		a.href = `/attendee/${attendeeData["id"]}/edit`;
		a.setAttribute("title", "Edit");
		td.appendChild(a);
		tr.appendChild(td);
		tableObj.appendChild(tr);
	};
}

function addHeaderToRegTable(tableObj) {
	tr = document.createElement("tr");
	th = document.createElement("th");
	th.appendChild(document.createTextNode("Status"));
	tr.appendChild(th);
	th = document.createElement("th");
	th.appendChild(document.createTextNode("Name"));
	tr.appendChild(th);
	th = document.createElement("th");
	th.appendChild(document.createTextNode("Org."));
	th.setAttribute("title", "Organization");
	tr.appendChild(th);
	th = document.createElement("th");
	th.appendChild(document.createTextNode("Degree"));
	tr.appendChild(th);
	th = document.createElement("th");
	th.style = "width: 32px";
	tr.appendChild(th);
	tableObj.appendChild(tr);
}

function updateRegs(id) {
	return function() {
		updateTableData(`/api/sections/${id}/attendees`, function(tableData) {
			refreshTable("reg_table", addHeaderToRegTable, addRowToRegTable, tableData);
		});
	};
}

function addRowToSectionTable(tableObj) {
	return function(sectionData) {
		tr = document.createElement("tr");
		td = document.createElement("td");
		td.appendChild(document.createTextNode(sectionData["name"]));
		tr.appendChild(td);
		td = document.createElement("td");
		td.appendChild(document.createTextNode(sectionData["building"]));
		tr.appendChild(td);
		td = document.createElement("td");
		td.appendChild(document.createTextNode(sectionData["room"]));
		tr.appendChild(td);
		td = document.createElement("td");
		a = document.createElement("a");
		a.classList.add("edit_button");
		a.setAttribute("title", "Edit");
		a.href = `/sections/${sectionData["id"]}/edit`;
		td.appendChild(a);
		tr.appendChild(td);
		td = document.createElement("td");
		a = document.createElement("a");
		a.classList.add("regs_button");
		a.setAttribute("title", "Registered to section");
		a.href = `/sections/${sectionData["id"]}`;
		td.appendChild(a);
		tr.appendChild(td);
		tableObj.appendChild(tr);
	};
}

function addHeaderToSectionTable(tableObj) {
	tr = document.createElement("tr");
	th = document.createElement("th");
	th.appendChild(document.createTextNode("Name"));
	tr.appendChild(th);
	th = document.createElement("th");
	th.appendChild(document.createTextNode("Building"));
	tr.appendChild(th);
	th = document.createElement("th");
	th.appendChild(document.createTextNode("Room"));
	tr.appendChild(th);
	th = document.createElement("th");
	th.style = "width: 32px";
	tr.appendChild(th);
	th = document.createElement("th");
	th.style = "width: 32px";
	tr.appendChild(th);
	tableObj.appendChild(tr);
}

function updateSections() {
	updateTableData("/api/sections", function(tableData) {
		refreshTable("section_table", addHeaderToSectionTable, addRowToSectionTable, tableData);
	});
}

function writeCard(id) {
	return function() {
		var write_modal = document.getElementById('write_modal');
		var ok_button = write_modal.getElementsByClassName("modal_ok")[0];
		var close_button = write_modal.getElementsByClassName("close")[0];
		write_modal.style.display = "block";
		var xhttp = new XMLHttpRequest();
		xhttp.addEventListener("load", function(event) {
			var response = JSON.parse(event.target.responseText);
			var text = document.getElementById("modal_text");
			text.textContent = response["status"]
			ok_button.style.display = "block";
		});
		close_button.addEventListener("click", function() {
			xhttp.abort();
		});
		xhttp.open("POST", `/api/attendees/${id}/card`, true);
		xhttp.send();
	}
}

function closeWriteModal() {
	var write_modal = document.getElementById('write_modal');
	var ok_button = document.getElementsByClassName("modal_ok")[0];
	var text = document.getElementById("modal_text");
	write_modal.style.display = "none";
	text.textContent = "Attach card to NFC module";
	ok_button.style.display = "none";
}

function loadForm(uri, formId, method, formHandler, responseHandler) {
	window.addEventListener("load", function() {
		var form = document.getElementById(formId);
		form.addEventListener("submit", function(event) {
			event.preventDefault();
			var xhttp = new XMLHttpRequest();
			var fd = new FormData(form);
			xhttp.addEventListener("load", function(event) {
				responseHandler(event.target.responseText, event.target.status);
			});
			var JSONStr = formHandler(form);
			if (JSONStr == null)
				return;
			xhttp.open(method, uri, true);
			xhttp.setRequestHeader("Content-Type", "application/json");
			xhttp.send(JSONStr);
		});
	});
}

function setOnchangeForm(formId, button=true) {
	inputs = document.forms[formId].getElementsByTagName("input");
	for (var i = 0; i < inputs.length; i++) {
		if (inputs[i].type != "submit")
			inputs[i].oninput = clearSubmit(button);
	};
}

function unsetOnchangeForm(formId) {
	inputs = document.forms[formId].getElementsByTagName("input");
	for (var i = 0; i < inputs.length; i++) {
		if (inputs[i].type != "submit")
			inputs[i].oninput = null;
	};
}

function clearSubmit(button=true) {
	return function() {
		if (button) {
			btn = document.getElementsByClassName("big_write_button")[0];
			if (btn.classList.contains("unwritten_button"))
				btn.classList.remove("unwritten_button");
			if (btn.classList.contains("written_button"))
				btn.classList.remove("written_button");
			btn.style.display = "none";
		}
		info = document.getElementsByClassName("info")[0];
		if (info.classList.contains("success"))
			info.classList.remove("success");
		if (info.classList.contains("error"))
			info.classList.remove("error");
		info.style.display = "none";
		info.innerHTML = null;
	}
}

function clearForm(form) {
	inputs = form.getElementsByTagName("input");
	for (var i = 0; i < inputs.length; i++) {
		if (inputs[i].type != "submit")
			if (inputs[i].checked)
				inputs[i].checked = false;
			else
				inputs[i].value = null;
	}
}

function sectionFormToJSON(form) {
	var data = new FormData(form);
	var json = {};
	data.forEach(function(value, key) {
		json[key] = value;
	});
	return JSON.stringify(json);
}

function attendeeFormToJSON(form) {
	var data = new FormData(form);
	var json = {"sections": []};
	data.forEach(function(value, key) {
		if (["name", "surname", "organization", "degree", "is_activated"].includes(key))
			json[key] = value;
		else
			json["sections"].push(key);
	});
	if ("is_activated" in json)
		json["is_activated"] = true;
	else
		json["is_activated"] = false;
	return JSON.stringify(json);
}

function formResponse(respBody, respCode) {
	infoBox = document.getElementsByClassName("info")[0];
	infoBox.style.display = "block";
	resp = JSON.parse(respBody);
	if (respCode == 200) {
		infoBox.classList.add("success");
		infoBox.innerHTML = `Done! Go to <a href=${JSON.parse(respBody)["uri"]}>link</a> for details`;
		btn = document.getElementsByClassName("big_write_button")[0];
		if (btn) {
			var xhttp = new XMLHttpRequest();
			xhttp.addEventListener("load", function(event) {
				var data = JSON.parse(event.target.responseText);
				if (Boolean(data["card_written"]))
					btn.classList.add("written_button");
				else
					btn.classList.add("unwritten_button");
			});
			xhttp.open("GET", `/api/attendees/${resp["id"]}`, true);
			xhttp.send();
			btn.onclick = writeCard(resp["id"]);
			btn.style.display = "block";
		}
		if ("attendee_form" in document.forms) {
			clearForm(document.forms["attendee_form"]);
		} else if ("section_form" in document.forms) {
			clearForm(document.forms["section_form"]);
		}
	} else {
		infoBox.classList.add("error");
		infoBox.innerHTML = resp["error"] + "!";
	}
}

function fillSectionForm(id) {
	var xhttp = new XMLHttpRequest();
	xhttp.addEventListener("load", function(event) {
		var data = JSON.parse(event.target.responseText);
		document.getElementsByName("name")[0].value = data["name"];
		document.getElementsByName("building")[0].value = data["building"];
		document.getElementsByName("room")[0].value = data["room"];
	});
	xhttp.open("GET", `/api/sections/${id}`, true);
	xhttp.send();
}

function fillAttendeeForm(id) {
	var xhttpA = new XMLHttpRequest();
	var xhttpS = new XMLHttpRequest();
	xhttpA.addEventListener("load", function(event) {
		var data = JSON.parse(event.target.responseText);
		document.getElementsByName("name")[0].value = data["name"];
		document.getElementsByName("surname")[0].value = data["surname"];
		document.getElementsByName("organization")[0].value = data["organization"];
		document.getElementsByName("degree")[0].value = data["degree"];
		document.getElementsByName("is_activated")[0].checked = Boolean(data["is_activated"]);
		btn = document.getElementsByClassName("big_write_button")[0];
		if (Boolean(data["card_written"]))
			btn.classList.add("written_button");
		else
			btn.classList.add("unwritten_button");
		btn.onclick = writeCard(id);
		btn.style.display = "block";
	});
	xhttpS.addEventListener("load", function(event) {
		var data = JSON.parse(event.target.responseText);
		data.forEach(function(item) {
			document.getElementsByName(item["id"])[0].checked = true;
		});
	});
	xhttpA.open("GET", `/api/attendees/${id}`, true);
	xhttpS.open("GET", `/api/attendees/${id}/sections`, true);
	xhttpA.send();
	xhttpS.send();
}

// Copyright (c) 2008, The Code Project. All rights reserved.
var obid, obtid, value

function rateItem(objId, objTypeId, forceComment){
	if(objId > 0 && objTypeId > 0){
		obid  = objId.toString();
		obtid = objTypeId.toString();
		value = 0;
		
		
		var elems = document.getElementsByTagName("input");
		var reg = /.+VoteRBL_\d{1}/;
		
		for (var i = 0; i < elems.length; i++){
			var attr = elems[i].getAttribute("id");
			if(!attr)continue;
			if(reg.test(attr)){
				var radio = document.getElementById(attr);
				if(radio&&radio.checked){
					value = radio.getAttribute("value");
					break;
				}
			}
		}
		
		var comment=$("#RateComment")[0];
		comment = comment.value.replace(/^\s+|\s+$/g,'');
		
		if (value <= 0)
			ShowErrorMessage("You must select a value to vote");
		else if (value <=2 && comment == '' && forceComment)
			ShowErrorMessage("You must provide a comment");
		else {
			PrepElements();
			$.get("/Script/Ratings/Ajax/RateItem.aspx?obid=" + obid + "&obtid=" + obtid + "&rvv=" + value + "&rvc=" + escape(comment), callback);
		}
	}
	return false;
}

function callback(data){
	if(data.length > 0){
		var voteRes = $("#voteRes")[0];
		if(voteRes) {
			voteRes.innerHTML = data;
			voteRes.style.display = "";
		}
		voteRes = $("#CurRat")[0];
  		if(voteRes)voteRes.style.display = "none";
	}
	var loader = $("#loaderImg")[0];
	if(loader&&loader.style)loader.style.display = "none";
}

function PrepElements(){
	var loader = $("#loaderImg")[0];
	if(loader&&loader.style.display == "none")
		loader.style.display = "";
		
	loader = $("#voteTbl")[0];
	if(loader)loader.style.display = "none";

	loader = $("#voteRes")[0];
	if(loader)loader.style.display = "none";

	loader = $("#RateComDiv")[0];
	if(loader)loader.style.display = "none";
}

function ShowErrorMessage(msg){
	var loader = $("#loaderImg")[0];
	if(loader)loader.style.display = "none";
	
	alert(msg);
	/*
	var voteRes = $("#voteRes");
	if(voteRes) {
		voteRes.innerHTML = "An error occurred. Your vote has not been saved. Please try again later.";
		voteRes.style.display = "";
	}
	*/
}
// 업로드 사진 미리보기
function cnn_process()
{
		
	var form = $('#FORM')[0];
	var formData = new FormData(form);
	formData.append("file", $("#file")[0].files[0]);	
	
	$.ajax({
	    url: '/cnn_process',
			processData: false,
			contentType: false,
			data: formData,
			type: 'POST',
			dataType:"json",
			success: function(result){
				var color = result["color"]
				var cloth = result["cloth"]
				var color_form = document.getElementById("color");
				color_form[color].selected = true;
				var category_form = document.getElementById("category");
				category_form[cloth].selected = true;
				console.log(result);
				}
	  });
  }
  function cosine_process()
  {
		  
	  var form = $('#FORM')[0];
	  var formData = new FormData(form);
	  var category = $("#category option:selected").val();
	  formData.append("file", $("#file")[0].files[0]);	
	  formData.append("category", category);
	  
	  $.ajax({
		  url: '/cosine_process',
			  processData: false,
			  contentType: false,
			  data: formData,
			  type: 'POST',
			  dataType:"json",
			  success: function(result){
				  result.innerHTML =
				  $("#result_price").html(
					""+
					"<span style='color:green; font-weight:bold'>평균가: " + result["mean"] + "</span><br>");
					$("#box_in_img1").html(
						"<div class='image_sample'><img src='." + result["img1"] + "'></div>");
					$("#box_in_img2").html(
						"<div class='image_sample'><img src='." + result["img2"] + "'></div>");
					$("#box_in_img3").html(
						"<div class='image_sample'><img src='." + result["img3"] + "'></div>");					
					$("#box_in_text1").html(
						"<br>유사도: " + result["sim1"] + "<br>" + 
						"가격: " + result["pri1"]);
					$("#box_in_text2").html(
						"<br>유사도: " + result["sim2"] + "<br>" + 
						"가격: " + result["pri2"]);
					$("#box_in_text3").html(
						"<br>유사도: " + result["sim3"] + "<br>" + 
						"가격: " + result["pri3"]);

				  console.log(result);
				  }
		});
	}
// 업로드 사진 미리보기
function rnn_process()
{
	var category = $("#category option:selected").val();

	var postdata = {
		"category":category
	}
	
	$.ajax({
	    url: '/rnn_process',
			processData: false,
			contentType: "application/json",
			data: JSON.stringify(postdata),
			type: 'POST',
			dataType:"JSON",
			success: function(result){
				console.log(result);
				document.getElementById("contents").value = result["text"];
				}
	  });
  }

// transformer 모델
function transformer_process()
{
	var category = $("#category option:selected").val();
	var color = $("#color option:selected").val();
	var size = $("#size option:selected").val();
	var washing = $("#washing option:selected").val();
	// 사이즈 size
	// 세탁 washing

	var postdata = {
		"category":category,
		"color":color,
		"size":size,
		"washing":washing
	}
	
	$.ajax({
		url: '/transformer_process',
			processData: false,
			contentType: "application/json",
			data: JSON.stringify(postdata),
			type: 'POST',
			dataType:"JSON",
			success: function(result){
				console.log(result);
				document.getElementById("contents").value = result["text"];
				}
	});
}
  

function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();
    reader.onload = function (e) {
      $('#preImage').attr('src', e.target.result);
    }
    reader.readAsDataURL(input.files[0]);
  }
}
$("#file").change(function() {
  readURL(this);
});


// 업로드upload 다음, 이전버튼
function next1() {
	var x = document.getElementById("upload1");
	var y = document.getElementById("upload2");
	x.style.display = "none";
	y.style.display = "block";
}
function previous1() {
  var x = document.getElementById("upload1");
	var y = document.getElementById("upload2");
	y.style.display = "none";
	x.style.display = "block";
}
function next2() {
	var y = document.getElementById("upload2");
	var z = document.getElementById("upload3");
	y.style.display = "none";
	z.style.display = "block";
}
function previous2() {
  var y = document.getElementById("upload2");
	var z = document.getElementById("upload3");
	z.style.display = "none";
	y.style.display = "block";
}
function next3() {
	var z = document.getElementById("upload3");
	var v = document.getElementById("upload4");
	z.style.display = "none";
	v.style.display = "block";
}
function previous3() {
  var z = document.getElementById("upload3");
	var v = document.getElementById("upload4");
	v.style.display = "none";
	z.style.display = "block";
}

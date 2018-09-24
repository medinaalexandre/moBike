var pos;

var $demo;

function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  } else {
    $demo.text("Geolocation is not supported by this browser.");
  }
}

function showPosition(position) {
  pos = position;
  var { latitude, longitude } = pos.coords;
  $demo.html(`Latitude: ${latitude}<br>Longitude: ${longitude}`);
  $('#btn_submit').attr("disabled", null);
}

$(document).ready(function() {
  $demo = $("#demo");
  $('#btn_submit').on('click', function() {
    var data = pos.coords;
    data.csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val();
    $.post("/ajax/", data, function() {
      alert("Saved Data!");
    });
  });
});

 $(document).on('submit', '#id', function(e){
      e.preventDefault();
      $.ajax(

       type='POST',
       url = 'abc/xyz',
       data : {

           lat:position.coords.latitude,
           long: position.coords.longitude
           csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
         },
        });
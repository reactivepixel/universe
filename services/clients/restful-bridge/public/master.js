function mqttPublish(action){
  return $.ajax({
    url: '/ctrl/' + action,
    context: document.body,
    dataType: 'json',
    method: 'POST',
    data: {
      action: action,
      derp: 'high'
    }
  }).done(function(res) {
    // $( this ).addClass( "done" );
    console.log('hit', res)
  });
}

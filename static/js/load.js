(function poll(){
   setTimeout(function(){
      $.ajax({ url: "server", success: function(data){
        //Update your dashboard gauge
        salesGauge.setValue(data.value);

        //Setup the next poll recursively
        poll();
      }, dataType: "json"});
  }, 30000);
})();

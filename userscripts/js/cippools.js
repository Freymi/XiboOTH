$( document ).ready(function() {
    getAndInsert();

    var requestLoop = setInterval(function(){
       getAndInsert();
    }, 300000);
});

  function getAndInsert() {
       $.getJSON("http://194.95.108.132/userscripts/untis.php", function(response) {
                var rooms = response.rooms;
    
                $("#wrapper").empty();

                for(var i = 0; i < rooms.length; i++) {
                     var room = rooms[i];
                     var classString = "content";
                     if(room.free == 1) {
                         classString += " free";
                     }
                     $("#wrapper").append('<div class="' + classString + '"><span class="title">' + room.name  + '</span><br>' + room.until + '</div>');
                }
            });
   }

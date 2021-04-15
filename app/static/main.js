$(function() {
  $(".pop-up-text").hover(function(){
    var tooltip = $('.pop-up'),
          ww = $(window).outerWidth(),
          tl = $(this).offset().left;

      if((tl * 2) > ww) tooltip.css({ 'right': '5px' });
      if((tl * 2) < ww) tooltip.css({ 'right': 'auto' });
  });
});


/* search list Zach Richard Design https://codepen.io/zrichard/pen/bymrI */


  //Sort by level
  $(function() {
      $.fn.sortList = function() {
      var mylist = $(this);
      var listitems = $('li', mylist).get();
      listitems.sort(function(a, b) {
          var compA = $(a).text().toUpperCase();
          var compB = $(b).text().toUpperCase();
          return (compA < compB) ? -1 : 1;
      });
      $.each(listitems, function(i, itm) {
          mylist.append(itm);
      });
     }
  });

  //Sort by rule
  $(function() {
      $.fn.sortListRule = function() {
      var mylist = $(this);
      var listitems = $('li', mylist).get();
      listitems.sort(function(a, b) {
          var compA = $('span', a).attr("value").toUpperCase();
          var compB = $('span', b).attr("value").toUpperCase();
          return (compA < compB) ? -1 : 1;
      });
      $.each(listitems, function(i, itm) {
          mylist.append(itm);
      });
     }
  });

  //Search filter
  (function ($) {
    // custom css expression for a case-insensitive contains()
    jQuery.expr[':'].Contains = function(a,i,m){
        return (a.textContent || a.innerText || "").toUpperCase().indexOf(m[3].toUpperCase())>=0;
    };


    function listFilter(searchDir, list) { 
      var form = $("<form>").attr({"class":"filterform","onsubmit":"return false;"}),
          input = $("<input>").attr({"class":"filterinput","type":"text"});
      $(form).append(input).appendTo(searchDir);

      $(input)
        .change( function () {
          var filter = $(this).val();
          if(filter) {
            $(list).find("li:not(:Contains(" + filter + ")) span:not([value*=" + filter + "])").closest("li").slideUp();
            $(list).find("li:Contains(" + filter + "), span[value*=" + filter + "]").closest("li").slideDown();
          } else {
            $(list).find("li").slideDown();
          }
          return false;
        })
      .keyup( function () {
          $(this).change();
      });
    }


    //ondomready
    $(function () {
      listFilter($("#searchDir"), $("#rule-list"));
    });
  }(jQuery));

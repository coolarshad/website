
(function ($) {
  // USE STRICT
  "use strict";

      Chart.defaults.global.tooltips.enabled = false;
  try {

    //trade request
    var ctx = document.getElementById("widgetChart1");
    if (ctx) {
      ctx.height = 130;
      var myChart = new Chart(ctx, {
        type: 'bar',
         data: {
          labels: ['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'],
          datasets: [
            {
             
              data: [78, 81, 80, 65, 58, 75, 60, 75, 65, 60, 60, 75],
              enableMouseTracking: false,
              borderColor: "transparent",
              borderWidth: "0",
              backgroundColor: "rgba(255,255,255,.3)",
                hoverBackgroundColor: "rgba(255,255,255,.3)"
            }
          ]
        },
        options: {
          maintainAspectRatio: true,
          legend: {
            display: false
          },
        
          layout: {
            padding: {
              left: 0,
              right: 0,
              top: 0,
              bottom: 0
            }
          },
          responsive: true,
          scales: {
            xAxes: [{
              gridLines: {
                color: 'transparent',
                zeroLineColor: 'transparent'
              },
              ticks: {
                fontSize: 2,
                fontColor: 'transparent'
              }
            }],
            yAxes: [{
              display: false,
              ticks: {
                display: false,
              }
            }]
          },
          title: {
            display: false,
          },
           elements: {
            line: {
              tension: 0.00001,
              borderWidth: 1
            },
            point: {
              radius: 4,
              hitRadius: 10,
              hoverRadius: 4
            }
          }
        }
      });
    }


    //trade approved
  var ctx = document.getElementById("widgetChart2");
    if (ctx) {
      ctx.height = 115;
      var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
          datasets: [
            {
             
              data: [78, 81, 80, 65, 58, 75, 60, 75, 65, 60, 60, 75],
              borderColor: "transparent",
              borderWidth: "0",
              backgroundColor: "rgba(255,255,255,.3)",
                hoverBackgroundColor: "rgba(255,255,255,.3)"
            }
          ]
        },
        options: {
          maintainAspectRatio: true,
          legend: {
            display: false
          },
          scales: {
            xAxes: [{
              display: false,
              categoryPercentage: 1,
              barPercentage: 0.65
            }],
            yAxes: [{
              display: false
            }]
          }
        }
      });
    }

    //trade unapproved
 var ctx = document.getElementById("widgetChart3");
    if (ctx) {
      ctx.height = 115;
      var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
          datasets: [
            {
             
              data: [78, 81, 80, 65, 58, 75, 60, 75, 65, 60, 60, 75],
              borderColor: "transparent",
              borderWidth: "0",
              backgroundColor: "rgba(255,255,255,.3)",
                hoverBackgroundColor: "rgba(255,255,255,.3)"
            }
          ]
        },
        options: {
          maintainAspectRatio: true,
          legend: {
            display: false
          },
          scales: {
            xAxes: [{
              display: false,
              categoryPercentage: 1,
              barPercentage: 0.65
            }],
            yAxes: [{
              display: false
            }]
          }
        }
      });
    }

    //Registered Users
    var ctx = document.getElementById("widgetChart4");
    if (ctx) {
      ctx.height = 115;
      var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
          datasets: [
            {
             
              data: [78, 81, 80, 65, 58, 75, 60, 75, 65, 60, 60, 75],
              borderColor: "transparent",
              borderWidth: "0",
              backgroundColor: "rgba(255,255,255,.3)",
               hoverBackgroundColor: "rgba(255,255,255,.3)"
            }
          ]
        },
        options: {
          maintainAspectRatio: true,
          legend: {
            display: false
          },
          scales: {
            xAxes: [{
              display: false,
              categoryPercentage: 1,
              barPercentage: 0.65
            }],
            yAxes: [{
              display: false
            }]
          }
        }
      });
    }

    // Recent Report
    const brandProduct = 'rgba(0,181,233,0.8)'
    const brandService = 'rgba(0,173,95,0.8)'

    var elements = 12
    var data1 = [52, 60, 55, 50, 65, 80, 57, 70, 105, 115,23,120]
    var data2 = [102, 70, 80, 100, 56, 53, 80, 75, 65, 90,80,50]

    var ctx = document.getElementById("recent-rep-chart");
    if (ctx) {
      ctx.height = 250;
      var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
         labels: ['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'],
          datasets: [
            {
              backgroundColor: brandService,
              borderColor: 'transparent',
              pointHoverBackgroundColor: 'transparent',
              borderWidth: 0,
              data: data1

            }
          ]
        },
        options: {
          maintainAspectRatio: true,
          legend: {
            display: false
          },
          responsive: true,
          scales: {
            xAxes: [{
              gridLines: {
                drawOnChartArea: true,
                color: '#f2f2f2'
              },
              ticks: {
                fontFamily: "Poppins",
                fontSize: 12
              }
            }],
            yAxes: [{
              ticks: {
                beginAtZero: true,
                maxTicksLimit: 5,
                stepSize: 50,
                max: 150,
                fontFamily: "Poppins",
                fontSize: 12
              },
              gridLines: {
                display: true,
                color: '#f2f2f2'

              }
            }]
          },
          elements: {
            point: {
              radius: 0,
              hitRadius: 10,
              hoverRadius: 4,
              hoverBorderWidth: 3
            }
          }


        }
      });
    }

    // Percent Chart
    var ctx = document.getElementById("percent-chart");
    if (ctx) {
      ctx.height = 280;
      var myChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
          datasets: [
            {
        
              data: [60, 40],
              backgroundColor: [
                '#00ad5f',
                '#fa4251'
              ],
              hoverBackgroundColor: [
                '#00ad5f',
                '#fa4251'
              ],
              borderWidth: [
                0, 0
              ],
              hoverBorderColor: [
                'transparent',
                'transparent'
              ]
            }
          ],
          labels: [
            'Profit',
            'Loss'
          ]
        },
        options: {
          maintainAspectRatio: false,
          responsive: true,
          cutoutPercentage: 55,
          animation: {
            animateScale: true,
            animateRotate: true
          },
          legend: {
            display: false
          },
          tooltips: {
            enabled: true,  
            titleFontFamily: "Poppins",
            xPadding: 15,
            yPadding: 10,
            caretPadding: 0,
            bodyFontSize: 16
          }
        }
      });
    }

  } catch (error) {
    console.log(error);
  }  
})(jQuery);






(function ($) {
  // USE STRICT
  "use strict";

  // Scroll Bar
  try {
    var jscr1 = $('.js-scrollbar1');
    if(jscr1[0]) {
      const ps1 = new PerfectScrollbar('.js-scrollbar1');      
    }

    var jscr2 = $('.js-scrollbar2');
    if (jscr2[0]) {
      const ps2 = new PerfectScrollbar('.js-scrollbar2');

    }

  } catch (error) {
    console.log(error);
  }

})(jQuery);
(function ($) {
  // USE STRICT
  "use strict";

  // Select 2
  try {

    $(".js-select2").each(function () {
      $(this).select2({
        minimumResultsForSearch: 20,
        dropdownParent: $(this).next('.dropDownSelect2')
      });
    });

  } catch (error) {
    console.log(error);
  }


})(jQuery);
(function ($) {
  // USE STRICT
  "use strict";

  // Dropdown 
  try {
    var menu = $('.js-item-menu');
    var sub_menu_is_showed = -1;

    for (var i = 0; i < menu.length; i++) {
      $(menu[i]).on('click', function (e) {
        e.preventDefault();
        $('.js-right-sidebar').removeClass("show-sidebar");        
        if (jQuery.inArray(this, menu) == sub_menu_is_showed) {
          $(this).toggleClass('show-dropdown');
          sub_menu_is_showed = -1;
        }
        else {
          for (var i = 0; i < menu.length; i++) {
            $(menu[i]).removeClass("show-dropdown");
          }
          $(this).toggleClass('show-dropdown');
          sub_menu_is_showed = jQuery.inArray(this, menu);
        }
      });
    }
    $(".js-item-menu, .js-dropdown").click(function (event) {
      event.stopPropagation();
    });

    $("body,html").on("click", function () {
      for (var i = 0; i < menu.length; i++) {
        menu[i].classList.remove("show-dropdown");
      }
      sub_menu_is_showed = -1;
    });

  } catch (error) {
    console.log(error);
  }

  var wW = $(window).width();
    // Right Sidebar
    var right_sidebar = $('.js-right-sidebar');
    var sidebar_btn = $('.js-sidebar-btn');

    sidebar_btn.on('click', function (e) {
      e.preventDefault();
      for (var i = 0; i < menu.length; i++) {
        menu[i].classList.remove("show-dropdown");
      }
      sub_menu_is_showed = -1;
      right_sidebar.toggleClass("show-sidebar");
    });

    $(".js-right-sidebar, .js-sidebar-btn").click(function (event) {
      event.stopPropagation();
    });

    $("body,html").on("click", function () {
      right_sidebar.removeClass("show-sidebar");

    });
 

  // Sublist Sidebar
  try {
    var arrow = $('.js-arrow');
    arrow.each(function () {
      var that = $(this);
      that.on('click', function (e) {
        e.preventDefault();
        that.find(".arrow").toggleClass("up");
        that.toggleClass("open");
        that.parent().find('.js-sub-list').slideToggle("250");

      });
    });

  } catch (error) {
    console.log(error);
  }


  try {
    // Hamburger Menu
    $('.hamburger').on('click', function () {
      $(this).toggleClass('is-active');
      $('.navbar-mobile').slideToggle('500');
    });
    $('.navbar-mobile__list li.has-dropdown > a').on('click', function () {
      var dropdown = $(this).siblings('ul.navbar-mobile__dropdown');
      $(this).toggleClass('active');
      $(dropdown).slideToggle('500');
      return false;
    });
  } catch (error) {
    console.log(error);
  }
})(jQuery);
(function ($) {
  // USE STRICT
  "use strict";

  // Load more
  try {
    var list_load = $('.js-list-load');
    if (list_load[0]) {
      list_load.each(function () {
        var that = $(this);
        that.find('.js-load-item').hide();
        var load_btn = that.find('.js-load-btn');
        load_btn.on('click', function (e) {
          $(this).text("Loading...").delay(1500).queue(function (next) {
            $(this).hide();
            that.find(".js-load-item").fadeToggle("slow", 'swing');
          });
          e.preventDefault();
        });
      })

    }
  } catch (error) {
    console.log(error);
  }

})(jQuery);
(function ($) {
  // USE STRICT
  "use strict";

  try {
    
    $('[data-toggle="tooltip"]').tooltip();

  } catch (error) {
    console.log(error);
  }

$('.date').datepicker({
  multidate: false,
  format: 'dd-mm-yyyy'
});


$('button[data-toggle="modal"]').click(function(){

     $('.header-desktop').css("z-index",0);
 
})
$('.modal.fade').click(function(){
$('.header-desktop').css("z-index",3);
});


$('.btn.btn-danger').click(function(){
  if(window.confirm("Do you really want to delete?")){

    $(this).parent().parent().remove();
  }
});



$("div[id^='entry']").each(function(){
  
  var currentModal = $(this);
  
  //click next
  currentModal.find('.btn-next').click(function(){

    currentModal.modal('hide');
    currentModal.closest("div[id^='entry']").nextAll("div[id^='entry']").first().modal('show'); 
     
  });
  
  //click prev
  currentModal.find('.btn-prev').click(function(){
 
    currentModal.modal('hide');
    currentModal.closest("div[id^='entry']").prevAll("div[id^='entry']").first().modal('show'); 

  });
  
});



var padding_right,
    currentModal,
    my_block;

$(document).on('shown.bs.modal', '.modal', function () {
  padding_right=$("body").css("padding-right"); /* create a variable with padding-right when modal is shown */
});

$(document).on('hidden.bs.modal', '.modal', function () {
  /* This function is triggered when a modal is hidden and... */
  if($('.modal:visible').length) 
    $(document.body).addClass('modal-open').css("padding-right", padding_right); /* ...if there are some modal visible, it put on body class "model-open" & padding-right */
  else
    $(document.body).removeAttr("style"); /* ...if not remove only style attribute: having put "data-dismiss="modal on button next and prev modal.js automaticaly remove "modal-open" */
});



$(".table-search").on("keyup", function() {
  var value = $(this).val().toLowerCase(),
    tableattr = $(this).attr("data-table-search"),
    tablesearch = $('#' + tableattr).find('tbody tr');

  tablesearch.hide();                           //start with all rows hidden
                  //initiate our stored rowspan with the default of 1

  tablesearch.each(function() {
    var $row = $(this);
    var $firstCell = $row.find("td:nth-child(5)");
    var id = $firstCell.text().toLowerCase();
    if (id.indexOf(value) > -1) {               //if the text is found
      $row.show();         //show this row, and the next (n-1) rows as well
    }

  });

});



$(".table-search-inventory").on("keyup", function() {
  var value = $(this).val().toLowerCase(),
    tableattr = $(this).attr("data-table-search"),
    tablesearch = $('#' + tableattr).find('tbody tr');

  tablesearch.hide();                           //start with all rows hidden
                  //initiate our stored rowspan with the default of 1

  tablesearch.each(function() {
    var $row = $(this);
    var $firstCell = $row.find("td:nth-child(3)");
    var id = $firstCell.text().toLowerCase();
    if (id.indexOf(value) > -1) {               //if the text is found
      $row.show();         //show this row, and the next (n-1) rows as well
    }

  });

});

$(".table-search-company").on("keyup", function() {
  var value = $(this).val().toLowerCase(),
    tableattr = $(this).attr("data-table-search"),
    tablesearch = $('#' + tableattr).find('tbody tr');

  tablesearch.hide();                           //start with all rows hidden
                  //initiate our stored rowspan with the default of 1

  tablesearch.each(function() {
    var $row = $(this);
    var $firstCell = $row.find("td:nth-child(3)");
    var id = $firstCell.text().toLowerCase();
    if (id.indexOf(value) > -1) {               //if the text is found
      $row.show();         //show this row, and the next (n-1) rows as well
    }

  });

});

  $(".table-searchstock").on("keyup", function() {
  var value = $(this).val().toLowerCase(),
    tableattr = $(this).attr("data-table-search"),
    tablesearch = $('#' + tableattr).find('tbody tr');

  tablesearch.hide();                           //start with all rows hidden
  
  var previousRowspan = 1;                      //initiate our stored rowspan with the default of 1

    tablesearch.each(function() {
    var $row = $(this);
    var $firstCell = $row.find("td:nth-child(2)");
    var id = $firstCell.text().toLowerCase();
    var rowspan = $firstCell.attr('rowspan');

if(previousRowspan>1){
  previousRowspan--;
  return true;
}

previousRowspan= +rowspan;

  //get the row's rowspan
    if (id.indexOf(value) > -1) {               //if the text is found
      var additionalRows = previousRowspan-1;   //use our n-1 formula
      var $additionalRows = $row.nextAll(':lt(' + additionalRows + ')');  //select the next (n-1) rows
      $row.add($additionalRows).show();         //show this row, and the next (n-1) rows as well
    }

  });
});
var user=$('#authority').text();
 // $('.editbtn0').click(function () {
 //             if( user== 'admin'){
 //                  alert('Permission denied');
 //               }
 //               else{


 //              var currentTD = $(this).parents('tr').find('td');
 //                if ($(this).text().trim() == 'Edit'){
 //              // if ($(this).html() == 'Edit') {
 //                  currentTD = $(this).parents('tr').find($("td").not(":nth-child(1),:nth-child(2),:nth-child(3),:nth-child(4),:nth-child(5),:nth-child(26),:last-child"));
 //                  $.each(currentTD, function () {
 //                      $(this).prop('contenteditable', true).css({
 //                        'background':'#fff',
 //                        'color':'#000'

 //                    })
 //                  });
 //              } else {
 //                 $.each(currentTD, function () {
 //                      $(this).prop('contenteditable', false).removeAttr("style");
 //                  });
 //              }
    
 //              $(this).html($(this).text().trim()== 'Edit' ? 'Save' : 'Edit')
 //              if ($(this).html() == 'Save'){
                
 //                $(this).prop('contenteditable',false)
 //              }
 //            }
 //          });


    $('.editbtn').click(function () {
      if( user== 'admin'){
                  alert('Permission denied');
               }
               else{
                
              var currentTD = $(this).parents('tr').find('td');
                if ($(this).text().trim() == 'Edit'){
              // if ($(this).html() == 'Edit') {
                  currentTD = $(this).parents('tr').find($("td").not(":nth-child(1),:nth-child(2),:nth-child(3),:nth-child(4),:nth-child(5),:last-child"));
                  $.each(currentTD, function () {
                      $(this).prop('contenteditable', true).css({
                        'background':'#fff',
                        'color':'#000'

                    });
                     
                  });

              } else {
                 $.each(currentTD, function () {
                      $(this).prop('contenteditable', false).removeAttr("style");
                  });

                  
              }
    
              $(this).html($(this).text().trim()== 'Edit' ? 'Save' : 'Edit');
              if ($(this).html() == 'Save'){
              // saveEditApproval(this.id);
                $(this).prop('contenteditable',false);
                
              }
    }
          });



    function saveEditApproval(id){
  alert(id);
}





    $('.editbtn1').click(function () {
              var currentTD = $(this).parents('tr').find('td');
                if ($(this).text().trim() == 'Edit'){
              // if ($(this).html() == 'Edit') {
                  currentTD = $(this).parents('tr').find($("td").not(":nth-child(1),:last-child"));
                  $.each(currentTD, function () {
                      $(this).prop('contenteditable', true).css({
                        'background':'#fff',
                        'color':'#000'

                    })
                  });
              } else {
                 $.each(currentTD, function () {
                      $(this).prop('contenteditable', false).removeAttr("style");
                  });
              }
    
              $(this).html($(this).text().trim()== 'Edit' ? 'Save' : 'Edit')
              if ($(this).html() == 'Save'){
                $(this).prop('contenteditable',false)
              }
    
          });

        $('.editbtn2').click(function () {
              var currentTD = $(this).parents('tr').find('td');
                if ($(this).text().trim() == 'Edit'){
              // if ($(this).html() == 'Edit') {
                  currentTD = $(this).parents('tr').find($("td").not(":nth-child(1),:nth-child(2),:nth-child(3),:last-child"));
                  $.each(currentTD, function () {
                      $(this).prop('contenteditable', true).css({
                        'background':'#fff',
                        'color':'#000'

                    })
                  });
              } else {
                 $.each(currentTD, function () {
                      $(this).prop('contenteditable', false).removeAttr("style");
                  });
              }
    
              $(this).html($(this).text().trim()== 'Edit' ? 'Save' : 'Edit')
              if ($(this).html() == 'Save'){
                $(this).prop('contenteditable',false)
              }
    
          });
        
// $('.add').click(function() {
//   // alert('add entry');
//   var $div = $('div[id^="data"]:last');
//   var num = parseInt( $div.prop("id").match(/\d+/g), 10 ) +1;
//   alert(num);
//   var $clone = $div.clone().prop('id', 'data'+num );
//   $clone.find('#consumptionproduct-input').prop('name','consumptionproduct-input'+num);
//   $clone.find('#consumptionquantity-input').prop('name','consumptionquantity-input'+num);
//   $clone.find('#consumptionunit-input').prop('name','consumptionunit-input'+num);
//   $clone.find('#consumptionquantityalt_unit-input').prop('name','consumptionquantityalt_unit-input'+num);
//   $clone.find('#consumptionquantityalt_unit-unit-input').prop('name','consumptionquantityalt_unit-unit-input'+num);
//   $div.after($clone);

  
// });
$('.editbtn3').click(function() {
  var edit = $(this).text().trim() == 'Edit';
  $(this).html($(this).text().trim() == 'Edit' ? 'Save' : 'Edit');
  var $rows = $("tr.set" + $(this).data("set"));
  $rows.each(function() {
    var index = $(this).index();
    var tdSet = $(this).find($("td")).not(':first').not('td:nth-child(2)').not('td:nth-child(3)').not(':last');
    if (index % 3) {
      tdSet = $(this).find($("td")).not('td:eq(n)');
    }

    tdSet.each(function() {
      if (edit) {
        $(this).prop('contenteditable', true).css({
          'background': '#fff',
          'color': '#000'
        })
      } else {
        $(this).prop('contenteditable', false).removeAttr("style");
      }
    });

  });
});
//new additives add block

// $('.addadditives').click(function(){
//   alert('add entry');
//   var $div = $('div[id^="additives-block"]:last');
//   var num = parseInt( $div.prop("id").match(/\d+/g), 10 ) +1;
//   // alert(num);
//   var $clone = $div.clone().prop('id', 'data'+num );
//   $clone.find('#additivesformationproduct-input').prop('name','additivesformationproduct-input'+num);
//   $clone.find('#additivesformation_importrate-input').prop('name','additivesformation_importrate-input'+num);
//   $clone.find('#additivesformation_addcost-input').prop('name','additivesformation_addcost-input'+num);
//   $clone.find('#additivesformation_total-input').prop('name','additivesformation_total-input'+num);
//   $clone.find('#additivesformation_mttokl-input').prop('name','additivesformation_mttokl-input'+num);
//   $clone.find('#additivesformation_usage-input').prop('name','additivesformation_usage-input'+num);
//   $clone.find('#additivesformation_netcost-input').prop('name','additivesformation_netcost-input'+num);
  
//   $div.after($clone);

  
// });
////////////////////



});


  
// 




(jQuery);


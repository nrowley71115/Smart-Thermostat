// In your script.js file
function setRadioButtons(system, fan, schedule) {
    // Get the value of the system radio button from the server
    var systemValue = system;
    // Get the value of the fan radio button from the server
    var fanValue = fan;
    // Get the value of the schedule radio button from the server
    var scheduleValue = schedule;
  
    // Check the correct system radio button
    var systemRadios = document.getElementsByName('system');
    for (var i = 0; i < systemRadios.length; i++) {
      if (systemRadios[i].value === systemValue) {
        systemRadios[i].checked = true;
      }
    }
  
    // Check the correct fan radio button
    var fanRadios = document.getElementsByName('fan');
    for (var i = 0; i < fanRadios.length; i++) {
      if (fanRadios[i].value === fanValue) {
        fanRadios[i].checked = true;
      }
    }
  
    // Check the correct schedule radio button
    var scheduleRadios = document.getElementsByName('schedule');
    for (var i = 0; i < scheduleRadios.length; i++) {
      if (scheduleRadios[i].value === scheduleValue) {
        scheduleRadios[i].checked = true;
      }
    }
  }

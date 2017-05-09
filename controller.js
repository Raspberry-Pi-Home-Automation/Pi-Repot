webiopi().ready(function() {
        // Create the buttons for LED, ALARM and Camera
        var button1 = webiopi().createGPIOButton(23, "Light", mousedown);

        var buzzBtn = webiopi().createGPIOButton(16, "Alarm", function() {
               buzzBtn = webiopi().digitalRead(16);
                // Reads the status of the LED pin abd changes it's output
               if(buzzBtn==1)
               {
                  webiopi().digitalWrite(16, 0);
               }
               else
               {
                   webiopi().digitalWrite(16, 1);
               }

        });
  
      var startCamButton = webiopi().createButton("startCamButton", "Camera", function() {
                        window.open('http://10.6.23.200:8081');                     
                });
      
         // Add buttons to their respective DIVs
        $("#control1").append(button1);
        $("#control2").append(buzzBtn);
        $("#control3").append(startCamButton);

        // pass true to refresh repeatedly of false to refresh once
                webiopi().refreshGPIO(true);
});



// Mouse down function for the LED button
function mousedown()
            {
               ledBtn= webiopi().digitalRead(23);
                // Reads the status of the LED pin abd changes it's output
               if(ledBtn==1)
               {
                  webiopi().digitalWrite(23, 0);
               }
               else
               {
                   webiopi().digitalWrite(23, 1);
               }
            }
// Every 2000ms (2 seconds) Call the function to go get the data from Python
setInterval ("callMacro_getData()", 2000);{
            }

// Go get the Data from the Python Macro getData
function callMacro_getData(){
           webiopi().callMacro("getData", [], macro_getData_Callback);
     }

// Get the Data returned from the Python macro getData
function macro_getData_Callback(macro, args, data) {
    //Parse data from python macro getData
             var i = JSON.parse(data);
                  motionDiv.innerHTML = i[0]
                  humidDiv.innerHTML = i[1]
                  tempDiv.innerHTML = i[2]

      }



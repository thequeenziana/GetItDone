function showToast(message, duration) {
    var toast = document.getElementById("toast");
    toast.innerHTML = message;
    toast.className = "toast show";
    setTimeout(function(){
      toast.className = toast.className.replace("show", "");
      localStorage.removeItem("toast_message");
    }, duration);
    localStorage.setItem("toast_message", message);
  }
  
  // Check if there's a stored toast message
  window.onload = function() {
    var storedMessage = localStorage.getItem("toast_message");
    if (storedMessage) {
      showToast(storedMessage, 3000); // Change duration here (in milliseconds)
    }
  };

  
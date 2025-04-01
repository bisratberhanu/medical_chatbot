document.addEventListener("DOMContentLoaded", function () {
  const chatBox = document.getElementById("chat-box");
  const messageInput = document.getElementById("message-input");
  const sendButton = document.getElementById("send-button");

  // Function to add message to chat box
  function addMessage(message, isUser) {
    const p = document.createElement("p");
    p.textContent = message;
    if (isUser) {
      p.style.background = "#444"; // User messages
      p.style.marginLeft = "20px";
    } else {
      p.style.background = "#333"; // Bot messages
    }
    chatBox.appendChild(p);
    chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to bottom
  }

  // Function to send message
  function sendMessage() {
    const message = messageInput.value.trim();
    if (message) {
      console.log("Sending message:", message); // Debugging
      console.log("Payload:", JSON.stringify({ message: message })); // Debugging
      addMessage(message, true); // Display user message
      messageInput.value = ""; // Clear input

      // Send message to backend API
      fetch("/api/chat/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"), // CSRF token for Django
        },
        body: JSON.stringify({ message: message }),
      })
        .then((response) => {
          if (!response.ok) {
            return response.json().then((data) => {
              throw new Error(data.error || "Unknown error");
            });
          }
          return response.json();
        })
        .then((data) => {
          addMessage(data.response, false); // Display bot response from Gemini
        })
        .catch((error) => {
          console.error("Error:", error);
          addMessage(`Error: ${error.message}`, false);
        });
    }
  }

  // Event listener for send button
  sendButton.addEventListener("click", sendMessage);

  // Event listener for Enter key
  messageInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      sendMessage();
    }
  });

  // Function to get CSRF token (required for POST requests in Django)
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});

const sendButton = document.getElementById('sendButton');
const micButton = document.getElementById('micButton');
const textInput = document.getElementById('textInput');

const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = 'en-US';
recognition.interimResults = false;
recognition.maxAlternatives = 1;

sendButton.onclick = () => {
    sendMessage(textInput.value);
};

micButton.onclick = () => {
  recognition.start();
};

recognition.onresult = async (event) => {
  const transcript = event.results[0][0].transcript.toLowerCase();
  textInput.value = transcript;
  if (transcript.includes('hey robo')) {
    sendMessage(transcript);
  }
};

async function sendMessage(message) {
  try {
    const response = await fetch('/send_input', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message })
    });

    const data = await response.json();
    // alert(data.response || data.error);
  } catch (err) {
    alert("Error sending message: " + err);
  }
}

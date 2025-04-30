const chat = document.getElementById('chat');
const input = document.getElementById('user-input');

const questions = [
  "Enter your name:",
  "Enter your age:",
  "Enter your gender (Male/Female):",
  "Enter your height in cm:",
  "Enter your weight in kg:",
  "Select difficulty (Beginner/Intermediate/Advanced):",
  "What's your fitness goal?"
];

const answers = {};
let currentQuestion = 0;

function addMessage(text, sender = 'bot') {
  const div = document.createElement('div');
  div.className = `message ${sender}`;
  div.textContent = text;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

function handleInput() {
  const value = input.value.trim();
  if (!value) return;

  addMessage(value, 'user');
  const keys = ['name', 'age', 'gender', 'height', 'weight', 'difficulty', 'goal'];
  answers[keys[currentQuestion]] = value;

  input.value = '';
  currentQuestion++;

  if (currentQuestion < questions.length) {
    setTimeout(() => addMessage(questions[currentQuestion]), 500);
  } else {
    fetch('/generate', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(answers)
    })
    .then(res => res.json())
    .then(data => addMessage(data.response))
    .catch(() => addMessage("Error contacting the server."));
  }
}

addMessage(questions[currentQuestion]);

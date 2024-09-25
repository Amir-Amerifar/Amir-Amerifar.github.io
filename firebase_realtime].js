

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

// References to Firebase services
const auth = firebase.auth();
const database = firebase.database();

// Function to send registration email
document.getElementById('sendEmail').addEventListener('click', () => {
  const email = document.getElementById('email').value;
  if (email) {
    auth.createUserWithEmailAndPassword(email, 'defaultpassword')
      .then((userCredential) => {
        const user = userCredential.user;
        alert(`Registration email sent to ${email}`);
        // Optionally send verification email
        user.sendEmailVerification();
      })
      .catch((error) => {
        alert(`Error: ${error.message}`);
      });
  } else {
    alert('Please enter a valid email');
  }
});

// Function to toggle relay
document.getElementById('toggleRelay').addEventListener('click', () => {
  const relayRef = database.ref('relay');
  
  relayRef.once('value', (snapshot) => {
    const relayStatus = snapshot.val();
    const newStatus = relayStatus === 'on' ? 'off' : 'on';

    relayRef.set(newStatus);
    updateRelayStatus(newStatus);
  });
});

// Function to update relay status on the page
function updateRelayStatus(status) {
  document.getElementById('relayStatus').innerText = status;
  const ledIndicator = document.getElementById('ledIndicator');

  if (status === 'on') {
    ledIndicator.classList.add('on');
    ledIndicator.classList.remove('off');
  } else {
    ledIndicator.classList.add('off');
    ledIndicator.classList.remove('on');
  }
}

// Listen for changes in relay status in real-time
database.ref('relay').on('value', (snapshot) => {
  const status = snapshot.val();
  updateRelayStatus(status);
});

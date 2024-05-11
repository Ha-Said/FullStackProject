



document.addEventListener('DOMContentLoaded', function() {
    const oldIdInput = document.getElementById('oldID');
    const joinButton = document.getElementById('joinButton');
  
    oldIdInput.addEventListener('input', function() {
   
      if (oldIdInput.value.trim() !== '') {
        joinButton.disabled = false;
      } else {
        joinButton.disabled = true;
      }
    }); 
    joinButton.addEventListener('click', function() {
      const sessionId = oldIdInput.value.trim();

      getQuestion(sessionId);
    });
  });

  
async function unregisterParticipant(activityCard, participant) {
    // Logic to unregister the participant
    const response = await fetch(`/activities/${activityCard.dataset.activity}/unregister?email=${encodeURIComponent(participant)}`, {
        method: 'DELETE',
    });
    if (response.ok) {
        // Remove the participant from the UI
        const participantsList = activityCard.querySelector('.participants-list');
        const participantItems = participantsList.querySelectorAll('li');
        participantItems.forEach(item => {
            if (item.textContent.includes(participant)) {
                participantsList.removeChild(item);
            }
        });
    } else {
        console.error('Failed to unregister participant.');
    }
}
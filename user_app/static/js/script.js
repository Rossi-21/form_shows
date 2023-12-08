async function handleLike(showId) {
    try {
        const response = await fetch(`/like/${showId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(), // Ensure you have a function to fetch CSRF token
            },
            body: JSON.stringify({ showId: showId }),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok.');
        }

        const data = await response.json();

        // Update the image and like count based on data received from the server
        const imageElement = document.getElementById(`image_${showId}`);
        // Update the image source based on the server response
        // ...

        // Update the like count if needed
        // ...

    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}
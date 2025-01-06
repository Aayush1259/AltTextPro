export const processImage = async (formData) => {
    try {
        const response = await fetch(`http://localhost:8000/api/process-image`, {
            method: 'POST',
            body: formData,
            mode: 'cors', // Ensure CORS settings match
            headers: {
                'Accept': 'application/json',
            },
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to process image');
        }
        const responseData = await response.json();
        console.log('Parsed Response Data:', responseData);
        return responseData;
    } catch (error) {
        console.error('API Error:', error);
        if (error.message.includes('CORS')) {
            throw new Error('CORS error: Check backend CORS settings.');
        } else if (error.message.includes('Failed to fetch')) {
            throw new Error('Network error: Ensure the server is running and accessible.');
        } else {
            throw new Error(`Server error: ${error.message}`);
        }
    }
};

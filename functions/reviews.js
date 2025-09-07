// Netlify Function to handle review storage and retrieval
// This function processes form submissions and stores reviews

exports.handler = async (event, context) => {
    // Enable CORS
    const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Content-Type': 'application/json'
    };

    // Handle preflight requests
    if (event.httpMethod === 'OPTIONS') {
        return {
            statusCode: 200,
            headers,
            body: ''
        };
    }

    // Handle GET requests to fetch reviews
    if (event.httpMethod === 'GET') {
        try {
            // Get app ID from path
            const pathParts = event.path.split('/');
            const appId = pathParts[pathParts.length - 1];

            // In a real implementation, you would fetch from a database
            // For now, we'll return sample data
            const reviews = getReviewsForApp(appId);

            return {
                statusCode: 200,
                headers,
                body: JSON.stringify({
                    success: true,
                    reviews: reviews,
                    count: reviews.length
                })
            };
        } catch (error) {
            return {
                statusCode: 500,
                headers,
                body: JSON.stringify({
                    success: false,
                    error: 'Failed to fetch reviews'
                })
            };
        }
    }

    // Handle POST requests to save reviews
    if (event.httpMethod === 'POST') {
        try {
            const data = JSON.parse(event.body);
            
            // Validate required fields
            if (!data.app_id || !data.reviewer_name || !data.rating || !data.review_comment) {
                return {
                    statusCode: 400,
                    headers,
                    body: JSON.stringify({
                        success: false,
                        error: 'Missing required fields'
                    })
                };
            }

            // Create review object
            const review = {
                id: generateId(),
                app_id: data.app_id,
                reviewer_name: data.reviewer_name,
                reviewer_email: data.reviewer_email || '',
                rating: parseInt(data.rating),
                review_title: data.review_title || '',
                review_comment: data.review_comment,
                recommend: data.recommend === 'yes',
                created_at: new Date().toISOString(),
                verified: false,
                helpful_count: 0
            };

            // In a real implementation, you would save to a database
            // For demonstration, we'll just return success
            saveReview(review);

            return {
                statusCode: 200,
                headers,
                body: JSON.stringify({
                    success: true,
                    message: 'Review submitted successfully',
                    review: review
                })
            };
        } catch (error) {
            console.error('Error processing review:', error);
            return {
                statusCode: 500,
                headers,
                body: JSON.stringify({
                    success: false,
                    error: 'Failed to process review'
                })
            };
        }
    }

    // Method not allowed
    return {
        statusCode: 405,
        headers,
        body: JSON.stringify({
            success: false,
            error: 'Method not allowed'
        })
    };
};

// Helper function to generate unique ID
function generateId() {
    return Date.now().toString(36) + Math.random().toString(36).substr(2);
}

// Mock database functions (replace with actual database in production)
const reviewsDatabase = {};

function saveReview(review) {
    if (!reviewsDatabase[review.app_id]) {
        reviewsDatabase[review.app_id] = [];
    }
    reviewsDatabase[review.app_id].unshift(review);
}

function getReviewsForApp(appId) {
    // Return stored reviews or sample data
    if (reviewsDatabase[appId]) {
        return reviewsDatabase[appId];
    }

    // Sample reviews for demonstration
    return [
        {
            id: '1',
            reviewer_name: 'John Doe',
            rating: 5,
            review_title: 'Excellent App!',
            review_comment: 'This app exceeded my expectations. The user interface is intuitive and the features are exactly what I needed.',
            recommend: true,
            created_at: new Date(Date.now() - 86400000).toISOString(),
            verified: true,
            helpful_count: 15
        },
        {
            id: '2',
            reviewer_name: 'Sarah Smith',
            rating: 4,
            review_title: 'Great but needs improvements',
            review_comment: 'Overall a good app with useful features. However, it could use some performance optimizations and bug fixes.',
            recommend: true,
            created_at: new Date(Date.now() - 172800000).toISOString(),
            verified: true,
            helpful_count: 8
        },
        {
            id: '3',
            reviewer_name: 'Mike Johnson',
            rating: 5,
            review_title: 'Best in its category',
            review_comment: 'I\'ve tried many similar apps and this one stands out. Regular updates and excellent customer support.',
            recommend: true,
            created_at: new Date(Date.now() - 259200000).toISOString(),
            verified: false,
            helpful_count: 12
        }
    ];
}

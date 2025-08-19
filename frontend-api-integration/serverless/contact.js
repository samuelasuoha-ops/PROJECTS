// Simple Node.js serverless handler (Netlify/AWS Lambda style)
exports.handler = async (event) => {
  try {
    const data = JSON.parse(event.body || '{}');
    if (!data.name || !data.email || !data.message) {
      return { statusCode: 400, body: JSON.stringify({ error: 'All fields are required' }) };
    }
    // Here you could send an email, write to DB, etc.
    console.log('Contact submission:', data);
    return { statusCode: 200, body: JSON.stringify({ success: true, message: 'Form submitted successfully!' }) };
  } catch (err) {
    return { statusCode: 500, body: JSON.stringify({ error: 'Server error', details: err.message }) };
  }
};

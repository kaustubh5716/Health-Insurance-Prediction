document.getElementById('insuranceForm').addEventListener('submit', function(e) {
    e.preventDefault();

    // Capture the input values in the specified order
    const age = parseInt(document.getElementById('age').value);
    const sex = document.getElementById('gender').value;  // Keep gender as a string
    const bmi = parseFloat(document.getElementById('bmi').value);  // Ensure bmi is a float
    const children = parseInt(document.getElementById('children').value); // Ensure children is an integer
    const smoker = document.getElementById('smoker').value;  // Keep smoker as a string
    const region = document.getElementById('region').value;

    // Prepare data to send to the backend
    const data = {
        age: age,
        sex: sex,
        bmi: bmi,
        children: children,
        smoker: smoker,
        region: region
    };

    // Send data to backend using fetch
    fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(result => {
        // Display the prediction result
        document.getElementById('result').innerText = `Predicted Insurance Cost: $${result.predicted_cost}`;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});


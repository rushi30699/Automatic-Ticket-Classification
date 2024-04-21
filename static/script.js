const form = document.getElementById("complaint-form");

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const complaintText = document.getElementById("complaint-text").value;
  console.log(complaintText);

  try {
    const response = await fetch("/submit-complaint", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ complaint: complaintText }),
    });

    const data = await response.json();
    console.log("dsdsdsdsd" + data.complaintText);
    if (response.ok) {
      alert("Complaint submitted successfully!");
      form.reset();
    } else {
      alert("Failed to submit complaint. Please try again.");
    }
  } catch (error) {
    console.error("Error:", error);
    alert("An error occurred. Please try again.");
  }
});

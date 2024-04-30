const loanComplaintsContainer = document.getElementById(
  "loan-complaints-container"
);
const creditCardComplaintsContainer = document.getElementById(
  "credit-card-complaints-container"
);
const Theftcontainer = document.getElementById("theft-container");

const BankAccountServiceContainer = document.getElementById("bank-container");

const other = document.getElementById("other-container");
const seenComplaintIds = new Set(); // Store seen complaint IDs

function fetchComplaints() {
  const eventSource = new EventSource("/stream");

  eventSource.onmessage = function (event) {
    const complaint = JSON.parse(event.data);

    if (!seenComplaintIds.has(complaint.id)) {
      seenComplaintIds.add(complaint.id); // Add ID to seen set

      const complaintDiv = document.createElement("div");
      complaintDiv.textContent = `${complaint.text} `;

      switch (complaint.department) {
        case "loan":
          loanComplaintsContainer.appendChild(complaintDiv);
          break;
        case "credit":
          creditCardComplaintsContainer.appendChild(complaintDiv);
          break;
        case "theft":
          Theftcontainer.appendChild(complaintDiv);
          break;
        case "bank":
          BankAccountServiceContainer.appendChild(complaintDiv);
          break;
        case "other":
          other.appendChild(complaintDiv);
          break;

        default:
          console.log(
            `Ignoring complaint with unknown department: ${complaint.department}`
          );
      }
    } else {
      console.log(`Ignoring duplicate complaint with ID: ${complaint.id}`);
    }
  };
}

fetchComplaints();

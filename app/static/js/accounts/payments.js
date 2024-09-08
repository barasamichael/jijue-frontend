  $(document).ready(function() {
      $('#example').DataTable();

      const toastContainer = document.getElementById('toastContainer');

      // Function to create and display a success toast
      function displaySuccess(message) {
          const toast = document.createElement('div');
          toast.className = 'toast align-items-center text-white bg-success border-0';
          toast.setAttribute('role', 'alert');
          toast.setAttribute('aria-live', 'assertive');
          toast.setAttribute('aria-atomic', 'true');
          toast.setAttribute('data-bs-autohide', 'true');
          toast.innerHTML = `
		 <div class="d-flex">
		 <div class="toast-body">
		 ${message}
		 </div>
		 <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
		 </div>
		 `;
          toastContainer.appendChild(toast);

          // Initialize and show the toast
          const bootstrapToast = new bootstrap.Toast(toast);
          bootstrapToast.show();
      }

      // Function to create and display an error toast
      function displayError(message) {
          const toast = document.createElement('div');
          toast.className = 'toast align-items-center text-white bg-danger border-0';
          toast.setAttribute('role', 'alert');
          toast.setAttribute('aria-live', 'assertive');
          toast.setAttribute('aria-atomic', 'true');
          toast.setAttribute('data-bs-autohide', 'true');
          toast.innerHTML = `
		 <div class="d-flex">
		 <div class="toast-body">
		 ${message}
		 </div>
		 <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
		 </div>
		 `;
          toastContainer.appendChild(toast);

          // Initialize and show the toast
          const bootstrapToast = new bootstrap.Toast(toast);
          bootstrapToast.show();
      }

      // Phone number validation on input
      document.getElementById('phone').addEventListener('input', function(e) {
          let phone = e.target.value.replace(/\D/g, ''); // Remove all non-digit characters
          if (phone.startsWith('07')) {
              phone = '2547' + phone.substring(2); // Replace '07' with '2547'
          } else if (phone.startsWith('01')) {
              phone = '2541' + phone.substring(2); // Replace '01' with '2541'
          } else if (phone.startsWith('+254')) {
              phone = '254' + phone.substring(4); // Remove '+'
          } else if (phone.startsWith('254') && phone.length > 10) {
              phone = '254' + phone.substring(3); // Ensure it only has 12 digits
          }
          e.target.value = phone;
      });

      // Validate phone number before making the payment
      document.getElementById('paymentForm').addEventListener('submit', function(e) {
          e.preventDefault(); // Prevent default form submission

          const phoneNumber = document.querySelector('#phone').value;
          const amount = document.querySelector('#amount').value;

          if (!validatePhoneNumber(phoneNumber)) {
              displayError('Please enter a valid phone number.');
              return;
          }

          if (!validateAmount(amount)) {
              return;
          }

          const businessId = document.querySelector('#businessId').value;
          const data = {
              phoneNumber,
              amount,
              businessId,
          };

          // Close the modal
          const modalElement = document.getElementById('formModal');
          const modal = bootstrap.Modal.getInstance(modalElement);
          modal.hide();

          // Display success
          displaySuccess("Your transaction request is sent successfully.")

          // Initiate payment
          initiatePayment(data);
      });

      function validatePhoneNumber(phone) {
          return phone.length === 12 && phone.startsWith('254');
      }

      function validateAmount(amount) {
          const numericAmount = parseFloat(amount);
          if (isNaN(numericAmount) || numericAmount <= 0) {
              displayError('Amount must be a positive number.');
              return false;
          }
          if (numericAmount > 500000) {
              displayError('Amount cannot exceed 500,000.');
              return false;
          }
          return true;
      }

      function initiatePayment(data) {
          fetch(`${serverName}account/payment/stk-push`, {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json',
                      Accept: 'application/json',
                  },
                  body: JSON.stringify(data),
              })
              .then(response => response.json())
              .then(data => {
                  if (data.message) {
                      displaySuccess(data.message);
                      checkStatus(data.checkoutRequestId);
                  } else if (data.error) {
                      displayError(data.error);
                  }
              })
              .catch(error => {
                  displayError('Transaction failed. Try again later.');
              });
      }

      function checkStatus(checkoutRequestId) {
          function queryStatus() {
              return fetch(`${serverName}account/payment/stk-query`, {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json',
                      Accept: 'application/json',
                      Authorization: `Bearer ${localStorage.getItem('jwt')}`,
                  },
                  body: JSON.stringify({
                      checkoutRequestId
                  }),
              });
          }

          function processStatus(statusData) {
              if (statusData.error) {
                  displayError(statusData.error);
              }

              if (statusData.message) {
		      // Display success message
                  displaySuccess(statusData.message);

		      // Redirect to the verification page
		      if (statusData.message.includes("processed successfully")) {
    setTimeout(function() {
        window.location.href = "/account/documents/verification";
    }, 3000);
}

              } else {
                  return new Promise(resolve => setTimeout(resolve, 5000))
                      .then(queryStatus)
                      .then(response => response.json())
                      .then(processStatus)
                      .catch(error => {
                          displayError('An unexpected error occurred while checking the transaction request status.');
                      });
              }
          }

          /* Query STK Status */
          return queryStatus()
              .then(response => response.json())
              .then(processStatus)
              .catch(error => {
                  displayError('An unexpected error occurred while checking the transaction request status.');
              });
      }
  });

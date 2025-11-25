document.addEventListener('DOMContentLoaded', () => {
    // Login handling
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
      loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const employeeId = document.getElementById('userid').value;
        const password = document.getElementById('password').value;
        const role = document.getElementById('role').value;
        const loginMessage = document.getElementById('loginMessage');
        try {
          const response = await fetch('http://localhost:8000/api/users/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              employeeId: parseInt(employeeId),
              password: password,
              role: role
            })
          });
          const data = await response.json();
          if (!response.ok) throw new Error(data.detail || 'Login failed');
          localStorage.setItem('employeeId', employeeId);
          loginMessage.classList.remove('text-danger');
          loginMessage.classList.add('text-success');
          loginMessage.textContent = 'Login successful!';
          window.location.href = role === 'employee' ? '/personal.html' : '/manage_employees.html';
        } catch (error) {
          loginMessage.classList.remove('text-success');
          loginMessage.classList.add('text-danger');
          loginMessage.textContent = error.message;
        }
      });
    }
  
    // Personal Details Page
    const personalForm = document.getElementById('personalDetailsForm');
    if (personalForm) {
      const employeeId = localStorage.getItem('employeeId');
      const loadingMessage = document.getElementById('loadingMessage');
      if (!employeeId) {
        loadingMessage.textContent = 'Employee ID not found.';
        return;
      }
      // Fetch and display personal details
      fetch(`http://localhost:8000/api/employees/details/${employeeId}`)
        .then(response => {
          if (!response.ok) throw new Error('Failed to fetch employee details');
          return response.json();
        })
        .then(data => {
          document.getElementById('fname').value = data.firstname || 'N/A';
          document.getElementById('email').value = data.email || 'N/A';
          document.getElementById('phone').value = data.phone || 'N/A';
          loadingMessage.style.display = 'none';
        })
        .catch(error => {
          loadingMessage.textContent = 'Error loading details.';
          console.error(error);
        });
    }
  
    // Salary Structure Page
    const effectiveDateForm = document.getElementById('effectiveDateForm');
    if (effectiveDateForm) {
      const employeeId = localStorage.getItem('employeeId');
      const salaryStructureDiv = document.getElementById('salaryStructure');
      effectiveDateForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const effectiveDate = document.getElementById('effectiveDate').value;
        if (!effectiveDate) {
          salaryStructureDiv.innerHTML = `<div class="alert alert-warning" role="alert">Please select a month and year</div>`;
          return;
        }
        salaryStructureDiv.innerHTML = `<div class="text-muted">Loading salary structure...</div>`;
        try {
          const [year, month] = effectiveDate.split('-');
          const formattedDate = `${year}-${month}-01`;
          const response = await fetch(
            `http://127.0.0.1:8000/api/salarystructure/salary/structure/${employeeId}/${formattedDate}`
          );
          const data = await response.json();
          if (!response.ok) throw new Error(data.detail || 'Failed to fetch salary structure');
          const monthName = new Date(year, month - 1).toLocaleString('default', { month: 'long' });
          salaryStructureDiv.innerHTML = `
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">Salary Structure for ${monthName} ${year}</h5>
                <ul class="list-group list-group-flush">
                  <li class="list-group-item"><strong>Basic Pay:</strong> $${data.basicpay?.toFixed(2) || 'N/A'}</li>
                  <li class="list-group-item"><strong>HRA:</strong> $${data.hra?.toFixed(2) || 'N/A'}</li>
                  <li class="list-group-item"><strong>Other Allowances:</strong> $${data.otherallowances?.toFixed(2) || 'N/A'}</li>
                  <li class="list-group-item"><strong>Total Salary:</strong> $${data.totalsalary?.toFixed(2) || 'N/A'}</li>
                </ul>
              </div>
            </div>
          `;
        } catch (error) {
          salaryStructureDiv.innerHTML = `<div class="alert alert-danger" role="alert">${error.message}</div>`;
          console.error(error);
        }
      });
    }
  
    // Salary Advance Page
    const salaryAdvanceForm = document.getElementById('salaryAdvanceForm');
    if (salaryAdvanceForm) {
      const employeeId = localStorage.getItem('employeeId');
      const advanceMessage = document.getElementById('advanceMessage');
      salaryAdvanceForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        if (!employeeId) return console.error('Employee ID is not set.');
        const advanceAmount = parseFloat(document.getElementById('advanceAmount').value);
        const repaymentMonths = parseInt(document.getElementById('repaymentMonths').value);
        const today = new Date();
        const monthYear = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}`;
        try {
          const response = await fetch('http://localhost:8000/api/salaryadvance/request', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              employeeid: employeeId,
              monthyear: monthYear,
              advanceamount: advanceAmount,
              repaymentmonths: repaymentMonths
            })
          });
          const data = await response.json();
          if (!response.ok) throw new Error(data.detail || 'Failed to request salary advance.');
          advanceMessage.classList.remove('d-none', 'alert-danger');
          advanceMessage.classList.add('alert-success');
          advanceMessage.textContent = 'Salary advance requested successfully!';
        } catch (error) {
          advanceMessage.classList.remove('d-none', 'alert-success');
          advanceMessage.classList.add('alert-danger');
          advanceMessage.textContent = error.message;
          console.error(error);
        }
      });
    }
  
    // Payroll Page
    const fetchPayrollBtn = document.getElementById('fetchPayrollBtn');
    if (fetchPayrollBtn) {
      const employeeId = localStorage.getItem('employeeId');
      fetchPayrollBtn.addEventListener('click', async () => {
        if (!employeeId) return console.error('Employee ID is not set.');
        const payrollDetails = document.getElementById('payrollDetails');
        payrollDetails.innerHTML = `<tr><td colspan="3" class="text-muted text-center">Fetching payroll details...</td></tr>`;
        try {
          const response = await fetch(`http://localhost:8000/api/payroll/getpayroll/${employeeId}`);
          const data = await response.json();
          if (!response.ok) throw new Error(data.detail || 'Failed to fetch payroll details.');
          payrollDetails.innerHTML = `
            <tr>
              <td>${data.monthyear}</td>
              <td>${data.totalpayable}</td>
              <td>${data.totaldeductions}</td>
              <td>${data.netpayable}</td>
            </tr>
          `;
        } catch (error) {
          payrollDetails.innerHTML = `<tr><td colspan="3" class="text-danger text-center">${error.message}</td></tr>`;
          console.error(error);
        }
      });
    }
  });
  
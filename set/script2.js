console.log("JavaScript file loaded successfully!");


const API_BASE_URL = "http://127.0.0.1:8000"; 

function toggleAddEmployee() {
    const addFields = document.getElementById("add_emp_fields");
    addFields.classList.toggle("hidden");
}



function createEmployee() {
    console.log("Create Employee function triggered"); 

    const employeeData = {
        firstname: document.getElementById('first_name').value,
        lastname: document.getElementById('last_name').value,
        dob: document.getElementById('dob').value,
        gender: document.getElementById('gender').value,
        address: document.getElementById('address').value,
        phone: document.getElementById('phone').value,
        email: document.getElementById('email').value,
        ifsc: document.getElementById('ifsc').value,
        bankaccountnumber: document.getElementById('bank_account').value,
        hiredate: document.getElementById('hire_date').value
    };
    

    console.log("Sending data:", employeeData); 

    fetch("http://127.0.0.1:8000/api/employees", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(employeeData)
    })
    .then(response => response.json())
    .then(data => console.log("Response:", data))
    .catch(error => console.error("Fetch Error:", error));
}

    
    document.getElementById('manageEmpForm').addEventListener('submit', function (event) {
        event.preventDefault();
        createEmployee();
    });
// Salary Structure (salary_structure2.html)
function createSalaryStructure() {
    const salaryData = {
        employeeid: parseInt(document.getElementById('salary_emp_id')?.value),
        effectivedate: document.getElementById('effective_date')?.value,
        basicpay: parseFloat(document.getElementById('basic_pay')?.value),
        hra: parseFloat(document.getElementById('hra')?.value),
        otherallowances: parseFloat(document.getElementById('other_allowances')?.value)
    };

    fetch(`${API_BASE_URL}/api/salarystructure/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(salaryData)
    })
    .then(response => response.json())
    .then(data => {
        const result = document.getElementById("salary_result");
        if (result) result.innerText = "Salary Structure Created Successfully!";
        console.log("Success:", data);
    })
    .catch(error => {
        const result = document.getElementById("salary_result");
        if (result) result.innerText = "Error creating salary structure.";
        console.error("Error:", error);
    });
}

function modifySalary() {
    const employeeid = parseInt(document.getElementById('salary_emp_id')?.value);
    const effectivedate = document.getElementById('effective_date')?.value;

    const salaryUpdateData = {
        employeeid: employeeid,
        effectivedate: effectivedate,
        basicpay: parseFloat(document.getElementById('basic_pay')?.value),
        hra: parseFloat(document.getElementById('hra')?.value),
        otherallowances: parseFloat(document.getElementById('other_allowances')?.value)
    };

    fetch(`${API_BASE_URL}/api/salarystructure/${employeeid}/${effectivedate}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(salaryUpdateData)
    })
    .then(response => response.json())
    .then(data => {
        const result = document.getElementById("salary_result");
        if (result) result.innerText = "Salary Structure Updated Successfully!";
        console.log("Success:", data);
    })
    .catch(error => {
        const result = document.getElementById("salary_result");
        if (result) result.innerText = "Error updating salary structure.";
        console.error("Error:", error);
    });
}

// Salary Advances (salary_advance_hr.html)
function viewSalaryAdvances() {
    const monthYear = document.getElementById("view_advance_month")?.value;

    if (!monthYear || !/^\d{4}-\d{2}$/.test(monthYear)) {
        alert("Please select a valid month and year in the format YYYY-MM.");
        return;
    }

    const [year, month] = monthYear.split('-');
    const formattedMonthYear = `${year}${month.padStart(2, '0')}`;

    fetch(`${API_BASE_URL}/api/salaryadvance/${formattedMonthYear}`)
        .then(response => response.json())
        .then(data => {
            displaySalaryAdvances(data);
        })
        .catch(error => {
            console.error("Error fetching salary advances:", error);
            alert("Failed to fetch salary advances.");
        });
}

function displaySalaryAdvances(data) {
    const resultContainer = document.getElementById("salary_advance_result");
    if (!resultContainer) return;

    resultContainer.innerHTML = ""; // Clear previous results

    if (data.length === 0) {
        resultContainer.innerHTML = "<p>No salary advances found for this month.</p>";
        return;
    }

    let table = `
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>Employee ID</th>
                    <th>Amount</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
    `;

    data.forEach(advance => {
        table += `
            <tr>
                <td>${advance.employeeid}</td>
                <td>${advance.advanceamount}</td>
                <td>${advance.status}</td>
            </tr>
        `;
    });

    table += `</tbody></table>`;
    resultContainer.innerHTML = table;
}

async function approveSalaryAdvance() {
    const employeeId = document.getElementById("advance_emp_id")?.value;
    const monthYear = document.getElementById("advance_month")?.value;

    if (!employeeId || !monthYear) {
        alert("Please enter Employee ID and Month-Year.");
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/api/salaryadvance/approve/${employeeId}/${monthYear}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const result = await response.json();
        const advanceResult = document.getElementById("advance_result");
        if (advanceResult) advanceResult.innerText = result.message;
    } catch (error) {
        console.error("Error approving salary advance:", error);
        const advanceResult = document.getElementById("advance_result");
        if (advanceResult) advanceResult.innerText = "Failed to approve salary advance.";
    }
}

async function rejectSalaryAdvance() {
    const employeeId = document.getElementById("advance_emp_id")?.value;
    const monthYear = document.getElementById("advance_month")?.value;

    if (!employeeId || !monthYear) {
        alert("Please enter Employee ID and Month-Year.");
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/api/salaryadvance/reject/${employeeId}/${monthYear}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const result = await response.json();
        const advanceResult = document.getElementById("advance_result");
        if (advanceResult) advanceResult.innerText = result.message;
    } catch (error) {
        console.error("Error rejecting salary advance:", error);
        const advanceResult = document.getElementById("advance_result");
        if (advanceResult) advanceResult.innerText = "Failed to reject salary advance.";
    }
}

// Leaves (leaves.html)
function addLeave() {
    const employeeid = parseInt(document.getElementById("leave_emp_id")?.value);
    const month = document.getElementById("leave_month")?.value;
    const unpaidleaves = parseInt(document.getElementById("unpaid_leaves")?.value);
    const effectivedate = month ? `${month}-01` : ''; // Format to YYYY-MM-DD

    const leaveData = {
        employeeid: employeeid,
        effectivedate: effectivedate,
        unpaidleaves: unpaidleaves
    };

    fetch(`${API_BASE_URL}/api/leaves/leaves/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(leaveData)
    })
    .then(res => {
        if (!res.ok) throw res;
        return res.json();
    })
    .then(data => {
        const leaveResult = document.getElementById("leave_result");
        if (leaveResult) leaveResult.innerText = "Leave entry created successfully.";
        console.log("Leave created:", data);
    })
    .catch(async err => {
        const errorText = await err.text();
        const leaveResult = document.getElementById("leave_result");
        if (leaveResult) leaveResult.innerText = `Error: ${errorText}`;
        console.error("Leave creation error:", errorText);
    });
}

// Payroll Processing (process_payroll.html)
function processPayrollAll() {
    const monthYear = document.getElementById("payroll_month_year")?.value;

    fetch(`${API_BASE_URL}/api/payroll/process_payroll_all?month_year=${monthYear}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" }
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        console.log("Payroll Processed:", data);
    })
    .catch(error => {
        console.error("Error processing payroll:", error);
        alert("Payroll processing failed.");
    });
}

// Event Listeners
document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM fully loaded. Adding event listeners.");
});


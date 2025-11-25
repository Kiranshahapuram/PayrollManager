document.addEventListener("DOMContentLoaded", function() {
    fetch('http://localhost:8000/employee/details')
        .then(response => response.json())
        .then(data => {
            document.getElementById('personalDetails').innerHTML = `
                <p><strong>Name:</strong> ${data.name}</p>
                <p><strong>Email:</strong> ${data.email}</p>
                <p><strong>Phone:</strong> ${data.phone}</p>`;
        });

    fetch('http://localhost:8000/salary/structure')
        .then(response => response.json())
        .then(data => {
            document.getElementById('salaryStructure').innerHTML = `
                <p><strong>Basic Pay:</strong> ${data.basicPay}</p>
                <p><strong>HRA:</strong> ${data.hra}</p>
                <p><strong>Other Allowances:</strong> ${data.otherAllowances}</p>
                <p><strong>Total Salary:</strong> ${data.totalSalary}</p>`;
        });

    fetch('http://localhost:8000/payroll')
        .then(response => response.json())
        .then(data => {
            document.getElementById('payrollDetails').innerHTML = `
                <p><strong>Month:</strong> ${data.month}</p>
                <p><strong>Net Payable:</strong> ${data.netPayable}</p>
                <p><strong>Status:</strong> ${data.paymentStatus}</p>`;
        });

    document.getElementById('salaryAdvanceForm').addEventListener('submit', function(event) {
        event.preventDefault();
        const advanceAmount = document.getElementById('advanceAmount').value;
        const repaymentMonths = document.getElementById('repaymentMonths').value;
        
        fetch('http://localhost:8000/salary/advance', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ advanceAmount, repaymentMonths })
        })
        .then(response => response.json())
        .then(data => alert(data.message));
    });
});

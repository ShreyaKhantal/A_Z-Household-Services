// Function to show the popup based on the element's id
function showPopup(popupId) {
    document.getElementById(popupId).style.display = 'flex';
}

function closePopup(popupId) {
    // Hide the popup
    document.getElementById(popupId).style.display = 'none';
}

// Function to show a specific section and save it in localStorage
function showSection(sectionId) {
    // Hide all sections
    const sections = document.querySelectorAll('.section-content');
    sections.forEach(section => section.style.display = 'none');

    // Hide the 'serv' div when showing another section

    // Show the selected section
    const selectedSection = document.getElementById(sectionId);
    if (selectedSection) {
        selectedSection.style.display = 'block';
    }

    // Save the selected section in localStorage
    localStorage.setItem('activeSection', sectionId);

    // Update button styles
    updateActiveButton(sectionId);
}

function showHome() {
    // Hide all sections
    document.querySelectorAll('.section-content').forEach(section => {
        section.style.display = 'none';
    });

    // Show the home section
    document.getElementById('serv').style.display = 'block';
}

// Function to load the active section on page load
function loadActiveSection() {
    const activeSection = localStorage.getItem('activeSection');
    if (activeSection && activeSection !== 'home') {
        showSection(activeSection);
    } else {
        showHome();
    }
}

// Function to update active button style
function updateActiveButton(activeSectionId) {
    // Remove the 'active' class from all buttons
    const buttons = document.querySelectorAll('.btn1');
    buttons.forEach(button => button.classList.remove('active'));

    // Add the 'active' class to the clicked button
    const activeButton = document.querySelector(`button[data-section="${activeSectionId}"]`);
    if (activeButton) {
        activeButton.classList.add('active');
    }
}

// Run loadActiveSection when the page loads
window.onload = loadActiveSection;


function openViewServiceMS(serviceId) {
    var popup = document.getElementById('viewServiceMS-' + serviceId);
    popup.style.display = 'flex'; // Use 'flex' to center it vertically and horizontally
}

document.getElementById("category").addEventListener("change", function() {
    var categoryId = this.value;
    fetch(`/get_subtypes/${categoryId}`)
        .then(response => response.json())
        .then(data => {
            var subtypeDropdown = document.getElementById("subtype");
            subtypeDropdown.innerHTML = '<option value="" disabled selected>Select a subtype</option>';
            
            data.forEach(function(subtype) {
                var option = document.createElement("option");
                option.value = subtype.id;
                option.text = `${subtype.name} (₹${subtype.base_price})`;
                subtypeDropdown.appendChild(option);
            });
        })
        .catch(error => console.error('Error:', error));
});

function showCategoryServices(categoryId) {
    const categoryDiv = document.getElementById(`category-${categoryId}`);
    categoryDiv.style.display = categoryDiv.style.display === "none" ? "block" : "none";
}
function showSubtypeDetails(subtypeId) {
    var popup = document.getElementById('viewSubtype-' + subtypeId);
    popup.style.display = 'flex'; // Use 'flex' to center it vertically and horizontally
}


function showProfessionals(subtypeId) {
    document.getElementById(`professionals-${subtypeId}`).style.display = 'block';
}

function showProviderDetails(professionalId) {
    document.getElementById(`provider-${professionalId}`).style.display = 'block';
}
function showProviderDetailsfind(professionalId) {
    document.getElementById(`providerf-${professionalId}`).style.display = 'block';
}


function showRequestDetails(requestId) {
    document.getElementById(`details-${requestId}`).style.display = 'block';
}

function closeRequestDetails(requestId) {
    document.getElementById(`details-${requestId}`).style.display = 'none';
}

function showPay(id) {
    document.getElementById(id).style.display = "block";
}

function showCustomerDetailsfind(custId) {
    document.getElementById(`customer-${custId}`).style.display = 'block';
}

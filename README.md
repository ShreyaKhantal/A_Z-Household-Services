# 🏠 A_Z Household Services

A_Z Household Services is a user-friendly platform connecting 🧑‍🤝‍🧑 **Customers** with 👷‍♂️ **Service Professionals**, enabling seamless service booking, management, and feedback. Built with **HTML**, **CSS**, **Jinja2**, and **Flask**, the platform provides unique functionalities for **Admin**, **Service Professionals**, and **Customers**, ensuring a smooth and efficient user experience.

---

## ✨ Features

### 👑 Admin
- **Dashboard**: 🖥️ Manage categories, subtypes, and users.
- **Category Management**: 📂 Add, view, and delete service categories and subtypes.
- **Base Pricing**: 💰 Define and set base prices for different services.
- **Service Approval**: ✅ Approve or reject Service Professional registrations.
- **User Monitoring**: 👀 Monitor user activity and block/unblock accounts.
- **Requests Overview**: 📋 View all service requests and monitor their statuses.
- **Find Section**:
  - 🔍 Search for customers, service professionals, and service requests.
- **Statistics**:
  - 📊 Analyze platform usage, service trends, and user activity.

---

### 👷‍♂️ Service Professional
- **Profile Management**: 📝 Update personal details and service offerings.
- **Service Slots**: ⏰ Define and manage available time slots for services.
- **Request Management**:
  - 📥 View incoming service requests.
  - ✅ Accept or ❌ reject requests based on availability.
  - 🔒 Close service requests once completed (only if the service date has arrived).
- **Find Section**:
  - 🔍 Search for customers who have requested their services.
- **Statistics**:
  - 📊 View data on completed requests, earnings, and ratings.
- **Ratings and Reviews**:
  - 🌟 View customer reviews to improve service offerings.

---

### 🧑‍🤝‍🧑 Customer
- **Service Booking**:
  - 🔍 Browse services by category, subtype, location, or pincode.
  - 🛒 Book services for available time slots.
  - 📅 View upcoming bookings and their status.
- **Request Status**:
  - 🕒 If the service date has not yet arrived, the request status displays **Upcoming**.
  - ✅ Once the date arrives, the Service Professional can close the request after completion.
- **Professional Visibility**:
  - 📍 Customers can only view Service Professionals with the same pincode as theirs.
- **Find Section**:
  - 🔍 Search for Service Professionals by category, pincode, or service ratings.
- **Statistics**:
  - 📊 Analyze booking history, reviews, and service trends.
- **Feedback**:
  - ✍️ Post reviews and ratings for Service Professionals.
  - 🌟 View ratings and reviews before booking.

---

## 🛠️ Workflow

1. **Admin Actions**:
   - Create and manage service categories and subtypes.
   - Approve Service Professional registrations.
   - Search for users and service requests via the **Find Section**.
   - Monitor platform statistics.
2. **Service Professional Actions**:
   - Define service slots and manage service requests.
   - Search for relevant customer requests via the **Find Section**.
   - Analyze their performance and earnings using the **Statistics Section**.
3. **Customer Actions**:
   - Book services from professionals in the same pincode.
   - Search for Service Professionals via the **Find Section**.
   - View booking and review statistics in the **Statistics Section**.

---

## 📆 Date-Sensitive Logic

- **Upcoming Requests**:  
  If the service date has not yet arrived, the status is displayed as **Coming Date**.  
- **Closing Requests**:  
  On or after the service date, Service Professionals can **close** the request upon completion.

---

## 🚀 Technologies Used
- **Frontend**: HTML, CSS, Jinja2
- **Backend**: Flask (Python)
- **Database**: SQLite (SQLAlchemy)

---


## 📂 Screenshots

Below are the screenshots showcasing the features and functionalities of the A_Z Household Services platform:

### 🏠 Home Page
![Home Page](screenshots/Home.png)

### 🔑 Login Page
![Login Page](screenshots/Login.png)

### 🔍 Service Professional Search
![Service Professional Search](screenshots/Prof_find.png)

### 🧑‍💻 Service Professional Home
![Service Professional Home](screenshots/Prof_home.png)

### 👤 Service Professional Profile
![Service Professional Profile](screenshots/Prof_profile.png)

### 📊 Service Professional Statistics
![Service Professional Statistics](screenshots/Prof_stat.png)

### 📝 Service Professional Registration
![Service Professional Registration](screenshots/Prov_regis.png)

### 📋 Admin Categories Management
![Admin Categories](screenshots/Admin_categ.png)

### 👥 Admin Customer Management
![Admin Customer Management](screenshots/Admin_cust.png)

### 🏠 Admin Home Page
![Admin Home](screenshots/Admin_home.png)

### 🚪 Admin Logout
![Admin Logout](screenshots/Admin_logout.png)

### 👤 Admin Profile
![Admin Profile](screenshots/Admin_profile.png)

### 👩‍💻 Admin Service Professional Management
![Admin Service Professional](screenshots/Admin_prov.png)

### 📝 Admin Service Request Management
![Admin Service Request](screenshots/Admin_request.png)

### 📊 Admin Statistics (1)
![Admin Statistics 1](screenshots/Admin_stat1.png)

### 📊 Admin Statistics (2)
![Admin Statistics 2](screenshots/Admin_stat2.png)

### 🧾 Admin Subtypes Management
![Admin Subtypes](screenshots/Admin_subtypes.png)

### 📚 Customer Booking Page
![Customer Booking](screenshots/Cust_book.png)

### 🔍 Customer Search for Professionals
![Customer Find Professional](screenshots/Cust_find.png)

### 🏠 Customer Home Page
![Customer Home](screenshots/Cust_home.png)

### 👤 Customer Profile
![Customer Profile](screenshots/Cust_profile.png)

### 👨‍🔧 Customer Service Professional Details
![Customer Service Professional](screenshots/Cust_prov.png)

### 📝 Customer Registration
![Customer Registration](screenshots/Cust_regis.png)

### 🧾 Customer Service Request
![Customer Service Request](screenshots/Cust_request.png)

### 💸 Customer Review and Payment
![Customer Review and Payment](screenshots/Cust_review_pay.png)

### 📊 Customer Statistics
![Customer Statistics](screenshots/Cust_stat.png)

### 🧑‍🔧 Customer Service Subtype
![Customer Service Subtype](screenshots/Cust_subtype.png)

---
## 📸 How to Run the Project

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/a-z-household-services.git
   ```
2. Navigate to the project directory:
   ```bash
   cd a-z-household-services
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Flask server:
   ```bash
   flask run
   ```
5. Open your browser and navigate to `http://127.0.0.1:5000`.

---

## 📬 Contact
For any queries or feedback, reach out at **[My Email](mailto:khantalshreya@gmail.com)**.

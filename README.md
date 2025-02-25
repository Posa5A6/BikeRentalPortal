

# **Bike Rental Portal 🏍️**

## **Overview**

The **Bike Rental Portal** is a web-based system that allows users to rent bikes online. It provides a **role-based** platform for customers, bike rental companies, and administrators. The system ensures a seamless experience for renting, managing, and tracking bike rentals efficiently.

The project is built using:

- **Flask** (backend)
- **MongoDB** (database)
- **HTML, CSS, JavaScript** (frontend)

## **Key Features**

### **🔹 Customer Features:**

✅ User registration & login  
✅ Browse and view available bikes  
✅ Book a bike for rental  
✅ Track ongoing and completed bookings  
✅ Cancel bike rentals if necessary  
✅ Profile management with rental history

### **🔹 Company Features:**

✅ Register & login as a bike rental company  
✅ Add, update, and remove bike details  
✅ Set rental prices & availability status  
✅ View and manage completed bookings  
✅ Track which bikes are currently rented

### **🔹 Admin Panel:**

✅ Manage users (customers & companies)  
✅ Assign and monitor user roles  
✅ Monitor system performance  
✅ View analytics and reports

### **🔹 Advanced Features (Upcoming Enhancements 🚀)**

✅ **Payment Gateway Integration** – Accept payments via Razorpay/Stripe/PayPal  
✅ **Google Maps Integration** – Show bike pickup/drop locations  
✅ **AI-Based Pricing Optimization** – Dynamic pricing based on demand  
✅ **Mobile App (React Native/Flutter)** – Cross-platform mobile support  
✅ **User Reviews & Ratings** – Customers can rate bikes & companies

---

## **Technology Stack**

### **Frontend:**

- **HTML5, CSS3, JavaScript**
- Bootstrap/Tailwind for styling

### **Backend:**

- **Python (Flask)**
- Flask-RESTful for API handling
- JWT-based authentication

### **Database:**

- **MongoDB** for scalable data storage
- MongoDB Atlas for cloud-based storage

### **Security & Authentication:**

- **Flask-Login** & **bcrypt** for secure user authentication
- **JWT Tokens** for session management
- **OAuth Integration** (Google Sign-in) – Optional

### **Deployment:**

- **Frontend:** Vercel
- **Backend & Database:** AWS/GCP/DigitalOcean
- **Containerization:** Docker

---

## **Project Structure**

```
/bike-rental-portal
│── /templates          # HTML files (Frontend views)
│── /static             # CSS, JavaScript, images
│── /routes             # Flask routes for APIs
│── /models             # Database models
│── /config             # Configuration settings
│── /utils              # Helper functions
│── app.py              # Main Flask application
│── config.py           # Configuration settings
│── requirements.txt    # Python dependencies
│── Dockerfile          # Containerization setup
│── README.md           # Project documentation
```

---

## **Installation & Setup**

### **Prerequisites:**

✔ Install Python (3.8+ recommended)  
✔ Install MongoDB (local or cloud-based MongoDB Atlas)  
✔ Install Docker (for containerized deployment)

### **1️⃣ Clone the Repository**

```sh
git clone https://github.com/Posa5A6/Bike-Rental-Portal.git
cd Bike-Rental-Portal
```

### **2️⃣ Create a Virtual Environment (Recommended)**

```sh
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### **3️⃣ Install Required Dependencies**

```sh
pip install -r requirements.txt
```

### **4️⃣ Configure Environment Variables**

Create a `.env` file and add MongoDB connection details:

```sh
MONGO_URI=your_mongodb_connection_string
SECRET_KEY=your_secret_key
```

### **5️⃣ Run the Application**

```sh
python app.py
```

### **6️⃣ Open the App in Browser**

```sh
http://127.0.0.1:5000
```

---

## **🚀 Deployment Guide**

### **Run with Docker**

1. **Build the Docker Image:**
   ```sh
   docker build -t bike-rental-portal .
   ```
2. **Run the Container:**
   ```sh
   docker run -p 5000:5000 bike-rental-portal
   ```
3. **Access the Application:**
   ```sh
   http://localhost:5000
   ```

### **Deploy to AWS/GCP**

1. Set up a cloud server (EC2/GCP VM).
2. Install Python, Flask, and MongoDB.
3. Clone the GitHub repo & configure `.env` settings.
4. Run `gunicorn` or `uWSGI` for production deployment.

### **Deploy Frontend on Vercel**

1. Go to **[Vercel](https://vercel.com/)**
2. Connect the repository & deploy the frontend

---

## **API Endpoints**

| Method     | Endpoint             | Description                  |
| ---------- | -------------------- | ---------------------------- |
| **GET**    | `/`                  | Home page                    |
| **POST**   | `/register`          | User registration            |
| **POST**   | `/login`             | User login                   |
| **GET**    | `/dashboard`         | User dashboard               |
| **GET**    | `/bikes`             | View available bikes         |
| **POST**   | `/book-bike`         | Book a bike                  |
| **GET**    | `/company-dashboard` | Company dashboard            |
| **POST**   | `/add-bike`          | Add a new bike               |
| **GET**    | `/admin-dashboard`   | Admin panel                  |
| **DELETE** | `/delete-bike/<id>`  | Remove a bike from inventory |
| **PATCH**  | `/update-bike/<id>`  | Update bike details          |

---

## **Security Features 🛡️**

✔ **JWT Token Authentication**  
✔ **Role-Based Access Control (RBAC)**  
✔ **Data Encryption for Passwords (bcrypt)**  
✔ **SQL/NoSQL Injection Prevention**  
✔ **CORS Handling for API Security**

---

## **Future Enhancements 📌**

🔹 **Integrate Google Maps for Ride Tracking**  
🔹 **Add Multi-language Support**  
🔹 **Implement AI-based Bike Pricing**  
🔹 **Introduce Subscription Plans for Companies**  
🔹 **Develop a Mobile App (React Native/Flutter)**

---

## **Contributing 🤝**

Contributions are welcome!

### **How to Contribute?**

1. **Fork** the repository
2. Create a new **feature branch**
   ```sh
   git checkout -b feature-new-functionality
   ```
3. **Commit your changes**
   ```sh
   git commit -m "Added new feature"
   ```
4. **Push to GitHub & create a Pull Request**
   ```sh
   git push origin feature-new-functionality
   ```
5. Wait for review & merge approval

---

## **License**

This project is **open-source** and available under the **MIT License**.

---

## **🚀 Developed by Narendra**

For queries or collaborations, feel free to connect!

🔗 **GitHub:** [Posa5A6](https://github.com/Posa5A6)  
✉ **Email:** narisnarendras6@gmail.com

---

This version includes **detailed sections** for installation, API endpoints, security, deployment, and future enhancements. Let me know if you need any more refinements! 🚀🔥

# Zero Flow Package Delivery API



Zero Flow is a RESTful API designed to manage package deliveries. It provides endpoints for creating, retrieving, updating, and deleting packages. This API allows authenticated users to track package statuses, manage sender and receiver information, and perform administrative tasks. Staff users have broader permissions, while regular users can manage packages they have issued.

## Features

* **User Authentication:** Secure JWT-based authentication for users.
* **Package Management:** Create, retrieve, update, and delete package records.
* **Package Tracking:** Track package statuses (pending, in transit, delivered, returned).
* **Soft Delete:** Implement soft delete for packages, allowing restoration.
* **Detailed Package Information:** Manage sender and receiver details, weight, destination, and more.
* **API Documentation:** Automatically generated API documentation using Swagger UI.
* **Data Validation:** Robust data validation for all API endpoints.
* **Pagination:** Efficient pagination for listing packages.
* **Logging:** Comprehensive logging for debugging and monitoring.

## Technologies Used

* **Python:** Programming language.
* **Django:** Web framework.
* **Django REST Framework (DRF):** Toolkit for building Web APIs.
* **DRF Simple JWT:** JWT authentication for DRF.
* **DRF Spectacular:** OpenAPI schema generation and Swagger UI.
* **PostgreSQL:** Database. (You can change this according to your database)

## Setup

1.  **Clone the Repository:**

    ```bash
    git clone [repository URL]
    cd zeroflow
    ```

2.  **Create a Virtual Environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  
    venv\Scripts\activate  
    ```

3.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Database Setup:**

    * Configure your database settings in `zeroflow/settings.py`.
    * Run migrations:

        ```bash
        python manage.py migrate
        ```

5.  **Create a Superuser:**

    ```bash
    python manage.py createsuperuser

    default admin ,admin
    ```

6.  **Load Initial Data (Optional):**

    * Place your initial data in a JSON file (e.g., `data.json`) in the `fixtures` directory of the respective app.
    * Run:

        ```bash
        python manage.py loaddata data.json
        ```

7.  **Environment Variables:**

    * Set environment variables for database credentials, secret keys, and other sensitive data.

8.  **Run the Development Server:**

    ```bash
    python manage.py runserver
    ```

9.  **Access API Documentation:**

    * Open your browser and go to `http://127.0.0.1:8000/api/schema/swagger-ui/`.

## API Endpoints

* **Authentication:**
    * `/api/token/` (POST): Obtain JWT tokens.
    * `/api/token/refresh/` (POST): Refresh JWT tokens.
* **Users:**
    * `/register/` (POST): Register a new user.
    * `/profileupdate/` (PUT/PATCH): Update user profile.
* **Packages:**
    * `/packages/` (GET): List packages.
    * `/packages/create/` (POST): Create a new package.
    * `/packages/<tracking_number>/` (GET/PUT/PATCH): Retrieve or update a package.
    * `/packages/<tracking_number>/delete/` (DELETE): Soft delete a package.
    * `/packages/<tracking_number>/restore/` (PUT): Restore a soft-deleted package.

## Usage Examples

* **Register a User (Demo User 1):**

    ```json
    {
        "username": "testuser789",
        "email": "testuser789@example.com",
        "password": "StrongPassword789!",
        "password2": "StrongPassword789!",
        "first_name": "John",
        "last_name": "Doe",
        "address": "100 Elm Street",
        "city": "Rivertown",
        "zip_code": "90210",
        "phone_number": "555-987-6543"
    }
    ```

* **Register a User (Demo User 2):**

    ```json
    {
        "username": "sampleuser456",
        "email": "sampleuser456@example.com",
        "password": "SecurePassword456!",
        "password2": "SecurePassword456!",
        "first_name": "Jane",
        "last_name": "Smith",
        "address": "200 Oak Avenue",
        "city": "Lakeside",
        "zip_code": "12345",
        "phone_number": "555-123-4567"
    }
    ```



## Testing

* Run tests using:

    ```bash
    python manage.py test
    ```





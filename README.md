# DARAJA API PRESENTATION (STK PUSH)

This project demonstrates the use of the DARAJA API to initiate STK Push payments. The setup guides you through configuring the project to make secure STK Push requests and handle callbacks.

## Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

- Python 3.x
- Virtualenv

### Installation

1. **Clone the repository**:

    ```bash
    git clone git@github.com:anomalous254/daraja_api_presentation.git
    cd daraja_api_presentation
    ```

2. **Create a virtual environment**:

    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment**:

    - For macOS/Linux:

      ```bash
      source venv/bin/activate
      ```

    - For Windows:

      ```bash
      venv\Scripts\activate
      ```

4. **Install the required packages**:

    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1. **Create a `.env` file** in the root directory of the project and add the following environment variables:

    ```dotenv
    DEBUG=True
    DARAJA_API_CONSUMER_KEY=<your-consumer-key>
    DARAJA_API_CONSUMER_SECRET=<your-consumer-secret>
    DARAJA_API_PASS_KEY=<your-pass-key>
    DARAJA_API_SHORT_CODE=<your-short-code>
    SECRET_KEY=<your-secret-key>
    ```

2. **Set up the callback URL**:

   - Navigate to the `daraja_api` folder (in the   `core.py`).
   - In the `send_stk_push` function, update the request body to include your callback URL:

    ```python
    # Example placeholder for the callback URL
    'CallbackURL': 'https://yourdomain.com/path/to/callback'
    ```

### Running the Project

To start the project, run:

```bash
python manage.py migrate
python manage.py runserver

# Django File Server

This project is a simple Django web application that serves the content of files based on the filename provided as a parameter in the URL.

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd django-file-server
   ```

2. **Create a virtual environment**:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages**:
   ```
   pip install -r requirements.txt
   ```

4. **Run the migrations** (if any):
   ```
   python manage.py migrate
   ```

5. **Run the development server**:
   ```
   python manage.py runserver
   ```

## Usage

To access the file content, navigate to the following URL in your web browser:

```
http://localhost:8000/files/<filename>
```

Replace `<filename>` with the name of the file you want to serve. Ensure that the file is located in the appropriate directory that the application has access to.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
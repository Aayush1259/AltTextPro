from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

##curl -X POST -F "image=@C:\Users\dellf\OneDrive\Pictures\Screenshots\Screenshot 2023-06-20 173049.png" http://localhost:8000/api/process-image
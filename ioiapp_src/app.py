from image_occlusion import app, db
# Run the Flask app
if __name__ == "__main__":
  db.create_all()
  # run the app
  app.run(debug=True, port=5000, host='0.0.0.0')
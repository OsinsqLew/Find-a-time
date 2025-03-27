Find a Time for You and Your Friends
1. Create your profile and a group for your friends.
2. Add your available time slots.
3. Specify how long you need and the minimum number of participants. Find a Time will find a common time slot for you.
4. Enjoy spending time together!

Technical Details:
  The application uses the Streamlit library to display the webpage.
  Data is fetched from a MySQL database using FastAPI.
  The connection between the database and the API is encrypted with SSL certificates.
  For additional security, the database operates in a Master-Slave setup,
  where writes occur only on the Master, and reads are handled exclusively by the Slave.
  For educational purposes app gives an opportunity to check how SQL injection works.

# GetItDone
Productivity Task Manager<br>
Get It Done is a collaborative task manager website where people can easily work on anything together and keep a track of their progress. With Get It Done, you can efficiently complete your tasks, prioritize, and make meaningful progress towards your 
goal. It is designed with a user-friendly interface to increase your productivity without added complexity. <br>

### Features
- Module 1: User Authentication 
1. User registration 
2. User login/logout 
3. User profiles 
4. Password reset functionality 
5. User-specific task views 
- Module 2: Task Management  
6. Create tasks 
7. Set task details (description, due date, priority) 
8. Edit existing tasks 
9. Mark tasks as complete 
10. Delete tasks 
11. Task completion timer 
- Module 3: Collaboration 
12. Share tasks with other users 
13. Collaborative task editing 
14. Task assignment 
15. Task comments 
16. Real-time updates on shared tasks 
- Module 4: Notification 
17. Task due date reminders 
18. User-specific notifications 
19. Email notifications 
20. In-website notifications 
21. Notification settings 
22. Pop-up notifications

### Technologies Used in Implementation 
- Framework:  <br>
● Bootstrap <br>
● Django <br>
- Database <br>
● Sqlite3 <br>
- Languages:  <br>
● HTML <br>
● CSS <br>
● JavaScript <br>
● Python<br>


## Manual

### How to pull from this repository to your computer?
1. download git<br>
1. Open Git Bash on the selected directory<br>
git clone https://github.com/thequeenziana/GetItDone.git <br>
3. Open VS Code and open the project folder <br>
### How to run the code?
1. Open VS Code and open the project folder<br>
2. Open New Terminal and open the Command Prompt<br>
python -m venv env <br>
\env\Scripts\activate <br>
pip install -r requirements.txt<br>
python manage.py makemigrations <br>
python manage.py migrate <br>
python manage.py runserver <br>

### How to commit into new repository? <br>
1. download git<br>
1. Open Git Bash on the selected directory<br>
git clone https://github.com/thequeenziana/GetItDone.git <br>
cd GetItDone <br>
git config --global user.name "Ziana Jesin Bhuiyan" <br>
git config --global user.email "bziana29@gmail.com" <br>
git add . <br>
git commit -m "Initial commit" <br>
git push -u origin main <br>

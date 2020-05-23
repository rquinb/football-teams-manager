CALL cd %~dp0
CALL pip install virtualenv
CALL virtualenv football-teams-manager
CALL football-teams-manager\Scripts\Activate
CALL pip install -r requirements.txt
CALL python app.py
PAUSE
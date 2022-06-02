@ECHO OFF

start python "tanque_oleo.py"
ECHO inciando tanque de oleo
start python "tanque_NAEToh.py"
ECHO inciando tanque de NAoh/EToh
start python "reator.py"
ECHO inciando reator
start python "decantador.py"
ECHO inciando reator
start python "secador.py"
ECHO inciando secador
start python "tanque_lavagem_1.py"
ECHO inciando tanque de lavagem 1
start python "tanque_lavagem_2.py"
ECHO inciando tanque de lavagem 2
start python "tanque_lavagem_3.py"
ECHO inciando tanque de lavagem 3
start python "tanque_glicerina.py"
ECHO inciando tanque glicerina
start python "tanque_bio.py"
ECHO inciando tanque bio-diesel
start python "orquestrador.py"
ECHO inciando orquestrador

PAUSE




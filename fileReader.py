from os import fdopen, remove
import os
from shutil import copymode, move
from tempfile import mkstemp
from flask import session

from category import getCategory


def isUserAuthorized():
    # Check if the user is authorized by checking if the session username is contained in the multiline file authorizedUser.txt
    with open('data/config/authorizedUser.txt', 'r') as file:
        authorizedUsers = file.readlines()
        for user in authorizedUsers:
            if session['username'] == user.strip().split(':')[0] and session['pin'] == user.strip().split(':')[1]:
                return True
    return False

def isAdministrator():
    # Check if the user is an administrator by checking if the session username is contained in the file administrator.txt
    with open('data/config/administrator.txt', 'r') as file:
        administrators = file.readlines()
        for user in administrators:
            if session['username'] == user.strip().split(':')[0] and session['pin'] == user.strip().split(':')[1]:
                return True
    return False

def isFirstConnection():
    # check if it is first user connection by checking if the username not is followed by hashed pin
    with open('data/config/authorizedUser.txt', 'r') as file:
        authorizedUsers = file.readlines()
        for user in authorizedUsers:
            if session['username'] == user.strip().split(':')[0] and len(user.strip().split(':'))==1:
                return True

def updatePin(username, newPin):
    # update the pin of the user in the file authorizedUser.txt
    file_path='data/config/authorizedUser.txt'
    with open(file_path, 'r') as file:
        authorizedUsers = file.readlines()
    fh, abs_path = mkstemp()
    with fdopen(fh,'w') as new_file:
        for user in authorizedUsers:
            if username == user.strip().split(':')[0]:
                new_file.write(f'{username}:{newPin}\n')
            else:
                new_file.write(user)
    #Copy the file permissions from the old file to the new file
    copymode(file_path, abs_path)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)

    # make the same for administrator.txt
    file_path='data/config/administrator.txt'
    with open(file_path, 'r') as file:
        administrators = file.readlines()
    fh, abs_path = mkstemp()
    with fdopen(fh,'w') as new_file:
        for user in administrators:
            if username == user.strip().split(':')[0]:
                new_file.write(f'{username}:{newPin}\n')
            else:
                new_file.write(user)
    #Copy the file permissions from the old file to the new file
    copymode(file_path, abs_path)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)

def getNumberOfUsers():
    # Get the number of users from the file authorizedUser.txt
    with open('data/config/authorizedUser.txt', 'r') as file:
        authorizedUsers = file.readlines()
        return len(authorizedUsers)
    
def getUserIndex(username):
    # Get the index of the user from the file authorizedUser.txt
    with open('data/config/authorizedUser.txt', 'r') as file:
        authorizedUsers = file.readlines()
        for i in range(len(authorizedUsers)):
            if username in authorizedUsers[i].split(':')[0]:
                return i
    return -1

def getSubjects(index):
    # Get the subjects from the file subjects.txt
    with open('data/config/subjects.txt', 'r') as file:
        subjects = file.readlines()
        if index is None:
            return subjects
        if index < 0 or index >= len(subjects):
            return "Invalid index"
        return subjects[index].strip()
    
def getOpinions(subject):
    # Get the opinions from the file opinions_{subject}.txt
    opinions = []
    # verify if file exist create it if not
    if not os.path.exists(f'data/opinions_{subject.strip()}.txt'):
        with open(f'data/opinions_{subject.strip()}.txt', 'w') as file:
            file.write('')
            
    with open(f'data/opinions_{subject.strip()}.txt', 'r') as file:
        opinions = file.readlines()
    
    for i in range(len(opinions)):
        opinions[i] = opinions[i].strip()

    return opinions

def addOpinion(subject, opinion, value, username):
    # add opinion if not already present then add the value to the opinion_{subject}_values.txt file
    opinions = getOpinions(subject)
    if opinion not in opinions:
        opinions.append(opinion)
        with open(f'data/opinions_{subject.strip()}.txt', 'w') as file:
            # split the opinion by newline
            file.writelines(opinion.strip() + '\n' for opinion in opinions)
    lineToAppend=opinions.index(opinion)
    userIndex=getUserIndex(username)
    # verify if file exist create it if not
    if not os.path.exists(f'data/opinions_{subject.strip()}_values.txt'):
        with open(f'data/opinions_{subject.strip()}_values.txt', 'w') as file:
            newLine='-1,'*getNumberOfUsers()
            newLine=newLine[:-1]+'\n'
            file.write(newLine)
    with open(f'data/opinions_{subject.strip()}_values.txt', 'r') as file:
        fh, abs_path = mkstemp()
        with fdopen(fh,'w') as new_file:
            done=False
            for i,line in enumerate(file):
                # if empty line write '-1,' for each user
                if line.strip()=='':
                    newLine='-1,'*getNumberOfUsers()
                    newLine=newLine[:-1]+'\n'
                    new_file.write(newLine)
                elif i==lineToAppend:
                    newLine=line
                    values=newLine.strip().split(',')
                    values[userIndex]=str(value)
                    newLine=','.join(values)
                    new_file.write(newLine+'\n')
                    done=True
                else:
                    new_file.write(line)
            if not done:
                newLine='-1,'*getNumberOfUsers()
                newLine=newLine[:-1]+'\n'
                new_file.write(newLine)
                
    file_path=f'data/opinions_{subject.strip()}_values.txt'
    #Copy the file permissions from the old file to the new file
    copymode(file_path, abs_path)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)
            

def getValuesForOpinions(subject,username):
    # get the values for the opinions from the file opinions_{subject}_values.txt
    userIndex=getUserIndex(username)
    values=[]
    # verify if file exist create it if not
    if not os.path.exists(f'data/opinions_{subject.strip()}_values.txt'):
        values=['']*len(getOpinions(subject))
        return values
    with open(f'data/opinions_{subject.strip()}_values.txt', 'r') as file:
        for line in file:
            vote=line.strip().split(',')
            if len(vote)>userIndex:
                values.append(vote[userIndex] if vote[userIndex]!='-1' else '')

    return values

def getResults(subject):
    # get the results for the opinions from the file opinions_{subject}_values.txt
    results=[] # list of tuples (opinion, votes)
    opinions=getOpinions(subject)
    allVotes=[]
    # verify if file return empty list if not exist
    if not os.path.exists(f'data/opinions_{subject.strip()}_values.txt'):
        return results
    with open(f'data/opinions_{subject.strip()}_values.txt', 'r') as file:
        for line in file:
            votes=line.strip().split(',')
            allVotes.append(votes)
    for i in range(len(opinions)):
        votes=[int(vote) for vote in allVotes[i] if vote!='-1']
        results.append((opinions[i],votes))
    return results

def getHumanReadableResults(subject):
    # get the human readable results for the opinions from the file opinions_{subject}_values.txt
    results=getResults(subject)
    numberOfUser=getNumberOfUsers()
    humanReadableResults=[]
    labels = ['Fortement en désaccord', 'En désaccord', 'Neutre', 'D’accord', 'Fortement d’accord']
    values = [2, 4, 6, 8, 10]
    for result in results:
        opinion=result[0]
        votes=result[1]
        # if no votes, don't add the opinion
        if len(votes)>0:
            vote_counts = [votes.count(value) for value in values]
            humanReadableResults.append((opinion, getCategory(votes), sum(votes)/len(votes) if len(votes)>0 else 0, len(votes)/numberOfUser*100, vote_counts, labels))
    return humanReadableResults # list of tuples (opinion, category, average, participation)
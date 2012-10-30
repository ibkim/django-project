import os, glob, tempfile, shutil
from git import *
import lockfile

USER_INDEX = 0
REPO_INDEX = 1
PERM_INDEX = 2
USRGRP_INDEX = 3

class Gitolite(object):

  modified_files = []
  deleted_files = []
  
  
  def __init__(self, path):
    self._repo_path = path
    self._user_repo_config = path + "/conf/user_repos.conf"
    self._key_path = path + "/keydir/"
    self._lock_file = path + "/lock"
    self._lock = lockfile.FileLock(self._lock_file)
    self._is_dirty = False

  def lock(self, timeout=60):
    while not self._lock.i_am_locking():
      try:
        self._lock.acquire(timeout)
      except lockfile.LockTimeout:
        self._lock.break_lock()
        self._lock.acquire()
        return False
    return True

  def unlock(self):
    self._lock.release()

  def createRepo(self, users, projectname):
    """
    Create a new repo to gitolite.
    returns true iff successfully added repo to config
    """

    repo_data = self.__load_repo()

    if projectname in repo_data:
      return False

    repo_data[projectname] = [(users, ['',], 'RW+', '@'+projectname+'_members')]
    project_data = repo_data[projectname]
    self.__save_repo(repo_data)

    if self._user_repo_config not in self.modified_files:
      self.modified_files.append(self._user_repo_config)
    self._is_dirty = True

    return True


  def rmProject(self, projectname):
    """
    Removes a repo
    returns true iff successfully removed repo from config.
    """

    repo_data = self.__load_repo()

    if projectname  not in repo_data:
      return False

    del repo_data[projectname]

    self.__save_repo(repo_data)

    if self._user_repo_config not in self.modified_files:
      self.modified_files.append(self._user_repo_config)
    self._is_dirty = True

    return True

  def addUser(self, projectname, users):
    """
    Removes a repo
    returns true iff successfully removed repo from config.
    """

    repo_data = self.__load_repo()

    if projectname  not in repo_data:
      return False

    project = repo_data[projectname]
    members = project[0][USER_INDEX]
    for user in users:
      if user not in members:
        members.append(user)

    self.__save_repo(repo_data)

    if self._user_repo_config not in self.modified_files:
      self.modified_files.append(self._user_repo_config)
    self._is_dirty = True

    return True

  def isThereUser(self, projectname, user):
    """
    Removes a repo
    returns true iff successfully removed repo from config.
    """

    repo_data = self.__load_repo()

    if projectname  not in repo_data:
      return False

    project = repo_data[projectname]
    members = project[0][USER_INDEX]

    if user in members:
      return True

    return False

  def rmUser(self, projectname, users):
    """
    Removes a repo
    returns true iff successfully removed repo from config.
    """

    repo_data = self.__load_repo()

    if projectname  not in repo_data:
      return False

    project = repo_data[projectname]
    members = project[0][USER_INDEX]
    for user in users:
      if user in members:
        members.remove(user)

    self.__save_repo(repo_data)

    if self._user_repo_config not in self.modified_files:
      self.modified_files.append(self._user_repo_config)
    self._is_dirty = True

    return True

  def addRepo(self, projectname, repos):
    """
    Removes a repo
    returns true iff successfully removed repo from config.
    """

    repo_data = self.__load_repo()

    if projectname  not in repo_data:
      return False

    project = repo_data[projectname]
    repository = project[0][REPO_INDEX]
    for repo in repos:
      if repo not in repository:
        repository.append(repo)

    self.__save_repo(repo_data)

    if self._user_repo_config not in self.modified_files:
      self.modified_files.append(self._user_repo_config)
    self._is_dirty = True

    return True

  def rmRepo(self, projectname, repos):
    """
    Removes a repo
    returns true iff successfully removed repo from config.
    """

    repo_data = self.__load_repo()

    #if projectname not in repo_data.keys():
    #  print repo_data
    #  return False

    project = repo_data[projectname]
    repository = project[0][REPO_INDEX]
    for repo in repos:
      if repo in repository:
        repository.remove(repo)

    self.__save_repo(repo_data)

    if self._user_repo_config not in self.modified_files:
      self.modified_files.append(self._user_repo_config)
    self._is_dirty = True

    return True

  def getRepos(self):
    return self.__load_repo()


  def addSSHKey(self, username, keyname, sshkey):

    key_file_name = self.__get_ssh_key_path(username, keyname)

    try:
      with open(key_file_name) as f:
        return False
    except IOError as e:
      pass

    new_key_file = open(key_file_name, 'w')
    new_key_file.write(sshkey)
    new_key_file.close()

    if key_file_name not in self.modified_files:
      self.modified_files.append(key_file_name)
      # handle for remove and then create
      if key_file_name in self.deleted_files:
        self.deleted_files.remove(key_file_name)
      self._is_dirty = True

    return True

  def rmSSHKey(self, username, keyname):

    key_file_name = self.__get_ssh_key_path(username, keyname)

    try:
      os.remove(key_file_name)
    except:
      return False

    if key_file_name not in self.deleted_files:
      self.deleted_files.append(key_file_name)
      # handle for add and then remov
      if key_file_name in self.modified_files:
        self.modified_files.remove(key_file_name)
      self._is_dirty = True

    return True

  def getSSHKeyValue(self, username, keyname):
    file_path = self.__get_ssh_key_path(username, keyname)
    f = open(file_path, 'r')
    key = f.read()
    f.close()
    return key

  def getSSHKeys(self):

    keys = glob.glob(self._key_path + '*@*.pub')

    key_data = {}

    for keyfile in keys:
      filename = os.path.basename(keyfile)[:-4]
      filename_split = filename.split('@',1)

      if len(filename_split) != 2:
        raise SyntaxError('Invalid key file name')

      username = filename_split[0].strip()
      keyname = filename_split[1].strip()

      if username not in key_data:
        key_data[username] = []

      key_data[username].append(keyname)

    return key_data

  def publish(self):
    if self._is_dirty == False:
      return True

    repo = Repo(self._repo_path, odbt=GitCmdObjectDB)
    repo.config_writer()
    git = repo.git

    message = 'Commit by django application\n\n'

    message = message + 'Modified:\n    '
    if len(self.modified_files) > 0:
      git.add(self.modified_files)
      for item in self.modified_files:
        message = message + item + '\n    '

    message = message.rstrip(' ')
    message = message + 'Deleted:\n    '
    if len(self.deleted_files) > 0:
      git.rm(self.deleted_files)
      for item in self.deleted_files:
        message = message + item + '\n    '

    try:
      #commit = index.commit(message)
      #o = repo.remotes.origin
      #o.push()
      git.execute(['git', 'commit', '-m', message,])
      git.execute(['git', 'push', 'origin', 'master'])
    except:
      return False

    self.modified_files = []
    self.deleted_files = []

    self._is_dirty = False

    return True

  def __get_ssh_key_path(self, username, keyname):
    return self._key_path + username + "@" + keyname + ".pub"

  def __load_repo(self):
    """
    Read gitolite config file
    """

    repo_data = {}
    project = ''

    #@someprj_members = ...
    #@someprj_repos = ...
    #repo @somprj_repos
    # RW+ = @someprj_members
    # R = @all

    repo_file_content = open(self._user_repo_config, 'r')

    line = repo_file_content.readline().strip()
    repo = ''

    while line != '':

      if line.startswith('@'):
        line_split = line.split('=', 1)
        if len(line_split) != 2:
          raise SyntaxError('Invalid Group def.')
        if line_split[0].split('_',1)[1].strip() == 'members':
          members = line_split[1].split()
        else:
          repos = line_split[1].split()

      elif line.startswith('repo'):
        line_split = line.split(None, 1)
        if len(line_split) != 2:
          raise SyntaxError('Invalid repository def.')
        #extract myprj project name from @myprj_repos
        project = line_split[1].split('_')[0][1:]

      elif line.startswith(' RW'):
        if project == '':
          raise SyntaxError('Missing repo def.')

        line_split = line.split('=', 1)
        if len(line_split) != 2:
          raise SyntaxError('Invalid rule')

        perm = line_split[0].strip()
        usergroup = line_split[1].strip()

        if project not in repo_data:
          repo_data[project] = []

        repo_data[project].append( ( members, repos, perm, usergroup) )
      elif line.startswith(' R '):
        pass
      else:
        raise SyntaxError('Invalid line')

      line = repo_file_content.readline()

    repo_file_content.close()
  
    return repo_data

  def __save_repo(self, repo_data):
    """
    Write gitolite config file
    """
    tmp_file = tempfile.NamedTemporaryFile('w')

    for key, values in repo_data.items():
      grp_prefix = '@' + key + '_'
      members_line = grp_prefix + 'members = '
      repos_line = grp_prefix + 'repos = '

      project = values[0]
      for user in project[USER_INDEX]:
        members_line = members_line + user + ' '

      for repo in project[REPO_INDEX]:
        repos_line = repos_line + repo + ' '

      tmp_file.write(members_line + '\n')
      tmp_file.write(repos_line + '\n')
      tmp_file.write('repo ' + str(repos_line.split(' ')[0]) + '\n')
      tmp_file.write(" " + project[PERM_INDEX] + " = " + project[USRGRP_INDEX] + '\n')
      tmp_file.write(" " + 'R' + " = @all" + '\n')
      
    tmp_file.flush()
    shutil.copyfile(tmp_file.name, self._user_repo_config)
    tmp_file.close()

if __name__ == "__main__":
  repo  = Gitolite('/opt/gitolite-admin')

  result = repo.createRepo(['abd', 'user2',], 'testprjwef')
  if result == False:
    print 'Project repo already exist'

  result = repo.rmProject('testprj')
  if result == False:
    print 'Project repo doesn\'t exist'

  result = repo.addUser('myprj', ['testadduser',])

  result = repo.rmUser('myprj', ['user1',])

  repo.addRepo('django-prj', ['djangorepo1','djangorepo3',])
  #repo.rmRepo('django-prj', ['djangorepo1','djangorepo3',])

  repo.addSSHKey('user1', 'default', 'wefw239ru8fu8394uctnr893')
  repo.addSSHKey('user1', 'desktop', 'wefw239ru8fu8394uctnr893')
  repo.addSSHKey('user1', 'office', 'wefw239ru8fu8394uctnr893')

  result = repo.publish()
  if result == False:
    print "publish error "

  data = repo.getSSHKeys()
  repo.rmSSHKey('user1', 'default')

  result = repo.publish()
  if result == False:
    print "publish error "

  print repo.modified_files
  print repo.deleted_files

  




